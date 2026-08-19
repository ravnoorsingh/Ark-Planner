"""Turn scraped documentation into a citation-backed implementation plan.

The corpus does not fit in one context window — five libraries measured at ~47k
tokens, and a wide stack projects to ~122k — so this is a map-reduce:

    map     one distill call per library  -> LibraryBrief
    reduce  one synthesis call over the briefs -> PlanDraft
    render  PlanDraft + briefs -> plan.md with a Sources table

Citations are assigned here rather than by the model. Keys are derived from the
documents we actually scraped, so a marker can only ever point at a real page, and
the Sources table carries the sha256 of the exact snapshot the claim was drawn from.
"""

from __future__ import annotations

import re
from pathlib import Path

from .state import Citation, LibraryBrief, PlanDraft, ScrapedDoc
from .tracing import annotate, traced

# Rough chars-per-token; used only to keep a distill call inside the window.
CHARS_PER_TOKEN = 4
DEFAULT_DISTILL_BUDGET = 60_000  # chars of docs per library, ~15k tokens

_KEY_SAFE = re.compile(r"[^a-z0-9]+")
_FOOTNOTE = re.compile(r"\[\^([^\]]+)\]")


def citation_key(library: str, index: int) -> str:
    slug = _KEY_SAFE.sub("-", library.lower()).strip("-") or "doc"
    return f"{slug}-{index}"


@traced("build_citations", run_type="tool")
def build_citations(documents: list[ScrapedDoc]) -> list[Citation]:
    """Assign a stable footnote key to every usable scraped page."""
    citations: list[Citation] = []
    counters: dict[str, int] = {}
    for doc in documents:
        if doc.status != "ok" or not doc.path:
            continue  # nothing to cite — the page was never stored
        counters[doc.library] = counters.get(doc.library, 0) + 1
        citations.append(
            Citation(
                key=citation_key(doc.library, counters[doc.library]),
                library=doc.library,
                # Cite where the text actually came from, not what we asked for.
                url=doc.resolved_url or doc.url,
                path=doc.path,
                sha256=doc.sha256,
                fetched_at=doc.fetched_at,
            )
        )
    annotate(documents=len(documents), citable=len(citations))
    return citations


def _strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


@traced("load_corpus", run_type="retriever")
def load_corpus(citations: list[Citation], budget: int = DEFAULT_DISTILL_BUDGET) -> str:
    """Concatenate cited pages into one prompt payload, capped at `budget` chars.

    The cap is shared out evenly rather than first-come, so one enormous page cannot
    crowd out a small but essential one (an install page is often the shortest file
    and the most important).
    """
    readable = [c for c in citations if c.path and Path(c.path).exists()]
    if not readable:
        return ""

    share = max(budget // len(readable), 1_000)
    chunks: list[str] = []
    for citation in readable:
        body = _strip_front_matter(Path(citation.path).read_text(encoding="utf-8")).strip()
        if len(body) > share:
            body = body[:share] + "\n\n[... truncated ...]"
        chunks.append(f"### SOURCE [^{citation.key}] — {citation.url}\n\n{body}")
    corpus = "\n\n---\n\n".join(chunks)
    annotate(
        pages=len(readable),
        unreadable=len(citations) - len(readable),
        per_page_share_chars=share,
        corpus_chars=len(corpus),
    )
    return corpus


def used_keys(*texts: str) -> set[str]:
    found: set[str] = set()
    for text in texts:
        found.update(_FOOTNOTE.findall(text or ""))
    return found


def cell(text: str) -> str:
    """Make a value safe inside a markdown table row.

    A newline or a bare pipe in a model-supplied string silently breaks the table
    for everything below it — docs often show install commands across two lines.
    """
    return " ".join(str(text).split()).replace("|", "\\|")


def _render_api(brief: LibraryBrief) -> list[str]:
    lines: list[str] = []
    for item in brief.api:
        heading = f"**`{item.signature or item.name}`**"
        lines.append(heading)
        if item.summary:
            lines.append(f"\n{item.summary}")
        if item.example:
            lines.append(f"\n```\n{item.example.strip()}\n```")
        lines.append("")
    return lines


@traced("render_plan", run_type="tool")
def render_plan(
    requirement: str,
    draft: PlanDraft,
    briefs: list[LibraryBrief],
    citations: list[Citation],
    *,
    model: str = "",
    generated_at: str = "",
) -> str:
    """Render the final plan.md: reference digest, phased plan, then Sources."""
    by_key = {c.key: c for c in citations}
    lines: list[str] = [f"# {draft.title or 'Implementation plan'}", ""]
    lines += [f"> **Goal:** {requirement.strip()}", ""]

    provenance = ", ".join(filter(None, [f"model `{model}`" if model else "", generated_at]))
    if provenance:
        grounding = (
            f"> Grounded in {len(citations)} documentation page(s) scraped for this "
            f"requirement. Generated by {provenance}."
        )
        lines += [grounding, ""]

    if draft.overview:
        lines += [draft.overview.strip(), ""]

    # --- dependency table ---------------------------------------------------------
    installable = [b for b in briefs if b.install or b.version]
    if installable:
        lines += [
            "## Stack",
            "",
            "| Package | Version | Install | Docs |",
            "|---|---|---|---|",
        ]
        for brief in installable:
            refs = " ".join(f"[^{k}]" for k in brief.citation_keys if k in by_key)
            install = f"`{cell(brief.install)}`" if brief.install else "—"
            version = cell(brief.version) if brief.version else "unpinned"
            lines.append(f"| {cell(brief.library)} | {version} | {install} | {refs or '—'} |")
        lines.append("")

    # --- per-library reference digest ---------------------------------------------
    documented = [b for b in briefs if b.api or b.summary]
    if documented:
        lines += ["## Library reference", ""]
        for brief in documented:
            refs = " ".join(f"[^{k}]" for k in brief.citation_keys if k in by_key)
            lines.append(f"### {brief.library} {refs}".rstrip())
            lines.append("")
            if brief.summary:
                lines += [brief.summary.strip(), ""]
            lines += _render_api(brief)

    # --- the phased plan ----------------------------------------------------------
    if draft.phases:
        lines += ["## Implementation", ""]
        for index, phase in enumerate(draft.phases, start=1):
            lines.append(f"### Phase {index} — {phase.title}")
            lines += ["", phase.body.strip(), ""]

    # --- pitfalls -----------------------------------------------------------------
    pitfalls = draft.pitfalls or [g for b in briefs for g in b.gotchas]
    if pitfalls:
        lines += ["## Pitfalls", ""]
        lines += [f"- {p.strip()}" for p in pitfalls]
        lines.append("")

    # --- sources ------------------------------------------------------------------
    # Only cite what the prose actually referenced; an unused entry implies the plan
    # rests on a page it never drew from.
    body_so_far = "\n".join(lines)
    referenced = used_keys(body_so_far)
    cited = [c for c in citations if c.key in referenced] or citations

    lines += ["## Sources", ""]
    lines += ["| Ref | Library | Page | Retrieved |", "|---|---|---|---|"]
    for citation in cited:
        stamp = (citation.fetched_at or "")[:19].replace("T", " ")
        lines.append(
            f"| [^{citation.key}] | {cell(citation.library)} | <{cell(citation.url)}> | {stamp} |"
        )
    lines.append("")

    for citation in cited:
        local = f" — local copy `{citation.path}`" if citation.path else ""
        digest = f", sha256 `{citation.sha256[:12]}`" if citation.sha256 else ""
        lines.append(f"[^{citation.key}]: {citation.url}{local}{digest}")

    annotate(
        phases=len(draft.phases),
        citations_available=len(citations),
        citations_referenced=len(cited),
    )
    return "\n".join(lines).rstrip() + "\n"
