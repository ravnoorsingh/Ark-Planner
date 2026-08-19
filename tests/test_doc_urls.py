"""User-supplied documentation URLs: pinning, multiple links, and extra entries."""

from __future__ import annotations

import sys

import pytest

import ark.nodes  # noqa: F401  — imports the submodules so sys.modules has them
from ark.config import Settings
from ark.state import DocSource, Library, SearchHit

# `ark.nodes` re-exports each node function under its module's own name, so the
# dotted attribute path resolves to the function; go through sys.modules instead.
SEARCH = sys.modules["ark.nodes.search_docs"]
CURATE = sys.modules["ark.nodes.curate_links"]
SCRAPE = sys.modules["ark.nodes.scrape_docs"]

LIBS = [Library(name="fastapi", reason="http"), Library(name="pydantic", reason="models")]


async def _instant(_seconds):
    """Skip the retry pause so tests stay fast."""


def _settings() -> Settings:
    return Settings(groq_api_key="k", firecrawl_api_key="k", search_max_results=3)


def _config(**configurable):
    base = {"settings": _settings(), "tools": {}, "max_alternates": 0}
    return {"configurable": {**base, **configurable}}


# --- matching --------------------------------------------------------------------


def test_pins_match_case_insensitively():
    """The user types `fastapi`; the model may have named it `FastAPI`."""
    matched, extra = SEARCH._match_provided(
        [Library(name="FastAPI")], {"fastapi": ["https://x.dev"]}
    )
    assert matched == {"FastAPI": ["https://x.dev"]}
    assert extra == []


def test_an_unmatched_label_becomes_its_own_library():
    """That is how a spec or internal page the requirement never named gets in."""
    matched, extra = SEARCH._match_provided(LIBS, {"acme-auth": ["https://internal.example/"]})
    assert matched == {"acme-auth": ["https://internal.example/"]}
    assert [lib.name for lib in extra] == ["acme-auth"]


def test_blank_urls_are_ignored():
    matched, extra = SEARCH._match_provided(LIBS, {"fastapi": ["   ", ""]})
    assert matched == {} and extra == []


# --- multiple URLs per library ---------------------------------------------------


async def test_several_urls_for_one_library_all_become_hits(monkeypatch):
    monkeypatch.setattr(SEARCH, "require_tool", lambda *a: object())
    out = await SEARCH.search_docs(
        {"libraries": LIBS},
        _config(doc_urls={"fastapi": ["https://a.dev/tutorial", "https://a.dev/advanced"]}),
    )
    assert [hit.url for hit in out["hits"]["fastapi"]] == [
        "https://a.dev/tutorial",
        "https://a.dev/advanced",
    ]


def test_first_url_is_primary_and_the_rest_are_alternates():
    source = CURATE.provided_source(
        Library(name="fastapi"), ["https://a.dev/one", "https://a.dev/two", "https://a.dev/three"]
    )
    assert source.url == "https://a.dev/one"
    assert source.alternates == ["https://a.dev/two", "https://a.dev/three"]
    assert source.confidence == 1.0
    assert source.user_supplied is True


def test_user_urls_are_never_trimmed_by_max_alternates():
    """The cap limits how many *guesses* get scraped; these are instructions."""
    source = DocSource(
        library="fastapi",
        url="https://a.dev/1",
        alternates=["https://a.dev/2", "https://a.dev/3", "https://a.dev/4"],
        user_supplied=True,
    )
    plan = SCRAPE.planned_urls([source], max_alternates=0)
    assert len(plan) == 4  # every URL the user named


def test_searched_alternates_still_respect_the_cap():
    source = DocSource(
        library="fastapi",
        url="https://a.dev/1",
        alternates=["https://a.dev/2", "https://a.dev/3"],
    )
    assert len(SCRAPE.planned_urls([source], max_alternates=1)) == 2


# --- search and curation are skipped ---------------------------------------------


async def test_pinned_library_is_not_searched(monkeypatch):
    searched = []

    async def fake_search(tool, library, settings):
        searched.append(library.name)
        return library.name, [SearchHit(url=f"https://found/{library.name}")]

    monkeypatch.setattr(SEARCH, "_search_one", fake_search)
    monkeypatch.setattr(SEARCH, "require_tool", lambda *a: object())

    out = await SEARCH.search_docs(
        {"libraries": LIBS}, _config(doc_urls={"fastapi": ["https://mine.dev/docs"]})
    )
    assert searched == ["pydantic"]
    assert out["hits"]["fastapi"][0].url == "https://mine.dev/docs"


async def test_all_pinned_means_no_search_backend_call(monkeypatch):
    def explode(*args):
        raise AssertionError("require_tool should not be called")

    monkeypatch.setattr(SEARCH, "require_tool", explode)
    out = await SEARCH.search_docs(
        {"libraries": LIBS},
        _config(doc_urls={"fastapi": ["https://a.dev"], "pydantic": ["https://b.dev"]}),
    )
    assert set(out["provided"]) == {"fastapi", "pydantic"}


async def test_no_pins_behaves_exactly_as_before(monkeypatch):
    async def fake_search(tool, library, settings):
        return library.name, [SearchHit(url=f"https://found/{library.name}")]

    monkeypatch.setattr(SEARCH, "_search_one", fake_search)
    monkeypatch.setattr(SEARCH, "require_tool", lambda *a: object())

    out = await SEARCH.search_docs({"libraries": LIBS}, _config())
    assert out["provided"] == {}
    assert sorted(out["hits"]) == ["fastapi", "pydantic"]


async def test_pinned_library_skips_the_llm_call(monkeypatch):
    called = []

    async def fake_curate(settings, library, hits, limiter):
        called.append(library.name)
        return DocSource(library=library.name, url=hits[0].url, confidence=0.9)

    monkeypatch.setattr(CURATE, "_curate_one", fake_curate)

    state = {
        "libraries": LIBS,
        "hits": {
            "fastapi": [SearchHit(url="https://mine.dev/docs")],
            "pydantic": [SearchHit(url="https://found")],
        },
        "provided": {"fastapi": ["https://mine.dev/docs"]},
    }
    out = await CURATE.curate_links(state, _config())

    assert called == ["pydantic"]  # fastapi cost no tokens
    by_lib = {s.library: s for s in out["doc_sources"]}
    assert by_lib["fastapi"].confidence == 1.0


# --- extra standalone links ------------------------------------------------------


async def test_extra_links_join_the_run_as_new_libraries(monkeypatch):
    async def fake_search(tool, library, settings):
        return library.name, [SearchHit(url=f"https://found/{library.name}")]

    monkeypatch.setattr(SEARCH, "_search_one", fake_search)
    monkeypatch.setattr(SEARCH, "require_tool", lambda *a: object())

    def ask(libraries, already):
        return {"acme-auth": ["https://internal.example/auth/"]}

    out = await SEARCH.search_docs({"libraries": LIBS}, _config(ask_doc_urls=ask))

    assert "acme-auth" in [lib.name for lib in out["libraries"]]
    assert out["hits"]["acme-auth"][0].url == "https://internal.example/auth/"
    assert out["provided"]["acme-auth"] == ["https://internal.example/auth/"]


async def test_callback_sees_urls_already_pinned_by_flag(monkeypatch):
    monkeypatch.setattr(SEARCH, "require_tool", lambda *a: object())
    seen = {}

    def ask(libraries, already):
        seen.update(already)
        return {}

    await SEARCH.search_docs(
        {"libraries": LIBS}, _config(doc_urls={"fastapi": ["https://a.dev"]}, ask_doc_urls=ask)
    )
    assert seen == {"fastapi": ["https://a.dev"]}  # not asked about again


# --- CLI parsing -----------------------------------------------------------------


def test_repeating_a_name_accumulates():
    from ark.cli import parse_doc_urls

    got = parse_doc_urls(
        ["fastapi=https://a.dev/1", "fastapi=https://a.dev/2", "pydantic=https://b.dev"]
    )
    assert got == {"fastapi": ["https://a.dev/1", "https://a.dev/2"], "pydantic": ["https://b.dev"]}


def test_urls_containing_equals_survive():
    from ark.cli import parse_doc_urls

    got = parse_doc_urls(["lib=https://x.dev/docs?v=2&lang=en"])
    assert got["lib"] == ["https://x.dev/docs?v=2&lang=en"]


@pytest.mark.parametrize("bad", ["fastapi", "=https://x.dev", "fastapi="])
def test_malformed_pairs_are_rejected(bad):
    import typer

    from ark.cli import parse_doc_urls

    with pytest.raises(typer.BadParameter):
        parse_doc_urls([bad])


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("https://a.dev https://b.dev", ["https://a.dev", "https://b.dev"]),
        ("https://a.dev, https://b.dev", ["https://a.dev", "https://b.dev"]),
        ("  https://a.dev  ", ["https://a.dev"]),
        ("", []),
    ],
)
def test_one_line_can_hold_several_urls(answer, expected):
    from ark.cli import _split_urls

    assert _split_urls(answer) == expected


@pytest.mark.parametrize(
    ("url", "label"),
    [
        ("https://docs.internal.acme.example/auth/", "acme"),
        ("https://fastapi.tiangolo.com/tutorial/", "tiangolo"),
        ("https://pypdf.readthedocs.io/en/stable/", "pypdf"),
    ],
)
def test_standalone_links_get_a_name_from_their_host(url, label):
    from ark.cli import _label_for

    assert _label_for(url) == label


# --- transient search failures ---------------------------------------------------


async def test_empty_search_is_retried_once(monkeypatch):
    calls = {"n": 0}

    class Tool:
        name = "firecrawl_search"

        async def ainvoke(self, args):
            calls["n"] += 1
            if calls["n"] == 1:
                return '{"data": {"web": []}}'
            return '{"data": {"web": [{"url": "https://pydantic.dev/docs"}]}}'

    monkeypatch.setattr(SEARCH.asyncio, "sleep", _instant)
    _, hits = await SEARCH._search_one(Tool(), Library(name="pydantic"), _settings())
    assert calls["n"] == 2
    assert hits[0].url == "https://pydantic.dev/docs"


async def test_persistently_empty_search_gives_up(monkeypatch):
    calls = {"n": 0}

    class Tool:
        name = "firecrawl_search"

        async def ainvoke(self, args):
            calls["n"] += 1
            return '{"data": {"web": []}}'

    monkeypatch.setattr(SEARCH.asyncio, "sleep", _instant)
    _, hits = await SEARCH._search_one(Tool(), Library(name="ghost"), _settings())
    assert calls["n"] == 2
    assert hits == []


def test_unresolved_libraries_stay_visible(capsys):
    """pydantic silently vanished from the results table after an empty search,
    having been listed as identified one line earlier."""
    from ark.render import render_results

    render_results(
        {
            "libraries": LIBS,
            "doc_sources": [DocSource(library="fastapi", url="https://fastapi.tiangolo.com")],
        }
    )
    out = capsys.readouterr().out
    assert "pydantic" in out
    assert "no documentation found" in out
