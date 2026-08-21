"""Revise a plan that is already in the store.

`ark refine` works from the artifact file on disk. The web UI has no file — it has a
catalogue slug — so this reads the same fields back out of the `runs` payload and runs
the identical synthesis call.

What makes this possible at all is that `to_payload` keeps the library briefs and the
previous draft: refinement re-runs synthesis from those, so nothing is re-searched,
re-scraped or re-distilled, and every citation stays verifiable because the markdown is
still assembled in code rather than edited by the model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .catalog import publish_plan
from .config import Settings
from .nodes.write_plan import refine_plan
from .plan import build_citations
from .state import LibraryBrief, PlanDraft, ScrapedDoc
from .tracing import annotate, traced


class NotRevisable(RuntimeError):
    """The stored run cannot be refined, with a reason worth showing a person."""


@traced("revise_stored_plan", run_type="chain")
async def revise_stored_plan(
    settings: Settings, store: Any, slug: str, instruction: str
) -> dict[str, Any]:
    """Apply `instruction` to the catalogued plan `slug`. One LLM call.

    Returns the new markdown, the revision number and the refreshed entry.
    """
    instruction = instruction.strip()
    if not instruction:
        raise NotRevisable("Say what to change.")
    if store is None:
        raise NotRevisable("The catalogue is offline.")

    entry = await store.get_plan(slug)
    if entry is None:
        raise NotRevisable("No such plan.")

    run_id = entry.get("run_id", "")
    payload = await store.db["runs"].find_one({"_id": run_id})
    if payload is None:
        raise NotRevisable("The run behind this plan is no longer stored.")

    try:
        briefs = [LibraryBrief.model_validate(b) for b in payload.get("briefs", [])]
        documents = [ScrapedDoc.model_validate(d) for d in payload.get("documents", [])]
        draft = PlanDraft.model_validate(payload.get("plan_draft") or {})
    except (ValidationError, ValueError) as exc:
        raise NotRevisable(f"That run's artifact is not readable: {exc}") from exc

    if not briefs:
        # Plans from before briefs were stored can be read but not revised: without
        # them the model would be rewriting from memory, not from the documentation.
        raise NotRevisable(
            "This plan predates stored briefs, so it cannot be refined. "
            "Generate it again to make it revisable."
        )

    requirement = payload.get("requirement", "")
    markdown, draft = await refine_plan(
        settings, requirement, briefs, build_citations(documents), draft, instruction
    )

    # Keep the stored draft in step so the *next* refinement builds on this one rather
    # than silently re-applying to the original.
    payload["plan_draft"] = draft.model_dump()
    await store.save_run(run_id, {k: v for k, v in payload.items() if k != "_id"})
    revision = await store.save_plan(run_id, markdown, settings.model, instruction)
    await publish_plan(
        settings,
        store,
        run_id=run_id,
        requirement=requirement,
        libraries=entry.get("libraries", []),
        markdown=markdown,
        model=settings.model,
        citations=entry.get("citations", 0),
    )
    _mirror_to_disk(settings, run_id, payload, markdown)

    annotate(slug=slug, revision=revision, instruction=instruction[:200])
    return {
        "slug": slug,
        "revision": revision,
        "markdown": markdown,
        "entry": await store.get_plan(slug),
    }


def _mirror_to_disk(settings: Settings, run_id: str, payload: dict, markdown: str) -> None:
    """Update the run directory too, when it is still there.

    A plan revised in the browser and a `plan.md` on disk showing the previous version
    is the kind of divergence that wastes an afternoon. Best-effort: the run may have
    been generated on another machine, and the store is the record either way.
    """
    run_dir = Path(settings.output_dir) / run_id
    if not run_dir.is_dir():
        return
    try:
        (run_dir / settings.plan_filename).write_text(markdown, encoding="utf-8")
        artifact = run_dir / "doc_sources.json"
        if artifact.exists():
            stored = json.loads(artifact.read_text(encoding="utf-8"))
            stored["plan_draft"] = payload["plan_draft"]
            artifact.write_text(json.dumps(stored, indent=2), encoding="utf-8")
    except OSError as exc:
        annotate(disk_mirror_failed=str(exc)[:200])
