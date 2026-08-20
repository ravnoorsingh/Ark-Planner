"""Name a plan in two or three words.

The catalogue lists plans the way a package registry lists packages, so each one
needs a handle a person can scan, recognise and search for. A requirement sentence
is far too long for that, and its first few words are usually "Build a production
…" — identical across half the catalogue.

The name is generated once, when the plan is first published, and then kept: a
catalogue entry whose name changes under a stable URL is a different thing wearing
the same address.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, Field

from .config import Settings
from .llm import build_llm, structured
from .prompts import NAME_PLAN_SYSTEM
from .tracing import annotate, traced

# Words that say nothing about what a plan does; the model is told to avoid them and
# this strips them when it does so anyway.
FILLER = frozenset({"plan", "guide", "project", "system", "solution", "implementation", "app"})


class PlanName(BaseModel):
    name: str = Field(description="Two or three words, Title Case")


def _tidy(raw: str) -> str:
    """Trim a model's answer down to two or three real words."""
    words = [word for word in re.split(r"[^A-Za-z0-9+#.]+", raw) if word]
    # Only drop filler while something specific survives — "Build Plan" reduced to
    # "Build" is worse than leaving it, and an empty name is worse still.
    trimmed = [word for word in words if word.lower() not in FILLER]
    if len(trimmed) >= 2:
        words = trimmed
    words = words[:3]
    return " ".join(word if word[:1].isupper() else word.capitalize() for word in words)


def fallback_name(requirement: str, libraries: list[str]) -> str:
    """A usable name without an LLM call, for when the model is unavailable.

    Naming must never be what fails a run: the plan itself is the expensive part and
    it is already written by the time we get here.
    """
    words = [
        word
        for word in re.split(r"[^A-Za-z0-9+#.]+", requirement)
        if len(word) > 2 and word.lower() not in FILLER and word.lower() not in _STOP
    ]
    if len(words) < 2 and libraries:
        words = [libraries[0], *words]
    return _tidy(" ".join(words[:3])) or "Untitled Plan"


_STOP = frozenset(
    ["build", "a", "an", "the", "that", "with", "and", "for", "from", "into", "using", "use", "make", "create", "service", "production", "its", "it", "of", "to", "on", "in"]
)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "plan"


@traced("name_plan", run_type="chain")
async def name_plan(settings: Settings, requirement: str, libraries: list[str]) -> str:
    """Ask the model for a short catalogue name, falling back to one derived locally."""
    llm = build_llm(settings, json_mode=True)
    user = f"Requirement:\n{requirement}\n\nLibraries: {', '.join(libraries) or 'none'}"
    try:
        result = await structured(llm, PlanName, NAME_PLAN_SYSTEM, user)
        name = _tidy(result.name)
    except Exception as exc:  # noqa: BLE001 — naming must not fail a finished plan
        annotate(naming_failed=str(exc)[:200])
        name = ""
    if len(name.split()) < 2:
        name = fallback_name(requirement, libraries)
    annotate(name=name)
    return name
