"""Let the user check the URL list before anything is scraped.

This is the last point where the complete set of links exists and nothing has been
spent: every URL here becomes a billed scrape record and, if it is wrong, a citation
in the plan. Curation is good but not infallible — it has picked a same-named
different project before — so the list is offered for editing rather than assumed.

The command handling lives here as a pure function so it can be tested without a
terminal; `cli.py` supplies the prompt loop around it.
"""

from __future__ import annotations

from dataclasses import dataclass

from .state import DocSource


@dataclass
class Row:
    """One reviewable URL, flattened out of the per-library DocSource list."""

    library: str
    url: str
    primary: bool


def to_rows(sources: list[DocSource], max_alternates: int) -> list[Row]:
    """Flatten sources into the numbered list the user sees.

    Alternates are trimmed to the cap first, so the list shows exactly what would
    be scraped — showing links that would not be fetched would be misleading.
    """
    rows: list[Row] = []
    for source in sources:
        extra = source.alternates if source.user_supplied else source.alternates[:max_alternates]
        rows.append(Row(source.library, source.url, True))
        rows.extend(Row(source.library, url, False) for url in extra)
    return rows


def to_sources(rows: list[Row], original: list[DocSource]) -> list[DocSource]:
    """Rebuild DocSources from the edited rows, preserving each library's metadata.

    A library whose rows were all deleted disappears. Anything edited is marked
    user-supplied so the alternates cap cannot later trim a link the user just
    chose to keep.
    """
    by_library: dict[str, list[str]] = {}
    for row in rows:
        if row.url:
            by_library.setdefault(row.library, []).append(row.url)

    known = {source.library: source for source in original}
    rebuilt: list[DocSource] = []
    for library, urls in by_library.items():
        source = known.get(library)
        if source is None:
            rebuilt.append(
                DocSource(
                    library=library,
                    url=urls[0],
                    title=library,
                    kind="official_docs",
                    confidence=1.0,
                    rationale="Added by the user at review.",
                    alternates=urls[1:],
                    user_supplied=True,
                )
            )
            continue
        changed = [source.url, *source.alternates] != urls
        rebuilt.append(
            source.model_copy(
                update={
                    "url": urls[0],
                    "alternates": urls[1:],
                    "user_supplied": source.user_supplied or changed,
                }
            )
        )
    return rebuilt


def apply_command(rows: list[Row], command: str) -> tuple[list[Row], str]:
    """Apply one edit command, returning the new rows and a message.

    Commands:
        d 3            drop row 3
        e 3 <url>      replace row 3's URL
        a <lib> <url>  add a URL for a library (new or existing)
    """
    parts = command.split()
    if not parts:
        return rows, ""
    verb, args = parts[0].lower(), parts[1:]

    def index(token: str) -> int | None:
        if not token.isdigit():
            return None
        position = int(token) - 1
        return position if 0 <= position < len(rows) else None

    if verb in {"d", "drop", "rm", "del"} and args:
        position = index(args[0])
        if position is None:
            return rows, f"No row {args[0]}."
        dropped = rows[position]
        return rows[:position] + rows[position + 1 :], f"Dropped {dropped.url}"

    if verb in {"e", "edit"} and len(args) >= 2:
        position = index(args[0])
        if position is None:
            return rows, f"No row {args[0]}."
        updated = list(rows)
        old = updated[position].url
        updated[position] = Row(updated[position].library, args[1], updated[position].primary)
        return updated, f"Replaced {old} → {args[1]}"

    if verb in {"a", "add"} and len(args) >= 2:
        library, url = args[0], args[1]
        # Keep a library's URLs together so the numbering stays readable.
        last = max((i for i, row in enumerate(rows) if row.library == library), default=None)
        new = Row(library, url, last is None)
        if last is None:
            return [*rows, new], f"Added {library}: {url}"
        return rows[: last + 1] + [new] + rows[last + 1 :], f"Added {library}: {url}"

    return rows, f"Unknown command {command!r}. Use d <n>, e <n> <url>, a <lib> <url>."
