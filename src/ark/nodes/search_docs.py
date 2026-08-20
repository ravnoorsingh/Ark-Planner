"""Node 2 — find candidate documentation URLs via the web-search MCP tool.

The tool is invoked directly by name rather than through LLM tool-calling: we know
exactly what to search for, so a deterministic call per library is cheaper and more
predictable than a ReAct loop.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import re
from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool

from ..config import Settings
from ..mcp_client import require_tool, search_arguments, search_tool_name
from ..state import DocResearchState, Library, SearchHit
from ..tracing import annotate, traced

_URL_RE = re.compile(r"https?://[^\s<>\"'\])}]+")


def _coerce_payload(raw: Any) -> Any:
    """Reduce whatever the MCP adapter returned down to text or a parsed structure.

    Depending on the adapter version and tool config this may be a plain string, a
    (content, artifact) tuple, a list of content blocks, or already-parsed JSON.
    """
    if isinstance(raw, tuple):
        raw = raw[0]
    if isinstance(raw, list):
        parts = []
        for block in raw:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            elif hasattr(block, "text"):
                parts.append(block.text)
            else:
                parts.append(str(block))
        raw = "\n".join(parts)
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return raw
    return raw


@traced("normalize_search_results", run_type="parser")
def _to_hits(raw: Any, *, limit: int = 10) -> list[SearchHit]:
    """Normalize a search response into SearchHits, whichever provider sent it.

    Firecrawl nests results under `web` and describes them with `description`;
    Tavily uses `results` and `content` plus a relevance `score`. Both shapes are
    accepted here so the node stays provider-agnostic — along with a bare list of
    results and an unstructured text response, from which URLs are recovered by
    regex.
    """
    payload = _coerce_payload(raw)

    results: list = []
    if isinstance(payload, dict):
        for key in ("results", "web", "data", "hits"):
            value = payload.get(key)
            if isinstance(value, list):
                results = value
                break
            # Firecrawl nests the list one level deeper: {"data": {"web": [...]}}
            if isinstance(value, dict):
                for inner in ("web", "results"):
                    if isinstance(value.get(inner), list):
                        results = value[inner]
                        break
            if results:
                break
    elif isinstance(payload, list):
        results = payload

    hits: list[SearchHit] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        url = item.get("url") or item.get("link")
        if not url:
            continue
        score = item.get("score")
        hits.append(
            SearchHit(
                url=str(url),
                title=str(item.get("title") or ""),
                snippet=str(
                    item.get("description")  # firecrawl
                    or item.get("content")  # tavily
                    or item.get("snippet")
                    or ""
                )[:1000],
                score=float(score) if isinstance(score, (int, float)) else None,
            )
        )

    if not hits and isinstance(payload, str):
        # Unstructured text response — salvage whatever URLs it mentions.
        seen: set[str] = set()
        for url in _URL_RE.findall(payload):
            url = url.rstrip(".,;")
            if url not in seen:
                seen.add(url)
                hits.append(SearchHit(url=url))

    return hits[:limit]


@traced("search_one_library", run_type="chain")
async def _search_one(
    tool: BaseTool, library: Library, settings: Settings
) -> tuple[str, list[SearchHit]]:
    query = f"{library.name} official documentation"
    if library.version_hint:
        query += f" {library.version_hint}"
    annotate(query=query, backend=settings.search_backend, tool=tool.name)

    # An empty result for a mainstream library is almost always a transient hiccup
    # rather than a real absence — losing the library costs far more than one retry.
    for attempt in range(2):
        raw = await tool.ainvoke(search_arguments(settings, query))
        hits = _to_hits(raw, limit=settings.search_max_results)
        if hits:
            return library.name, hits
        if attempt == 0:
            annotate(empty_result_retried=True)
            await asyncio.sleep(1.0)
    return library.name, []


def _match_provided(
    libraries: list[Library], provided: dict[str, list[str]]
) -> tuple[dict[str, list[str]], list[Library]]:
    """Split user URLs into ones for detected libraries and ones for new entries.

    Matching is case-insensitive because the user types `fastapi` while the model
    may have named it `FastAPI`, and a strict match would silently ignore the pin
    and search anyway. A label matching nothing detected becomes a library of its
    own — that is how a spec, an internal page or anything the requirement never
    mentioned gets into the run.
    """
    by_lower = {library.name.lower(): library.name for library in libraries}
    matched: dict[str, list[str]] = {}
    extra: list[Library] = []

    for name, urls in provided.items():
        label = name.strip()
        clean = [url.strip() for url in urls if url and url.strip()]
        if not label or not clean:
            continue
        canonical = by_lower.get(label.lower())
        if canonical is None:
            canonical = label
            extra.append(Library(name=label, reason="documentation supplied by the user"))
        matched[canonical] = clean
    return matched, extra


async def search_docs(state: DocResearchState, config: RunnableConfig) -> dict:
    settings: Settings = config["configurable"]["settings"]
    provider = config["configurable"]["tools"]
    libraries = state.get("libraries", [])
    if not libraries:
        return {"hits": {}}

    # Libraries the user pinned a URL for skip search entirely — and skip curation
    # too, since there is nothing left to choose between.
    provided, extra = _match_provided(libraries, config["configurable"].get("doc_urls") or {})
    ask = config["configurable"].get("ask_doc_urls")
    if ask is not None:
        answered = ask([*libraries, *extra], provided)
        if inspect.isawaitable(answered):
            answered = await answered
        more, more_extra = _match_provided([*libraries, *extra], answered or {})
        provided.update(more)
        extra.extend(more_extra)

    # Labels the requirement never mentioned still belong in the run.
    libraries = [*libraries, *extra]

    hits: dict[str, list[SearchHit]] = {
        name: [
            SearchHit(url=url, title=name, snippet="Documentation URL supplied by the user.")
            for url in urls
        ]
        for name, urls in provided.items()
    }
    to_search = [library for library in libraries if library.name not in provided]
    if provided:
        annotate(provided=sorted(provided), searched=[lib.name for lib in to_search])
    if not to_search:
        return {"hits": hits, "provided": provided, "libraries": libraries}

    # Only now is a search backend needed at all. Tests pass a plain dict of tools;
    # the pipeline passes a LazyTools that connects on this first call.
    tools = provider if isinstance(provider, dict) else await provider.get()
    tool = require_tool(tools, search_tool_name(settings))
    outcomes = await asyncio.gather(
        *(_search_one(tool, library, settings) for library in to_search),
        return_exceptions=True,
    )

    errors: list[str] = []
    for library, outcome in zip(to_search, outcomes):
        if isinstance(outcome, BaseException):
            errors.append(f"{library.name}: search failed — {outcome}")
            continue
        name, library_hits = outcome
        if not library_hits:
            errors.append(f"{name}: search returned no usable results")
        hits[name] = library_hits

    annotate(
        libraries=len(libraries),
        hits_per_library={name: len(found) for name, found in hits.items()},
        failed=len(errors),
    )
    return {"hits": hits, "provided": provided, "libraries": libraries, "errors": errors}
