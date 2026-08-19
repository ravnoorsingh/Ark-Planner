"""Console rendering and the JSON artifact that later pipeline phases consume."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .state import DocResearchState, DocSource, Library, ScrapedDoc
from .tracing import annotate, traced

console = Console()

# Diagnostics that must not land in `ark docs --json`'s stdout payload.
err_console = Console(stderr=True)

_KIND_STYLE = {
    "official_docs": "green",
    "api_reference": "cyan",
    "github": "yellow",
    "other": "dim",
}


def _slug(text: str, limit: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit] or "run"


def _confidence_style(value: float) -> str:
    if value >= 0.75:
        return "green"
    if value >= 0.45:
        return "yellow"
    return "red"


def render_results(state: DocResearchState) -> None:
    doc_sources: list[DocSource] = state.get("doc_sources", [])
    libraries: list[Library] = state.get("libraries", [])
    errors: list[str] = state.get("errors", [])

    if libraries:
        names = ", ".join(f"[bold]{library.name}[/bold]" for library in libraries)
        console.print(f"\n[dim]Libraries identified:[/dim] {names}")

    resolved = {source.library for source in doc_sources}
    unresolved = [library.name for library in libraries if library.name not in resolved]

    if doc_sources:
        table = Table(title="Documentation sources", title_justify="left", header_style="bold")
        table.add_column("Library", style="bold")
        table.add_column("Documentation URL", overflow="fold")
        table.add_column("Kind")
        table.add_column("Conf.", justify="right")

        for source in doc_sources:
            table.add_row(
                source.library,
                f"[link={source.url}]{source.url}[/link]",
                f"[{_KIND_STYLE.get(source.kind, 'dim')}]{source.kind}[/]",
                f"[{_confidence_style(source.confidence)}]{source.confidence:.2f}[/]",
            )
        # A library whose search found nothing would otherwise vanish from the
        # table without explanation, having been listed as identified moments ago.
        for name in unresolved:
            table.add_row(name, "[red]no documentation found[/red]", "—", "—")
        console.print(table)
    else:
        console.print("[yellow]No documentation sources resolved.[/yellow]")

    if errors:
        console.print(
            Panel(
                "\n".join(f"• {error}" for error in errors),
                title="Warnings",
                border_style="yellow",
            )
        )


_STATUS_STYLE = {"ok": "green", "empty": "yellow", "failed": "red"}


def _human_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def render_scrape_results(documents: list[ScrapedDoc], errors: list[str] | None = None) -> None:
    if not documents:
        console.print("[yellow]No documents scraped.[/yellow]")
        return

    table = Table(title="Scraped documents", title_justify="left", header_style="bold")
    table.add_column("Library", style="bold")
    table.add_column("Role")
    table.add_column("Status")
    table.add_column("Size", justify="right")
    table.add_column("Path", overflow="fold")

    for doc in documents:
        role = doc.role if doc.role == "primary" else f"alt {doc.rank}"
        table.add_row(
            doc.library,
            role,
            f"[{_STATUS_STYLE.get(doc.status, 'dim')}]{doc.status}[/]",
            _human_bytes(doc.bytes) if doc.bytes else "—",
            doc.path or "—",
        )
    console.print(table)

    ok = sum(1 for doc in documents if doc.status == "ok")
    console.print(f"[dim]{ok}/{len(documents)} pages stored.[/dim]")

    if errors:
        console.print(
            Panel(
                "\n".join(f"• {error}" for error in errors),
                title="Scrape warnings",
                border_style="yellow",
            )
        )


@traced("save_plan", run_type="tool")
def save_plan(markdown: str, run_dir: Path, filename: str = "plan.md") -> tuple[Path, Path]:
    """Write the plan beside the artifact it cites, and at the project root.

    The run-folder copy is canonical — it stays paired with the exact doc snapshot
    its footnotes point at. The root copy is the convenient handoff file, and is
    overwritten on every run.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    canonical = run_dir / filename
    canonical.write_text(markdown, encoding="utf-8")

    root = Path.cwd() / filename
    root.write_text(markdown, encoding="utf-8")
    return canonical, root


def render_plan_summary(markdown: str, canonical: Path, root: Path) -> None:
    """Show what the plan contains without dumping the whole file to the terminal."""
    headings = [line for line in markdown.splitlines() if line.startswith("## ")]
    phases = [line for line in markdown.splitlines() if line.startswith("### Phase ")]
    citations = len({m for m in re.findall(r"\[\^([^\]]+)\]", markdown)})

    console.print(
        Panel(
            f"[bold]{len(markdown) // 1024} KB[/bold]   "
            f"[bold]{len(phases)}[/bold] phase(s)   "
            f"[bold]{citations}[/bold] citation(s)\n"
            + "  ".join(h.removeprefix("## ") for h in headings),
            title="Plan",
            border_style="green",
        )
    )
    console.print(f"[dim]Plan →[/dim] {canonical}")
    console.print(f"[dim]     →[/dim] {root}")


@traced("to_payload", run_type="tool")
def to_payload(state: DocResearchState, model: str) -> dict:
    return {
        "requirement": state.get("requirement", ""),
        "plan_path": state.get("plan_path", ""),
        "model": model,
        "generated_at": datetime.now(UTC).isoformat(),
        "libraries": [library.model_dump() for library in state.get("libraries", [])],
        "doc_sources": [source.model_dump() for source in state.get("doc_sources", [])],
        "documents": [doc.model_dump() for doc in state.get("documents", [])],
        # Kept so `ark refine` can revise the plan without re-distilling the docs.
        "briefs": [brief.model_dump() for brief in state.get("briefs", [])],
        "plan_draft": (
            state["plan_draft"].model_dump() if state.get("plan_draft") else None
        ),
        "errors": state.get("errors", []),
    }


@traced("save_artifact", run_type="tool")
def save_artifact(state: DocResearchState, model: str, output_dir: Path) -> Path:
    """Write output/<UTC-timestamp>-<slug>/doc_sources.json and return the path."""
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_dir / f"{stamp}-{_slug(state.get('requirement', ''))}"
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "doc_sources.json"
    path.write_text(json.dumps(to_payload(state, model), indent=2), encoding="utf-8")
    annotate(artifact=str(path))
    return path
