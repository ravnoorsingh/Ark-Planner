"""Reduce a scraped page to its documentation content.

A raw doc page is mostly not documentation: sidebars, tables of contents, header
and footer chrome, "edit this page" links. Measured on real output, that was 17-27%
of the stored markdown on some pages — dead weight in a RAG store, and text a
planning agent would read as if it were content.

Cleanup happens structurally on the HTML, before markdown conversion, because tags
say what a region *is*. Doing it on the markdown afterwards would mean guessing from
link density, which cannot tell a navigation sidebar from a legitimate API index.
"""

from __future__ import annotations

import copy
import re

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

from .tracing import annotate, traced

# The element holding the actual documentation, most specific first.
MAIN_SELECTORS = (
    'div[itemprop="articleBody"]',  # Sphinx / ReadTheDocs
    "article.md-content__inner",  # MkDocs Material
    ".theme-doc-markdown",  # Docusaurus
    ".markdown-body",  # GitHub
    ".document",  # older Sphinx
    "main article",
    'article[role="main"]',
    'div[role="main"]',
    "main",
    "article",
    "#main-content",
)

# Never documentation, whatever the page — safe to remove unconditionally.
ALWAYS_DROP = (
    "nav", "aside", "header", "footer", "script", "style", "noscript",
    "form", "iframe", "svg", "button",
    '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]', '[role="search"]',
    '[aria-label="breadcrumb"]', '[aria-label="Pagination"]',
    ".md-sidebar", ".md-nav", ".md-header", ".md-footer", ".md-search", ".md-skip",
    ".sphinxsidebar", ".wy-nav-side", ".wy-side-nav-search", ".rst-footer-buttons",
    ".related", ".breadcrumb", ".breadcrumbs",
    ".headerlink",  # the ¶ anchor Sphinx/MkDocs append to every heading
    ".navbar", ".sidebar", ".edit-page", ".pagination-nav",
    ".theme-doc-toc-desktop", ".theme-doc-toc-mobile", ".theme-doc-breadcrumbs",
    ".skip-to-content", ".announcement", ".cookie", ".banner",
)

# Usually chrome — but on a documentation *index* page the toctree is the entire
# point of the page. Measured on rich.readthedocs.io's root: 1722 of 1802 characters.
# So these are dropped only when enough content survives without them.
SOFT_DROP = (".toc", ".toctree-wrapper", ".contents", ".local-toc")

# Below this, a candidate container is boilerplate rather than the page body.
MIN_MAIN_CHARS = 200

# Soft drops are kept only if the page still reads as a page afterwards: at least
# this many characters, and at least this share of what was there before. The
# proportional test is what distinguishes an on-page ToC beside real prose (a few
# percent — drop it) from an index page that *is* its table of contents (most of
# the text — keep it). An absolute threshold alone put two near-identical Sphinx
# index pages on opposite sides of the line.
MIN_CONTENT_AFTER_SOFT_DROP = 200
MIN_SHARE_AFTER_SOFT_DROP = 0.4

# Accessibility skip links appear under many different class names (or none), so
# match them by their text rather than trying to enumerate the markup.
_SKIP_LINK = re.compile(r"^\s*skip\s+(to|navigation)", re.IGNORECASE)
_EMPTY_LINK = re.compile(r"\[\s*\]\([^)]*\)")
_BLANK_RUN = re.compile(r"\n{3,}")
_PILCROW = re.compile(r"[¶¶]")


@traced("normalize_code_blocks", run_type="tool")
def normalize_code_blocks(container) -> None:
    """Repair code blocks shattered by DOM re-serialization.

    Syntax highlighters wrap every token in its own `<span>`, and a serializer that
    pretty-prints will insert a newline between them. Inside `<pre>` that whitespace
    is significant, so a single statement arrives split across a dozen lines:

        return {          ->      return {
            "item_name":            "item_name"
            item.name               : item
                                    .
                                    name

    Highlighters also wrap each *line* in its own element, which is the signal used
    here: if a line element's own text contains newlines, they were injected, so the
    line is rejoined and real breaks are restored between the wrappers.
    """
    for pre in container.find_all("pre"):
        code = pre.find("code") or pre
        wrappers = [child for child in code.children if getattr(child, "name", None)]
        if not wrappers:
            continue  # plain text block, nothing to repair

        # A line wrapper holds the whole line, so it contains nested token elements.
        # A token span is a leaf. Without this check the token spans of a Pygments
        # block get mistaken for lines and every token lands on its own line.
        nested = sum(1 for w in wrappers if w.find(True) is not None)
        line_wrapped = nested * 2 >= len(wrappers)

        if line_wrapped and any("\n" in w.get_text() for w in wrappers):
            # Themes that wrap each line in its own element (MkDocs Material):
            # newlines inside a wrapper were injected, breaks belong between them.
            rebuilt = "\n".join(w.get_text().replace("\n", "") for w in wrappers)
            code.clear()
            code.append(NavigableString(rebuilt))
            continue

        # Themes with no line wrappers: tokens are siblings and the serializer put
        # a newline wherever the source had *nothing* between two tags. Real spaces
        # survive as " " and real breaks as "\n" plus indentation, so:
        #   "\n"      -> artifact between two tags, drop it
        #   "\n(\n"   -> GitHub wraps the artifact around content, unwrap it
        #   "\n    "  -> a real break plus indentation, keep
        #   "\n\n"    -> a real blank line, keep
        # Dropping a standalone "\n" is only safe in a densely tokenized block, where
        # a bare newline between two tags is overwhelmingly likely to be serializer
        # padding. Pygments — Sphinx, MkDocs, ReadTheDocs — names its token classes
        # in one to three letters ("k", "kn", "mf", "gp"); GitHub uses "pl-*" and
        # leaves real column-0 newlines that look identical to padding, where
        # deleting one welds two statements together. A block with no token spans at
        # all (plain text, a stray link) is left alone for the same reason.
        drop_bare_newlines = any(
            len(name) <= 3
            for element in code.select("span[class]")
            for name in element.get("class", [])
        )

        for node in [n for n in code.descendants if isinstance(n, NavigableString)]:
            text = str(node)
            if not text.strip():
                if text == "\n" and drop_bare_newlines:
                    node.extract()
                continue
            cleaned = re.sub(r"^\n(?=\S)", "", text)  # only when nothing is indented after
            cleaned = re.sub(r"\n$", "", cleaned)
            if cleaned != text:
                node.replace_with(NavigableString(cleaned))


def collapse_inline_whitespace(container) -> None:
    """Collapse serializer whitespace in ordinary prose.

    The same pretty-printing that breaks `<pre>` also scatters prose across lines —
    "The\\n`fastapi dev`\\nserver" instead of one sentence. Outside `<pre>` HTML
    whitespace is insignificant, so collapsing it is lossless; paragraph structure
    lives in the elements, not the text nodes.
    """
    for node in list(container.find_all(string=True)):
        if node.find_parent(["pre", "code", "textarea"]):
            continue  # significant in here
        collapsed = re.sub(r"\s+", " ", str(node))
        if collapsed != str(node):
            node.replace_with(NavigableString(collapsed))


@traced("extract_main", run_type="parser")
def extract_main(html: str) -> str:
    """Return the HTML of the page's documentation body, chrome removed."""
    soup = BeautifulSoup(html, "html.parser")

    container = None
    chosen = ""
    for selector in MAIN_SELECTORS:
        candidate = soup.select_one(selector)
        # Guard on text length: many themes ship an empty <main> wrapper, and
        # picking it would throw away the whole page.
        if candidate and len(candidate.get_text(strip=True)) >= MIN_MAIN_CHARS:
            container = candidate
            chosen = selector
            break
    if container is None:
        container = soup.body or soup
        chosen = "body (no main-content selector matched)"

    # Before anything else: whitespace inside <pre> is significant, and a
    # re-serialized DOM arrives with it corrupted.
    normalize_code_blocks(container)
    collapse_inline_whitespace(container)

    for selector in ALWAYS_DROP:
        for node in container.select(selector):
            node.decompose()

    for anchor in container.find_all("a"):
        if _SKIP_LINK.match(anchor.get_text(" ", strip=True)):
            anchor.decompose()

    # Try the conditional drops on a copy, and keep the result only if the page
    # still has content afterwards. On an index page the table of contents is the
    # content, and removing it would leave an empty file in the store.
    before = len(container.get_text(strip=True))
    trimmed = copy.copy(container)
    for selector in SOFT_DROP:
        for node in trimmed.select(selector):
            node.decompose()

    after = len(trimmed.get_text(strip=True))
    keeps_enough = after >= MIN_CONTENT_AFTER_SOFT_DROP
    keeps_share = before == 0 or after / before >= MIN_SHARE_AFTER_SOFT_DROP
    if keeps_enough and keeps_share:
        container = trimmed

    annotate(
        main_selector=chosen,
        html_chars_in=len(html),
        text_chars_before_soft_drop=before,
        text_chars_after_soft_drop=after,
        soft_drop_applied=keeps_enough and keeps_share,
    )
    return str(container)


@traced("tidy_markdown", run_type="parser")
def tidy_markdown(text: str) -> str:
    """Remove conversion artifacts that carry no meaning."""
    text = _EMPTY_LINK.sub("", text)
    text = _PILCROW.sub("", text)
    lines = [line.rstrip() for line in text.splitlines()]
    return _BLANK_RUN.sub("\n\n", "\n".join(lines)).strip()


@traced("html_to_markdown", run_type="parser")
def html_to_markdown(html: str) -> str:
    """Full path: isolate the documentation body, then convert it to markdown."""
    return tidy_markdown(markdownify(extract_main(html), heading_style="ATX"))
