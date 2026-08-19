"""Node 3 — pick the canonical documentation URL for each library.

This is where the LLM earns its keep: separating fastapi.tiangolo.com from a Medium
tutorial that happens to rank well.
"""

from __future__ import annotations

import asyncio
import re
from urllib.parse import urlparse

from langchain_core.runnables import RunnableConfig

from ..config import Settings
from ..llm import build_llm, structured
from ..prompts import CURATE_LINKS_SYSTEM
from ..state import DocResearchState, DocSource, Library, SearchHit
from ..tracing import annotate, traced

# Domains that are never first-party documentation, whatever the model decides.
# The next pipeline stage scrapes these URLs, so a video or forum thread is useless.
NON_DOC_DOMAINS = frozenset(
    {
        "youtube.com",
        "youtu.be",
        "medium.com",
        "dev.to",
        "reddit.com",
        "stackoverflow.com",
        "quora.com",
        "x.com",
        "twitter.com",
        "linkedin.com",
        "facebook.com",
        "substack.com",
    }
)


# Paths that exist on documentation hosts but are not documentation. A GitHub repo
# root is a genuinely useful fallback (it renders the README); an issue thread is one
# person's problem, and scraping it wastes a record and pollutes the citations.
NON_DOC_PATHS = (
    "/issues", "/pull", "/pulls", "/discussions", "/commit", "/commits",
    "/blame", "/compare", "/search", "/stargazers", "/forks", "/actions",
    "/blog/", "/news/", "/tutorials/", "/posts/",
)


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def _is_non_doc(url: str) -> bool:
    host = _host(url)
    return any(host == domain or host.endswith("." + domain) for domain in NON_DOC_DOMAINS)


def _mentions_library(url: str, library: str) -> bool:
    """Is this URL plausibly about the library at all?

    A loose check on purpose — it only catches results that drifted to an unrelated
    project, which search does often enough for one-word package names.
    """
    stem = re.sub(r"[^a-z0-9]+", "", library.lower())
    haystack = re.sub(r"[^a-z0-9]+", "", url.lower())
    return not stem or stem in haystack


def _is_repo_root(url: str) -> bool:
    """github.com/<org>/<repo> — GitHub renders the README there, which is real docs.

    Anything deeper is an issue, a pull request or a file view.
    """
    if _host(url) != "github.com":
        return False
    return len([part for part in urlparse(url).path.split("/") if part]) == 2


def useful_alternate(url: str, library: str, primary: str) -> bool:
    """Is this runner-up worth a scrape and a citation?

    Alternates are scraped and cited like any other page, so a bad one costs a
    record and then dilutes the plan's grounding. Judged structurally rather than
    by asking the model again.
    """
    if not url or url == primary:
        return False
    if _is_non_doc(url):
        return False

    path = urlparse(url).path.rstrip("/").lower()
    if any(marker.rstrip("/") in path for marker in NON_DOC_PATHS):
        return False
    if _host(url).startswith(("blog.", "news.", "community.", "forum.", "discuss.")):
        return False
    if not _mentions_library(url, library):
        return False

    # The decisive test: an alternate is either more of the same documentation site,
    # or the project's repository. Search reaches for a same-named project often
    # enough — "httpx" returned a Go security scanner — and a page from an unrelated
    # project is worse than no alternate at all, because it gets cited.
    return _host(url) == _host(primary) or _is_repo_root(url)


@traced("filter_alternates", run_type="tool")
def filter_alternates(source: DocSource) -> list[str]:
    seen: set[str] = set()
    keep: list[str] = []
    for url in source.alternates:
        if url in seen or not useful_alternate(url, source.library, source.url):
            continue
        seen.add(url)
        keep.append(url)
    return keep


@traced("enforce_doc_domain", run_type="tool")
def _enforce_doc_domain(source: DocSource, hits: list[SearchHit]) -> DocSource:
    """Keep obviously non-documentation domains out of the results.

    The prompt already demotes them, but models still occasionally label a YouTube
    video `official_docs`. Prefer any usable alternative; if there is none, keep the
    URL but stop it claiming to be documentation.
    """
    if not _is_non_doc(source.url):
        return source

    replacement = next((hit for hit in hits if not _is_non_doc(hit.url)), None)
    if replacement is not None:
        source.alternates = [source.url, *source.alternates][:3]
        source.url = replacement.url
        source.title = replacement.title or source.title
        source.confidence = min(source.confidence, 0.5)
        source.rationale = (
            f"{source.rationale} (Model selected a non-documentation domain; "
            "substituted the best remaining candidate.)"
        ).strip()
        return source

    source.kind = "other"
    source.confidence = min(source.confidence, 0.2)
    source.rationale = (
        f"{source.rationale} (No first-party documentation found — this is not an "
        "official docs source.)"
    ).strip()
    return source


def _format_hits(hits: list[SearchHit]) -> str:
    lines = []
    for index, hit in enumerate(hits, start=1):
        score = f" (relevance {hit.score:.2f})" if hit.score is not None else ""
        lines.append(f"{index}. {hit.title or '(untitled)'}{score}\n   URL: {hit.url}")
        if hit.snippet:
            lines.append(f"   {hit.snippet[:400]}")
    return "\n".join(lines)


@traced("finalize_doc_source", run_type="tool")
def _finalize(source: DocSource, library: Library, hits: list[SearchHit]) -> DocSource:
    """Apply the guards every curated source must pass, however it was produced."""
    # The library name is ours to assign, not the model's — keep it authoritative.
    source.library = library.name

    # Guard against a hallucinated URL: fall back to the top search hit.
    allowed = {hit.url for hit in hits}
    if source.url not in allowed:
        annotate(hallucinated_url=source.url, fell_back_to=hits[0].url)
        source.alternates = [source.url, *source.alternates][:3]
        source.url = hits[0].url
        source.confidence = min(source.confidence, 0.4)
        source.rationale = (
            f"{source.rationale} (Model proposed a URL absent from the search results; "
            "fell back to the top hit.)"
        ).strip()
    source = _enforce_doc_domain(source, hits)
    source.alternates = filter_alternates(source)[:3]
    return source


def provided_source(library: Library, urls: list[str]) -> DocSource:
    """A source the user pinned. No search ran, so there is nothing to curate.

    Confidence is 1.0 because this is not the model's guess — it is an instruction.
    The first URL is the primary and any others become alternates, so several pages
    of one library all reach the store. Nothing is added beyond what was given:
    padding with guesses would put unrequested URLs into the scrape and citations.
    """
    return DocSource(
        library=library.name,
        url=urls[0],
        title=library.name,
        kind="official_docs",
        confidence=1.0,
        rationale="Documentation URL(s) supplied by the user.",
        alternates=list(urls[1:]),
        user_supplied=True,
    )


@traced("curate_one_library", run_type="chain")
async def _curate_one(
    settings: Settings,
    library: Library,
    hits: list[SearchHit],
    limiter: asyncio.Semaphore,
) -> DocSource:
    llm = build_llm(settings, json_mode=True)
    version = f" (user asked for version {library.version_hint})" if library.version_hint else ""
    user = (
        f"Library: {library.name} [{library.ecosystem}]{version}\n"
        f"Needed because: {library.reason or 'unspecified'}\n\n"
        f"Search results:\n{_format_hits(hits)}"
    )
    async with limiter:  # bounded so we don't trip Groq's tokens-per-minute limit
        source = await structured(llm, DocSource, CURATE_LINKS_SYSTEM, user)
    final = _finalize(source, library, hits)
    annotate(
        library=library.name,
        chosen=final.url,
        kind=final.kind,
        confidence=final.confidence,
        alternates=final.alternates,
    )
    return final


async def curate_links(state: DocResearchState, config: RunnableConfig) -> dict:
    settings: Settings = config["configurable"]["settings"]
    hits = state.get("hits", {})
    libraries = [library for library in state.get("libraries", []) if hits.get(library.name)]
    if not libraries:
        return {"doc_sources": []}

    provided = state.get("provided", {})
    curated: dict[str, DocSource] = {
        library.name: provided_source(library, provided[library.name])
        for library in libraries
        if library.name in provided
    }
    to_curate = [library for library in libraries if library.name not in curated]

    limiter = asyncio.Semaphore(settings.llm_concurrency)
    outcomes = await asyncio.gather(
        *(_curate_one(settings, library, hits[library.name], limiter) for library in to_curate),
        return_exceptions=True,
    )

    errors: list[str] = []
    for library, outcome in zip(to_curate, outcomes):
        if isinstance(outcome, BaseException):
            # Curation failing shouldn't lose the search work — keep the top hit.
            top = hits[library.name][0]
            errors.append(f"{library.name}: curation failed ({outcome}); used top search result")
            curated[library.name] = DocSource(
                library=library.name,
                url=top.url,
                title=top.title,
                confidence=0.3,
                rationale="Curation step failed; this is the highest-ranked search result.",
            )
            continue
        curated[library.name] = outcome

    # Keep the order the libraries were identified in.
    doc_sources = [curated[lib.name] for lib in libraries if lib.name in curated]
    annotate(curated=len(doc_sources), provided=len(provided), failed=len(errors))
    return {"doc_sources": doc_sources, "errors": errors}
