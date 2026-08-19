"""Redaction, configuration and the decorator's behaviour when tracing is off.

The redaction tests carry the weight here: every traced node is called with a
`Settings` object holding the process's API keys, so a regression in `safe` would
upload them to a third party without anything else failing.
"""

from __future__ import annotations

import pytest

from ark.config import Settings
from ark.state import DocSource, SearchHit
from ark.tracing import (
    REDACTED,
    annotate,
    configure,
    is_enabled,
    missing_api_key,
    safe,
    scrub_inputs,
    scrub_outputs,
    trace_run,
    traced,
)


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch, tmp_path):
    for name in (
        "LANGSMITH_TRACING",
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
        "LANGSMITH_ENDPOINT",
        "LANGCHAIN_TRACING_V2",
        "ARK_TRACE_MAX_CHARS",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)  # no .env to pick up here


# --- redaction --------------------------------------------------------------------


def test_settings_never_leaks_credentials():
    """The one that matters: nodes take Settings, and Settings holds every key."""
    settings = Settings(
        GROQ_API_KEY="gsk_secret",
        TAVILY_API_KEY="tvly_secret",
        FIRECRAWL_API_KEY="fc_secret",
        BRIGHT_DATA_API_TOKEN="bd_secret",
        LANGSMITH_API_KEY="lsv2_secret",
    )
    rendered = repr(safe(settings))

    for secret in ("gsk_secret", "tvly_secret", "fc_secret", "bd_secret", "lsv2_secret"):
        assert secret not in rendered
    assert REDACTED in rendered
    # Redacted, not dropped — the non-secret settings are the reason to trace it.
    assert "openai/gpt-oss-20b" in rendered


@pytest.mark.parametrize(
    "key",
    ["api_key", "API-KEY", "groq_api_key", "authorization", "Bearer", "password", "token"],
)
def test_secret_key_names_are_redacted(key):
    assert safe({key: "sensitive"}) == {key: REDACTED}


def test_secrets_are_redacted_at_depth():
    nested = {"outer": {"headers": {"Authorization": "Bearer abc"}}}
    assert safe(nested)["outer"]["headers"]["Authorization"] == REDACTED


def test_long_text_is_truncated_with_its_real_length():
    reduced = safe("x" * 5_000)
    assert reduced.startswith("x" * 100)
    assert "5000 chars total" in reduced
    assert len(reduced) < 5_000


def test_truncation_limit_is_configurable(monkeypatch):
    monkeypatch.setenv("ARK_TRACE_MAX_CHARS", "100")
    assert len(safe("y" * 1_000)) < 200


def test_long_lists_are_capped():
    reduced = safe(list(range(500)))
    assert len(reduced) == 41  # MAX_ITEMS plus the "… N more" marker
    assert "460 more item(s)" in reduced[-1]


def test_pydantic_models_are_dumped_not_repred():
    reduced = safe(DocSource(library="fastapi", url="https://fastapi.tiangolo.com"))
    assert reduced["library"] == "fastapi"
    assert reduced["url"] == "https://fastapi.tiangolo.com"


def test_callable_objects_are_still_clipped():
    """A BeautifulSoup Tag is callable and reprs to its whole subtree."""
    from bs4 import BeautifulSoup

    tag = BeautifulSoup("<main>" + "<p>x</p>" * 2_000 + "</main>", "html.parser").main
    assert len(safe(tag)) < 3_000


def test_named_callables_reduce_to_their_name():
    assert safe(print) == "print"


def test_cycles_and_odd_objects_do_not_recurse_forever():
    cycle: dict = {}
    cycle["self"] = cycle
    assert safe(cycle)  # bounded by MAX_DEPTH rather than hanging


def test_scrub_inputs_drops_plumbing_arguments():
    scrubbed = scrub_inputs(
        {
            "settings": Settings(GROQ_API_KEY="gsk_secret"),
            "limiter": object(),
            "llm": object(),
            "url": "https://x.dev",
            "on_tick": print,
        }
    )
    # Settings is kept because the run's configuration is worth seeing; the
    # semaphore, the client object and the progress callback are pure noise.
    assert set(scrubbed) == {"settings", "url"}
    assert scrubbed["settings"]["groq_api_key"] == REDACTED


def test_scrub_outputs_always_produces_a_dict():
    assert scrub_outputs([SearchHit(url="https://x.dev")]) == {
        "output": [{"url": "https://x.dev", "title": "", "snippet": "", "score": None}]
    }
    assert scrub_outputs({"hits": 2}) == {"hits": 2}


# --- decorator --------------------------------------------------------------------


def test_traced_is_transparent_when_tracing_is_off():
    @traced("adder", run_type="tool")
    def add(left: int, right: int) -> int:
        return left + right

    assert add(2, 3) == 5


async def test_traced_preserves_async_results_and_exceptions():
    @traced("boom")
    async def boom() -> None:
        raise ValueError("kaboom")

    with pytest.raises(ValueError, match="kaboom"):
        await boom()


def test_annotate_is_a_noop_outside_a_run():
    annotate(anything="at all")  # must not raise when nothing is tracing


def test_trace_run_yields_a_handle_with_no_url_when_disabled():
    with trace_run("ark docs", requirement="x") as handle:
        assert handle.url == ""


# --- configuration ----------------------------------------------------------------


def test_configure_enables_tracing_and_publishes_the_project(monkeypatch):
    settings = Settings(LANGSMITH_TRACING=True, LANGSMITH_API_KEY="lsv2_key")
    assert configure(settings) is True
    assert is_enabled()
    import os

    assert os.environ["LANGSMITH_PROJECT"] == "ark-scrapper"
    assert os.environ["LANGSMITH_API_KEY"] == "lsv2_key"


def test_configure_without_a_key_stays_off():
    settings = Settings(LANGSMITH_TRACING=True, LANGSMITH_API_KEY="   ")
    assert configure(settings) is False
    assert not is_enabled()
    assert missing_api_key(settings)


def test_disabled_config_overrides_an_inherited_env_var(monkeypatch):
    """An exported LANGSMITH_TRACING must not re-enable what the config turned off."""
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    assert configure(Settings(LANGSMITH_TRACING=False)) is False
    assert not is_enabled()


def test_tracing_is_off_by_default():
    assert Settings().langsmith_tracing is False
    assert configure(Settings()) is False
