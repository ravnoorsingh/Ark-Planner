"""Settings loading, CLI overrides, and credential checks."""

from __future__ import annotations

from pathlib import Path

import pytest

from ark.config import MissingCredentials, Settings, load_settings


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch, tmp_path):
    """Keep a developer's real .env / exported keys out of these tests."""
    for name in (
        "GROQ_API_KEY",
        "TAVILY_API_KEY",
        "ARK_MODEL",
        "ARK_OUTPUT_DIR",
        "ARK_TAVILY_MCP_URL",
        "BRIGHT_DATA_API_TOKEN",
        "BRIGHT_DATA_COLLECTOR_ID",
        "BRIGHT_DATA_CONTENT_FIELD",
        "ARK_DATA_DIR",
        "ARK_MAX_ALTERNATES",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)  # no .env to pick up here


def test_cli_override_is_applied_not_silently_dropped():
    """Regression: fields carry env aliases, so init-by-name needs populate_by_name."""
    settings = load_settings(model="openai/gpt-oss-120b")
    assert settings.model == "openai/gpt-oss-120b"


def test_cli_override_beats_the_environment(monkeypatch):
    monkeypatch.setenv("ARK_MODEL", "from-env")
    assert load_settings(model="from-cli").model == "from-cli"


def test_environment_is_used_when_no_override(monkeypatch):
    monkeypatch.setenv("ARK_MODEL", "from-env")
    assert load_settings(model=None).model == "from-env"


def test_none_overrides_are_dropped():
    assert load_settings(model=None, output_dir=None).model == "openai/gpt-oss-20b"


def test_output_dir_override():
    assert load_settings(output_dir=Path("/tmp/artifacts")).output_dir == Path("/tmp/artifacts")


def test_require_credentials_names_every_missing_key():
    with pytest.raises(MissingCredentials) as exc:
        Settings().require_credentials("GROQ_API_KEY", "TAVILY_API_KEY")
    message = str(exc.value)
    assert "GROQ_API_KEY" in message
    assert "TAVILY_API_KEY" in message
    assert "console.groq.com" in message  # the fix, not just the symptom


def test_require_credentials_rejects_whitespace_only_keys():
    with pytest.raises(MissingCredentials, match="GROQ_API_KEY"):
        Settings(groq_api_key="   ", tavily_api_key="tvly-x").require_credentials(
            "GROQ_API_KEY", "TAVILY_API_KEY"
        )


def test_require_credentials_passes_when_both_present():
    Settings(groq_api_key="gsk-x", tavily_api_key="tvly-x").require_credentials(
        "GROQ_API_KEY", "TAVILY_API_KEY"
    )


def test_scrape_does_not_require_llm_or_search_keys():
    """`ark scrape` reads an existing artifact; demanding LLM keys would be a false barrier."""
    settings = Settings(brightdata_api_token="tok", brightdata_collector_id="c_1")
    settings.require_credentials("BRIGHT_DATA_API_TOKEN", "BRIGHT_DATA_COLLECTOR_ID")


def test_missing_brightdata_credentials_point_at_the_console():
    with pytest.raises(MissingCredentials) as exc:
        Settings().require_credentials("BRIGHT_DATA_API_TOKEN", "BRIGHT_DATA_COLLECTOR_ID")
    message = str(exc.value)
    assert "brightdata.com/cp/setting" in message
    assert "brightdata.com/cp/scrapers" in message
    assert "GROQ_API_KEY" not in message  # only what this command needs


def test_requiring_nothing_never_raises():
    Settings().require_credentials()


def test_unknown_credential_name_is_a_programming_error():
    with pytest.raises(ValueError, match="NOPE_KEY"):
        Settings().require_credentials("NOPE_KEY")


def test_brightdata_defaults():
    settings = Settings()
    # Web Unlocker is page-exact with no collector to maintain; Scraper Studio
    # remains selectable via ARK_SCRAPE_BACKEND=collector.
    assert settings.scrape_backend == "unlocker"
    assert settings.data_dir == Path("data")
    assert settings.max_alternates == 2
    assert settings.brightdata_content_field == ""  # empty means auto-detect


def test_mcp_endpoint_appends_key_as_query_param():
    settings = Settings(tavily_api_key="tvly-secret")
    assert settings.tavily_mcp_endpoint == "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-secret"


def test_mcp_endpoint_uses_ampersand_when_url_already_has_a_query():
    settings = Settings(
        tavily_api_key="k", tavily_mcp_url="https://example.com/mcp/?foo=bar"
    )
    assert settings.tavily_mcp_endpoint == "https://example.com/mcp/?foo=bar&tavilyApiKey=k"
