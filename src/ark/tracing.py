"""LangSmith tracing for the pipeline.

Tracing is opt-in and off by default: set `LANGSMITH_TRACING=true` plus a
`LANGSMITH_API_KEY` in `.env`. With it off, every decorator here short-circuits
inside langsmith before touching its arguments, so instrumentation costs a normal
run nothing.

Two layers feed one trace tree:

  * LangGraph, ChatGroq and the MCP tools trace *themselves* through LangChain's
    callback system as soon as the environment is configured — nothing here does
    that work.
  * Everything else — Bright Data, the document store, HTML cleaning, citation
    assembly, plan rendering — is annotated with `@traced`, so a run's non-LLM
    work appears in the same tree instead of showing up as a silent gap between
    two model calls.

`@traced` wraps langsmith's `traceable` with a scrubber (`safe`) on the way in and
out. That is not cosmetic. Nodes are called with a `Settings` object holding every
API key in the process, and a scraped page runs to hundreds of kilobytes; both
would otherwise be uploaded verbatim.
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .config import Settings

try:  # langsmith ships with langchain-core, but tracing must never be a hard dep
    from langsmith import traceable as _traceable
    from langsmith.run_helpers import get_current_run_tree
    from langsmith.run_helpers import trace as _trace
    from langsmith.utils import get_env_var

    LANGSMITH_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only in a stripped environment
    LANGSMITH_AVAILABLE = False

    def _traceable(*args: Any, **kwargs: Any):  # type: ignore[misc]
        """No-op stand-in with `traceable`'s dual bare/parameterized calling form."""
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]

        def decorator(func: Callable) -> Callable:
            return func

        return decorator

    def get_current_run_tree():  # type: ignore[misc]
        return None

    def get_env_var(*args: Any, **kwargs: Any):  # type: ignore[misc]
        return None

    @contextmanager
    def _trace(*args: Any, **kwargs: Any):  # type: ignore[misc]
        yield None


# --- redaction --------------------------------------------------------------------

# Matched against argument names and dict keys, at any depth.
SECRET_PATTERN = re.compile(
    r"(api[_-]?key|_key$|^key$|token|secret|password|passwd|authorization|bearer|credential)",
    re.IGNORECASE,
)
REDACTED = "***"

# Arguments that are plumbing rather than data: they serialize to noise, to a
# repr with a memory address, or (for the callbacks) not at all.
SKIP_ARGS = frozenset(
    {"self", "cls", "client", "session", "limiter", "llm", "tool", "tools",
     "on_tick", "on_step", "run_tree", "config"}
)

# Trace payloads are meant to be read, and LangSmith charges by ingested bytes.
# A scraped page is ~100 KB and a distill corpus is 12 KB by default; both are
# recognizable from their opening lines, and the untruncated text is already on
# disk in `data/`.
DEFAULT_MAX_CHARS = 2_000
MAX_ITEMS = 40
MAX_DEPTH = 6


def _max_chars() -> int:
    raw = os.environ.get("ARK_TRACE_MAX_CHARS", "")
    try:
        return max(int(raw), 80)
    except ValueError:
        return DEFAULT_MAX_CHARS


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}… [{len(text)} chars total, truncated]"


def safe(value: Any, *, depth: int = 0, limit: int | None = None) -> Any:
    """Recursively reduce `value` to something small and secret-free.

    Applied to every traced function's inputs and outputs. Pydantic models are
    dumped so their fields stay searchable in the UI rather than collapsing to a
    repr, then walked like any other mapping so a nested key still gets redacted.
    """
    limit = _max_chars() if limit is None else limit

    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return _clip(value, limit)
    if depth >= MAX_DEPTH:
        return _clip(repr(value), limit)

    if isinstance(value, dict):
        reduced = {}
        for key, item in list(value.items())[:MAX_ITEMS]:
            name = str(key)
            reduced[name] = REDACTED if SECRET_PATTERN.search(name) else safe(
                item, depth=depth + 1, limit=limit
            )
        if len(value) > MAX_ITEMS:
            reduced["…"] = f"{len(value) - MAX_ITEMS} more key(s)"
        return reduced

    if isinstance(value, (list, tuple, set, frozenset)):
        items = list(value)
        reduced = [safe(item, depth=depth + 1, limit=limit) for item in items[:MAX_ITEMS]]
        if len(items) > MAX_ITEMS:
            reduced.append(f"… {len(items) - MAX_ITEMS} more item(s)")
        return reduced

    dump = getattr(value, "model_dump", None)
    if callable(dump):
        try:
            return safe(dump(mode="json"), depth=depth + 1, limit=limit)
        except Exception:
            pass  # a model that won't serialize falls through to its repr

    if isinstance(value, BaseException):
        return f"{type(value).__name__}: {_clip(str(value), limit)}"
    if callable(value):
        # Not necessarily a function: a BeautifulSoup Tag is callable too, and its
        # repr is the entire subtree — so this falls back to a clipped repr rather
        # than returning one unbounded.
        return getattr(value, "__name__", None) or _clip(repr(value), limit)
    return _clip(repr(value), limit)


def scrub_inputs(inputs: dict) -> dict:
    """Drop plumbing arguments, redact credentials, truncate bulk text."""
    return {
        name: safe(value)
        for name, value in inputs.items()
        if name not in SKIP_ARGS and not callable(value)
    }


def scrub_outputs(outputs: Any) -> dict:
    """Same treatment for a return value, always shaped as a dict for the UI."""
    reduced = safe(outputs)
    return reduced if isinstance(reduced, dict) else {"output": reduced}


# --- decorator --------------------------------------------------------------------


def traced(
    name: str | None = None,
    *,
    run_type: str = "chain",
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    process_inputs: Callable[[dict], dict] | None = None,
    process_outputs: Callable[[Any], dict] | None = None,
):
    """`langsmith.traceable` with this project's redaction applied by default.

    Works on sync functions, async functions and async generators alike, because
    that is all `traceable` itself does with them.
    """
    def decorator(func: Callable) -> Callable:
        return _traceable(
            run_type=run_type,
            name=name or func.__name__,
            tags=tags,
            metadata=metadata,
            process_inputs=process_inputs or scrub_inputs,
            process_outputs=process_outputs or scrub_outputs,
        )(func)

    return decorator


def annotate(**fields: Any) -> None:
    """Attach metadata to the run in progress; a no-op when nothing is tracing.

    Used for facts that are only known part-way through a call — how many retries
    a Groq request needed, which content field a Bright Data row turned out to
    use — which are exactly the facts worth having when a run looks wrong.
    """
    run = get_current_run_tree()
    if run is None:
        return
    try:
        run.add_metadata({key: safe(value, limit=500) for key, value in fields.items()})
    except Exception:  # pragma: no cover - telemetry must never break the run
        pass


# --- configuration ----------------------------------------------------------------

TRACING_ENV = {
    "tracing": "LANGSMITH_TRACING",
    "api_key": "LANGSMITH_API_KEY",
    "project": "LANGSMITH_PROJECT",
    "endpoint": "LANGSMITH_ENDPOINT",
}


def configure(settings: Settings) -> bool:
    """Publish the tracing settings to the environment. Returns whether it is on.

    Env vars rather than `langsmith.configure()` on purpose: LangChain's callback
    manager, the LangGraph runtime and langsmith's own `traceable` all read the
    same variables, so one write turns on every layer at once.

    Must run before the first LangChain object is built — `_configure` decides
    whether to attach a tracer when a Runnable is invoked, and langsmith caches
    environment lookups.
    """
    if not settings.langsmith_tracing:
        # Explicitly off, so an inherited LANGSMITH_TRACING=true from the parent
        # shell cannot quietly re-enable what the config says is disabled.
        os.environ[TRACING_ENV["tracing"]] = "false"
        _forget_cached_env()
        return False

    if not settings.langsmith_api_key.strip():
        os.environ[TRACING_ENV["tracing"]] = "false"
        _forget_cached_env()
        return False

    os.environ[TRACING_ENV["tracing"]] = "true"
    os.environ[TRACING_ENV["api_key"]] = settings.langsmith_api_key
    os.environ[TRACING_ENV["project"]] = settings.langsmith_project
    os.environ[TRACING_ENV["endpoint"]] = settings.langsmith_endpoint
    _forget_cached_env()
    return LANGSMITH_AVAILABLE


def _forget_cached_env() -> None:
    """langsmith memoizes environment reads, so a late write would be ignored."""
    cache_clear = getattr(get_env_var, "cache_clear", None)
    if callable(cache_clear):  # pragma: no branch - always present in langsmith
        cache_clear()


def missing_api_key(settings: Settings) -> bool:
    """Tracing was asked for but cannot run — worth one line of warning, not a failure."""
    return settings.langsmith_tracing and not settings.langsmith_api_key.strip()


class RunHandle:
    """A started root run, exposing just its URL. Empty when tracing is off."""

    def __init__(self, run: Any = None) -> None:
        self._run = run

    @property
    def url(self) -> str:
        if self._run is None:
            return ""
        try:
            return self._run.get_url()
        except Exception:  # pragma: no cover - a URL is a nicety, never a blocker
            return ""


@contextmanager
def trace_run(name: str, **inputs: Any) -> Iterator[RunHandle]:
    """Open one root run for a whole CLI command.

    Everything the command does — the graph, the model calls, the scrape — nests
    under it, so a run is a single trace instead of several unrelated trees.
    Context variables are copied into the task `asyncio.run` creates, so opening
    this synchronously around an `asyncio.run(...)` still parents the async work.
    """
    if not LANGSMITH_AVAILABLE or not is_enabled():
        yield RunHandle()
        return

    with _trace(name=name, run_type="chain", inputs=scrub_inputs(inputs)) as run:
        yield RunHandle(run)


def is_enabled() -> bool:
    return os.environ.get(TRACING_ENV["tracing"], "").strip().lower() == "true"


def project_name() -> str:
    return os.environ.get(TRACING_ENV["project"], "")
