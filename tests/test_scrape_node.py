"""The scrape node: URL planning (what gets billed) and failure degradation."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from ark.brightdata import BrightDataError
from ark.config import Settings
from ark.nodes.scrape_docs import planned_urls, scrape_to_store
from ark.state import DocSource
from ark.store import load_manifest

# `ark.nodes` re-exports the node function under its module's name, so the dotted
# string "ark.nodes.scrape_docs" resolves to the function. Patch the module object.
SCRAPE_MODULE = sys.modules["ark.nodes.scrape_docs"]

FASTAPI = DocSource(
    library="fastapi",
    url="https://fastapi.tiangolo.com",
    alternates=["https://github.com/fastapi/fastapi", "https://pypi.org/project/fastapi"],
)
LANGGRAPH = DocSource(
    library="langgraph",
    url="https://docs.langchain.com/langgraph",
    alternates=["https://reference.langchain.com/langgraph"],
)


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.chdir(tmp_path)
    for name in ("GROQ_API_KEY", "TAVILY_API_KEY", "BRIGHT_DATA_API_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    return Settings(
        brightdata_api_token="tok",
        brightdata_collector_id="c_test",
        data_dir=tmp_path / "data",
    )


# --- planning ----------------------------------------------------------------------


def test_primary_first_then_ranked_alternates():
    plan = planned_urls([FASTAPI], max_alternates=2)
    assert plan == [
        ("fastapi", "https://fastapi.tiangolo.com", "primary", 0),
        ("fastapi", "https://github.com/fastapi/fastapi", "alternate", 1),
        ("fastapi", "https://pypi.org/project/fastapi", "alternate", 2),
    ]


def test_max_alternates_zero_scrapes_primaries_only():
    plan = planned_urls([FASTAPI, LANGGRAPH], max_alternates=0)
    assert len(plan) == 2
    assert all(role == "primary" for _, _, role, _ in plan)


def test_max_alternates_trims_the_tail():
    assert len(planned_urls([FASTAPI], max_alternates=1)) == 2


def test_duplicate_urls_are_billed_once():
    """The same URL can be one library's primary and another's alternate."""
    shared = "https://docs.langchain.com/langgraph"
    other = DocSource(library="langchain", url="https://a.dev", alternates=[shared])
    plan = planned_urls([LANGGRAPH, other], max_alternates=2)

    urls = [url for _, url, _, _ in plan]
    assert urls.count(shared) == 1


def test_empty_urls_are_skipped():
    plan = planned_urls([DocSource(library="x", url="", alternates=["", "https://ok.dev"])], 2)
    assert [url for _, url, _, _ in plan] == ["https://ok.dev"]


def test_no_sources_plans_nothing():
    assert planned_urls([], max_alternates=2) == []


# --- scraping ----------------------------------------------------------------------


async def test_writes_store_and_manifest(settings, monkeypatch):
    async def fake_scrape(_settings, urls, **_kwargs):
        return {url: {"markdown": f"# docs for {url}", "title": "T"} for url in urls}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=1)

    assert errors == []
    assert [doc.status for doc in documents] == ["ok", "ok"]
    assert (settings.data_dir / "manifest.json").exists()
    assert "# docs for" in Path(documents[0].path).read_text(encoding="utf-8")


async def test_missing_row_degrades_to_failed_without_losing_the_rest(settings, monkeypatch):
    async def fake_scrape(_settings, urls, **_kwargs):
        return {urls[0]: {"markdown": "# ok"}, urls[1]: None}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=1)

    assert [doc.status for doc in documents] == ["ok", "failed"]
    assert len(errors) == 1 and "no row returned" in errors[0]


async def test_row_without_a_content_field_is_flagged_with_the_fix(settings, monkeypatch):
    async def fake_scrape(_settings, urls, **_kwargs):
        return {url: {"url": url, "status_code": 200} for url in urls}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=0)

    assert documents[0].status == "empty"
    assert "BRIGHT_DATA_CONTENT_FIELD" in errors[0]


async def test_snapshot_failure_records_every_url_as_failed(settings, monkeypatch):
    async def fake_scrape(_settings, _urls, **_kwargs):
        raise BrightDataError("401 bad token")

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI, LANGGRAPH], max_alternates=1)

    # The manifest should reflect what was attempted, not go silent.
    assert len(documents) == 4
    assert all(doc.status == "failed" for doc in documents)
    assert "401 bad token" in errors[0]


async def test_rescrape_does_not_duplicate_manifest_entries(settings, monkeypatch):
    async def fake_scrape(_settings, urls, **_kwargs):
        return {url: {"markdown": "# v"} for url in urls}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    await scrape_to_store(settings, [FASTAPI], max_alternates=1)
    await scrape_to_store(settings, [FASTAPI], max_alternates=1)

    assert len(load_manifest(settings.data_dir).documents) == 2


async def test_no_sources_is_a_no_op(settings):
    assert await scrape_to_store(settings, []) == ([], [])


async def test_settings_default_applies_when_max_alternates_is_none(settings, monkeypatch):
    captured: list[list[str]] = []

    async def fake_scrape(_settings, urls, **_kwargs):
        captured.append(urls)
        return {url: {"markdown": "# v"} for url in urls}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    await scrape_to_store(settings, [FASTAPI], max_alternates=None)

    assert len(captured[0]) == 1 + settings.max_alternates


# --- citation integrity ------------------------------------------------------------


async def test_drifted_page_is_flagged_and_records_where_text_really_came_from(
    settings, monkeypatch
):
    """The generated collector may crawl to a sub-page instead of the URL requested."""

    async def fake_scrape(_settings, urls, **_kwargs):
        return {
            urls[0]: {
                "canonical_url": "https://fastapi.tiangolo.com/tutorial/path-params/",
                "main_content": "<h1>Path Parameters</h1>",
            }
        }

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=0)

    doc = documents[0]
    assert doc.url == "https://fastapi.tiangolo.com"
    assert doc.resolved_url == "https://fastapi.tiangolo.com/tutorial/path-params/"
    assert any("but the collector returned" in error for error in errors)

    text = Path(doc.path).read_text(encoding="utf-8")
    assert "resolved_url:" in text  # a citation must not silently point at the wrong page


async def test_same_page_is_not_treated_as_drift(settings, monkeypatch):
    """A trailing slash or scheme difference is the same page, not a redirect."""

    async def fake_scrape(_settings, urls, **_kwargs):
        return {urls[0]: {"canonical_url": "https://fastapi.tiangolo.com/", "markdown": "# ok"}}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=0)

    assert documents[0].resolved_url == ""
    assert errors == []
    assert "resolved_url:" not in Path(documents[0].path).read_text(encoding="utf-8")


async def test_row_without_any_url_field_is_not_flagged_as_drift(settings, monkeypatch):
    async def fake_scrape(_settings, urls, **_kwargs):
        return {urls[0]: {"markdown": "# ok"}}

    monkeypatch.setattr(SCRAPE_MODULE, "scrape_urls", fake_scrape)
    documents, errors = await scrape_to_store(settings, [FASTAPI], max_alternates=0)

    assert documents[0].resolved_url == ""
    assert errors == []
