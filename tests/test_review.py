"""The pre-scrape review: the last point before anything is billed."""

from __future__ import annotations

import sys

import pytest

import ark.nodes  # noqa: F401
from ark.config import Settings
from ark.review import apply_command, to_rows, to_sources
from ark.state import DocSource

SCRAPE = sys.modules["ark.nodes.scrape_docs"]

SOURCES = [
    DocSource(
        library="fastapi",
        url="https://fastapi.tiangolo.com",
        alternates=["https://github.com/fastapi/fastapi", "https://pypi.org/project/fastapi"],
        confidence=0.99,
        kind="official_docs",
    ),
    DocSource(library="pydantic", url="https://pydantic.dev/docs", confidence=0.98),
]


# --- what the user is shown ------------------------------------------------------


def test_the_list_shows_exactly_what_would_be_scraped():
    """Showing links that the cap would drop would misrepresent the cost."""
    assert len(to_rows(SOURCES, max_alternates=1)) == 3   # fastapi + 1 alt, pydantic
    assert len(to_rows(SOURCES, max_alternates=2)) == 4


def test_user_supplied_urls_are_all_shown():
    source = DocSource(
        library="x", url="https://a.dev/1",
        alternates=["https://a.dev/2", "https://a.dev/3"], user_supplied=True,
    )
    assert len(to_rows([source], max_alternates=0)) == 3


# --- editing ---------------------------------------------------------------------


def test_drop_removes_a_row():
    rows = to_rows(SOURCES, 2)
    out, message = apply_command(rows, "d 2")
    assert len(out) == len(rows) - 1
    assert "Dropped" in message


def test_edit_replaces_a_url():
    rows = to_rows(SOURCES, 2)
    out, message = apply_command(rows, "e 1 https://mine.dev")
    assert out[0].url == "https://mine.dev"
    assert out[0].library == "fastapi"  # library is not changed by an edit
    assert "Replaced" in message


def test_add_places_the_url_with_its_library():
    rows = to_rows(SOURCES, 2)
    out, _ = apply_command(rows, "a fastapi https://fastapi.tiangolo.com/advanced/")
    libraries = [row.library for row in out]
    assert libraries == sorted(libraries, key=lambda n: libraries.index(n))  # kept grouped
    assert out[3].url == "https://fastapi.tiangolo.com/advanced/"


def test_add_can_introduce_a_new_library():
    out, _ = apply_command(to_rows(SOURCES, 0), "a httpx https://www.python-httpx.org")
    assert out[-1].library == "httpx"
    assert out[-1].primary is True


@pytest.mark.parametrize("bad", ["d 99", "e 99 https://x.dev", "nonsense", "d"])
def test_bad_commands_explain_themselves_and_change_nothing(bad):
    rows = to_rows(SOURCES, 2)
    out, message = apply_command(rows, bad)
    assert out == rows
    assert message == "" or "No row" in message or "Unknown command" in message


# --- rebuilding ------------------------------------------------------------------


def test_edits_survive_the_round_trip():
    rows = to_rows(SOURCES, 2)
    rows, _ = apply_command(rows, "e 1 https://mine.dev")
    rows, _ = apply_command(rows, "d 2")
    rebuilt = {source.library: source for source in to_sources(rows, SOURCES)}

    assert rebuilt["fastapi"].url == "https://mine.dev"
    assert "https://github.com/fastapi/fastapi" not in rebuilt["fastapi"].alternates
    assert rebuilt["pydantic"].url == "https://pydantic.dev/docs"


def test_an_edited_library_is_marked_user_supplied():
    """Otherwise the alternates cap could trim a link the user just chose to keep."""
    rows, _ = apply_command(to_rows(SOURCES, 2), "e 2 https://mine.dev/alt")
    rebuilt = {s.library: s for s in to_sources(rows, SOURCES)}
    assert rebuilt["fastapi"].user_supplied is True
    assert rebuilt["pydantic"].user_supplied is False  # untouched


def test_deleting_every_row_of_a_library_removes_it():
    rows = [row for row in to_rows(SOURCES, 2) if row.library != "pydantic"]
    assert "pydantic" not in {source.library for source in to_sources(rows, SOURCES)}


def test_untouched_sources_keep_their_curation_metadata():
    rebuilt = {s.library: s for s in to_sources(to_rows(SOURCES, 2), SOURCES)}
    assert rebuilt["fastapi"].confidence == 0.99
    assert rebuilt["fastapi"].kind == "official_docs"


def test_a_library_added_at_review_is_first_class():
    rows, _ = apply_command(to_rows(SOURCES, 0), "a httpx https://www.python-httpx.org")
    added = {s.library: s for s in to_sources(rows, SOURCES)}["httpx"]
    assert added.confidence == 1.0
    assert added.user_supplied is True


# --- the node hook ---------------------------------------------------------------


async def test_review_output_is_what_gets_scraped(monkeypatch):
    scraped = {}

    async def fake_store(settings, sources, **kwargs):
        scraped["libraries"] = [s.library for s in sources]
        return [], []

    monkeypatch.setattr(SCRAPE, "scrape_to_store", fake_store)

    def review(sources):
        return [s for s in sources if s.library != "pydantic"]

    out = await SCRAPE.scrape_docs(
        {"doc_sources": SOURCES, "requirement": "r"},
        {"configurable": {"settings": Settings(), "review_urls": review, "max_alternates": 0}},
    )
    assert scraped["libraries"] == ["fastapi"]
    # the artifact must record what was scraped, not what curation proposed
    assert [s.library for s in out["doc_sources"]] == ["fastapi"]


async def test_cancelling_scrapes_nothing(monkeypatch):
    async def explode(*a, **k):
        raise AssertionError("nothing should be scraped after a cancel")

    monkeypatch.setattr(SCRAPE, "scrape_to_store", explode)
    out = await SCRAPE.scrape_docs(
        {"doc_sources": SOURCES, "requirement": "r"},
        {"configurable": {"settings": Settings(), "review_urls": lambda s: None,
                          "max_alternates": 0}},
    )
    assert out["documents"] == []
    assert "cancelled" in out["errors"][0].lower()


async def test_no_callback_means_no_change_in_behaviour(monkeypatch):
    async def fake_store(settings, sources, **kwargs):
        return [], []

    monkeypatch.setattr(SCRAPE, "scrape_to_store", fake_store)
    out = await SCRAPE.scrape_docs(
        {"doc_sources": SOURCES, "requirement": "r"},
        {"configurable": {"settings": Settings(), "max_alternates": 0}},
    )
    assert out["documents"] == []


def test_the_cli_override_decides_what_the_list_shows():
    """A --max-alternates override must reach the review, or the list promises
    more URLs than the scrape will actually fetch."""
    from ark.cli import _review_urls

    captured = {}

    def fake_input(*a, **k):
        return ""

    import ark.cli as cli

    cli.console.input = fake_input
    cli.console.print = lambda *a, **k: captured.setdefault("printed", []).append(a)

    review = _review_urls(0)          # cap of zero: primaries only
    out = review(SOURCES)
    assert [s.url for s in out] == [SOURCES[0].url, SOURCES[1].url]
    assert all(not s.alternates for s in out)
