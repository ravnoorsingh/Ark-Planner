"""Publishing a finished plan to the public catalogue.

One place, because three callers need identical behaviour and the details are easy to
get subtly wrong: `ark docs --plan` and `ark plan` publish a new entry, `ark refine`
updates an existing one, the web UI does both, and `ark publish` back-fills an old
run. Divergence here shows up as a listing whose plan text no longer matches the file
on disk.

Two rules hold for every caller:

* **A run keeps its slug and its name.** Those are the entry's identity — the URL
  people share and the row they recognise. Re-naming on every revision would make a
  refinement look like a different plan, and would spend an LLM call to do it.
* **Installs belong to the entry, not the revision.** `MongoStore.publish` only sets
  the counter on insert, so revising a plan never resets what it has earned.
"""

from __future__ import annotations

import re
from typing import Any

from .config import Settings
from .naming import name_plan, slugify
from .tracing import annotate, traced

# The plan template numbers its phases "### Phase 3 — …". Counting `## ` instead would
# count the document's top-level sections, which is a different (and much smaller)
# number wearing the same label on the UI.
_PHASE = re.compile(r"^#{2,4}\s*Phase\b", re.MULTILINE)


def count_phases(markdown: str) -> int:
    return len(_PHASE.findall(markdown))


async def publish_plan(
    settings: Settings,
    store: Any,
    *,
    run_id: str,
    requirement: str,
    libraries: list[str],
    markdown: str,
    model: str = "",
    citations: int = 0,
    name: str = "",
) -> tuple[str, str]:
    """List (or re-list) a run's plan. Returns `(slug, name)`, or `("", "")`.

    Naming costs one LLM call, so it happens only for a run that has never been
    published — a revision reuses what the entry already has.
    """
    if store is None or not markdown.strip():
        return "", ""

    existing = await _entry_for_run(store, run_id)
    if existing is not None:
        slug = existing.get("_id", "")
        title = name.strip() or existing.get("name", "")
    else:
        title = name.strip() or await name_plan(settings, requirement, libraries)
        slug = await _free_slug(store, slugify(title), run_id)

    await store.publish(
        slug,
        {
            "name": title,
            "run_id": run_id,
            "requirement": requirement,
            "libraries": libraries,
            "markdown": markdown,
            "model": model or settings.model,
            "citations": citations,
            "phases": count_phases(markdown),
            "bytes": len(markdown.encode()),
        },
    )
    annotate(slug=slug, name=title, revised=existing is not None)
    return slug, title


@traced("catalog_lookup", run_type="retriever")
async def _entry_for_run(store: Any, run_id: str) -> dict | None:
    """The catalogue entry this run already owns, if any."""
    try:
        return await store.db["catalog"].find_one({"run_id": run_id})
    except Exception:  # noqa: BLE001 — a cache miss and a hiccup mean the same here
        return None


async def _free_slug(store: Any, base: str, run_id: str) -> str:
    """`base`, or `base-2`, `base-3`… — never somebody else's entry.

    Two runs of "build a REST API" produce the same name often enough that silently
    overwriting the first one would be a real way to lose a plan.
    """
    slug, n = base, 2
    while True:
        existing = await store.get_plan(slug)
        if existing is None or existing.get("run_id") == run_id:
            return slug
        slug, n = f"{base}-{n}", n + 1
