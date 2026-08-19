"""Node 5 — turn the scraped docs into a citation-backed plan.md.

Map-reduce, because the corpus exceeds one context window: distill each library
concurrently, then synthesize a single plan from the briefs.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import UTC, datetime

from langchain_core.runnables import RunnableConfig

from ..config import Settings
from ..llm import build_llm, explain_quota, is_too_large, structured
from ..plan import build_citations, load_corpus, render_plan
from ..prompts import DISTILL_SYSTEM, REFINE_PLAN_SYSTEM, SYNTHESIZE_SYSTEM
from ..state import Citation, DocResearchState, LibraryBrief, PlanDraft
from ..tracing import annotate, traced


@traced("distill_library", run_type="chain")
async def _distill(
    settings: Settings,
    library: str,
    citations: list[Citation],
    limiter: asyncio.Semaphore,
) -> LibraryBrief:
    """Condense one library's docs, shrinking the excerpt if the tier rejects it.

    Groq's free tier caps a single request at 8000 tokens and answers an oversized
    one with 413. Waiting cannot fix that, so on each rejection we halve how much
    documentation is sent and try again — a shorter brief beats no brief.
    """
    llm = build_llm(settings, json_mode=True)
    keys = ", ".join(f"[^{c.key}]" for c in citations)
    budget = settings.distill_budget

    for attempt in range(3):
        corpus = load_corpus(citations, budget)
        if not corpus:
            return LibraryBrief(library=library)
        user = (
            f"Library: {library}\n"
            f"Available citation keys: {keys}\n\n"
            f"Documentation:\n\n{corpus}"
        )
        annotate(**{f"attempt_{attempt + 1}_budget_chars": budget, "corpus_chars": len(corpus)})
        try:
            async with limiter:
                brief = await structured(llm, LibraryBrief, DISTILL_SYSTEM, user)
            break
        except Exception as exc:
            if not is_too_large(exc) or attempt == 2:
                raise
            annotate(**{f"attempt_{attempt + 1}_rejected": "413 request too large"})
            budget //= 2
    else:  # pragma: no cover - the loop always breaks or raises
        return LibraryBrief(library=library)

    # The library name and citation keys are ours to control, not the model's.
    brief.library = library
    valid = {c.key for c in citations}
    brief.citation_keys = [k for k in brief.citation_keys if k in valid] or sorted(valid)
    annotate(api_items=len(brief.api), gotchas=len(brief.gotchas), version=brief.version)
    return brief


@traced("brief_digest", run_type="tool")
def _brief_digest(brief: LibraryBrief) -> str:
    """Compact text form of a brief, for the synthesis prompt."""
    parts = [f"## {brief.library}  (cite as {' '.join(f'[^{k}]' for k in brief.citation_keys)})"]
    if brief.version:
        parts.append(f"Version stated in docs: {brief.version}")
    if brief.install:
        parts.append(f"Install: {brief.install}")
    if brief.summary:
        parts.append(brief.summary)
    for item in brief.api:
        line = f"- {item.signature or item.name}"
        if item.summary:
            line += f" — {item.summary}"
        parts.append(line)
        if item.example:
            parts.append(f"  ```\n  {item.example.strip()}\n  ```")
    for gotcha in brief.gotchas:
        parts.append(f"- GOTCHA: {gotcha}")
    return "\n".join(parts)


@traced("build_plan", run_type="chain")
async def build_plan(
    settings: Settings,
    requirement: str,
    documents: list,
    *,
    on_step: Callable[[str], None] | None = None,
) -> tuple[str, list[LibraryBrief], list[str]]:
    """Return (plan_markdown, briefs, draft, errors)."""
    citations = build_citations(documents)
    if not citations:
        return "", [], PlanDraft(), [
            "No stored documents to build a plan from — run a scrape first."
        ]

    by_library: dict[str, list[Citation]] = {}
    for citation in citations:
        by_library.setdefault(citation.library, []).append(citation)

    # --- map ----------------------------------------------------------------------
    if on_step:
        on_step(f"Distilling {len(by_library)} librar(y/ies)")
    # TPM is a per-minute budget shared across requests, so distills go one at a
    # time; firing them concurrently just trades 413s for 429s.
    limiter = asyncio.Semaphore(1)
    outcomes = await asyncio.gather(
        *(_distill(settings, lib, cits, limiter) for lib, cits in by_library.items()),
        return_exceptions=True,
    )

    briefs: list[LibraryBrief] = []
    errors: list[str] = []
    for library, outcome in zip(by_library, outcomes):
        if isinstance(outcome, BaseException):
            # One library failing shouldn't cost us the plan; the rest still ground it.
            errors.append(f"{library}: could not distill docs — {explain_quota(outcome)}")
            continue
        briefs.append(outcome)

    annotate(distilled=len(briefs), distill_failures=len(errors))
    if not briefs:
        return "", [], PlanDraft(), errors + [
            "Every library failed to distill; no plan written."
        ]

    # --- reduce -------------------------------------------------------------------
    if on_step:
        on_step("Synthesizing plan")
    digest = "\n\n".join(_brief_digest(b) for b in briefs)
    user = (
        f"Project requirement:\n{requirement}\n\n"
        f"Library briefs, drawn from freshly scraped official documentation:\n\n{digest}"
    )
    llm = build_llm(settings, json_mode=True)
    try:
        draft = await structured(llm, PlanDraft, SYNTHESIZE_SYSTEM, user)
    except Exception as exc:
        errors.append(f"Plan synthesis failed: {explain_quota(exc)}")
        annotate(synthesis_failed=explain_quota(exc))
        draft = PlanDraft(title=f"Implementation plan: {requirement[:60]}")

    markdown = render_plan(
        requirement,
        draft,
        briefs,
        citations,
        model=settings.model,
        generated_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
    annotate(plan_chars=len(markdown), phases=len(draft.phases), citations=len(citations))
    return markdown, briefs, draft, errors


@traced("refine_plan", run_type="chain")
async def refine_plan(
    settings: Settings,
    requirement: str,
    briefs: list[LibraryBrief],
    citations: list,
    previous: PlanDraft,
    instruction: str,
) -> tuple[str, PlanDraft]:
    """Revise an existing plan from the same briefs — one LLM call, no re-distilling.

    Synthesis is re-run rather than letting the model edit the markdown directly:
    the citations and section structure are assembled in code, so regenerating the
    draft keeps every `[^key]` verifiable instead of drifting into prose the model
    has rewritten by hand.
    """
    digest = "\n\n".join(_brief_digest(brief) for brief in briefs)
    user = (
        f"Project requirement:\n{requirement}\n\n"
        f"PREVIOUS PLAN (JSON):\n{previous.model_dump_json(indent=2)}\n\n"
        f"USER INSTRUCTION:\n{instruction}\n\n"
        f"Library briefs (the only source of fact):\n\n{digest}"
    )
    llm = build_llm(settings, json_mode=True)
    draft = await structured(llm, PlanDraft, REFINE_PLAN_SYSTEM, user)
    annotate(instruction=instruction[:200], phases=len(draft.phases))

    markdown = render_plan(
        requirement,
        draft,
        briefs,
        citations,
        model=settings.model,
        generated_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
    return markdown, draft


async def write_plan(state: DocResearchState, config: RunnableConfig) -> dict:
    settings: Settings = config["configurable"]["settings"]
    documents = state.get("documents", [])
    if not documents:
        return {"plan_markdown": "", "errors": ["No documents scraped; skipping plan."]}

    markdown, briefs, draft, errors = await build_plan(
        settings, state.get("requirement", ""), documents
    )
    return {
        "plan_markdown": markdown,
        "briefs": briefs,
        "plan_draft": draft,
        "errors": errors,
    }
