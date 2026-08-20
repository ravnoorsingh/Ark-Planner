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

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

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


class LazyTools:
    """Opens the MCP session the first time a search actually needs it.

    Connecting eagerly means a search-provider outage kills runs that never search —
    every library pinned with `--doc-url`, or every page already in the cache. The
    session is still opened at most once and reused for the whole run.

    It is held open by a task of its own rather than inline, because the session's
    streams sit behind anyio cancel scopes, which must be exited by the task that
    entered them. The graph opens the session from inside a node's task while the
    run's cleanup happens in the caller's, so entering it inline fails the whole run
    with "Attempted to exit cancel scope in a different task". Owning a task keeps
    both ends in one place.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._lock = asyncio.Lock()
        self._owner: asyncio.Task | None = None
        self._ready: asyncio.Future[dict[str, BaseTool]] | None = None
        self._stop: asyncio.Event | None = None

    async def _serve(self) -> None:
        """Hold the session open until `aclose()` asks for it back."""
        ready, stop = self._ready, self._stop
        assert ready is not None and stop is not None
        try:
            async with search_tools(self._settings) as tools:
                ready.set_result(tools)
                await stop.wait()
        except BaseException as exc:
            # A failure to connect belongs to whoever asked for the tools, not to a
            # background task nobody is watching.
            if not ready.done():
                ready.set_exception(exc)
            raise

    async def get(self) -> dict[str, BaseTool]:
        async with self._lock:  # concurrent searches must not open two sessions
            if self._owner is None:
                self._ready = asyncio.get_running_loop().create_future()
                self._stop = asyncio.Event()
                self._owner = asyncio.create_task(self._serve())
            ready = self._ready
        assert ready is not None
        return await ready

    async def aclose(self) -> None:
        owner, stop = self._owner, self._stop
        self._owner = self._ready = self._stop = None
        if owner is None or stop is None:
            return
        stop.set()
        # Any failure here was already delivered to whoever awaited get().
        with suppress(Exception):
            await owner


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
