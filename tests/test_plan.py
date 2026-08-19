"""Citation assignment, corpus budgeting, and plan rendering."""

from __future__ import annotations

from ark.plan import (
    build_citations,
    cell,
    citation_key,
    load_corpus,
    render_plan,
    used_keys,
)
from ark.state import ApiItem, Citation, LibraryBrief, PlanDraft, PlanSection, ScrapedDoc


def _doc(library: str, url: str, **kwargs) -> ScrapedDoc:
    base = {
        "library": library,
        "url": url,
        "role": "primary",
        "status": "ok",
        "path": f"data/{library}/page.md",
        "sha256": "a" * 64,
        "fetched_at": "2026-08-17T14:58:06+00:00",
    }
    return ScrapedDoc(**{**base, **kwargs})


# --- citation keys ------------------------------------------------------------------


def test_keys_are_slugged_and_numbered():
    assert citation_key("tavily-python", 1) == "tavily-python-1"
    assert citation_key("@scope/Pkg Name", 2) == "scope-pkg-name-2"


def test_keys_number_per_library():
    docs = [
        _doc("typer", "https://typer.tiangolo.com"),
        _doc("typer", "https://github.com/fastapi/typer", role="alternate", rank=1),
        _doc("rich", "https://rich.readthedocs.io"),
    ]
    assert [c.key for c in build_citations(docs)] == ["typer-1", "typer-2", "rich-1"]


def test_unstored_documents_are_never_citable():
    """A failed or empty page has nothing to cite; a footnote to it would be a lie."""
    docs = [
        _doc("a", "https://a.dev", status="failed", path=None),
        _doc("b", "https://b.dev", status="empty"),
        _doc("c", "https://c.dev"),
    ]
    assert [c.library for c in build_citations(docs)] == ["c"]


def test_citation_points_at_where_the_text_actually_came_from():
    docs = [_doc("x", "https://x.dev", resolved_url="https://x.dev/en/latest/")]
    assert build_citations(docs)[0].url == "https://x.dev/en/latest/"


def test_citation_carries_the_snapshot_digest():
    citation = build_citations([_doc("x", "https://x.dev")])[0]
    assert citation.sha256 == "a" * 64
    assert citation.fetched_at.startswith("2026-08-17")


# --- corpus budgeting ---------------------------------------------------------------


def _write(tmp_path, name: str, body: str) -> Citation:
    path = tmp_path / name
    path.write_text(f'---\nlibrary: "x"\nurl: "https://x.dev"\n---\n\n{body}', encoding="utf-8")
    return Citation(key=name.replace(".md", ""), library="x", url="https://x.dev", path=str(path))


def test_front_matter_is_stripped_from_the_corpus():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        citation = _write(Path(tmp), "a.md", "REAL CONTENT")
        corpus = load_corpus([citation])
    assert "REAL CONTENT" in corpus
    assert "library:" not in corpus


def test_budget_is_shared_so_a_huge_page_cannot_crowd_out_a_small_one(tmp_path):
    """An install page is often the shortest file and the most important."""
    big = _write(tmp_path, "big.md", "X" * 100_000)
    small = _write(tmp_path, "small.md", "pip install thing")
    corpus = load_corpus([big, small], budget=20_000)

    assert "pip install thing" in corpus
    assert "truncated" in corpus  # the big one was cut, not the small one


def test_each_source_is_labelled_with_its_citation_key(tmp_path):
    corpus = load_corpus([_write(tmp_path, "a.md", "content here")])
    assert "SOURCE [^a]" in corpus
    assert "https://x.dev" in corpus


def test_missing_files_are_skipped_not_fatal():
    ghost = Citation(key="g", library="x", url="https://x.dev", path="/nope/gone.md")
    assert load_corpus([ghost]) == ""


# --- footnote scanning --------------------------------------------------------------


def test_used_keys_finds_markers_across_texts():
    assert used_keys("see [^a-1] and [^b-2]", "also [^a-1]") == {"a-1", "b-2"}


def test_used_keys_on_empty_input():
    assert used_keys("", None) == set()


# --- rendering ----------------------------------------------------------------------

CITATIONS = [
    Citation(key="typer-1", library="typer", url="https://typer.tiangolo.com",
             path="data/typer/p.md", sha256="b" * 64, fetched_at="2026-08-17T14:58:06+00:00"),
    Citation(key="rich-1", library="rich", url="https://rich.readthedocs.io",
             path="data/rich/p.md", sha256="c" * 64, fetched_at="2026-08-17T14:58:07+00:00"),
]

BRIEFS = [
    LibraryBrief(
        library="typer", install="uv add typer", version="0.15.0",
        summary="CLI framework built on type hints.",
        api=[ApiItem(name="typer.Typer", signature="typer.Typer()",
                     summary="App object.", example="import typer\napp = typer.Typer()")],
        gotchas=["Completion needs --install-completion."],
        citation_keys=["typer-1"],
    ),
    LibraryBrief(library="rich", install="pip install rich", summary="Terminal formatting.",
                 citation_keys=["rich-1"]),
]

DRAFT = PlanDraft(
    title="CLI tool",
    overview="Build a CLI with typer and rich.",
    phases=[PlanSection(title="Setup", body="1. Run `uv add typer`[^typer-1].")],
    pitfalls=["Pin versions before shipping."],
)


def _plan() -> str:
    return render_plan("build a CLI", DRAFT, BRIEFS, CITATIONS, model="m", generated_at="now")


def test_plan_has_the_expected_sections():
    md = _plan()
    for section in ("## Stack", "## Library reference", "## Implementation", "## Sources"):
        assert section in md


def test_goal_and_provenance_are_recorded():
    md = _plan()
    assert "build a CLI" in md
    assert "model `m`" in md
    assert "2 documentation page(s)" in md


def test_stack_table_carries_version_and_install():
    md = _plan()
    assert "| typer | 0.15.0 | `uv add typer` |" in md
    assert "unpinned" in md  # rich stated no version, and that is said plainly


def test_verbatim_example_survives_rendering():
    assert "app = typer.Typer()" in _plan()


def test_phases_are_numbered_in_order():
    assert "### Phase 1 — Setup" in _plan()


def test_every_footnote_marker_resolves_to_a_definition():
    """A dangling [^key] is a citation that cannot be checked."""
    md = _plan()
    for key in used_keys(md):
        assert f"[^{key}]: " in md


def test_sources_include_local_copy_and_digest():
    md = _plan()
    assert "data/typer/p.md" in md
    assert "sha256 `bbbbbbbbbbbb`" in md


def test_unreferenced_citations_are_dropped_from_sources():
    """Listing a page the plan never drew on overstates its grounding."""
    extra = [*CITATIONS, Citation(key="ghost-1", library="ghost", url="https://ghost.dev")]
    draft = PlanDraft(title="t", phases=[PlanSection(title="P", body="only [^typer-1] here")])
    md = render_plan("req", draft, [BRIEFS[0]], extra)
    assert "ghost.dev" not in md


def test_falls_back_to_brief_gotchas_when_synthesis_produced_none():
    draft = PlanDraft(title="t", phases=[PlanSection(title="P", body="body [^typer-1]")])
    md = render_plan("req", draft, BRIEFS, CITATIONS)
    assert "Completion needs --install-completion." in md


def test_renders_without_phases_when_synthesis_failed():
    """Distilling is the expensive half; its output must still reach the user."""
    md = render_plan("req", PlanDraft(title="t"), BRIEFS, CITATIONS)
    assert "## Library reference" in md
    assert "## Implementation" not in md
    assert "## Sources" in md


# --- table safety -------------------------------------------------------------------


def test_cell_flattens_newlines():
    """Docs often print an install command across two lines; a raw newline would
    break every table row below it."""
    assert cell("pip install uvicorn\n# or\nuv add uvicorn") == "pip install uvicorn # or uv add uvicorn"


def test_cell_escapes_pipes():
    assert cell("a | b") == "a \\| b"


def test_stack_table_rows_stay_on_one_line():
    brief = LibraryBrief(library="uvicorn", install="pip install uvicorn\nuv add uvicorn",
                         citation_keys=["rich-1"])
    md = render_plan("req", DRAFT, [brief], CITATIONS)
    stack = md.split("## Stack")[1].split("##")[0]
    rows = [r for r in stack.splitlines() if r.startswith("|")]
    assert len(rows) == 3  # header, separator, one package


# --- surviving a partly malformed response -------------------------------------------


def test_a_malformed_api_entry_does_not_lose_the_brief():
    """Under load the model emits "" where an object belongs. Rejecting the whole
    response for one bad element costs an entire library's brief."""
    brief = LibraryBrief.model_validate(
        {"library": "pydantic",
         "api": [{"name": "BaseModel"}, "", {"name": "Field"}, None]}
    )
    assert [item.name for item in brief.api] == ["BaseModel", "Field"]


def test_a_malformed_phase_does_not_lose_the_plan():
    """`phases.4` arriving as a string cost all six phases of a real run."""
    draft = PlanDraft.model_validate(
        {"title": "t",
         "phases": [{"title": "Setup", "body": "a"}, "tit", {"title": "Run", "body": "b"}]}
    )
    assert [phase.title for phase in draft.phases] == ["Setup", "Run"]


def test_blank_strings_are_dropped_from_string_lists():
    brief = LibraryBrief.model_validate(
        {"library": "x", "gotchas": ["real warning", "", "   "], "citation_keys": ["x-1", ""]}
    )
    assert brief.gotchas == ["real warning"]
    assert brief.citation_keys == ["x-1"]


def test_well_formed_responses_are_untouched():
    brief = LibraryBrief.model_validate(
        {"library": "x", "api": [{"name": "a"}, {"name": "b"}], "gotchas": ["one", "two"]}
    )
    assert len(brief.api) == 2
    assert brief.gotchas == ["one", "two"]
