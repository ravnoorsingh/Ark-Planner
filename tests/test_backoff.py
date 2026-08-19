"""Rate-limit backoff — Groq's free tier caps tokens per minute."""

from __future__ import annotations

import pytest

from ark.llm import _invoke_with_backoff, _rate_limit_delay

GROQ_429 = (
    "Error code: 429 - {'error': {'message': 'Rate limit reached for model "
    "`openai/gpt-oss-120b` ... on tokens per minute (TPM): Limit 8000, Used 7847, "
    "Requested 1275. Please try again in 8.415s.', 'code': 'rate_limit_exceeded'}}"
)


def test_honours_the_wait_groq_states():
    delay = _rate_limit_delay(Exception(GROQ_429))
    assert delay == pytest.approx(8.915)  # stated wait plus a small margin


def test_falls_back_to_fixed_delay_when_no_duration_given():
    assert _rate_limit_delay(Exception("Error code: 429 rate_limit_exceeded")) == 5.0


def test_returns_none_for_unrelated_errors():
    assert _rate_limit_delay(Exception("401 invalid api key")) is None
    assert _rate_limit_delay(ValueError("bad json")) is None


class FlakyLLM:
    def __init__(self, failures: int, exc: Exception) -> None:
        self.failures = failures
        self.exc = exc
        self.calls = 0

    async def ainvoke(self, messages):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.exc
        return "ok"


@pytest.fixture(autouse=True)
def _no_real_sleeping(monkeypatch):
    async def instant(_seconds):
        return None

    monkeypatch.setattr("ark.llm.asyncio.sleep", instant)


async def test_retries_past_rate_limits_and_succeeds():
    llm = FlakyLLM(failures=2, exc=Exception(GROQ_429))
    assert await _invoke_with_backoff(llm, []) == "ok"
    assert llm.calls == 3


async def test_gives_up_after_the_attempt_budget():
    llm = FlakyLLM(failures=99, exc=Exception(GROQ_429))
    with pytest.raises(Exception, match="429"):
        await _invoke_with_backoff(llm, [], attempts=3)
    assert llm.calls == 3


async def test_does_not_retry_non_rate_limit_errors():
    llm = FlakyLLM(failures=99, exc=Exception("403 model blocked at org level"))
    with pytest.raises(Exception, match="403"):
        await _invoke_with_backoff(llm, [])
    assert llm.calls == 1  # failed fast, no pointless waiting


# --- oversized requests --------------------------------------------------------------

GROQ_413 = (
    "Error code: 413 - {'error': {'message': 'Request too large for model "
    "`openai/gpt-oss-120b` ... on tokens per minute (TPM): Limit 8000, Requested 13472, "
    "please reduce your message size and try again.', 'code': 'rate_limit_exceeded'}}"
)


def test_oversized_request_is_recognised():
    from ark.llm import is_too_large

    assert is_too_large(Exception(GROQ_413)) is True
    assert is_too_large(Exception(GROQ_429)) is False


def test_oversized_request_is_not_retried():
    """Its body says `rate_limit_exceeded`, but waiting can never make it fit —
    only sending less can. Retrying just burns the minute's budget."""
    assert _rate_limit_delay(Exception(GROQ_413)) is None


async def test_backoff_fails_fast_on_an_oversized_request():
    llm = FlakyLLM(failures=99, exc=Exception(GROQ_413))
    with pytest.raises(Exception, match="413"):
        await _invoke_with_backoff(llm, [])
    assert llm.calls == 1


# --- daily quota vs per-minute limit --------------------------------------------------

GROQ_TPD = (
    "Error code: 429 - {'error': {'message': 'Rate limit reached for model "
    "`openai/gpt-oss-120b` ... on tokens per day (TPD): Limit 200000, Used 199778, "
    "Requested 1773. Please try again in 8m37.968s.', 'code': 'rate_limit_exceeded'}}"
)


def test_compound_durations_are_parsed():
    """A TPD message says "8m37.968s"; an "([0-9.]+)s" pattern misses it entirely
    and silently backs off 5s instead."""
    from ark.llm import parse_retry_after

    assert parse_retry_after(GROQ_TPD) == pytest.approx(517.968)
    assert parse_retry_after("try again in 8.415s") == pytest.approx(8.415)
    assert parse_retry_after("try again in 1h2m3s") == pytest.approx(3723.0)
    assert parse_retry_after("no duration here") is None


def test_daily_limit_is_recognised():
    from ark.llm import is_daily_limit

    assert is_daily_limit(Exception(GROQ_TPD)) is True
    assert is_daily_limit(Exception(GROQ_429)) is False


def test_daily_limit_is_not_retried():
    """It can be hours away — four attempts just delay the same failure."""
    assert _rate_limit_delay(Exception(GROQ_TPD)) is None


async def test_backoff_fails_fast_on_a_daily_limit():
    llm = FlakyLLM(failures=99, exc=Exception(GROQ_TPD))
    with pytest.raises(Exception, match="429"):
        await _invoke_with_backoff(llm, [])
    assert llm.calls == 1


def test_quota_errors_are_explained_briefly():
    """One 400-char JSON blob per library buries the run's real output."""
    from ark.llm import explain_quota

    daily = explain_quota(Exception(GROQ_TPD))
    assert "daily token quota" in daily
    assert len(daily) < 100

    assert "per-minute" in explain_quota(Exception(GROQ_429))
    assert "per-request token ceiling" in explain_quota(Exception(GROQ_413))
