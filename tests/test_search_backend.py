"""Provider differences between the Firecrawl and Tavily search backends."""

from __future__ import annotations

import json

import pytest

from ark.config import Settings
from ark.mcp_client import _connection, search_arguments, search_tool_name
from ark.nodes.search_docs import _to_hits


@pytest.fixture(autouse=True)
def _isolate(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for name in ("FIRECRAWL_API_KEY", "TAVILY_API_KEY", "ARK_SEARCH_BACKEND"):
        monkeypatch.delenv(name, raising=False)


def _settings(backend: str) -> Settings:
    return Settings(
        search_backend=backend,
        firecrawl_api_key="fc-key",
        tavily_api_key="tvly-key",
        search_max_results=5,
    )


# --- tool names and arguments --------------------------------------------------------


def test_firecrawl_is_the_default_backend():
    assert Settings().search_backend == "firecrawl"


def test_tool_names_per_backend():
    assert search_tool_name(_settings("firecrawl")) == "firecrawl_search"
    assert search_tool_name(_settings("tavily")) == "tavily_search"


def test_firecrawl_uses_limit_not_max_results():
    """Sending the wrong parameter name is silently ignored by the server and only
    shows up much later as "only one result came back"."""
    args = search_arguments(_settings("firecrawl"), "fastapi docs")
    assert args == {"query": "fastapi docs", "limit": 5}
    assert "max_results" not in args


def test_tavily_keeps_its_own_parameters():
    args = search_arguments(_settings("tavily"), "fastapi docs")
    assert args["max_results"] == 5
    assert args["search_depth"] == "advanced"


# --- authentication ------------------------------------------------------------------


def test_firecrawl_authenticates_with_a_bearer_header():
    """Firecrawl's docs are explicit that the key must not be in the MCP URL."""
    conn = _connection(_settings("firecrawl"))
    assert conn["headers"]["Authorization"] == "Bearer fc-key"
    assert "fc-key" not in conn["url"]


def test_tavily_authenticates_in_the_query_string():
    conn = _connection(_settings("tavily"))
    assert "tavilyApiKey=tvly-key" in conn["url"]
    assert "headers" not in conn


def test_both_use_streamable_http():
    for backend in ("firecrawl", "tavily"):
        assert _connection(_settings(backend))["transport"] == "streamable_http"


# --- response normalization ----------------------------------------------------------

TAVILY_RESPONSE = {
    "results": [
        {"url": "https://fastapi.tiangolo.com", "title": "FastAPI",
         "content": "FastAPI framework", "score": 0.97}
    ]
}

FIRECRAWL_RESPONSE = {
    "web": [
        {"url": "https://fastapi.tiangolo.com", "title": "FastAPI",
         "description": "FastAPI framework"}
    ]
}

FIRECRAWL_NESTED = {"data": {"web": FIRECRAWL_RESPONSE["web"]}}


@pytest.mark.parametrize(
    "payload", [TAVILY_RESPONSE, FIRECRAWL_RESPONSE, FIRECRAWL_NESTED]
)
def test_both_response_shapes_normalize(payload):
    hits = _to_hits(json.dumps(payload))
    assert len(hits) == 1
    assert hits[0].url == "https://fastapi.tiangolo.com"
    assert hits[0].title == "FastAPI"
    assert "FastAPI framework" in hits[0].snippet


def test_firecrawl_has_no_relevance_score():
    """Tavily ranks with a score; Firecrawl does not, and a missing one must not
    be invented or treated as an error."""
    assert _to_hits(json.dumps(FIRECRAWL_RESPONSE))[0].score is None
    assert _to_hits(json.dumps(TAVILY_RESPONSE))[0].score == 0.97
