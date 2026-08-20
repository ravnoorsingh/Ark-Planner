"""Runtime configuration, loaded from the environment / .env."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MissingCredentials(RuntimeError):
    """Raised when a required API key is absent, so the CLI can print a clean message."""


CREDENTIAL_HELP = {
    "GROQ_API_KEY": "Groq key:            https://console.groq.com/keys",
    "TAVILY_API_KEY": "Tavily key:          https://app.tavily.com",
    "FIRECRAWL_API_KEY": "Firecrawl key:       https://firecrawl.dev/app/api-keys",
    "BRIGHT_DATA_API_TOKEN": "Bright Data token:   https://brightdata.com/cp/setting",
    "BRIGHT_DATA_COLLECTOR_ID": "Collector ID (c_…):  https://brightdata.com/cp/scrapers",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # Fields carry env aliases; without this, CLI overrides passed by field
        # name (Settings(model=...)) would be silently dropped by extra="ignore".
        populate_by_name=True,
    )

    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    tavily_api_key: str = Field(default="", alias="TAVILY_API_KEY")
    firecrawl_api_key: str = Field(default="", alias="FIRECRAWL_API_KEY")
    brightdata_api_token: str = Field(default="", alias="BRIGHT_DATA_API_TOKEN")
    brightdata_collector_id: str = Field(default="", alias="BRIGHT_DATA_COLLECTOR_ID")

    model: str = Field(default="openai/gpt-oss-20b", alias="ARK_MODEL")
    temperature: float = Field(default=0.1, alias="ARK_TEMPERATURE")
    max_libraries: int = Field(default=8, alias="ARK_MAX_LIBRARIES")
    search_max_results: int = Field(default=5, alias="ARK_SEARCH_MAX_RESULTS")
    # Curation fires one LLM call per library; cap the parallelism so a wide stack
    # doesn't blow Groq's free-tier tokens-per-minute limit in a single burst.
    llm_concurrency: int = Field(default=3, ge=1, alias="ARK_LLM_CONCURRENCY")
    # Note: gpt-oss models also support Groq's strict json_schema mode, but the
    # json_mode path in llm.py works on every model, so it stays the single route.
    output_dir: Path = Field(default=Path("output"), alias="ARK_OUTPUT_DIR")
    # Web search runs over MCP. "firecrawl" is the default; "tavily" remains
    # selectable and both are exercised by the same code path.
    search_backend: Literal["firecrawl", "tavily"] = Field(
        default="firecrawl", alias="ARK_SEARCH_BACKEND"
    )
    firecrawl_mcp_url: str = Field(
        default="https://mcp.firecrawl.dev/v2/mcp", alias="ARK_FIRECRAWL_MCP_URL"
    )
    tavily_mcp_url: str = Field(
        default="https://mcp.tavily.com/mcp/", alias="ARK_TAVILY_MCP_URL"
    )

    # --- Bright Data ----------------------------------------------------------------
    # "unlocker" (default) hits Bright Data's Web Unlocker API: page-exact by
    # construction, one request per URL, no collector to build or maintain.
    # "collector" drives a Scraper Studio collector via /dca/trigger; it needs
    # BRIGHT_DATA_COLLECTOR_ID and a collector that fetches the exact input URL.
    scrape_backend: Literal["unlocker", "collector"] = Field(
        default="unlocker", alias="ARK_SCRAPE_BACKEND"
    )
    brightdata_unlocker_zone: str = Field(
        default="cli_unlocker", alias="BRIGHT_DATA_UNLOCKER_ZONE"
    )
    data_dir: Path = Field(default=Path("data"), alias="ARK_DATA_DIR")
    # A collector's output schema is defined when it is built, so the field holding
    # page content is unknown ahead of time. Empty means "auto-detect"; set this when
    # your collector uses a name outside brightdata.CONTENT_FIELD_CANDIDATES.
    brightdata_content_field: str = Field(default="", alias="BRIGHT_DATA_CONTENT_FIELD")
    brightdata_base_url: str = Field(
        default="https://api.brightdata.com", alias="BRIGHT_DATA_BASE_URL"
    )
    poll_interval: float = Field(default=5.0, gt=0, alias="BRIGHT_DATA_POLL_INTERVAL")
    scrape_timeout: float = Field(default=600.0, gt=0, alias="BRIGHT_DATA_TIMEOUT")
    # Each URL is one billed Bright Data record, so alternates are capped by default.
    max_alternates: int = Field(default=2, ge=0, alias="ARK_MAX_ALTERNATES")

    # --- LangSmith tracing ----------------------------------------------------------
    # Off unless asked for: tracing uploads prompts and page excerpts to a third
    # party, which should never happen because a key happened to be in the shell.
    langsmith_tracing: bool = Field(default=False, alias="LANGSMITH_TRACING")
    langsmith_api_key: str = Field(default="", alias="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="ark-scrapper", alias="LANGSMITH_PROJECT")
    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com", alias="LANGSMITH_ENDPOINT"
    )

    # --- MongoDB (optional) ----------------------------------------------------------
    # Unset means filesystem-only: the pipeline behaves exactly as it did before.
    mongodb_uri: str = Field(default="", alias="MONGODB_URI")
    mongodb_db: str = Field(default="ark", alias="MONGODB_DB")
    mongodb_timeout_ms: int = Field(default=3000, gt=0, alias="MONGODB_TIMEOUT_MS")
    # Documentation goes stale — that is the premise of this project — so a cached
    # page is reused only while it is younger than this.
    doc_cache_ttl_days: int = Field(default=14, ge=0, alias="ARK_DOC_CACHE_TTL_DAYS")

    # --- plan generation ------------------------------------------------------------
    # Characters of documentation fed to one distill call. The full corpus does not
    # fit in a single context window, which is why plans are built map-reduce.
    # Default is sized for Groq's free tier, which rejects any single request over
    # 8000 tokens with a 413: ~12k chars is ~3k tokens, leaving room for the prompt,
    # the JSON schema and the response. Raise it on a paid tier for richer briefs.
    distill_budget: int = Field(default=12_000, gt=0, alias="ARK_DISTILL_BUDGET")
    plan_filename: str = Field(default="plan.md", alias="ARK_PLAN_FILENAME")

    @property
    def _credentials(self) -> dict[str, str]:
        return {
            "GROQ_API_KEY": self.groq_api_key,
            "TAVILY_API_KEY": self.tavily_api_key,
            "FIRECRAWL_API_KEY": self.firecrawl_api_key,
            "BRIGHT_DATA_API_TOKEN": self.brightdata_api_token,
            "BRIGHT_DATA_COLLECTOR_ID": self.brightdata_collector_id,
        }

    def require_credentials(self, *names: str) -> None:
        """Fail fast with an actionable message rather than a 401 from deep in the stack.

        Takes the names each command actually needs — `ark scrape` reads an existing
        artifact and talks only to Bright Data, so demanding LLM keys there would be
        a false barrier.
        """
        available = self._credentials
        unknown = [name for name in names if name not in available]
        if unknown:
            raise ValueError(f"Unknown credential(s): {', '.join(unknown)}")

        missing = [name for name in names if not available[name].strip()]
        if missing:
            raise MissingCredentials(
                f"Missing required environment variable(s): {', '.join(missing)}.\n"
                "Copy .env.example to .env and fill them in, or export them in your shell.\n"
                + "".join(f"  {CREDENTIAL_HELP[name]}\n" for name in missing).rstrip("\n")
            )

    @property
    def tavily_mcp_endpoint(self) -> str:
        """Remote Tavily MCP endpoint with the API key attached as a query parameter."""
        separator = "&" if "?" in self.tavily_mcp_url else "?"
        return f"{self.tavily_mcp_url}{separator}tavilyApiKey={self.tavily_api_key}"


def load_settings(**overrides: object) -> Settings:
    """Build Settings, applying any non-None CLI overrides on top of the environment."""
    clean = {key: value for key, value in overrides.items() if value is not None}
    return Settings(**clean)  # type: ignore[arg-type]
