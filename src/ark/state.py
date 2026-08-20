"""Graph state and the data contract downstream pipeline phases consume.

`DocSource` is deliberately the shape the future Bright Data scrape phase will
iterate over — it is the seam between this phase and the next.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, Field, field_validator

DocKind = Literal["official_docs", "api_reference", "github", "other"]


class Library(BaseModel):
    name: str = Field(description="Canonical package name, e.g. 'fastapi'")
    ecosystem: str = Field(default="python", description="python | node | rust | go | ...")
    version_hint: str | None = Field(
        default=None, description="Only set when the user explicitly stated a version"
    )
    reason: str = Field(default="", description="Why this requirement needs the library")


class LibraryList(BaseModel):
    """Wrapper so the model returns a JSON object (json_mode cannot return a bare array)."""

    libraries: list[Library] = Field(default_factory=list)


class SearchHit(BaseModel):
    url: str
    title: str = ""
    snippet: str = ""
    score: float | None = None


class DocSource(BaseModel):
    library: str
    url: str = Field(description="Chosen official documentation entry point")
    title: str = ""
    kind: DocKind = "other"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    rationale: str = ""
    alternates: list[str] = Field(
        default_factory=list, description="Runner-up URLs, kept for the scrape phase"
    )
    user_supplied: bool = Field(
        default=False,
        description="The user named these URLs, so --max-alternates must not trim them",
    )


class ScrapedDoc(BaseModel):
    """One scraped page on disk. The unit the planning phase will cite."""

    library: str
    query: str = Field(
        default="",
        description="The requirement this page was scraped for; scopes it in the store",
    )
    url: str = Field(description="The URL we asked the collector for")
    resolved_url: str = Field(
        default="",
        description=(
            "The URL the content actually came from. Set only when it differs from `url` "
            "— a collector may redirect or crawl to another page, and a citation must "
            "point at the page the text is really on."
        ),
    )
    role: Literal["primary", "alternate"]
    rank: int = Field(default=0, description="0 for the primary URL, 1..N for alternates")
    status: Literal["ok", "empty", "failed"] = "ok"
    path: str | None = Field(default=None, description="Repo-relative markdown path")
    raw_path: str | None = Field(default=None, description="Repo-relative raw JSON row path")
    title: str = ""
    bytes: int = 0
    sha256: str = ""
    fetched_at: str = ""
    from_cache: bool = Field(
        default=False, description="Served from the MongoDB cache instead of scraped"
    )
    error: str | None = None

    @property
    def key(self) -> tuple[str, str, str]:
        """Manifest identity — a re-scrape updates this entry rather than adding one.

        The query is part of the identity because the store is scoped per run: the
        same library scraped for two projects lives in two folders, and collapsing
        them would leave one entry pointing at a file the other run overwrote.
        """
        return (self.library, self.query, self.url)


class Citation(BaseModel):
    """A scraped page a plan can point at, with its footnote marker."""

    key: str = Field(description="Footnote marker without brackets, e.g. 'fastapi-1'")
    library: str
    url: str
    path: str | None = None
    sha256: str = ""
    fetched_at: str = ""


class ApiItem(BaseModel):
    """One documented API surface, quoted from the docs rather than recalled."""

    name: str = Field(description="Function, class or command, e.g. 'typer.Option'")
    signature: str = ""
    summary: str = ""
    example: str = Field(default="", description="Code copied verbatim from the docs")


def _drop_malformed(value):
    """Discard list entries the model got structurally wrong.

    Under load the model occasionally emits `""` where an object belongs. Pydantic
    would reject the whole response for one bad element, costing an entire library
    brief or every phase of a plan — so the bad entries are dropped and the rest of
    a genuinely useful answer is kept.
    """
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict | BaseModel)]
    return value


def _drop_blank_strings(value):
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item.strip()]
    return value


class LibraryBrief(BaseModel):
    """The distilled result of reading one library's scraped pages.

    This is the map step of the map-reduce: the full corpus does not fit in one
    context window, so each library is condensed before synthesis.
    """

    library: str = ""
    install: str = Field(default="", description="Install command as the docs give it")
    version: str = Field(default="", description="Version stated in the docs, if any")
    summary: str = ""
    api: list[ApiItem] = Field(default_factory=list)
    gotchas: list[str] = Field(default_factory=list)
    citation_keys: list[str] = Field(default_factory=list)

    _clean_api = field_validator("api", mode="before")(_drop_malformed)
    _clean_lists = field_validator("gotchas", "citation_keys", mode="before")(
        _drop_blank_strings
    )


class PlanSection(BaseModel):
    title: str
    body: str = Field(description="Markdown, with [^key] footnote markers inline")


class PlanDraft(BaseModel):
    """The synthesis step's output, before rendering to markdown."""

    title: str = ""
    overview: str = ""
    phases: list[PlanSection] = Field(default_factory=list)
    pitfalls: list[str] = Field(default_factory=list)

    _clean_phases = field_validator("phases", mode="before")(_drop_malformed)
    _clean_pitfalls = field_validator("pitfalls", mode="before")(_drop_blank_strings)


class Manifest(BaseModel):
    """Index of everything in the data/ store, merged across runs."""

    updated_at: str = ""
    fetched_via: str = ""
    documents: list[ScrapedDoc] = Field(default_factory=list)


def _merge_provided(
    left: dict[str, list[str]], right: dict[str, list[str]]
) -> dict[str, list[str]]:
    return {**left, **right}


def _merge_hits(
    left: dict[str, list[SearchHit]], right: dict[str, list[SearchHit]]
) -> dict[str, list[SearchHit]]:
    return {**left, **right}


def _extend(left: list, right: list) -> list:
    return [*left, *right]


class DocResearchState(TypedDict, total=False):
    """State threaded through the graph.

    `errors` accumulates so a single library failing never aborts the run.
    """

    requirement: str
    libraries: list[Library]
    hits: Annotated[dict[str, list[SearchHit]], _merge_hits]
    # library -> URLs the user supplied instead of searching for any
    provided: Annotated[dict[str, list[str]], _merge_provided]
    doc_sources: list[DocSource]
    documents: list[ScrapedDoc]
    briefs: list[LibraryBrief]
    plan_draft: PlanDraft
    plan_markdown: str
    plan_path: str
    errors: Annotated[list[str], _extend]
