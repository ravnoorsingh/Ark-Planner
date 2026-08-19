"""Bright Data Scraper Studio client.

The API is two calls (see docs/bright_data_docs.md):

    POST /dca/trigger?collector=<c_...>&queue_next=1   body: [{"url": ...}, ...]
        -> {"collection_id": "j_..."}
    GET  /dca/dataset?id=<collection_id>
        -> {"status": "building"}  while running, a JSON array once ready

`collection_id` and `snapshot_id` are the same value under two names.

One trigger accepts many inputs, so a whole run is a single snapshot and a single
poll loop rather than one request per URL.
"""

from __future__ import annotations

import asyncio
import re
import time
from collections.abc import Callable
from typing import Any

import httpx

from .clean import html_to_markdown
from .config import Settings
from .tracing import annotate, traced

# Tried in order when the collector's content field isn't configured explicitly.
# A collector's output schema is defined when it's built, so this cannot be known
# ahead of time; BRIGHT_DATA_CONTENT_FIELD overrides the guess.
CONTENT_FIELD_CANDIDATES = (
    "markdown",
    "content",
    "text",
    "page_content",
    "body",
    "main_content",
    "html",
    "raw_html",
)

TITLE_FIELD_CANDIDATES = ("title", "page_title", "heading", "name")

_HTML_HINT = re.compile(r"<(?:html|body|div|p|h[1-6]|article|main|section)\b", re.IGNORECASE)


class BrightDataError(RuntimeError):
    """A Bright Data API failure, phrased so the CLI can print it verbatim."""


def _explain_status(status: int, body: str, settings: Settings) -> str:
    """Turn an HTTP status into the fix, not just the code."""
    match status:
        case 401:
            return (
                "Bright Data rejected the API token (401). Re-copy it from "
                "https://brightdata.com/cp/setting and update BRIGHT_DATA_API_TOKEN."
            )
        case 404:
            return (
                f"Collector '{settings.brightdata_collector_id}' not found (404). Check the "
                "ID at https://brightdata.com/cp/scrapers — it should start with 'c_'."
            )
        case 422:
            return (
                "Inputs rejected by the collector's schema (422). This client sends "
                '[{"url": ...}]; confirm the Inputs tab of your collector expects a '
                f"'url' field. Response: {body[:300]}"
            )
        case _:
            return f"Bright Data API error {status}: {body[:300]}"


@traced("brightdata.request", run_type="tool", tags=["http", "brightdata"])
async def _request(
    client: httpx.AsyncClient,
    settings: Settings,
    method: str,
    url: str,
    *,
    json: Any = None,
    attempts: int = 4,
) -> httpx.Response:
    """Issue a request, retrying transient 5xx/network errors with exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            response = await client.request(method, url, json=json)
        except httpx.HTTPError as exc:  # connection reset, read timeout, ...
            last_error = exc
            if attempt == attempts - 1:
                raise BrightDataError(f"Could not reach Bright Data: {exc}") from exc
            await asyncio.sleep(2**attempt)
            continue

        if response.status_code < 400:
            annotate(status=response.status_code, attempts_used=attempt + 1)
            return response
        if response.status_code >= 500 and attempt < attempts - 1:
            annotate(**{f"retry_{attempt + 1}_status": response.status_code})
            await asyncio.sleep(2**attempt)  # 1s, 2s, 4s
            continue
        raise BrightDataError(_explain_status(response.status_code, response.text, settings))

    raise BrightDataError(f"Could not reach Bright Data: {last_error}")


def _headers(settings: Settings) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {settings.brightdata_api_token}",
        "Content-Type": "application/json",
    }


@traced("brightdata.trigger", run_type="tool", tags=["brightdata"])
async def trigger(client: httpx.AsyncClient, settings: Settings, urls: list[str]) -> str:
    """Queue every URL in one request and return the snapshot (collection) ID."""
    endpoint = (
        f"{settings.brightdata_base_url.rstrip('/')}/dca/trigger"
        f"?collector={settings.brightdata_collector_id}&queue_next=1"
    )
    response = await _request(
        client, settings, "POST", endpoint, json=[{"url": url} for url in urls]
    )
    payload = response.json()
    snapshot_id = payload.get("collection_id") or payload.get("snapshot_id")
    if not snapshot_id:
        raise BrightDataError(f"Trigger returned no collection_id. Response: {payload!r}")
    return snapshot_id


@traced("brightdata.poll", run_type="tool", tags=["brightdata"])
async def poll(
    client: httpx.AsyncClient,
    settings: Settings,
    snapshot_id: str,
    *,
    on_tick: Callable[[float], None] | None = None,
) -> list[dict]:
    """Poll the dataset endpoint until it serves the finished JSON array."""
    endpoint = f"{settings.brightdata_base_url.rstrip('/')}/dca/dataset?id={snapshot_id}"
    deadline = time.monotonic() + settings.scrape_timeout
    polls = 0

    while True:
        polls += 1
        response = await _request(client, settings, "GET", endpoint)
        try:
            body = response.json()
        except ValueError as exc:
            raise BrightDataError(
                f"Dataset endpoint returned non-JSON for snapshot {snapshot_id}: "
                f"{response.text[:200]}"
            ) from exc

        # A list means the snapshot is finished — including an empty one, which
        # means no rows or an expired snapshot rather than "still working".
        if isinstance(body, list):
            annotate(rows=len(body), waited_s=round(polls * settings.poll_interval, 1))
            return body

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise BrightDataError(
                f"Snapshot {snapshot_id} was still building after "
                f"{settings.scrape_timeout:.0f}s. It may still finish — retrieve it later "
                f"with: GET {settings.brightdata_base_url}/dca/dataset?id={snapshot_id}"
            )
        if on_tick:
            on_tick(remaining)
        await asyncio.sleep(min(settings.poll_interval, remaining))


def normalize_url(url: str) -> str:
    """Canonical form used only to match returned rows against requested URLs."""
    cleaned = url.strip().rstrip("/")
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    return cleaned.removeprefix("www.").lower()


def _row_url(row: dict) -> str | None:
    source = row.get("input")
    if isinstance(source, dict) and source.get("url"):
        return str(source["url"])
    return str(row["url"]) if row.get("url") else None


@traced("brightdata.match_rows", run_type="parser")
def match_rows(urls: list[str], rows: list[dict]) -> dict[str, dict | None]:
    """Map each requested URL to its row, or None when the collector returned none.

    Precedence matters. A crawling collector can return many rows that all echo the
    *same* `input.url`, so keying on the echo alone collapses them and keeps an
    arbitrary one — while the genuinely requested page sits unused further down the
    list. So a row whose own canonical URL matches the request always wins; the
    input echo is only a fallback for collectors that don't report a page URL.

    Matching is on the normalized URL because collectors routinely return a
    redirected or trailing-slash-normalized variant of what was requested.
    """
    by_actual: dict[str, dict] = {}
    by_input: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        actual = row_canonical_url(row)
        if actual:
            by_actual.setdefault(normalize_url(actual), row)
        source = row.get("input")
        if isinstance(source, dict) and source.get("url"):
            by_input.setdefault(normalize_url(str(source["url"])), row)

    matched: dict[str, dict | None] = {}
    for url in urls:
        key = normalize_url(url)
        matched[url] = by_actual.get(key) or by_input.get(key)

    # Exactly one URL requested and one row back, under a different address: a
    # redirect, so claim it. Only ever when a single URL was requested — with more
    # than one in flight, a crawling collector's spare rows would otherwise be
    # handed to whichever library happened to come up short, attributing one
    # project's docs to another.
    if len(urls) == 1 and matched[urls[0]] is None and len(by_actual) == 1:
        matched[urls[0]] = next(iter(by_actual.values()))
    annotate(
        requested=len(urls),
        rows=len(rows),
        unmatched=[url for url, row in matched.items() if row is None],
    )
    return matched


def pick_content_field(row: dict, override: str = "") -> str | None:
    """Return the row key holding page content, or None if nothing usable is present."""
    if override:
        return override if isinstance(row.get(override), str) and row[override].strip() else None
    for candidate in CONTENT_FIELD_CANDIDATES:
        value = row.get(candidate)
        if isinstance(value, str) and value.strip():
            return candidate
    return None


def looks_like_html(text: str) -> bool:
    return bool(_HTML_HINT.search(text))


@traced("row_to_markdown", run_type="parser")
def row_to_markdown(row: dict, override: str = "") -> str:
    """Extract page content as markdown, converting from HTML when necessary.

    HTML goes through `clean.html_to_markdown`, which strips sidebars and other
    chrome before converting. Content that already arrives as markdown is left
    alone — the structure needed to identify navigation is gone by then, and
    guessing from link density would eat legitimate API indexes.
    """
    field = pick_content_field(row, override)
    if field is None:
        annotate(content_field=None, available_fields=sorted(row))
        return ""
    content = row[field].strip()
    was_html = looks_like_html(content)
    if was_html:
        content = html_to_markdown(content)
    annotate(content_field=field, converted_from_html=was_html, markdown_chars=len(content))
    return content


URL_FIELD_CANDIDATES = ("canonical_url", "url", "page_url", "product_page_url", "final_url")


def row_canonical_url(row: dict) -> str:
    """The URL the row's content actually came from.

    Collectors may redirect, or (when the generated scraper includes a discovery
    step) crawl to a different page than the one requested. Citations must point
    at the page the text is really on, so this is recorded separately.
    """
    for candidate in URL_FIELD_CANDIDATES:
        value = row.get(candidate)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def same_page(a: str, b: str) -> bool:
    """True when two URLs address the same page, ignoring scheme/www/trailing slash."""
    return normalize_url(a) == normalize_url(b)


def row_title(row: dict) -> str:
    for candidate in TITLE_FIELD_CANDIDATES:
        value = row.get(candidate)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


@traced("scrape_via_collector", run_type="chain", tags=["brightdata"])
async def scrape_via_collector(
    settings: Settings,
    urls: list[str],
    *,
    on_tick: Callable[[float], None] | None = None,
) -> dict[str, dict | None]:
    """Trigger one Scraper Studio snapshot for every URL and return {url: row or None}."""
    timeout = httpx.Timeout(60.0, connect=15.0)
    async with httpx.AsyncClient(headers=_headers(settings), timeout=timeout) as client:
        snapshot_id = await trigger(client, settings, urls)
        rows = await poll(client, settings, snapshot_id, on_tick=on_tick)
    return match_rows(urls, rows)


@traced("unlock_one_url", run_type="tool", tags=["brightdata"])
async def _unlock_one(
    client: httpx.AsyncClient, settings: Settings, url: str, limiter: asyncio.Semaphore
) -> tuple[str, dict | None]:
    endpoint = f"{settings.brightdata_base_url.rstrip('/')}/request"
    payload = {"zone": settings.brightdata_unlocker_zone, "url": url, "format": "raw"}
    async with limiter:
        response = await _request(client, settings, "POST", endpoint, json=payload)
    # `format: raw` returns the page itself, not JSON. Requesting HTML rather than
    # Web Unlocker's own markdown is deliberate: its converter flattens <pre> blocks
    # onto one line, while row_to_markdown keeps code samples intact.
    annotate(html_chars=len(response.text))
    return url, {"url": url, "html": response.text}


@traced("scrape_via_unlocker", run_type="chain", tags=["brightdata"])
async def scrape_via_unlocker(
    settings: Settings,
    urls: list[str],
    *,
    on_tick: Callable[[float], None] | None = None,
) -> dict[str, dict | None]:
    """Fetch each URL through the Web Unlocker API — page-exact, no collector."""
    timeout = httpx.Timeout(120.0, connect=15.0)
    limiter = asyncio.Semaphore(5)
    async with httpx.AsyncClient(headers=_headers(settings), timeout=timeout) as client:
        outcomes = await asyncio.gather(
            *(_unlock_one(client, settings, url, limiter) for url in urls),
            return_exceptions=True,
        )

    rows: dict[str, dict | None] = {}
    for url, outcome in zip(urls, outcomes):
        # One page failing must not lose the others.
        rows[url] = None if isinstance(outcome, BaseException) else outcome[1]
    annotate(fetched=sum(1 for row in rows.values() if row), requested=len(urls))
    return rows


@traced("scrape_urls", run_type="chain", tags=["brightdata"])
async def scrape_urls(
    settings: Settings,
    urls: list[str],
    *,
    on_tick: Callable[[float], None] | None = None,
) -> dict[str, dict | None]:
    """Fetch every URL through the configured backend. Returns {url: row or None}."""
    if not urls:
        return {}
    if settings.scrape_backend == "collector":
        return await scrape_via_collector(settings, urls, on_tick=on_tick)
    return await scrape_via_unlocker(settings, urls, on_tick=on_tick)
