"""Deterministic guards applied on top of the model's curation judgment."""

from __future__ import annotations

import pytest

from ark.nodes.curate_links import _enforce_doc_domain, _host, _is_non_doc
from ark.state import DocSource, SearchHit


def _source(url: str, **kwargs) -> DocSource:
    defaults = {
        "library": "chromadb",
        "url": url,
        "title": "t",
        "kind": "official_docs",
        "confidence": 0.9,
        "rationale": "because",
    }
    return DocSource(**{**defaults, **kwargs})


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.youtube.com/watch?v=abc", True),
        ("https://youtu.be/abc", True),
        ("https://medium.com/@someone/post", True),
        ("https://blog.medium.com/post", True),
        ("https://stackoverflow.com/questions/1", True),
        ("https://docs.trychroma.com/", False),
        ("https://fastapi.tiangolo.com/", False),
        ("https://github.com/chroma-core/chroma", False),
        # Must not match on a substring of a longer, unrelated hostname.
        ("https://notyoutube.com/docs", False),
        ("https://mycompany-medium.com/docs", False),
    ],
)
def test_non_doc_domain_detection(url, expected):
    assert _is_non_doc(url) is expected


def test_host_strips_www():
    assert _host("https://www.example.com/a") == "example.com"


def test_clean_url_passes_through_untouched():
    source = _source("https://docs.trychroma.com/")
    assert _enforce_doc_domain(source, []) == source


def test_substitutes_best_remaining_candidate():
    hits = [
        SearchHit(url="https://www.youtube.com/watch?v=abc", title="video"),
        SearchHit(url="https://docs.trychroma.com/", title="Chroma Docs"),
    ]
    result = _enforce_doc_domain(_source("https://www.youtube.com/watch?v=abc"), hits)

    assert result.url == "https://docs.trychroma.com/"
    assert result.title == "Chroma Docs"
    assert "https://www.youtube.com/watch?v=abc" in result.alternates
    assert result.confidence <= 0.5


def test_demotes_when_every_candidate_is_non_doc():
    hits = [SearchHit(url="https://www.youtube.com/watch?v=abc")]
    result = _enforce_doc_domain(_source("https://www.youtube.com/watch?v=abc"), hits)

    # A YouTube URL must never survive as `official_docs` — the scrape phase
    # consumes these URLs.
    assert result.kind == "other"
    assert result.confidence <= 0.2
    assert result.url == "https://www.youtube.com/watch?v=abc"


# --- alternate quality ---------------------------------------------------------------

from ark.nodes.curate_links import filter_alternates, useful_alternate

TYPER = "https://typer.tiangolo.com"


@pytest.mark.parametrize(
    ("url", "keep"),
    [
        # Real alternates seen in a live run for `typer` — only the last is useful.
        ("https://github.com/fastapi/typer/issues/221", False),
        ("https://opensciencelabs.org/blog/typer-a-python-library-for-cli", False),
        ("https://github.com/fastapi/typer", True),
        # Sub-pages of a repo are not documentation.
        ("https://github.com/fastapi/typer/pull/12", False),
        ("https://github.com/fastapi/typer/discussions/7", False),
        ("https://github.com/fastapi/typer/commits/master", False),
        # Blocklisted hosts stay blocked for alternates too.
        ("https://medium.com/@x/typer-guide", False),
        ("https://stackoverflow.com/questions/1/typer", False),
        ("https://blog.example.com/typer-intro", False),
        # First-party docs sub-pages remain fine.
        ("https://typer.tiangolo.com/tutorial/options/", True),
    ],
)
def test_alternate_usefulness(url, keep):
    assert useful_alternate(url, "typer", TYPER) is keep


def test_a_repo_root_is_a_legitimate_fallback():
    """GitHub renders the README there, which is real documentation."""
    assert useful_alternate("https://github.com/textualize/rich", "rich", "https://x.dev") is True


def test_an_unrelated_project_is_dropped():
    """Search drifts to same-named projects for one-word package names."""
    assert useful_alternate("https://github.com/someone/unrelated-tool", "typer", TYPER) is False


def test_the_primary_is_not_repeated_as_its_own_alternate():
    assert useful_alternate(TYPER, "typer", TYPER) is False


def test_filter_keeps_order_and_drops_duplicates():
    source = DocSource(
        library="typer",
        url=TYPER,
        alternates=[
            "https://github.com/fastapi/typer/issues/221",
            "https://github.com/fastapi/typer",
            "https://github.com/fastapi/typer",
            "https://opensciencelabs.org/blog/typer-a-python-library",
        ],
    )
    assert filter_alternates(source) == ["https://github.com/fastapi/typer"]


def test_filtering_can_legitimately_leave_none():
    """Better to scrape nothing than to bill for a page that misleads the plan."""
    source = DocSource(
        library="typer", url=TYPER,
        alternates=["https://github.com/fastapi/typer/issues/1", "https://medium.com/x"],
    )
    assert filter_alternates(source) == []


def test_only_same_site_or_repo_root_alternates_survive():
    """Real case: searching "httpx" surfaced projectdiscovery/httpx, a Go security
    scanner. A page from a same-named different project is worse than no alternate,
    because it gets scraped and then cited in the plan."""
    primary = "https://www.python-httpx.org"
    assert useful_alternate("https://www.python-httpx.org/async/", "httpx", primary) is True
    assert useful_alternate("https://docs.projectdiscovery.io/httpx", "httpx", primary) is False
    assert useful_alternate("https://base.bangwu.me/Python/libs/httpx", "httpx", primary) is False


def test_support_forums_are_dropped():
    assert (
        useful_alternate(
            "https://community.openai.com/c/documentation/14",
            "openai",
            "https://developers.openai.com/api/docs",
        )
        is False
    )


def test_other_pages_of_the_same_docs_site_are_kept():
    primary = "https://developers.openai.com/api/docs"
    assert useful_alternate(f"{primary}/quickstart", "openai", primary) is True


@pytest.mark.parametrize(
    ("url", "keep"),
    [
        ("https://github.com/textualize/rich", True),          # repo root
        ("https://github.com/textualize/rich/tree/main/docs", False),  # deeper
        ("https://github.com/textualize", False),              # org page
    ],
)
def test_repo_root_only(url, keep):
    assert useful_alternate(url, "rich", "https://rich.readthedocs.io") is keep
