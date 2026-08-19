"""Resolve generic capabilities in a requirement into specific libraries.

A requirement often names a *capability* rather than a package — "a vector
database", "an ORM", "a task queue". Left alone, `parse_libraries` silently picks
one, and the user gets a plan grounded in docs for a library they never chose.

So ambiguity is surfaced instead: detect the open slots, offer real candidates, and
let the user pick one or type their own. The chosen names are folded back into the
requirement, so everything downstream — search, curation, scraping, citations —
works on a requirement that names its stack explicitly.

Nothing here is vector-database specific; the model decides what counts as an open
slot, so it works equally for "a web framework" or "a background job runner".
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .config import Settings
from .llm import build_llm, structured
from .prompts import DETECT_CHOICES_SYSTEM
from .tracing import annotate, traced


class LibraryOption(BaseModel):
    name: str = Field(description="Installable package name, e.g. 'qdrant-client'")
    note: str = Field(default="", description="One short line on when to prefer it")


class LibraryChoice(BaseModel):
    """One unresolved capability in the requirement."""

    slot: str = Field(description="The capability, e.g. 'vector database'")
    reason: str = Field(default="", description="What the project needs it for")
    options: list[LibraryOption] = Field(default_factory=list)
    recommended: str = Field(default="", description="Name of the sensible default")

    def default(self) -> str:
        """The option to use when nobody is around to ask."""
        if self.recommended:
            return self.recommended
        return self.options[0].name if self.options else ""


class ChoiceSet(BaseModel):
    choices: list[LibraryChoice] = Field(default_factory=list)


@traced("detect_choices", run_type="chain")
async def detect_choices(settings: Settings, requirement: str) -> list[LibraryChoice]:
    """Find capabilities the requirement leaves open to interpretation."""
    llm = build_llm(settings, json_mode=True)
    result = await structured(
        llm, ChoiceSet, DETECT_CHOICES_SYSTEM, f"Project requirement:\n{requirement}"
    )

    choices: list[LibraryChoice] = []
    seen: set[str] = set()
    for choice in result.choices:
        slot = choice.slot.strip().lower()
        # A slot with nothing to choose between is not a choice.
        if not slot or slot in seen or len(choice.options) < 2:
            continue
        seen.add(slot)
        choices.append(choice)
    annotate(
        proposed=len(result.choices),
        open_slots={choice.slot: choice.default() for choice in choices},
    )
    return choices


@traced("apply_choices", run_type="tool")
def apply_choices(requirement: str, decisions: dict[str, str]) -> str:
    """Fold the picks back into the requirement as plain, explicit sentences.

    Rewriting the requirement rather than passing a side-channel keeps one source of
    truth: the artifact, the plan's goal line and the store's folder names all show
    the stack that was actually researched.
    """
    picked = [(slot, name.strip()) for slot, name in decisions.items() if name and name.strip()]
    if not picked:
        return requirement

    sentences = " ".join(f"Use {name} for the {slot}." for slot, name in picked)
    return f"{requirement.rstrip().rstrip('.')}. {sentences}"


def describe(choice: LibraryChoice, selection: str) -> str:
    """One-line summary of a resolved slot, for logs and non-interactive runs."""
    return f"{choice.slot} → {selection}"
