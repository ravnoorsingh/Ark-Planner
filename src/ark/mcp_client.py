"""Connection to the web-search MCP server.

Two providers are supported and selected with `ARK_SEARCH_BACKEND`:

    firecrawl  https://mcp.firecrawl.dev/v2/mcp   Authorization: Bearer <key>
    tavily     https://mcp.tavily.com/mcp/        ?tavilyApiKey=<key>

Both speak streamable HTTP, but they differ in how they authenticate, what their
search tool is called, and what arguments it takes — so those three things are
declared per provider here rather than being spread through the search node.

Note on naming: Tavily's published docs write its tools hyphenated
(`tavily-search`) while the live server exposes them underscored. `require_tool`
matches on a normalized name so either convention resolves.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from .config import Settings
from .tracing import annotate, traced

SEARCH_TOOLS = {
    "firecrawl": "firecrawl_search",
    "tavily": "tavily_search",
}

EXTRACT_TOOLS = {
    "firecrawl": "firecrawl_scrape",
    "tavily": "tavily_extract",
}


class ToolUnavailable(RuntimeError):
    """Raised when the MCP server does not expose an expected tool."""


def search_tool_name(settings: Settings) -> str:
    return SEARCH_TOOLS[settings.search_backend]


def search_arguments(settings: Settings, query: str) -> dict:
    """Provider-specific arguments for one search call.

    Firecrawl takes `limit`; Tavily takes `max_results` and a `search_depth`.
    Sending the wrong one is silently ignored by the server, which shows up much
    later as "only 1 result came back", so keep them declared side by side.
    """
    if settings.search_backend == "firecrawl":
        return {"query": query, "limit": settings.search_max_results}
    return {
        "query": query,
        "max_results": settings.search_max_results,
        "search_depth": "advanced",
    }


def _connection(settings: Settings) -> dict:
    if settings.search_backend == "firecrawl":
        # The key goes in a header, not the URL: Firecrawl's docs are explicit that
        # it should never be embedded in the MCP URL.
        return {
            "transport": "streamable_http",
            "url": settings.firecrawl_mcp_url,
            "headers": {"Authorization": f"Bearer {settings.firecrawl_api_key}"},
        }
    return {"transport": "streamable_http", "url": settings.tavily_mcp_endpoint}


@traced("load_mcp_tools", run_type="tool", tags=["mcp"])
async def _load_tools(session, backend: str) -> dict[str, BaseTool]:
    """Discover the server's tools.

    Split out of `search_tools` so it can be traced: `traceable` wraps functions,
    and an `@asynccontextmanager` that yields for the whole run would produce a
    span spanning the session rather than the handshake it is meant to time.
    """
    tools = await load_mcp_tools(session)
    annotate(backend=backend, tools=sorted(tool.name for tool in tools))
    return {tool.name: tool for tool in tools}


@asynccontextmanager
async def search_tools(settings: Settings) -> AsyncGenerator[dict[str, BaseTool]]:
    """Open one MCP session for the whole run and yield its tools keyed by name.

    Holding a single session means the per-library searches reuse one connection
    instead of reconnecting on every tool call.
    """
    name = settings.search_backend
    client = MultiServerMCPClient({name: _connection(settings)})
    async with client.session(name) as session:
        yield await _load_tools(session, name)


def _normalize(name: str) -> str:
    return name.replace("-", "_").lower()


def require_tool(tools: dict[str, BaseTool], name: str) -> BaseTool:
    """Look a tool up by name, tolerating hyphen/underscore drift in tool naming."""
    if name in tools:
        return tools[name]
    wanted = _normalize(name)
    for candidate, tool in tools.items():
        if _normalize(candidate) == wanted:
            return tool
    raise ToolUnavailable(
        f"The search MCP server did not expose a '{name}' tool. Available: {sorted(tools)}"
    )
