"""CLI entry point: `ark docs "<requirement>"` and `ark chat`."""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import typer
from dotenv import load_dotenv
from pydantic import ValidationError
from rich.panel import Panel

from .choices import LibraryChoice, apply_choices, describe, detect_choices
from .config import MissingCredentials, load_settings
from .graph import NODE_LABELS, research_session
from .mongo import connect
from .nodes.scrape_docs import planned_urls, scrape_to_store
from .nodes.write_plan import build_plan, refine_plan
from .plan import build_citations
from .render import (
    console,
    err_console,
    render_plan_summary,
    render_results,
    render_scrape_results,
    save_artifact,
    save_plan,
    to_payload,
)
from .review import apply_command, to_rows, to_sources
from .state import (
    DocResearchState,
    DocSource,
    LibraryBrief,
    PlanDraft,
    ScrapedDoc,
)
from .tracing import configure as configure_tracing
from .tracing import missing_api_key, project_name, trace_run

app = typer.Typer(
    add_completion=False,
    help="Find the official documentation for the libraries a project needs.",
)


def _explain(exc: BaseException) -> str:
    """Flatten ExceptionGroups so MCP/anyio failures don't surface as 'unhandled errors
    in a TaskGroup (1 sub-exception)'."""
    if isinstance(exc, BaseExceptionGroup):
        return "; ".join(_explain(sub) for sub in exc.exceptions)
    message = str(exc).strip()
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


def discovery_credentials(backend: str) -> tuple[str, ...]:
    """Only the search provider actually in use needs a key."""
    search = "FIRECRAWL_API_KEY" if backend == "firecrawl" else "TAVILY_API_KEY"
    return ("GROQ_API_KEY", search)


def scrape_credentials(backend: str) -> tuple[str, ...]:
    """The Web Unlocker backend needs no collector, so don't demand one."""
    if backend == "collector":
        return ("BRIGHT_DATA_API_TOKEN", "BRIGHT_DATA_COLLECTOR_ID")
    return ("BRIGHT_DATA_API_TOKEN",)


def _settings(*required: str, discovery: bool = False, scrape: bool = False, **overrides):
    """Load settings, then check only the credentials this invocation actually needs.

    Which keys are required depends on the configured backends, so settings must be
    loaded before the check rather than alongside it.
    """
    load_dotenv()
    settings = load_settings(**overrides)

    # Before any LangChain object exists: whether a Runnable gets a tracer attached
    # is decided when it is built, so configuring later would trace nothing.
    # stderr, because `ark docs --json` writes a machine-readable payload to stdout.
    if missing_api_key(settings):
        err_console.print(
            "[yellow]LANGSMITH_TRACING is on but LANGSMITH_API_KEY is empty — "
            "continuing untraced.[/yellow]"
        )
    if configure_tracing(settings):
        err_console.print(f"[dim]Tracing to LangSmith project[/dim] {project_name()}")

    names = tuple(required)
    if discovery:
        names += discovery_credentials(settings.search_backend)
    if scrape:
        names += scrape_credentials(settings.scrape_backend)
    settings.require_credentials(*names)
    return settings


def _trace_link(handle) -> None:
    """Print the trace URL once the run has an ID, so a failure is one click away."""
    if handle.url:
        err_console.print(f"[dim]Trace →[/dim] {handle.url}")


def _confirm_scrape(plan: list[tuple[str, str, str, int]], assume_yes: bool) -> bool:
    """Scraping bills one Bright Data record per URL, so show the cost and confirm.

    Non-interactive stdin proceeds without prompting so scripted use isn't wedged.
    """
    console.print(
        f"\n[bold]{len(plan)} URL(s)[/bold] will be scraped "
        f"([dim]1 Bright Data record each[/dim]):"
    )
    for library, url, role, rank in plan:
        label = role if role == "primary" else f"alt {rank}"
        console.print(f"  [dim]{label:<7}[/dim] [bold]{library}[/bold]  {url}")

    if assume_yes or not sys.stdin.isatty():
        return True
    return typer.confirm("\nProceed?", default=True)


def _ask_choice(choice: LibraryChoice) -> str:
    """Offer the options, allowing a free-typed answer the model never listed."""
    console.print(f"\n[bold]{choice.slot}[/bold] — [dim]{choice.reason}[/dim]")
    for index, option in enumerate(choice.options, start=1):
        star = " [green](recommended)[/green]" if option.name == choice.recommended else ""
        note = f"  [dim]{option.note}[/dim]" if option.note else ""
        console.print(f"  [bold]{index}[/bold]. {option.name}{star}{note}")
    console.print("  [bold]o[/bold]. other — type a package name")

    default = choice.default()
    while True:
        answer = console.input(f"[bold cyan]›[/bold cyan] [dim]({default})[/dim] ").strip()
        if not answer:
            return default
        if answer.lower() in {"o", "other"}:
            typed = console.input("[bold cyan]›[/bold cyan] package name: ").strip()
            if typed:
                return typed
            continue
        if answer.isdigit() and 1 <= int(answer) <= len(choice.options):
            return choice.options[int(answer) - 1].name
        # Anything else is taken as a package name typed directly.
        return answer


async def _resolve_requirement(
    settings, requirement: str, *, interactive: bool
) -> tuple[str, list[str]]:
    """Pin any open capability slots before the pipeline researches the wrong library.

    Returns the requirement with the picks folded in, plus a line per decision.
    """
    choices = await detect_choices(settings, requirement)
    if not choices:
        return requirement, []

    decisions: dict[str, str] = {}
    if interactive:
        console.print(
            f"[dim]{len(choices)} choice(s) left open by the requirement. "
            "Press enter to accept the default.[/dim]"
        )
        for choice in choices:
            decisions[choice.slot] = _ask_choice(choice)
    else:
        # Non-interactive runs must still be reproducible, so take the defaults —
        # but say so, because the user did not pick them.
        for choice in choices:
            decisions[choice.slot] = choice.default()

    resolved = [describe(c, decisions[c.slot]) for c in choices if decisions.get(c.slot)]
    return apply_choices(requirement, decisions), resolved


def parse_doc_urls(pairs: list[str] | None) -> dict[str, list[str]]:
    """Parse `--doc-url fastapi=https://…` pairs into {library: [urls]}.

    Repeating a name accumulates rather than overwrites, so several pages of one
    library can be pinned. A name that matches no detected library becomes an entry
    of its own.
    """
    urls: dict[str, list[str]] = {}
    for pair in pairs or []:
        name, _, url = pair.partition("=")
        if not name.strip() or not url.strip():
            raise typer.BadParameter(f"expected library=URL, got {pair!r}")
        urls.setdefault(name.strip(), []).append(url.strip())
    return urls


def _split_urls(answer: str) -> list[str]:
    """Several URLs on one line, separated by spaces or commas."""
    return [part for part in re.split(r"[\s,]+", answer.strip()) if part]


def _label_for(url: str) -> str:
    """A name for a standalone link, derived from its host.

    `https://docs.internal.acme.example/auth/` becomes `acme`, which is what the
    store folder and the citation will be grouped under.
    """
    host = urlparse(url).netloc.lower().removeprefix("www.")
    # Drop the TLD rather than maintaining a list of them, then walk back to the
    # first label that names something: "docs.internal.acme.example" -> "acme".
    parts = host.split(".")[:-1]
    generic = {"docs", "doc", "www", "api", "readthedocs", "github", "gitlab", "internal"}
    for part in reversed(parts):
        if part and part not in generic:
            return part
    return parts[0] if parts else "reference"


def _ask_doc_urls(status=None):
    """Offer to pin a documentation URL for each detected library.

    Runs after detection because that is the first moment the library list exists.
    A pinned URL skips both the search and the curation call for that library.
    """

    def ask(libraries, already: dict[str, str]) -> dict[str, str]:
        pending = [lib for lib in libraries if lib.name not in already]
        if not pending:
            return {}
        if status is not None:
            status.stop()  # the spinner would fight the prompt for the terminal
        try:
            console.print(
                "\n[dim]Paste a documentation URL to use it directly, or press enter "
                "to search for one.[/dim]"
            )
            picked: dict[str, list[str]] = {}
            for library in pending:
                try:
                    answer = console.input(
                        f"  [bold]{library.name}[/bold] [dim]({library.reason or 'docs'})[/dim] › "
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    # Ctrl-D or a closed stdin means "stop asking", not "abort the
                    # run" — searching for the rest is the existing behaviour.
                    console.print("\n[dim]  (skipping remaining prompts)[/dim]")
                    return picked
                if answer:
                    picked[library.name] = _split_urls(answer)

            # A second round for anything the requirement never named: a spec, an
            # internal page, a design doc. These become entries of their own.
            console.print(
                "\n[dim]Any other documentation links? One per line, blank to finish. "
                "Prefix with a name to group them: [/dim][bold]auth=https://…[/bold]"
            )
            while True:
                try:
                    answer = console.input("  [dim]extra ›[/dim] ").strip()
                except (EOFError, KeyboardInterrupt):
                    console.print()
                    break
                if not answer:
                    break
                label, sep, rest = answer.partition("=")
                if sep and rest.strip().startswith("http"):
                    name, urls = label.strip(), _split_urls(rest)
                else:
                    urls = _split_urls(answer)
                    name = _label_for(urls[0]) if urls else ""
                if name and urls:
                    picked.setdefault(name, []).extend(urls)
                    console.print(f"    [dim]→ {name}: {len(urls)} link(s)[/dim]")
            return picked
        finally:
            if status is not None:
                status.start()

    return ask


def _review_urls(max_alternates: int, status=None):
    """Show every URL that would be scraped and let the user edit the list.

    Takes the *effective* cap rather than reading it from settings: a --max-alternates
    override would otherwise be ignored here and the list would promise more URLs
    than the scrape actually fetches.
    """

    def review(sources: list[DocSource]):
        rows = to_rows(sources, max_alternates)
        if status is not None:
            status.stop()  # the spinner would fight the prompt for the terminal
        try:
            while True:
                console.print(
                    f"\n[bold]{len(rows)} URL(s)[/bold] will be scraped "
                    f"[dim](1 Bright Data record each)[/dim]:"
                )
                for number, row in enumerate(rows, start=1):
                    label = "primary" if row.primary else "alt"
                    console.print(
                        f"  [dim]{number:>2}.[/dim] [dim]{label:<7}[/dim] "
                        f"[bold]{row.library}[/bold]  {row.url}"
                    )
                console.print(
                    "[dim]  enter = scrape · [/dim][bold]d 3[/bold][dim] drop · [/dim]"
                    "[bold]e 3 <url>[/bold][dim] replace · [/dim]"
                    "[bold]a <lib> <url>[/bold][dim] add · [/dim][bold]q[/bold][dim] cancel[/dim]"
                )
                try:
                    answer = console.input("[bold cyan]›[/bold cyan] ").strip()
                except (EOFError, KeyboardInterrupt):
                    console.print()
                    return to_sources(rows, sources)
                if not answer:
                    return to_sources(rows, sources)
                if answer.lower() in {"q", "quit", "cancel"}:
                    return None
                rows, message = apply_command(rows, answer)
                if message:
                    console.print(f"[dim]  {message}[/dim]")
        finally:
            if status is not None:
                status.start()

    return review


async def _persist(settings, artifact: Path, payload: dict, markdown: str,
                   instruction: str | None = None) -> None:
    """Mirror the run and its plan into MongoDB. Best-effort by design."""
    store = await connect(settings)
    if store is None:
        return
    run_id = artifact.parent.name
    await store.save_run(run_id, payload)
    if markdown:
        revision = await store.save_plan(run_id, markdown, settings.model, instruction)
        if revision:
            console.print(f"[dim]MongoDB →[/dim] run {run_id} · plan revision {revision}")
    await store.close()


def _merge(states: list[DocResearchState]) -> DocResearchState:
    """Fold a REPL session's turns into one state for display and saving."""
    merged: DocResearchState = {
        "requirement": "\n".join(state.get("requirement", "") for state in states),
        "libraries": [],
        "hits": {},
        "doc_sources": [],
        "errors": [],
    }
    seen_libraries: set[str] = set()
    seen_sources: set[str] = set()
    for state in states:
        for library in state.get("libraries", []):
            if library.name.lower() not in seen_libraries:
                seen_libraries.add(library.name.lower())
                merged["libraries"].append(library)
        for source in state.get("doc_sources", []):
            if source.library.lower() not in seen_sources:
                seen_sources.add(source.library.lower())
                merged["doc_sources"].append(source)
        merged["errors"].extend(state.get("errors", []))
        merged["hits"].update(state.get("hits", {}))
    return merged


@app.command()
def docs(
    requirement: str = typer.Argument(..., help="Project requirement, or libraries to look up."),
    model: str | None = typer.Option(None, "--model", help="Override the Groq model ID."),
    out: Path | None = typer.Option(None, "--out", help="Output directory for the artifact."),
    as_json: bool = typer.Option(False, "--json", help="Print raw JSON for piping."),
    no_save: bool = typer.Option(False, "--no-save", help="Skip writing the JSON artifact."),
    scrape: bool = typer.Option(
        False, "--scrape", help="Also scrape the pages via Bright Data into data/."
    ),
    plan: bool = typer.Option(
        False, "--plan", help="Write a citation-backed plan.md (implies --scrape)."
    ),
    max_alternates: int | None = typer.Option(
        None, "--max-alternates", help="Alternate URLs to scrape per library."
    ),
    assume_yes: bool = typer.Option(False, "--yes", "-y", help="Skip the scrape confirmation."),
    no_choices: bool = typer.Option(
        False, "--no-choices", help="Don't ask about capabilities the requirement leaves open."
    ),
    doc_url: list[str] = typer.Option(
        None, "--doc-url", help="Pin a library's docs: --doc-url fastapi=https://… (repeatable)."
    ),
    no_ask_urls: bool = typer.Option(
        False, "--no-ask-urls", help="Don't offer to pin a docs URL per detected library."
    ),
    no_review: bool = typer.Option(
        False, "--no-review", help="Don't show the URL list for approval before scraping."
    ),
    no_cache: bool = typer.Option(
        False, "--no-cache", help="Re-scrape even if a page is in the MongoDB cache."
    ),
) -> None:
    """Resolve official documentation links for one requirement and exit."""
    scrape = scrape or plan  # a plan is only grounded if the docs were fetched
    try:
        settings = _settings(
            discovery=True, scrape=scrape, model=model, output_dir=out
        )
    except MissingCredentials as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    if scrape:
        # --scrape is itself the opt-in, and the URL list isn't known until curation
        # finishes mid-graph, so there's no useful prompt to raise here. Use the
        # standalone `ark scrape` when you want to review links before paying.
        limit = settings.max_alternates if max_alternates is None else max_alternates
        console.print(
            f"[dim]Scraping enabled — up to {1 + limit} URL(s) per library, "
            "1 Bright Data record each.[/dim]"
        )

    async def go() -> DocResearchState:
        # Choice resolution shares this event loop rather than getting an
        # `asyncio.run()` of its own: its HTTP client would otherwise be finalized
        # against a loop that had already closed, printing an "Event loop is closed"
        # traceback over the next stage's output.
        goal = requirement
        if not no_choices:
            interactive = sys.stdin.isatty() and not as_json
            try:
                goal, resolved = await _resolve_requirement(
                    settings, requirement, interactive=interactive
                )
            except Exception as exc:
                # Never let this optional step block the pipeline.
                console.print(
                    f"[yellow]Could not check for open choices:[/yellow] {_explain(exc)}"
                )
                resolved = []
            for line in resolved:
                marker = "" if interactive else " [dim](default)[/dim]"
                console.print(f"[dim]·[/dim] {line}{marker}")

        # Optional: absent or unreachable, everything below runs filesystem-only.
        store = await connect(settings)
        if store is not None:
            console.print(f"[dim]MongoDB store: {settings.mongodb_db}[/dim]")

        pinned = parse_doc_urls(doc_url)
        # Only offer the per-library prompt when there is a terminal to answer on.
        interactive_urls = not no_ask_urls and sys.stdin.isatty() and not as_json

        if as_json:
            async with research_session(
                settings, scrape=scrape, plan=plan,
                max_alternates=max_alternates, doc_urls=pinned,
                store=store, use_cache=not no_cache,
            ) as run:
                return await run(goal)

        with console.status("[bold]Starting…[/bold]", spinner="dots") as status:
            def on_step(node: str) -> None:
                status.update(f"[bold]{NODE_LABELS.get(node, node)}…[/bold]")

            async with research_session(
                settings, scrape=scrape, plan=plan,
                max_alternates=max_alternates, doc_urls=pinned,
                store=store, use_cache=not no_cache,
                ask_doc_urls=_ask_doc_urls(status) if interactive_urls else None,
                review_urls=(
                    _review_urls(
                        settings.max_alternates if max_alternates is None else max_alternates,
                        status,
                    )
                    if scrape and not no_review and sys.stdin.isatty()
                    else None
                ),
            ) as run:
                return await run(goal, on_step)

    # Opened synchronously around asyncio.run: the task it creates copies the
    # current context, so the graph, the model calls and the scrape all nest under
    # this one root run instead of surfacing as separate traces.
    with trace_run(
        "ark docs",
        requirement=requirement,
        model=settings.model,
        scrape=scrape,
        plan=plan,
    ) as trace:
        try:
            state = asyncio.run(go())
        except Exception as exc:  # surface a readable failure, not a traceback wall
            console.print(f"[red]Run failed:[/red] {_explain(exc)}")
            _trace_link(trace)
            raise typer.Exit(code=1) from exc
        _trace_link(trace)

    if as_json:
        print(json.dumps(to_payload(state, settings.model), indent=2))
        return

    render_results(state)
    if scrape:
        render_scrape_results(state.get("documents", []))

    if not no_save:
        artifact = save_artifact(state, settings.model, settings.output_dir)
        console.print(f"[dim]Saved →[/dim] {artifact}")
        markdown = state.get("plan_markdown", "")
        if markdown:
            canonical, root = save_plan(markdown, artifact.parent, settings.plan_filename)
            render_plan_summary(markdown, canonical, root)
        asyncio.run(
            _persist(settings, artifact, to_payload(state, settings.model), markdown)
        )
    elif state.get("plan_markdown"):
        console.print(state["plan_markdown"])


@app.command()
def chat(
    model: str | None = typer.Option(None, "--model", help="Override the Groq model ID."),
    out: Path | None = typer.Option(None, "--out", help="Output directory for artifacts."),
) -> None:
    """Interactive session; results accumulate across turns."""
    try:
        settings = _settings(discovery=True, model=model, output_dir=out)
    except MissingCredentials as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    async def go() -> None:
        history: list[DocResearchState] = []
        console.print(
            Panel(
                "Describe a project or name libraries to look up.\n"
                "[bold]/list[/bold] accumulated results   [bold]/save[/bold] write artifact   "
                "[bold]/clear[/bold] reset   [bold]/quit[/bold] exit",
                title=f"ARK docs research · {settings.model}",
                border_style="cyan",
            )
        )

        async with research_session(settings) as run:
            while True:
                try:
                    line = console.input("\n[bold cyan]›[/bold cyan] ").strip()
                except (EOFError, KeyboardInterrupt):
                    console.print()
                    return
                if not line:
                    continue

                if line in {"/quit", "/exit", "/q"}:
                    return
                if line == "/clear":
                    history.clear()
                    console.print("[dim]Session cleared.[/dim]")
                    continue
                if line == "/list":
                    if history:
                        render_results(_merge(history))
                    else:
                        console.print("[dim]Nothing accumulated yet.[/dim]")
                    continue
                if line == "/save":
                    if not history:
                        console.print("[dim]Nothing to save yet.[/dim]")
                        continue
                    path = save_artifact(_merge(history), settings.model, settings.output_dir)
                    console.print(f"[dim]Saved →[/dim] {path}")
                    continue
                if line.startswith("/"):
                    console.print(f"[yellow]Unknown command {line}[/yellow]")
                    continue

                try:
                    with console.status("[bold]Starting…[/bold]", spinner="dots") as status:
                        def on_step(node: str) -> None:
                            status.update(f"[bold]{NODE_LABELS.get(node, node)}…[/bold]")

                        state = await run(line, on_step)
                except Exception as exc:  # one bad turn shouldn't end the session
                    console.print(f"[red]Turn failed:[/red] {_explain(exc)}")
                    continue

                history.append(state)
                render_results(state)

    with trace_run("ark chat", model=settings.model) as trace:
        try:
            asyncio.run(go())
        except Exception as exc:
            console.print(f"[red]Session failed:[/red] {_explain(exc)}")
            _trace_link(trace)
            raise typer.Exit(code=1) from exc
        _trace_link(trace)
    console.print("[dim]Bye.[/dim]")


@app.command()
def scrape(
    artifact: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="A doc_sources.json from `ark docs`."
    ),
    max_alternates: int | None = typer.Option(
        None, "--max-alternates", help="Alternate URLs to scrape per library."
    ),
    library: list[str] = typer.Option(
        None, "--library", "-l", help="Only scrape these libraries (repeatable)."
    ),
    data_dir: Path | None = typer.Option(None, "--data-dir", help="Where to write the store."),
    assume_yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation."),
    no_cache: bool = typer.Option(
        False, "--no-cache", help="Re-scrape even if a page is in the MongoDB cache."
    ),
) -> None:
    """Scrape the doc URLs in an artifact via Bright Data into the data/ store.

    Needs only Bright Data credentials — no LLM or search calls are made.
    """
    try:
        settings = _settings(scrape=True, data_dir=data_dir)
    except MissingCredentials as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        sources = [DocSource.model_validate(row) for row in payload.get("doc_sources", [])]
    except (ValidationError, ValueError, KeyError, AttributeError) as exc:
        console.print(f"[red]{artifact} is not a valid doc_sources artifact:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if library:
        wanted = {name.lower() for name in library}
        sources = [source for source in sources if source.library.lower() in wanted]

    if not sources:
        console.print("[yellow]No doc sources to scrape.[/yellow]")
        raise typer.Exit(code=1)

    limit = settings.max_alternates if max_alternates is None else max_alternates
    plan = planned_urls(sources, limit)
    if not _confirm_scrape(plan, assume_yes):
        console.print("[dim]Aborted.[/dim]")
        raise typer.Exit(code=1)

    async def go():
        store = await connect(settings)
        if store is not None:
            console.print(f"[dim]MongoDB store: {settings.mongodb_db}[/dim]")
        with console.status("[bold]Triggering Bright Data collector…[/bold]", spinner="dots") as s:

            def on_tick(remaining: float) -> None:
                s.update(f"[bold]Waiting for snapshot…[/bold] [dim]{remaining:.0f}s left[/dim]")

            try:
                return await scrape_to_store(
                    settings,
                    sources,
                    query=payload.get("requirement", ""),
                    max_alternates=limit,
                    on_tick=on_tick,
                    store=store,
                    use_cache=not no_cache,
                )
            finally:
                if store is not None:
                    await store.close()

    with trace_run(
        "ark scrape",
        artifact=str(artifact),
        urls=len(plan),
        backend=settings.scrape_backend,
    ) as trace:
        try:
            documents, errors = asyncio.run(go())
        except Exception as exc:
            console.print(f"[red]Scrape failed:[/red] {_explain(exc)}")
            _trace_link(trace)
            raise typer.Exit(code=1) from exc
        _trace_link(trace)

    render_scrape_results(documents, errors)
    console.print(f"[dim]Store →[/dim] {settings.data_dir}")
    if all(doc.status == "failed" for doc in documents):
        raise typer.Exit(code=1)


@app.command()
def plan(
    artifact: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="A doc_sources.json from a scraped run."
    ),
    model: str | None = typer.Option(None, "--model", help="Override the Groq model ID."),
    out: Path | None = typer.Option(None, "--out", help="Where to write plan.md."),
    stdout: bool = typer.Option(False, "--stdout", help="Print the plan instead of writing."),
) -> None:
    """Write a citation-backed plan.md from an already-scraped artifact.

    Re-runs only the LLM steps, so iterating on plan quality costs no Bright Data
    credits and no search calls.
    """
    try:
        settings = _settings("GROQ_API_KEY", model=model)
    except MissingCredentials as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        documents = [ScrapedDoc.model_validate(row) for row in payload.get("documents", [])]
    except (ValidationError, ValueError, AttributeError) as exc:
        console.print(f"[red]{artifact} is not a valid scraped artifact:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    stored = [doc for doc in documents if doc.status == "ok"]
    if not stored:
        console.print(
            "[yellow]This artifact has no stored documents.[/yellow] "
            "Run `ark scrape` on it first, or use `ark docs \"...\" --plan`."
        )
        raise typer.Exit(code=1)

    requirement = payload.get("requirement", "")
    console.print(
        f"[dim]Planning from {len(stored)} page(s) across "
        f"{len({d.library for d in stored})} librar(y/ies).[/dim]"
    )

    async def go():
        with console.status("[bold]Distilling docs…[/bold]", spinner="dots") as status:
            return await build_plan(
                settings,
                requirement,
                stored,
                on_step=lambda step: status.update(f"[bold]{step}…[/bold]"),
            )

    with trace_run(
        "ark plan",
        artifact=str(artifact),
        requirement=requirement,
        model=settings.model,
        pages=len(stored),
    ) as trace:
        try:
            markdown, briefs, draft, errors = asyncio.run(go())
        except Exception as exc:
            console.print(f"[red]Plan generation failed:[/red] {_explain(exc)}")
            _trace_link(trace)
            raise typer.Exit(code=1) from exc
        _trace_link(trace)

    if errors:
        console.print(
            Panel("\n".join(f"• {e}" for e in errors), title="Warnings", border_style="yellow")
        )
    if not markdown:
        raise typer.Exit(code=1)

    if stdout:
        print(markdown)
        return

    run_dir = out or artifact.parent
    canonical, root = save_plan(markdown, run_dir, settings.plan_filename)

    # Store the briefs and the draft so `ark refine` can revise this plan for one
    # LLM call instead of distilling every library again.
    payload["briefs"] = [brief.model_dump() for brief in briefs]
    payload["plan_draft"] = draft.model_dump()
    artifact.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    asyncio.run(_persist(settings, artifact, payload, markdown))
    render_plan_summary(markdown, canonical, root)


@app.command()
def refine(
    artifact: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="A doc_sources.json that already has a plan."
    ),
    instruction: str | None = typer.Argument(
        None, help="What to change. Omit to start an interactive session."
    ),
    model: str | None = typer.Option(None, "--model", help="Override the Groq model ID."),
    out: Path | None = typer.Option(None, "--out", help="Where to write plan.md."),
) -> None:
    """Revise an existing plan by telling the model what to change.

    Costs one LLM call per instruction: the library briefs are reused from the
    artifact, so nothing is re-searched, re-scraped or re-distilled.
    """
    try:
        settings = _settings("GROQ_API_KEY", model=model)
    except MissingCredentials as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        briefs = [LibraryBrief.model_validate(b) for b in payload.get("briefs", [])]
        documents = [ScrapedDoc.model_validate(d) for d in payload.get("documents", [])]
        draft = PlanDraft.model_validate(payload.get("plan_draft") or {})
    except (ValidationError, ValueError, AttributeError) as exc:
        console.print(f"[red]{artifact} is not a valid artifact:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if not briefs:
        console.print(
            "[yellow]This artifact has no stored briefs.[/yellow] It predates plan "
            "refinement — run [bold]ark plan[/bold] on it once, then refine."
        )
        raise typer.Exit(code=1)

    requirement = payload.get("requirement", "")
    citations = build_citations(documents)
    run_dir = out or artifact.parent

    async def apply(text: str) -> None:
        nonlocal draft
        with console.status("[bold]Revising the plan…[/bold]", spinner="dots"):
            markdown, draft = await refine_plan(
                settings, requirement, briefs, citations, draft, text
            )
        canonical, root = save_plan(markdown, run_dir, settings.plan_filename)
        # Keep the artifact in step so the next refinement builds on this revision.
        payload["plan_draft"] = draft.model_dump()
        artifact.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        await _persist(settings, artifact, payload, markdown, instruction=text)
        render_plan_summary(markdown, canonical, root)

    async def go() -> None:
        if instruction:
            await apply(instruction)
            return

        console.print(
            Panel(
                f"Refining [bold]{artifact.parent.name}[/bold] — "
                f"{len(briefs)} librar(y/ies), {len(citations)} citation(s).\n"
                "Describe a change, or [bold]/quit[/bold] to stop.",
                border_style="cyan",
            )
        )
        while True:
            try:
                text = console.input("\n[bold cyan]›[/bold cyan] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print()
                return
            if not text:
                continue
            if text in {"/quit", "/exit", "/q"}:
                return
            try:
                await apply(text)
            except Exception as exc:  # one bad revision shouldn't end the session
                console.print(f"[red]Revision failed:[/red] {_explain(exc)}")

    try:
        asyncio.run(go())
    except Exception as exc:
        console.print(f"[red]Refinement failed:[/red] {_explain(exc)}")
        raise typer.Exit(code=1) from exc


def main() -> None:
    app()


if __name__ == "__main__":
    main()
