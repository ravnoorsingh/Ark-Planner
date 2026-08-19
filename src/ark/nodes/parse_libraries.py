"""Node 1 — turn a free-form requirement into a list of libraries."""

from __future__ import annotations

from langchain_core.runnables import RunnableConfig

from ..config import Settings
from ..llm import build_llm, structured
from ..prompts import PARSE_LIBRARIES_SYSTEM
from ..state import DocResearchState, LibraryList
from ..tracing import annotate


async def parse_libraries(state: DocResearchState, config: RunnableConfig) -> dict:
    settings: Settings = config["configurable"]["settings"]
    llm = build_llm(settings, json_mode=True)

    result = await structured(
        llm,
        LibraryList,
        PARSE_LIBRARIES_SYSTEM.format(max_libraries=settings.max_libraries),
        f"Project requirement:\n{state['requirement']}",
    )

    # Deduplicate on lowercased name, preserving the model's ordering, then cap.
    seen: set[str] = set()
    libraries = []
    for library in result.libraries:
        key = library.name.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        libraries.append(library)

    libraries = libraries[: settings.max_libraries]
    annotate(
        proposed=len(result.libraries),
        kept=len(libraries),
        names=[library.name for library in libraries],
    )
    errors = [] if libraries else ["No libraries could be identified from the requirement."]
    return {"libraries": libraries, "errors": errors}
