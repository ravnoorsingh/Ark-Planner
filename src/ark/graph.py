"""StateGraph wiring.

    START -> parse_libraries -> search_docs -> curate_links
          [-> scrape_docs [-> write_plan]] -> END

`scrape_docs` is opt-in because it spends Bright Data credits and takes minutes.
`write_plan` reads the pages that scrape stored, so it can only follow one.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager

from langgraph.graph import END, START, StateGraph

from .config import Settings
from .mcp_client import LazyTools
from .nodes import curate_links, parse_libraries, scrape_docs, search_docs, write_plan
from .state import DocResearchState
from .tracing import traced

NODE_LABELS = {
    "parse_libraries": "Identifying libraries",
    "search_docs": "Searching docs via web-search MCP",
    "curate_links": "Curating official links",
    "scrape_docs": "Scraping docs via Bright Data",
    "write_plan": "Writing the plan from the scraped docs",
}


@traced("build_graph", run_type="tool")
def build_graph(*, scrape: bool = False, plan: bool = False):
    graph = StateGraph(DocResearchState)
    graph.add_node("parse_libraries", parse_libraries)
    graph.add_node("search_docs", search_docs)
    graph.add_node("curate_links", curate_links)

    graph.add_edge(START, "parse_libraries")
    graph.add_edge("parse_libraries", "search_docs")
    graph.add_edge("search_docs", "curate_links")

    if not scrape:
        graph.add_edge("curate_links", END)
        return graph.compile()

    graph.add_node("scrape_docs", scrape_docs)
    graph.add_edge("curate_links", "scrape_docs")

    # Planning reads the stored documents, so it can only follow a scrape.
    if plan:
        graph.add_node("write_plan", write_plan)
        graph.add_edge("scrape_docs", "write_plan")
        graph.add_edge("write_plan", END)
    else:
        graph.add_edge("scrape_docs", END)
    return graph.compile()


@asynccontextmanager
async def research_session(
    settings: Settings,
    *,
    scrape: bool = False,
    plan: bool = False,
    max_alternates: int | None = None,
    doc_urls: dict[str, str] | None = None,
    ask_doc_urls: Callable | None = None,
    review_urls: Callable | None = None,
    store: object | None = None,
    use_cache: bool = True,
) -> AsyncGenerator[Callable]:
    """Yield a `run(requirement, on_step=None)` coroutine.

    The search session is opened lazily, on the first library that actually needs a
    search, and then reused for the rest of the run — so a REPL still connects once,
    and a run whose libraries are all pinned never connects at all.
    """
    app = build_graph(scrape=scrape, plan=plan)

    tools = LazyTools(settings)
    try:

        async def run(requirement: str, on_step: Callable[[str], None] | None = None):
            # run_name/tags/metadata are LangChain's own tracing controls: they name
            # the graph's span and label it, so a trace shows "docs-research
            # (scrape=True)" rather than a bare "LangGraph". They are inert when
            # tracing is off. Note that only str/int/float/bool entries of
            # `configurable` reach the trace as metadata, so `settings` — which
            # holds every API key — is never uploaded by this path.
            config = {
                "run_name": "docs-research",
                "tags": ["ark", f"search:{settings.search_backend}"],
                "metadata": {
                    "model": settings.model,
                    "search_backend": settings.search_backend,
                    "scrape_backend": settings.scrape_backend if scrape else "",
                    "scrape": scrape,
                    "plan": plan,
                },
                "configurable": {
                    "settings": settings,
                    "tools": tools,
                    "max_alternates": max_alternates,
                    # URLs the user pinned up front, plus a hook the search node
                    # calls once the libraries are known so they can pin more.
                    "doc_urls": dict(doc_urls or {}),
                    "ask_doc_urls": ask_doc_urls,
                    "review_urls": review_urls,
                    "store": store,
                    "use_cache": use_cache,
                },
            }
            state: DocResearchState = {
                "requirement": requirement,
                "libraries": [],
                "hits": {},
                "provided": {},
                "doc_sources": [],
                "documents": [],
                "briefs": [],
                "plan_markdown": "",
                "errors": [],
            }
            # "updates" drives the progress display; "values" carries the reduced
            # state, so accumulators like `errors` are not clobbered.
            async for mode, chunk in app.astream(
                state, config=config, stream_mode=["updates", "values"]
            ):
                if mode == "updates":
                    if on_step:
                        for node in chunk:
                            on_step(node)
                elif mode == "values":
                    state = chunk
            return state

        yield run
    finally:
        await tools.aclose()
