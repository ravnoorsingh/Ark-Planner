"""Node 4 — scrape the curated doc URLs via Bright Data into the `data/` store.

Every URL in the run goes out in a single trigger, because `/dca/trigger` accepts
an array of inputs and bills per record either way. One snapshot, one poll loop.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from datetime import UTC, datetime

from langchain_core.runnables import RunnableConfig

from ..brightdata import (
    BrightDataError,
    row_canonical_url,
    row_title,
    row_to_markdown,
    same_page,
    scrape_urls,
)
from ..config import Settings
from ..state import DocResearchState, DocSource, ScrapedDoc
from ..store import failed_document, load_manifest, merge_manifest, save_manifest, write_document
from ..tracing import annotate, traced


@traced("planned_urls", run_type="tool")
def planned_urls(
    doc_sources: list[DocSource], max_alternates: int
) -> list[tuple[str, str, str, int]]:
    """Expand doc sources into (library, url, role, rank), de-duplicated.

    The same URL can legitimately appear as one library's primary and another's
    alternate; scraping it twice would bill twice for identical content.
    """
    planned: list[tuple[str, str, str, int]] = []
    seen: set[str] = set()
    for source in doc_sources:
        # --max-alternates caps how many *guessed* runner-ups get scraped. URLs the
        # user named are instructions, not guesses, so they are all fetched.
        extra = source.alternates if source.user_supplied else source.alternates[:max_alternates]
        candidates = [(source.url, "primary", 0)]
        candidates += [(url, "alternate", rank) for rank, url in enumerate(extra, start=1)]
        for url, role, rank in candidates:
            if not url or url in seen:
                continue
            seen.add(url)
            planned.append((source.library, url, role, rank))
    return planned


@traced("scrape_to_store", run_type="chain")
async def scrape_to_store(
    settings: Settings,
    doc_sources: list[DocSource],
    *,
    query: str = "",
    max_alternates: int | None = None,
    on_tick: Callable[[float], None] | None = None,
    store: object | None = None,
    use_cache: bool = True,
) -> tuple[list[ScrapedDoc], list[str]]:
    """Scrape every planned URL and persist it. Returns (documents, errors)."""
    limit = settings.max_alternates if max_alternates is None else max_alternates
    plan = planned_urls(doc_sources, limit)
    if not plan:
        return [], []

    urls = [url for _, url, _, _ in plan]
    annotate(urls=len(urls), backend=settings.scrape_backend, max_alternates=limit)

    # Pages another run already fetched are reused rather than paid for again. The
    # cache is keyed by URL, not by query, which is what makes it shareable.
    cached: dict[str, dict] = {}
    if store is not None and use_cache:
        cached = await store.cached(urls, settings.doc_cache_ttl_days)
    to_fetch = [url for url in urls if url not in cached]

    rows: dict[str, dict | None] = {url: doc["raw"] for url, doc in cached.items()}
    try:
        if to_fetch:
            rows.update(await scrape_urls(settings, to_fetch, on_tick=on_tick))
    except BrightDataError as exc:
        # The whole snapshot failed: record every URL as failed rather than
        # returning nothing, so the manifest reflects what was attempted.
        message = str(exc)
        return (
            [
                failed_document(lib, url, role, rank, message, query)
                for lib, url, role, rank in plan
            ],
            [f"Bright Data scrape failed: {message}"],
        )

    reused = len(cached)

    provenance = (
        f"brightdata-collector:{settings.brightdata_collector_id}"
        if settings.scrape_backend == "collector"
        else f"brightdata-unlocker:{settings.brightdata_unlocker_zone}"
    )
    documents: list[ScrapedDoc] = []
    errors: list[str] = []
    for library, url, role, rank in plan:
        row = rows.get(url)
        if row is None:
            documents.append(
                failed_document(
                    library, url, role, rank, "Collector returned no row for this URL", query
                )
            )
            errors.append(f"{library}: no row returned for {url}")
            continue

        markdown = row_to_markdown(row, settings.brightdata_content_field)

        # A collector that crawls rather than fetching the exact URL will hand back
        # a different page. Record where the text really came from, and say so —
        # silently filing it under the requested URL would poison every citation
        # built on this store.
        actual = row_canonical_url(row)
        drifted = bool(actual) and not same_page(actual, url)
        if drifted:
            errors.append(f"{library}: asked for {url} but the collector returned {actual}")

        doc = write_document(
            settings.data_dir,
            library=library,
            url=url,
            role=role,
            rank=rank,
            markdown=markdown,
            raw_row=row,
            title=row_title(row),
            fetched_via=provenance,
            resolved_url=actual if drifted else "",
            query=query,
            from_cache=url in cached,
        )
        if doc.status == "empty":
            errors.append(
                f"{library}: no content field found in the row for {url}. "
                "Run scripts/check_brightdata.py and set BRIGHT_DATA_CONTENT_FIELD."
            )
        # Only successful pages are cached: a transient hiccup must not be served
        # back for the whole TTL.
        elif store is not None and url in cached:
            # Already stored — just note that this query used it too, so the reuse
            # is visible in the store rather than only in this run's console output.
            await store.reused(url, query)
        elif store is not None:
            await store.remember(
                url,
                {
                    "markdown": markdown,
                    "raw": row,
                    "sha256": doc.sha256,
                    "bytes": doc.bytes,
                    "resolved_url": doc.resolved_url,
                    "fetched_via": provenance,
                    "fetched_at": datetime.now(UTC),
                },
                query,
            )
        documents.append(doc)

    manifest = merge_manifest(
        load_manifest(settings.data_dir), documents, provenance
    )
    save_manifest(settings.data_dir, manifest)
    annotate(
        stored=sum(1 for doc in documents if doc.status == "ok"),
        empty=sum(1 for doc in documents if doc.status == "empty"),
        failed=sum(1 for doc in documents if doc.status == "failed"),
        bytes_stored=sum(doc.bytes for doc in documents),
        cache_hits=reused,
        fetched=len(to_fetch),
    )
    return documents, errors


async def scrape_docs(state: DocResearchState, config: RunnableConfig) -> dict:
    settings: Settings = config["configurable"]["settings"]
    doc_sources = state.get("doc_sources", [])
    if not doc_sources:
        return {"documents": []}

    # Last look before anything is billed: every URL below becomes a scrape record
    # and, if it is wrong, a citation in the plan. This is the only point where the
    # complete list exists and nothing has been spent yet.
    review = config["configurable"].get("review_urls")
    if review is not None:
        reviewed = review(doc_sources)
        if inspect.isawaitable(reviewed):
            reviewed = await reviewed
        if reviewed is None:  # the user backed out
            return {"documents": [], "errors": ["Scrape cancelled at the review step."]}
        doc_sources = reviewed

    documents, errors = await scrape_to_store(
        settings,
        doc_sources,
        query=state.get("requirement", ""),
        max_alternates=config["configurable"].get("max_alternates"),
        store=config["configurable"].get("store"),
        use_cache=config["configurable"].get("use_cache", True),
    )
    # Return the reviewed sources so the artifact records what was actually
    # scraped rather than what curation originally proposed.
    return {"documents": documents, "doc_sources": doc_sources, "errors": errors}
