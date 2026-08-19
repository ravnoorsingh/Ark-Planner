"""Normalization of whatever shape the Tavily MCP tool hands back."""

from __future__ import annotations

import json

from ark.nodes.search_docs import _to_hits

TAVILY_JSON = {
    "query": "fastapi official documentation",
    "results": [
        {
            "title": "FastAPI",
            "url": "https://fastapi.tiangolo.com/",
            "content": "FastAPI framework, high performance",
            "score": 0.97,
        },
        {
            "title": "Tutorial on Medium",
            "url": "https://medium.com/some-post",
            "content": "How I built an API",
            "score": 0.41,
        },
    ],
}


def test_parses_documented_json_string():
    hits = _to_hits(json.dumps(TAVILY_JSON))
    assert [hit.url for hit in hits] == [
        "https://fastapi.tiangolo.com/",
        "https://medium.com/some-post",
    ]
    assert hits[0].title == "FastAPI"
    assert hits[0].score == 0.97


def test_parses_already_parsed_dict():
    assert len(_to_hits(TAVILY_JSON)) == 2


def test_parses_content_block_list():
    blocks = [{"type": "text", "text": json.dumps(TAVILY_JSON)}]
    assert _to_hits(blocks)[0].url == "https://fastapi.tiangolo.com/"


def test_parses_content_and_artifact_tuple():
    assert _to_hits((json.dumps(TAVILY_JSON), None))[0].url == "https://fastapi.tiangolo.com/"


def test_parses_bare_result_list():
    assert len(_to_hits(TAVILY_JSON["results"])) == 2


def test_falls_back_to_url_regex_on_unstructured_text():
    text = "Top result: https://docs.tavily.com/welcome, then https://github.com/tavily-ai."
    hits = _to_hits(text)
    assert [hit.url for hit in hits] == [
        "https://docs.tavily.com/welcome",
        "https://github.com/tavily-ai",
    ]


def test_tolerates_missing_score_and_title():
    hits = _to_hits({"results": [{"url": "https://example.com"}]})
    assert hits[0].score is None
    assert hits[0].title == ""


def test_skips_entries_without_a_url():
    hits = _to_hits({"results": [{"title": "no url here"}, {"url": "https://ok.dev"}]})
    assert [hit.url for hit in hits] == ["https://ok.dev"]


def test_respects_limit():
    results = [{"url": f"https://example.com/{i}"} for i in range(10)]
    assert len(_to_hits({"results": results}, limit=3)) == 3


def test_empty_response_yields_no_hits():
    assert _to_hits({"results": []}) == []
    assert _to_hits("") == []
