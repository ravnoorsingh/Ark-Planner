"""Verify the web-search MCP connection and print the tools it exposes.

Run this before spending LLM tokens — it isolates credential/endpoint problems,
and shows which provider is active.

    uv run python scripts/check_mcp.py
"""

from __future__ import annotations

import asyncio
import sys

from dotenv import load_dotenv

from ark.config import MissingCredentials, load_settings
from ark.mcp_client import search_arguments, search_tool_name, search_tools


async def main() -> int:
    load_dotenv()
    settings = load_settings()
    backend = settings.search_backend
    key = "FIRECRAWL_API_KEY" if backend == "firecrawl" else "TAVILY_API_KEY"
    try:
        settings.require_credentials(key)
    except MissingCredentials as exc:
        print(exc)
        return 1

    url = settings.firecrawl_mcp_url if backend == "firecrawl" else settings.tavily_mcp_url
    print(f"Backend:  {backend}")
    print(f"Endpoint: {url}\n")

    async with search_tools(settings) as tools:
        print(f"Connected. {len(tools)} tool(s) exposed:")
        for name in sorted(tools):
            summary = (tools[name].description or "").split("\n")[0][:100]
            print(f"  • {name} — {summary}")

        wanted = search_tool_name(settings)
        if wanted not in tools:
            print(f"\n!! Expected tool '{wanted}' is missing.")
            return 1

        print(f"\nSmoke-testing {wanted} …")
        raw = await tools[wanted].ainvoke(
            search_arguments(settings, "fastapi official documentation")
        )
        text = raw if isinstance(raw, str) else str(raw)
        print(text[:600])
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
