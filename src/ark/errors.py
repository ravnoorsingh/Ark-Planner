"""Turn an exception into something worth showing a person.

Shared by the CLI and the web UI: an MCP or anyio failure arrives wrapped in an
ExceptionGroup, and "unhandled errors in a TaskGroup (1 sub-exception)" tells nobody
that the search provider returned a 503.
"""

from __future__ import annotations


def explain(exc: BaseException) -> str:
    """Flatten exception groups down to the messages that actually say what broke."""
    if isinstance(exc, BaseExceptionGroup):
        return "; ".join(explain(sub) for sub in exc.exceptions)
    message = str(exc).strip()
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__
