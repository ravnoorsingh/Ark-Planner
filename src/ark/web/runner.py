"""Run the pipeline for a browser instead of a terminal.

The CLI asks its questions with `console.input()` — it blocks the run until someone
types. A web request cannot block like that, so each question becomes an event on a
stream and a Future the pipeline awaits; a later HTTP call resolves it. The pipeline
itself is untouched: it already accepts awaitable hooks, which is exactly the seam
this needs.

Jobs live in memory. They are in-flight work, not records — what deserves to outlive
the process is the plan, and that goes to Mongo and to disk like any other run.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..choices import apply_choices, describe, detect_choices
from ..config import Settings
from ..errors import explain
from ..graph import research_session
from ..mongo import MongoStore
from ..naming import name_plan, slugify
from ..render import save_artifact, to_payload
from ..review import Row, to_rows, to_sources
from ..state import DocResearchState, DocSource

# A browser tab can close mid-question. Without a deadline the pipeline would wait
# on that Future forever, holding an MCP session and a slot in the job table.
ANSWER_TIMEOUT = 900.0

STEP_LABELS = {
    "parse_libraries": "Identifying libraries",
    "search_docs": "Searching for documentation",
    "curate_links": "Choosing official sources",
    "scrape_docs": "Scraping documentation",
    "write_plan": "Writing the plan",
}


@dataclass
class Question:
    """Something the pipeline needs answered before it can continue."""

    id: str
    kind: str  # choices | doc_urls | review
    payload: dict[str, Any]
    future: asyncio.Future


@dataclass
class Job:
    id: str
    requirement: str
    status: str = "running"  # running | waiting | done | error
    steps: list[str] = field(default_factory=list)
    events: asyncio.Queue = field(default_factory=asyncio.Queue)
    question: Question | None = None
    result: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def emit(self, event: str, **data: Any) -> None:
        # Named `event`, not `kind`: questions carry their own `kind` field, and a
        # collision here is a TypeError at the one moment the run needs an answer.
        self.events.put_nowait({"event": event, **data})

    async def ask(self, kind: str, payload: dict[str, Any], default: Any) -> Any:
        """Put a question on the stream and wait for the browser to answer it."""
        question = Question(
            uuid.uuid4().hex[:8], kind, payload, asyncio.get_running_loop().create_future()
        )
        self.question = question
        self.status = "waiting"
        self.emit("question", id=question.id, kind=kind, **payload)
        try:
            return await asyncio.wait_for(question.future, timeout=ANSWER_TIMEOUT)
        except TimeoutError:
            # Nobody is coming back. Carry on with what the pipeline would have done
            # unattended rather than discarding a half-finished run.
            self.emit("note", text="No answer received — continuing with defaults.")
            return default
        finally:
            self.question = None
            self.status = "running"

    def answer(self, question_id: str, value: Any) -> bool:
        question = self.question
        if question is None or question.id != question_id or question.future.done():
            return False
        question.future.set_result(value)
        return True


class Jobs:
    """The in-memory job table."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._tasks: dict[str, asyncio.Task] = {}

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def start(self, settings: Settings, requirement: str, options: dict[str, Any]) -> Job:
        job = Job(id=uuid.uuid4().hex[:12], requirement=requirement)
        self._jobs[job.id] = job
        self._tasks[job.id] = asyncio.create_task(_run(job, settings, options))
        return job

    def cancel(self, job_id: str) -> bool:
        task = self._tasks.get(job_id)
        if task is None or task.done():
            return False
        task.cancel()
        return True

    def prune(self, keep: int = 200) -> None:
        """Drop the oldest finished jobs; a long-lived server must not grow forever."""
        finished = sorted(
            (job for job in self._jobs.values() if job.status in {"done", "error"}),
            key=lambda job: job.started_at,
        )
        for job in finished[: max(0, len(finished) - keep)]:
            self._jobs.pop(job.id, None)
            self._tasks.pop(job.id, None)


async def _resolve_choices(job: Job, settings: Settings, requirement: str) -> tuple[str, list[str]]:
    """Offer the open capability slots to the browser, then fold the answers in."""
    choices = await detect_choices(settings, requirement)
    if not choices:
        return requirement, []

    payload = {
        "choices": [
            {
                "slot": choice.slot,
                "reason": choice.reason,
                "recommended": choice.recommended,
                "options": [
                    {"name": option.name, "note": option.note} for option in choice.options
                ],
            }
            for choice in choices
        ]
    }
    defaults = {choice.slot: choice.default() for choice in choices}
    answers = await job.ask("choices", payload, defaults) or defaults
    decisions = {
        choice.slot: (answers.get(choice.slot) or choice.default()).strip() for choice in choices
    }
    resolved = [
        describe(choice, decisions[choice.slot]) for choice in choices if decisions[choice.slot]
    ]
    return apply_choices(requirement, decisions), resolved


def _doc_url_hook(job: Job, pinned: dict[str, list[str]]):
    """Let the browser pin documentation URLs once the libraries are known."""

    async def ask(libraries, already: dict[str, list[str]]) -> dict[str, list[str]]:
        pending = [lib for lib in libraries if lib.name not in already]
        if not pending:
            return {}
        payload = {
            "libraries": [
                {"name": lib.name, "reason": lib.reason, "ecosystem": lib.ecosystem}
                for lib in pending
            ]
        }
        answer = await job.ask("doc_urls", payload, {})
        picked = {**pinned, **(answer or {})}
        return {name: urls for name, urls in picked.items() if urls}

    return ask


def _review_hook(job: Job, max_alternates: int):
    """Show every URL that would be scraped and let the browser edit the list."""

    async def review(sources: list[DocSource]) -> list[DocSource] | None:
        rows = to_rows(sources, max_alternates)
        payload = {
            "rows": [
                {"library": row.library, "url": row.url, "primary": row.primary} for row in rows
            ]
        }
        answer = await job.ask("review", payload, None)
        if answer is None:  # timed out — scrape the list as curated
            return to_sources(rows, sources)
        if answer.get("cancel"):
            return None
        edited = [
            Row(row["library"], row["url"], bool(row.get("primary")))
            for row in answer.get("rows", [])
            if row.get("url")
        ]
        return to_sources(edited, sources)

    return review


async def _run(job: Job, settings: Settings, options: dict[str, Any]) -> None:
    """Drive one requirement all the way to a published plan."""
    try:
        job.emit("status", status="running", step="Reading the requirement")
        requirement = job.requirement
        resolved: list[str] = []
        if options.get("ask_choices", True):
            requirement, resolved = await _resolve_choices(job, settings, requirement)
            if resolved:
                job.emit("resolved", choices=resolved, requirement=requirement)

        max_alternates = int(options.get("max_alternates", settings.max_alternates))
        pinned: dict[str, list[str]] = options.get("doc_urls") or {}

        store = options.get("store")
        async with research_session(
            settings,
            scrape=True,
            plan=True,
            max_alternates=max_alternates,
            doc_urls=pinned,
            ask_doc_urls=_doc_url_hook(job, pinned) if options.get("ask_urls", True) else None,
            review_urls=_review_hook(job, max_alternates) if options.get("review", True) else None,
            store=store,
            use_cache=options.get("use_cache", True),
        ) as run:
            state: DocResearchState = await run(
                requirement,
                on_step=lambda node: job.emit("step", node=node, label=STEP_LABELS.get(node, node)),
            )

        await _publish(job, settings, state, store, options)
    except asyncio.CancelledError:
        job.status, job.error = "error", "Cancelled."
        job.emit("error", message="Cancelled.")
        raise
    except Exception as exc:  # noqa: BLE001 — the browser gets the message, not a 500
        job.status = "error"
        # Flattened: the browser must see the 503, not the TaskGroup wrapper.
        job.error = explain(exc)
        job.emit("error", message=job.error)


async def _publish(
    job: Job,
    settings: Settings,
    state: DocResearchState,
    store: MongoStore | None,
    options: dict[str, Any],
) -> None:
    """Write the artifact, name the plan, and list it in the catalogue."""
    markdown = state.get("plan_markdown", "")
    libraries = [library.name for library in state.get("libraries", [])]
    payload = to_payload(state, settings.model)

    artifact = save_artifact(state, settings.model, Path(settings.output_dir))
    run_id = artifact.parent.name
    plan_path = artifact.parent / "plan.md"
    if markdown:
        plan_path.write_text(markdown, encoding="utf-8")

    if not markdown:
        job.status = "error"
        job.error = "The run produced no plan."
        job.emit("error", message=job.error, errors=state.get("errors", []))
        return

    job.emit("step", node="name_plan", label="Naming the plan")
    name = await name_plan(settings, job.requirement, libraries)

    slug = slugify(name)
    if store is not None:
        await store.save_run(run_id, payload)
        await store.save_plan(run_id, markdown, settings.model)
        # A name collision must not overwrite somebody else's entry, so the slug
        # gains a suffix rather than the publish silently replacing a plan.
        base, n = slug, 2
        while True:
            existing = await store.get_plan(slug)
            if existing is None or existing.get("run_id") == run_id:
                break
            slug, n = f"{base}-{n}", n + 1
        await store.publish(
            slug,
            {
                "name": name,
                "run_id": run_id,
                "requirement": job.requirement,
                "resolved_requirement": state.get("requirement", ""),
                "libraries": libraries,
                "markdown": markdown,
                "model": settings.model,
                "citations": len(state.get("documents", [])),
                "phases": markdown.count("\n## "),
                "bytes": len(markdown.encode()),
            },
        )

    job.status = "done"
    job.result = {
        "slug": slug,
        "name": name,
        "run_id": run_id,
        "libraries": libraries,
        "markdown": markdown,
        "path": str(plan_path),
        "errors": state.get("errors", []),
        "published": store is not None,
    }
    job.emit("done", **{key: value for key, value in job.result.items() if key != "markdown"})
