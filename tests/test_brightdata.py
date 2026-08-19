"""Bright Data client: content-field detection, row matching, poll loop, errors.

Fully mocked — no network, no credentials.
"""

from __future__ import annotations

import json

import httpx
import pytest

from ark.brightdata import (
    BrightDataError,
    looks_like_html,
    match_rows,
    normalize_url,
    pick_content_field,
    poll,
    row_canonical_url,
    row_title,
    row_to_markdown,
    same_page,
    trigger,
)
from ark.config import Settings


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    # Isolate from the developer's real .env — otherwise a failing assertion
    # prints live API keys into the test output.
    monkeypatch.chdir(tmp_path)
    for name in ("GROQ_API_KEY", "TAVILY_API_KEY", "BRIGHT_DATA_API_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    return Settings(
        brightdata_api_token="tok",
        brightdata_collector_id="c_test",
        poll_interval=0.01,
        scrape_timeout=1.0,
    )


@pytest.fixture(autouse=True)
def _no_real_sleeping(monkeypatch):
    async def instant(_seconds):
        return None

    monkeypatch.setattr("ark.brightdata.asyncio.sleep", instant)


def _client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


# --- content field detection -------------------------------------------------------


def test_detection_prefers_markdown_over_html():
    row = {"html": "<p>hi</p>", "markdown": "# hi", "text": "hi"}
    assert pick_content_field(row) == "markdown"


def test_detection_falls_through_candidate_order():
    assert pick_content_field({"body": "text here"}) == "body"
    assert pick_content_field({"raw_html": "<p>x</p>"}) == "raw_html"


def test_detection_skips_empty_and_non_string_values():
    assert pick_content_field({"markdown": "   ", "content": "real"}) == "content"
    assert pick_content_field({"markdown": {"nested": 1}, "text": "real"}) == "text"


def test_detection_returns_none_when_nothing_usable():
    assert pick_content_field({"url": "https://x.dev", "status": 200}) is None


def test_override_wins_over_candidates():
    row = {"markdown": "# auto", "my_field": "custom"}
    assert pick_content_field(row, "my_field") == "my_field"


def test_override_that_is_missing_returns_none_rather_than_guessing():
    """A wrong override must surface, not silently fall back to another field."""
    assert pick_content_field({"markdown": "# auto"}, "nope") is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("<html><body><p>hi</p></body></html>", True),
        ("<div class='x'>hi</div>", True),
        ("<h1>Title</h1>", True),
        ("# Markdown heading\n\nSome text", False),
        ("plain text with a < sign", False),
    ],
)
def test_html_detection(text, expected):
    assert looks_like_html(text) is expected


def test_html_content_is_converted_to_markdown():
    row = {"html": "<h1>FastAPI</h1><p>A <b>fast</b> framework</p>"}
    result = row_to_markdown(row)
    assert "# FastAPI" in result
    assert "<h1>" not in result
    assert "**fast**" in result


def test_markdown_content_passes_through_unconverted():
    assert row_to_markdown({"markdown": "# FastAPI\n\nAlready markdown"}).startswith("# FastAPI")


def test_missing_content_yields_empty_string():
    assert row_to_markdown({"url": "https://x.dev"}) == ""


def test_row_title_candidates():
    assert row_title({"title": "FastAPI"}) == "FastAPI"
    assert row_title({"page_title": "Docs"}) == "Docs"
    assert row_title({"url": "https://x.dev"}) == ""


# --- row matching ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("https://x.dev", "https://x.dev/"),
        ("https://X.dev/", "https://x.dev"),
        ("https://www.x.dev", "https://x.dev"),
        ("http://x.dev", "https://x.dev"),
    ],
)
def test_normalize_url_treats_variants_as_equal(a, b):
    assert normalize_url(a) == normalize_url(b)


def test_normalize_url_keeps_distinct_paths_distinct():
    assert normalize_url("https://x.dev/a") != normalize_url("https://x.dev/b")


def test_match_uses_input_url_not_final_url():
    """Collectors echo the requested URL under `input`; a redirect changes `url`."""
    rows = [{"url": "https://x.dev/en/latest", "input": {"url": "https://x.dev"}}]
    assert match_rows(["https://x.dev"], rows)["https://x.dev"] == rows[0]


def test_match_tolerates_trailing_slash_difference():
    rows = [{"input": {"url": "https://x.dev/"}}]
    assert match_rows(["https://x.dev"], rows)["https://x.dev"] is not None


def test_unmatched_url_maps_to_none():
    matched = match_rows(["https://a.dev", "https://b.dev"], [{"url": "https://a.dev"}])
    assert matched["https://a.dev"] is not None
    assert matched["https://b.dev"] is None


def test_single_redirected_row_is_claimed_by_the_single_pending_url():
    """One request, one row, hostnames differ — a redirect, not a mismatch."""
    rows = [{"url": "https://docs.x.dev/latest/"}]
    assert match_rows(["https://x.dev"], rows)["https://x.dev"] == rows[0]


def test_redirect_fallback_does_not_fire_with_multiple_pending():
    """With ambiguity, guessing would attach the wrong page to a library."""
    rows = [{"url": "https://other.dev"}]
    matched = match_rows(["https://a.dev", "https://b.dev"], rows)
    assert matched == {"https://a.dev": None, "https://b.dev": None}


def test_match_ignores_malformed_rows():
    matched = match_rows(["https://a.dev"], ["not a dict", {"no_url": 1}, {"url": "https://a.dev"}])
    assert matched["https://a.dev"] is not None


# --- trigger -----------------------------------------------------------------------


async def test_trigger_sends_url_array_and_returns_collection_id(settings):
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["body"] = request.read().decode()
        return httpx.Response(200, json={"collection_id": "j_123"})

    async with _client(handler) as client:
        assert await trigger(client, settings, ["https://a.dev", "https://b.dev"]) == "j_123"

    assert "collector=c_test" in seen["url"]
    assert "queue_next=1" in seen["url"]
    # One request carries every URL — the whole point of the batch trigger.
    assert json.loads(seen["body"]) == [{"url": "https://a.dev"}, {"url": "https://b.dev"}]


async def test_trigger_accepts_snapshot_id_alias(settings):
    async with _client(lambda r: httpx.Response(200, json={"snapshot_id": "j_9"})) as client:
        assert await trigger(client, settings, ["https://a.dev"]) == "j_9"


async def test_trigger_without_an_id_is_an_error(settings):
    async with _client(lambda r: httpx.Response(200, json={"ok": True})) as client:
        with pytest.raises(BrightDataError, match="no collection_id"):
            await trigger(client, settings, ["https://a.dev"])


# --- error mapping -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (401, "token"),
        (404, "c_test"),
        (422, "url"),
    ],
)
async def test_client_errors_explain_the_fix(settings, status, expected):
    async with _client(lambda r: httpx.Response(status, text="nope")) as client:
        with pytest.raises(BrightDataError, match=expected):
            await trigger(client, settings, ["https://a.dev"])


async def test_5xx_is_retried_then_succeeds(settings):
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503, text="unavailable")
        return httpx.Response(200, json={"collection_id": "j_ok"})

    async with _client(handler) as client:
        assert await trigger(client, settings, ["https://a.dev"]) == "j_ok"
    assert calls["n"] == 3


async def test_5xx_gives_up_after_the_attempt_budget(settings):
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(500, text="boom")

    async with _client(handler) as client:
        with pytest.raises(BrightDataError, match="500"):
            await trigger(client, settings, ["https://a.dev"])
    assert calls["n"] == 4


async def test_4xx_is_not_retried(settings):
    """Retrying a bad token just wastes time — it will never start working."""
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(401, text="bad token")

    async with _client(handler) as client:
        with pytest.raises(BrightDataError):
            await trigger(client, settings, ["https://a.dev"])
    assert calls["n"] == 1


async def test_network_failure_is_wrapped(settings):
    def handler(request):
        raise httpx.ConnectError("no route to host")

    async with _client(handler) as client:
        with pytest.raises(BrightDataError, match="Could not reach Bright Data"):
            await trigger(client, settings, ["https://a.dev"])


# --- polling -----------------------------------------------------------------------


async def test_poll_waits_through_building_then_returns_rows(settings):
    responses = [
        httpx.Response(200, json={"status": "building"}),
        httpx.Response(200, json={"status": "building"}),
        httpx.Response(200, json=[{"url": "https://a.dev"}]),
    ]

    async with _client(lambda r: responses.pop(0)) as client:
        rows = await poll(client, settings, "j_1")
    assert rows == [{"url": "https://a.dev"}]


async def test_poll_treats_empty_array_as_finished(settings):
    """An empty array means no rows or an expired snapshot, not 'still working'."""
    async with _client(lambda r: httpx.Response(200, json=[])) as client:
        assert await poll(client, settings, "j_1") == []


async def test_poll_timeout_names_the_snapshot_for_manual_recovery(settings):
    settings.scrape_timeout = 0.05
    async with _client(lambda r: httpx.Response(200, json={"status": "building"})) as client:
        with pytest.raises(BrightDataError, match="j_slow"):
            await poll(client, settings, "j_slow")


async def test_poll_reports_progress_via_callback(settings):
    responses = [
        httpx.Response(200, json={"status": "building"}),
        httpx.Response(200, json=[{"url": "https://a.dev"}]),
    ]
    ticks: list[float] = []

    async with _client(lambda r: responses.pop(0)) as client:
        await poll(client, settings, "j_1", on_tick=ticks.append)
    assert len(ticks) == 1


async def test_poll_rejects_non_json_body(settings):
    async with _client(lambda r: httpx.Response(200, text="<html>gateway</html>")) as client:
        with pytest.raises(BrightDataError, match="non-JSON"):
            await poll(client, settings, "j_1")


# --- resolved URL ------------------------------------------------------------------


def test_canonical_url_prefers_canonical_over_url():
    row = {"url": "https://x.dev/redirected", "canonical_url": "https://x.dev/real"}
    assert row_canonical_url(row) == "https://x.dev/real"


def test_canonical_url_falls_through_candidates():
    assert row_canonical_url({"product_page_url": "https://x.dev/p"}) == "https://x.dev/p"
    assert row_canonical_url({"final_url": "https://x.dev/f"}) == "https://x.dev/f"


def test_canonical_url_absent_returns_empty():
    assert row_canonical_url({"markdown": "# hi"}) == ""


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("https://x.dev", "https://x.dev/", True),
        ("http://www.x.dev/", "https://x.dev", True),
        ("https://x.dev", "https://x.dev/tutorial/path-params/", False),
        ("https://x.dev/a", "https://y.dev/a", False),
    ],
)
def test_same_page(a, b, expected):
    assert same_page(a, b) is expected


# --- crawling collectors -----------------------------------------------------------


def test_correct_page_wins_over_input_echo_when_many_rows_share_it():
    """A crawling collector returns many rows all echoing the same input.url.

    Keying on the echo alone would keep an arbitrary row while the genuinely
    requested page sat unused further down the list.
    """
    requested = "https://fastapi.tiangolo.com/tutorial/query-params/"
    rows = [
        {"canonical_url": "https://fastapi.tiangolo.com/reference/request/",
         "input": {"url": requested}, "main_content": "wrong"},
        {"canonical_url": "https://fastapi.tiangolo.com/alternatives/",
         "input": {"url": requested}, "main_content": "also wrong"},
        {"canonical_url": requested, "input": {"url": requested}, "main_content": "right"},
    ]
    assert match_rows([requested], rows)[requested]["main_content"] == "right"


def test_input_echo_still_used_when_no_row_reports_its_own_url():
    rows = [{"input": {"url": "https://x.dev"}, "markdown": "# hi"}]
    assert match_rows(["https://x.dev"], rows)["https://x.dev"]["markdown"] == "# hi"


def test_crawl_results_do_not_leak_across_requested_urls():
    """Row for one library's page must never be handed to another library."""
    rows = [
        {"canonical_url": "https://a.dev/one", "input": {"url": "https://a.dev"}},
        {"canonical_url": "https://a.dev/two", "input": {"url": "https://a.dev"}},
    ]
    matched = match_rows(["https://a.dev", "https://b.dev"], rows)
    assert matched["https://b.dev"] is None
