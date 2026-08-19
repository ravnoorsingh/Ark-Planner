"""The json_mode structured-output helper, including its repair retry.

Groq's strict json_schema mode is unavailable on Qwen, so `structured()` has to
tolerate near-miss JSON and repair it. Fully mocked — no network.
"""

from __future__ import annotations

import json

import pytest
from pydantic import BaseModel

from ark.llm import (
    _extract_json,
    repair_truncated_json,
    salvage_partial_json,
    structured,
)


class Answer(BaseModel):
    name: str
    count: int


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.content = content


@pytest.fixture(autouse=True)
def _no_real_sleeping(monkeypatch):
    """The retry pause is real seconds; tests must not actually wait them out."""

    async def instant(_seconds):
        return None

    monkeypatch.setattr("ark.llm.asyncio.sleep", instant)


class FakeLLM:
    """Returns each scripted reply in turn, recording the messages it received."""

    def __init__(self, *replies: str) -> None:
        self._replies = list(replies)
        self.calls: list[list] = []

    async def ainvoke(self, messages):
        self.calls.append(messages)
        return FakeResponse(self._replies.pop(0))


async def test_parses_clean_json_first_try():
    llm = FakeLLM('{"name": "fastapi", "count": 2}')
    result = await structured(llm, Answer, "system", "user")
    assert result == Answer(name="fastapi", count=2)
    assert len(llm.calls) == 1


async def test_injects_schema_into_system_prompt():
    llm = FakeLLM('{"name": "x", "count": 1}')
    await structured(llm, Answer, "SYSTEM-MARKER", "user")
    system = llm.calls[0][0].content
    assert "SYSTEM-MARKER" in system
    assert "count" in system  # the JSON Schema was appended


async def test_repairs_invalid_json_on_retry():
    llm = FakeLLM('{"name": "fastapi"}', '{"name": "fastapi", "count": 3}')
    result = await structured(llm, Answer, "system", "user")
    assert result.count == 3
    assert len(llm.calls) == 2
    # The retry must tell the model what was wrong.
    assert "not valid for the schema" in llm.calls[1][-1].content


async def test_raises_after_retries_are_exhausted():
    llm = FakeLLM("not json at all", "still not json")
    with pytest.raises(ValueError, match="schema-valid JSON"):
        await structured(llm, Answer, "system", "user")
    assert len(llm.calls) == 2


async def test_honours_retries_zero():
    llm = FakeLLM("{}")
    with pytest.raises(ValueError):
        await structured(llm, Answer, "system", "user", retries=0)
    assert len(llm.calls) == 1


@pytest.mark.parametrize(
    "raw",
    [
        '{"name": "a", "count": 1}',
        '```json\n{"name": "a", "count": 1}\n```',
        '```\n{"name": "a", "count": 1}\n```',
        'Here you go:\n{"name": "a", "count": 1}\nHope that helps!',
    ],
)
async def test_tolerates_fences_and_surrounding_prose(raw):
    """Reasoning models wrap output even in JSON mode."""
    result = await structured(FakeLLM(raw), Answer, "system", "user")
    assert result == Answer(name="a", count=1)


def test_extract_json_returns_text_unchanged_when_no_object_present():
    assert _extract_json("no braces here") == "no braces here"


# --- salvaging truncated generations -------------------------------------------------


def test_repair_closes_open_brackets():
    assert repair_truncated_json('{"a": [1, 2') == '{"a": [1, 2]}'
    assert repair_truncated_json('{"a": {"b": 1') == '{"a": {"b": 1}}'


def test_repair_drops_an_unterminated_string_and_its_element():
    """Generation stops mid-word; that element is unusable but the rest is fine."""
    partial = '{"title":"Plan","phases":[{"title":"Setup"},{"title":"Project initializati'

    result = json.loads(repair_truncated_json(partial))
    assert result["title"] == "Plan"
    assert [p["title"] for p in result["phases"]] == ["Setup"]


def test_repair_removes_a_dangling_comma():

    assert json.loads(repair_truncated_json('{"a": [1, 2, ')) == {"a": [1, 2]}


def test_repair_leaves_complete_json_alone():
    assert repair_truncated_json('{"a": 1}') == '{"a": 1}'


def test_repair_ignores_brackets_inside_strings():

    assert json.loads(repair_truncated_json('{"a": "a [weird} value"')) == {
        "a": "a [weird} value"
    }


GROQ_JSON_FAIL = (
    "Error code: 400 - {'error': {'message': \"Failed to generate JSON.\", "
    "'code': 'json_validate_failed', 'failed_generation': "
    "'{\"name\": \"fastapi\", \"count\": 3, \"extra\": [1, 2'}}"
)


def test_salvage_extracts_and_repairs_the_partial_generation():

    salvaged = salvage_partial_json(Exception(GROQ_JSON_FAIL))
    assert json.loads(salvaged)["name"] == "fastapi"


def test_salvage_returns_none_for_unrelated_errors():
    assert salvage_partial_json(Exception("429 rate limited")) is None


async def test_structured_recovers_a_truncated_response():
    """The content was generated and billed; a clipped tail shouldn't waste it."""

    class Failing:
        calls = 0

        async def ainvoke(self, messages):
            Failing.calls += 1
            raise Exception(GROQ_JSON_FAIL)

    result = await structured(Failing(), Answer, "system", "user")
    assert result == Answer(name="fastapi", count=3)
    assert Failing.calls == 1  # salvaged, not retried


async def test_unsalvageable_error_still_propagates():
    bad = (
        "Error code: 400 - {'error': {'code': 'json_validate_failed', "
        "'failed_generation': '{\"unrelated\": true'}}"
    )

    class Failing:
        async def ainvoke(self, messages):
            raise Exception(bad)

    with pytest.raises(Exception, match="json_validate_failed"):
        await structured(Failing(), Answer, "system", "user")


def test_salvage_survives_a_different_error_envelope():
    """The old pattern anchored on a literal "'}}" at end-of-string, so any
    variation in the tail — another key after failed_generation, extra braces —
    silently lost a plan that had already been generated and billed."""
    err = (
        "Error code: 400 - {'error': {'code': 'json_validate_failed', "
        "'failed_generation': '{\"name\": \"fastapi\", \"count\": 7, \"x\": [1', "
        "'type': 'invalid_request_error'}}"
    )
    salvaged = salvage_partial_json(Exception(err))
    assert salvaged is not None
    assert json.loads(salvaged)["count"] == 7


def test_salvage_handles_a_double_quoted_key():
    err = 'Error 400 {"failed_generation": "{\\"name\\": \\"x\\", \\"count\\": 1"}'
    salvaged = salvage_partial_json(Exception(err))
    assert json.loads(salvaged)["name"] == "x"


def test_salvage_ignores_an_error_without_a_payload():
    assert salvage_partial_json(Exception("failed_generation: ")) is None


def test_salvage_does_not_truncate_at_a_key_inside_the_payload():
    """The payload's own `"title":` must not be mistaken for the error object's
    next key — that would throw away most of a recoverable plan."""
    payload = '{"name": "a", "count": 2, "nested": {"title": "keep me"'
    err = (
        "Error 400 {'code': 'json_validate_failed', 'failed_generation': "
        f"'{payload}', 'type': 'invalid_request_error'}}}}"
    )
    salvaged = salvage_partial_json(Exception(err))
    assert "keep me" in salvaged
    assert json.loads(salvaged)["count"] == 2


# --- truncated generations are contention, not bad prompts ----------------------------

TRUNCATED = (
    "Error code: 400 - {'error': {'message': \"Failed to generate JSON.\", "
    "'code': 'json_validate_failed', 'failed_generation': '{\"unusable\": true'}}"
)


def test_truncation_is_recognised():
    from ark.llm import is_truncated_generation

    assert is_truncated_generation(Exception(TRUNCATED)) is True
    assert is_truncated_generation(Exception("429 rate limited")) is False


async def test_an_unsalvageable_truncation_is_retried():
    """It happens when the per-minute budget runs down mid-response, so the same
    call usually succeeds moments later — worth a retry before giving up."""

    class Flaky:
        calls = 0

        async def ainvoke(self, messages):
            Flaky.calls += 1
            if Flaky.calls == 1:
                raise Exception(TRUNCATED)
            return FakeResponse('{"name": "pinecone-client", "count": 1}')

    result = await structured(Flaky(), Answer, "system", "user")
    assert result.name == "pinecone-client"
    assert Flaky.calls == 2


async def test_a_persistent_truncation_still_raises():
    class Always:
        calls = 0

        async def ainvoke(self, messages):
            Always.calls += 1
            raise Exception(TRUNCATED)

    with pytest.raises(Exception, match="json_validate_failed"):
        await structured(Always(), Answer, "system", "user")
    assert Always.calls == 2  # original attempt plus one retry


async def test_other_errors_are_not_retried():
    """A 401 will never fix itself; retrying just delays the failure."""

    class Always:
        calls = 0

        async def ainvoke(self, messages):
            Always.calls += 1
            raise Exception("401 invalid api key")

    with pytest.raises(Exception, match="401"):
        await structured(Always(), Answer, "system", "user")
    assert Always.calls == 1
