"""Stripping page chrome without eating documentation."""

from __future__ import annotations

from ark.clean import extract_main, html_to_markdown, tidy_markdown

BODY = "<p>" + ("Real documentation prose. " * 20) + "</p>"

PAGE = f"""
<html><body>
  <header class="md-header"><a href="/">Logo</a></header>
  <nav class="md-nav">
    <a href="/a">Installation</a><a href="/b">Security</a><a href="/c">Metadata</a>
  </nav>
  <aside class="toc"><a href="#one">One</a><a href="#two">Two</a></aside>
  <article class="md-content__inner">
    <h1>Query Parameters<a class="headerlink" href="#q">&para;</a></h1>
    {BODY}
    <pre><code>from fastapi import FastAPI

app = FastAPI()</code></pre>
  </article>
  <footer class="md-footer">Copyright 2026</footer>
  <script>analytics()</script>
</body></html>
"""


def test_main_container_is_isolated():
    html = extract_main(PAGE)
    assert "Real documentation prose" in html
    assert "Installation" not in html
    assert "Copyright 2026" not in html


def test_chrome_is_gone_from_markdown():
    md = html_to_markdown(PAGE)
    for chrome in ("Installation", "Security", "Metadata", "Copyright 2026", "analytics()"):
        assert chrome not in md


def test_documentation_survives():
    md = html_to_markdown(PAGE)
    assert "Query Parameters" in md
    assert "Real documentation prose" in md


def test_code_blocks_keep_their_line_breaks():
    """The whole point of converting HTML ourselves rather than taking the
    provider's markdown."""
    md = html_to_markdown(PAGE)
    assert "from fastapi import FastAPI" in md
    assert "app = FastAPI()" in md
    assert "from fastapi import FastAPI app = FastAPI()" not in md  # not flattened


def test_headerlink_pilcrow_is_removed():
    assert "¶" not in html_to_markdown(PAGE)


def test_falls_back_to_body_when_no_main_container():
    page = f"<html><body><nav><a href='/x'>Nav</a></nav>{BODY}</body></html>"
    md = html_to_markdown(page)
    assert "Real documentation prose" in md
    assert "Nav" not in md  # chrome still stripped on the fallback path


def test_empty_main_wrapper_is_not_mistaken_for_the_body():
    """Themes ship empty <main> wrappers; picking one would discard the page."""
    page = f"<html><body><main></main><div class='document'>{BODY}</div></body></html>"
    assert "Real documentation prose" in extract_main(page)


def test_a_page_that_is_only_chrome_yields_little():
    page = "<html><body><nav><a href='/a'>A</a></nav></body></html>"
    assert html_to_markdown(page).strip() == ""


def test_legitimate_link_lists_inside_content_are_kept():
    """An API index is links too — cleanup is structural, never link-density based."""
    page = (
        "<html><body><article class='md-content__inner'>"
        "<h2>API reference</h2>"
        "<ul><li><a href='/api/get'>get()</a></li>"
        "<li><a href='/api/post'>post()</a></li>"
        "<li><a href='/api/put'>put()</a></li></ul>"
        f"{BODY}</article></body></html>"
    )
    md = html_to_markdown(page)
    for name in ("get()", "post()", "put()"):
        assert name in md


def test_tidy_collapses_blank_runs_and_empty_links():
    assert tidy_markdown("a\n\n\n\n\nb") == "a\n\nb"
    assert tidy_markdown("text [](https://x.dev) more") == "text  more"
    assert tidy_markdown("  padded  \n\n") == "padded"


def test_markdown_input_is_left_alone():
    """Structure is gone by then; guessing would eat real content."""
    from ark.brightdata import row_to_markdown

    md = "# Title\n\n* [Install](a.html)\n* [Usage](b.html)\n\nProse."
    assert row_to_markdown({"markdown": md}) == md


def test_skip_links_are_removed_regardless_of_markup():
    """Skip links appear under many class names, so they're matched by text."""
    page = (
        "<html><body><a href='#content'>Skip to main content</a>"
        f"<div class='document'>{BODY}</div></body></html>"
    )
    md = html_to_markdown(page)
    assert "Skip to main content" not in md
    assert "Real documentation prose" in md


def test_a_heading_that_merely_starts_with_skip_is_not_a_skip_link():
    page = f"<html><body><article role='main'><h1>Skipping records</h1>{BODY}</article></body></html>"
    assert "Skipping records" in html_to_markdown(page)


def test_index_page_keeps_its_table_of_contents():
    """On a docs index the toctree IS the content — stripping it empties the page.

    Measured on rich.readthedocs.io's root: the toctree was 1722 of 1802 chars.
    """
    page = (
        "<html><body><div class='document'>"
        "<h1>Welcome to Rich's documentation!</h1>"
        "<div class='toctree-wrapper'><ul>"
        + "".join(f"<li><a href='{n}.html'>Chapter about {n} and its usage</a></li>"
                  for n in ("console", "style", "markup", "tables", "panels", "progress"))
        + "</ul></div></div></body></html>"
    )
    md = html_to_markdown(page)
    assert "Chapter about console" in md
    assert "Chapter about progress" in md


def test_content_page_still_drops_its_toc():
    """When real prose exists, the on-page ToC is chrome and goes."""
    page = (
        "<html><body><article role='main'>"
        "<div class='toc'><a href='#a'>Jump to A</a><a href='#b'>Jump to B</a></div>"
        f"{BODY}</article></body></html>"
    )
    md = html_to_markdown(page)
    assert "Jump to A" not in md
    assert "Real documentation prose" in md


def test_index_page_keeps_toc_even_when_prose_clears_the_absolute_floor():
    """Regression: pypdf's index had 432 chars of prose beside a toctree holding
    73% of the page. An absolute-only threshold dropped the toctree there while
    keeping it on rich's near-identical index (194 chars). The share test fixes it."""
    # Proportions taken from the real page: 432 chars of prose, 1649 total.
    prose = "<p>" + ("pypdf is a free and open source pure-python PDF library. " * 8) + "</p>"
    sections = (
        "install", "extract", "encrypt", "merge", "crop", "metadata", "images",
        "attachments", "robustness", "security", "warnings", "transforming",
        "annotations", "forms", "streaming", "reading", "writing", "adding",
        "compression", "cli",
    )
    toc = "<div class='toctree-wrapper'><ul>" + "".join(
        f"<li><a href='{n}.html'>Chapter covering {n} in detail and at length</a></li>"
        for n in sections
    ) + "</ul></div>"
    md = html_to_markdown(f"<html><body><div class='document'>{prose}{toc}</div></body></html>")

    assert "pypdf is a free" in md
    assert "Chapter covering install" in md


def test_small_toc_beside_substantial_prose_is_still_dropped():
    prose = "<p>" + ("Real documentation prose explaining the API in depth. " * 40) + "</p>"
    toc = "<div class='toc'><a href='#a'>Jump to A</a></div>"
    md = html_to_markdown(f"<html><body><article role='main'>{toc}{prose}</article></body></html>")

    assert "Jump to A" not in md
    assert "Real documentation prose" in md


# --- code block fidelity -------------------------------------------------------------

# How a DOM serializer emits a highlighted block: one wrapper per line, tokens in
# their own spans, and a newline injected between every one of them.
SHATTERED = """
<html><body><article role="main">
<pre><code><span id="__span-1"><span class="k">def</span>
<span class="w"> </span>
<span class="nf">read_item</span>
<span class="p">(</span>
<span class="n">item_id</span>
<span class="p">:</span> <span class="nb">int</span>
<span class="p">):</span>
</span><span id="__span-2">    <span class="k">return</span> <span class="p">{</span>
<span class="s2">"item_id"</span>
<span class="p">:</span> <span class="n">item_id</span>
<span class="p">}</span>
</span></code></pre>
<p>The
<code>fastapi dev</code>
server reloads.</p>
</article></body></html>
"""


def test_shattered_code_block_is_rejoined():
    """A statement split across a dozen lines is not runnable Python, and this
    store exists to give coding agents runnable code."""
    md = html_to_markdown(SHATTERED)
    assert "def read_item(item_id: int):" in md
    assert 'return {"item_id": item_id}' in md


def test_real_line_breaks_survive_rejoining():
    md = html_to_markdown(SHATTERED)
    body = md[md.find("def read_item") :]
    assert body.splitlines()[0].startswith("def read_item")
    assert body.splitlines()[1].startswith("    return")  # indentation preserved


def test_already_clean_code_is_untouched():
    """Raw HTML off the wire has correct whitespace — don't 'fix' it."""
    clean = (
        "<html><body><article role='main'><pre><code>"
        "def f():\n    return 1\n</code></pre></article></body></html>"
    )
    md = html_to_markdown(clean)
    assert "def f():" in md
    assert "    return 1" in md


def test_plain_pre_without_wrappers_is_untouched():
    page = "<html><body><article role='main'><pre>line one\nline two</pre></article></body></html>"
    md = html_to_markdown(page)
    assert "line one\nline two" in md


def test_prose_whitespace_is_collapsed():
    md = html_to_markdown(SHATTERED)
    assert "The `fastapi dev` server reloads." in md


def test_collapsing_prose_does_not_touch_code():
    md = html_to_markdown(SHATTERED)
    assert "def read_item(item_id: int): return" not in md  # code kept its newline


# Tokens as bare siblings, artifacts as standalone "\n" text nodes (uvicorn.dev).
SIBLING_TOKENS = """
<html><body><article role="main"><pre><code>
<span class="k">async</span> <span class="k">def</span>
<span class="w"> </span>
<span class="nf">app</span>
<span class="p">(</span>
<span class="n">scope</span>
<span class="p">):</span>
<span class="k">assert</span> <span class="n">scope</span>
</code></pre></article></body></html>
"""

# GitHub wraps the artifact *around* the content: "\n(\n" where source had "(".
GITHUB_STYLE = """
<html><body><article role="main"><pre>
<span class="pl-k">from</span> <span class="pl-s1">rich</span> <span class="pl-k">import</span> <span class="pl-s1">print</span>

<span class="pl-en">print</span>
<span class="pl-s">"Hello"</span>
<span class="pl-s">":vampire:"</span>
</pre></article></body></html>
"""


def test_sibling_token_artifacts_are_dropped():
    md = html_to_markdown(SIBLING_TOKENS)
    assert "async def app(scope):" in md


def test_indentation_after_a_real_break_is_preserved():
    page = SIBLING_TOKENS.replace(
        '<span class="p">):</span>\n', '<span class="p">):</span>\n    '
    )
    md = html_to_markdown(page)
    assert "\n    assert scope" in md


def test_blank_lines_in_code_survive():
    md = html_to_markdown(GITHUB_STYLE)
    block = md[md.find("from rich") :]
    assert "\n\n" in block  # the blank line between import and call


def test_artifacts_wrapped_around_content_are_unwrapped():
    page = GITHUB_STYLE.replace(
        '<span class="pl-en">print</span>\n', '<span class="pl-en">print</span>\n(\n'
    )
    md = html_to_markdown(page)
    assert "print(" in md


def test_bare_pre_never_welds_two_statements_together():
    """GitHub's <pre> has no <code>, and its real breaks include column-0 newlines
    that look exactly like artifacts. Deleting one produced
    'import Consoleconsole = Console()' — plausible-looking, broken Python."""
    page = (
        "<html><body><article role='main'><pre>"
        '<span class="pl-k">from</span> <span class="pl-s1">rich.console</span> '
        '<span class="pl-k">import</span> <span class="pl-v">Console</span>'
        "\n"
        '<span class="pl-s1">console</span> <span class="pl-c1">=</span> '
        '<span class="pl-v">Console</span>'
        "</pre></article></body></html>"
    )
    md = html_to_markdown(page)
    assert "Consoleconsole" not in md
    assert "import Console\nconsole" in md


# Pygments (Sphinx/ReadTheDocs): bare <pre>, token spans as leaves, whitespace
# tokenized into <span class="w">.
PYGMENTS_TOKENS = """
<html><body><article role="main"><pre>
<span></span>
<span class="kn">from</span>
<span class="w"> </span>
<span class="nn">hypothesis</span>
<span class="w"> </span>
<span class="kn">import</span> <span class="nn">given</span>
<span class="w">    </span><span class="k">pass</span>
</pre></article></body></html>
"""


def test_pygments_token_spans_are_not_mistaken_for_lines():
    """61 token spans were being treated as 61 lines, putting every token on its own
    line. Line wrappers contain nested elements; token spans are leaves."""
    md = html_to_markdown(PYGMENTS_TOKENS)
    assert "from hypothesis import given" in md


def test_pygments_indentation_is_preserved():
    md = html_to_markdown(PYGMENTS_TOKENS)
    assert "    pass" in md


def test_whitespace_token_marks_a_block_as_fully_tokenized():
    """<span class="w"> is the signal that the markup accounts for its own
    whitespace, so leftover bare newlines are serializer artifacts."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(PYGMENTS_TOKENS, "html.parser")
    assert soup.select_one("pre").select_one("span.w") is not None
