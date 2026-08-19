"""Resolving generic capabilities ("a vector database") into named libraries."""

from __future__ import annotations

import pytest

from ark.choices import ChoiceSet, LibraryChoice, LibraryOption, apply_choices, describe

VECTOR_DB = LibraryChoice(
    slot="vector database",
    reason="store and query document embeddings",
    options=[
        LibraryOption(name="chromadb", note="simplest to run locally"),
        LibraryOption(name="qdrant-client", note="best filtering support"),
        LibraryOption(name="faiss-cpu", note="fastest for static in-memory indexes"),
    ],
    recommended="chromadb",
)


# --- defaults -----------------------------------------------------------------------


def test_recommended_is_the_default():
    assert VECTOR_DB.default() == "chromadb"


def test_first_option_is_the_default_when_none_recommended():
    choice = VECTOR_DB.model_copy(update={"recommended": ""})
    assert choice.default() == "chromadb"


def test_no_options_yields_no_default():
    assert LibraryChoice(slot="x").default() == ""


# --- folding picks back into the requirement ----------------------------------------


def test_pick_is_stated_explicitly_in_the_requirement():
    """Downstream stages read the requirement, so the decision has to live there —
    the artifact, plan goal and store folder names all show what was researched."""
    out = apply_choices("Build a RAG app with a vector database", {"vector database": "qdrant-client"})
    assert out == "Build a RAG app with a vector database. Use qdrant-client for the vector database."


def test_trailing_full_stop_is_not_doubled():
    out = apply_choices("Build a RAG app.", {"vector database": "qdrant-client"})
    assert ".. " not in out
    assert out.startswith("Build a RAG app. Use qdrant-client")


def test_several_slots_are_all_recorded():
    out = apply_choices("Build an app", {"vector database": "qdrant-client", "orm": "sqlmodel"})
    assert "Use qdrant-client for the vector database." in out
    assert "Use sqlmodel for the orm." in out


@pytest.mark.parametrize("decisions", [{}, {"vector database": ""}, {"orm": "   "}])
def test_empty_decisions_leave_the_requirement_alone(decisions):
    assert apply_choices("Build an app", decisions) == "Build an app"


def test_a_typed_library_is_used_verbatim():
    """The user may name something the model never listed; that must survive."""
    out = apply_choices("Build a RAG app", {"vector database": "lancedb"})
    assert "Use lancedb for the vector database." in out


def test_describe_reads_as_a_decision():
    assert describe(VECTOR_DB, "faiss-cpu") == "vector database → faiss-cpu"


# --- detection filtering ------------------------------------------------------------


async def _detect(monkeypatch, payload: ChoiceSet):
    import ark.choices as module

    async def fake_structured(_llm, _schema, _system, _user, **_kwargs):
        return payload

    monkeypatch.setattr(module, "structured", fake_structured)
    monkeypatch.setattr(module, "build_llm", lambda *a, **k: object())
    from ark.config import Settings

    return await module.detect_choices(Settings(), "Build a RAG app")


async def test_slot_with_a_single_option_is_not_a_choice(monkeypatch):
    """Presenting a one-item menu wastes the user's time; it's a decision, not a choice."""
    payload = ChoiceSet(
        choices=[LibraryChoice(slot="orm", options=[LibraryOption(name="sqlmodel")])]
    )
    assert await _detect(monkeypatch, payload) == []


async def test_duplicate_slots_are_collapsed(monkeypatch):
    payload = ChoiceSet(choices=[VECTOR_DB, VECTOR_DB.model_copy()])
    assert len(await _detect(monkeypatch, payload)) == 1


async def test_slots_are_matched_case_insensitively(monkeypatch):
    payload = ChoiceSet(
        choices=[VECTOR_DB, VECTOR_DB.model_copy(update={"slot": "Vector Database"})]
    )
    assert len(await _detect(monkeypatch, payload)) == 1


async def test_a_fully_specified_requirement_produces_no_choices(monkeypatch):
    """Naming ChromaDB settles it — offering alternatives second-guesses the user."""
    assert await _detect(monkeypatch, ChoiceSet(choices=[])) == []


async def test_real_choices_survive(monkeypatch):
    choices = await _detect(monkeypatch, ChoiceSet(choices=[VECTOR_DB]))
    assert [c.slot for c in choices] == ["vector database"]
    assert len(choices[0].options) == 3


# --- the interactive prompt ---------------------------------------------------------


def _answer(monkeypatch, *replies):
    """Feed scripted replies to the prompt."""
    from ark import cli

    queue = list(replies)
    monkeypatch.setattr(cli.console, "input", lambda *a, **k: queue.pop(0))
    monkeypatch.setattr(cli.console, "print", lambda *a, **k: None)
    return cli


def test_enter_accepts_the_recommendation(monkeypatch):
    cli = _answer(monkeypatch, "")
    assert cli._ask_choice(VECTOR_DB) == "chromadb"


def test_a_number_selects_that_option(monkeypatch):
    cli = _answer(monkeypatch, "2")
    assert cli._ask_choice(VECTOR_DB) == "qdrant-client"


def test_out_of_range_number_is_treated_as_a_package_name(monkeypatch):
    """Better to trust the input than to silently pick something else."""
    cli = _answer(monkeypatch, "9")
    assert cli._ask_choice(VECTOR_DB) == "9"


def test_other_prompts_for_a_typed_name(monkeypatch):
    cli = _answer(monkeypatch, "o", "lancedb")
    assert cli._ask_choice(VECTOR_DB) == "lancedb"


def test_other_reprompts_when_nothing_is_typed(monkeypatch):
    cli = _answer(monkeypatch, "other", "", "3")
    assert cli._ask_choice(VECTOR_DB) == "faiss-cpu"


def test_a_package_name_can_be_typed_directly(monkeypatch):
    """Users who know what they want shouldn't have to go through the menu."""
    cli = _answer(monkeypatch, "pgvector")
    assert cli._ask_choice(VECTOR_DB) == "pgvector"
