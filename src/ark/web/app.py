"""The HTTP API and the static site in front of it.

Two halves, deliberately separate:

* `/api/runs/*` is the private half — one browser tab driving one pipeline run,
  including the questions the run needs answered.
* `/api/plans/*` is the public half — the catalogue. Anyone can list, search and
  download, no run required and no key needed.

Only the second half needs a database. With Mongo unconfigured a run still produces
a plan on disk and returns it to the tab that asked; it simply is not catalogued.
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ..config import Settings, load_settings
from ..mongo import connect
from ..naming import slugify
from .runner import Jobs

STATIC = Path(__file__).parent / "static"

# How long a browser may sit on the events stream with nothing happening before we
# send a comment to keep proxies from closing it.
HEARTBEAT = 20.0


class RunRequest(BaseModel):
    requirement: str = Field(min_length=8, max_length=4000)
    ask_choices: bool = True
    ask_urls: bool = True
    review: bool = True
    use_cache: bool = True
    max_alternates: int = Field(default=1, ge=0, le=5)
    doc_urls: dict[str, list[str]] = Field(default_factory=dict)


class AnswerRequest(BaseModel):
    question_id: str
    answer: Any = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = load_settings()
    app.state.jobs = Jobs()
    # None when Mongo is unconfigured or down: the catalogue then reads as empty and
    # runs still work, which is the same degradation the CLI already has.
    app.state.store = await connect(app.state.settings)
    yield
    if app.state.store is not None:
        await app.state.store.close()


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="ARK Scrapper", lifespan=lifespan, docs_url="/api/docs")
    if settings is not None:  # tests inject their own
        app.state.settings = settings

    def store():
        return app.state.store

    # --- running a plan -------------------------------------------------------------

    @app.post("/api/runs")
    async def start_run(body: RunRequest) -> dict:
        jobs: Jobs = app.state.jobs
        jobs.prune()
        job = jobs.start(
            app.state.settings,
            body.requirement.strip(),
            {
                "ask_choices": body.ask_choices,
                "ask_urls": body.ask_urls,
                "review": body.review,
                "use_cache": body.use_cache,
                "max_alternates": body.max_alternates,
                "doc_urls": body.doc_urls,
                "store": store(),
            },
        )
        return {"job_id": job.id}

    @app.get("/api/runs/{job_id}/events")
    async def run_events(job_id: str, request: Request) -> StreamingResponse:
        job = app.state.jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "No such run")

        async def stream():
            # Replay nothing: the tab that started the run attaches immediately, and
            # a reconnecting tab gets the current status from /api/runs/{id}.
            while True:
                if await request.is_disconnected():
                    return
                try:
                    event = await asyncio.wait_for(job.events.get(), timeout=HEARTBEAT)
                except TimeoutError:
                    yield ": keep-alive\n\n"
                    continue
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("event") in {"done", "error"}:
                    return

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/api/runs/{job_id}")
    async def run_status(job_id: str) -> dict:
        job = app.state.jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "No such run")
        question = job.question
        return {
            "id": job.id,
            "status": job.status,
            "requirement": job.requirement,
            "error": job.error,
            "result": {key: value for key, value in job.result.items() if key != "markdown"},
            "question": (
                {"id": question.id, "kind": question.kind, **question.payload}
                if question
                else None
            ),
        }

    @app.post("/api/runs/{job_id}/answer")
    async def answer_run(job_id: str, body: AnswerRequest) -> dict:
        job = app.state.jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "No such run")
        if not job.answer(body.question_id, body.answer):
            # Usually a double-submit or a stale tab; not worth a 500.
            raise HTTPException(409, "That question is no longer open")
        return {"ok": True}

    @app.post("/api/runs/{job_id}/cancel")
    async def cancel_run(job_id: str) -> dict:
        return {"cancelled": app.state.jobs.cancel(job_id)}

    @app.get("/api/runs/{job_id}/plan.md", response_class=PlainTextResponse)
    async def run_plan(job_id: str) -> str:
        """The finished plan, for the tab that produced it — before it is catalogued."""
        job = app.state.jobs.get(job_id)
        if job is None or not job.result.get("markdown"):
            raise HTTPException(404, "No plan for that run")
        return job.result["markdown"]

    # --- the public catalogue --------------------------------------------------------

    @app.get("/api/plans")
    async def list_plans(q: str = "", sort: str = "trending", library: str = "", limit: int = 60):
        current = store()
        if current is None:
            return {"plans": [], "offline": True}
        rows = await current.search(q.strip(), sort=sort, library=library.strip(), limit=limit)
        trends = await current.recent_installs([row["_id"] for row in rows])
        return {
            "plans": [_card(row, trends.get(row["_id"], [])) for row in rows],
            "offline": False,
        }

    @app.get("/api/plans/{slug}")
    async def plan_detail(slug: str):
        current = store()
        if current is None:
            raise HTTPException(503, "The catalogue is offline")
        row = await current.get_plan(slug)
        if row is None:
            raise HTTPException(404, "No such plan")
        trend = (await current.recent_installs([slug], days=14)).get(slug, [])
        return {**_card(row, trend), "markdown": row.get("markdown", ""), "trend_days": 14}

    @app.get("/api/plans/{slug}/download")
    async def download_plan(slug: str):
        """Hand over the markdown and count it. Open to anyone, by design."""
        current = store()
        if current is None:
            raise HTTPException(503, "The catalogue is offline")
        row = await current.get_plan(slug)
        if row is None:
            raise HTTPException(404, "No such plan")
        installs = await current.record_install(slug)
        filename = f"{slugify(row.get('name', slug))}-plan.md"
        return PlainTextResponse(
            row.get("markdown", ""),
            media_type="text/markdown; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Install-Count": str(installs),
            },
        )

    @app.get("/api/libraries")
    async def libraries():
        current = store()
        return {"libraries": await current.libraries() if current is not None else []}

    @app.get("/api/stats")
    async def stats():
        current = store()
        if current is None:
            return {"offline": True}
        return {"offline": False, **await current.stats()}

    # --- the site --------------------------------------------------------------------

    @app.get("/plan/{slug}", include_in_schema=False)
    async def plan_page(slug: str) -> FileResponse:
        # Client-side routing would need a build step; a second static page does not.
        return FileResponse(STATIC / "plan.html")

    if STATIC.is_dir():
        app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")

    return app


def _card(row: dict[str, Any], trend: list[int]) -> dict[str, Any]:
    """The shape every listing renders, with the heavy markdown left out."""
    published = row.get("published_at")
    return {
        "slug": row.get("_id") or row.get("slug", ""),
        "name": row.get("name", "Untitled"),
        "requirement": row.get("requirement", ""),
        "libraries": row.get("libraries", []),
        "installs": int(row.get("installs", 0)),
        "recent": sum(trend),
        "trend": trend,
        "citations": int(row.get("citations", 0)),
        "phases": int(row.get("phases", 0)),
        "bytes": int(row.get("bytes", 0)),
        "model": row.get("model", ""),
        "published_at": (published or datetime.now(UTC)).isoformat(),
    }


app = create_app()
