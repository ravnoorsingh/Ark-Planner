# Reference — commands, flags and settings

Every command, flag and environment variable, and what each one is for.

- [Commands](#commands)
- [Flags by feature](#flags-by-feature)
- [Environment variables](#environment-variables)
- [Which credentials each command needs](#which-credentials-each-command-needs)
- [What each stage costs](#what-each-stage-costs)

## Commands

| Command | Does | Costs |
|---|---|---|
| `ark docs "<requirement>"` | the pipeline: identify libraries → find docs → optionally scrape and plan | `2N + 3` LLM calls |
| `ark chat` | interactive discovery; results accumulate across turns | as above, per turn |
| `ark scrape <artifact.json>` | scrape an artifact's URLs — no LLM, no search | Bright Data records only |
| `ark plan <artifact.json>` | build a plan from already-scraped pages | `N + 1` LLM calls |
| `ark refine <artifact.json> ["instruction"]` | revise an existing plan | **1** LLM call per instruction |

`N` is the number of libraries. `ark refine` with no instruction opens an interactive
session; `/quit` ends it.

---

## Flags by feature

### Resolving what to research

| Flag | Command | Meaning |
|---|---|---|
| `--no-choices` | `docs` | Skip the question about capabilities the requirement leaves open ("a vector database"). Saves 1 LLM call; the model then picks silently. |
| `--doc-url name=URL` | `docs` | Pin a library's documentation. **Repeatable** — repeating a name adds more URLs for it, and a name matching no detected library becomes an entry of its own. Skips both search and curation for that library. |
| `--no-ask-urls` | `docs` | Don't offer the per-library URL prompt after detection. |

A pinned library costs no search credit and no curation call, and lands at confidence
`1.00`. Its URLs are exempt from `--max-alternates`, because a URL you named is an
instruction rather than a guess.

### Controlling what gets scraped

| Flag | Command | Meaning |
|---|---|---|
| `--scrape` | `docs` | Fetch the pages into `data/`. Off by default because it spends money. |
| `--max-alternates N` | `docs`, `scrape` | Runner-up URLs to scrape per library. `0` = primaries only. Default `2`. |
| `--no-review` | `docs` | Don't show the URL list for approval before scraping. |
| `--library NAME` / `-l` | `scrape` | Only scrape these libraries. Repeatable. |
| `--data-dir PATH` | `scrape` | Write the store somewhere else — useful for experimenting without touching `data/`. |
| `--yes` / `-y` | `docs`, `scrape` | Skip the confirmation prompt. |
| `--no-cache` | `docs`, `scrape` | Re-scrape even if MongoDB has the page. Use when you know a page changed. |

**The review step** is the last point before anything is billed. It lists every URL
that would be fetched and accepts:

```
enter          scrape as listed
d 3            drop row 3
e 3 <url>      replace row 3's URL
a <lib> <url>  add a URL (a new library works too)
q              cancel — nothing is scraped
```

Anything you edit is marked user-supplied, so the alternates cap cannot later trim a
link you just chose to keep.

### Planning

| Flag | Command | Meaning |
|---|---|---|
| `--plan` | `docs` | Write a citation-backed `plan.md`. Implies `--scrape`. |
| `--stdout` | `plan` | Print the plan instead of writing it. |
| `--out PATH` | all | Where the artifact or plan is written. |

### Output and scripting

| Flag | Command | Meaning |
|---|---|---|
| `--json` | `docs` | Print the raw payload for piping. Disables every interactive prompt. |
| `--no-save` | `docs` | Don't write the artifact. |
| `--model ID` | `docs`, `chat`, `plan`, `refine` | Override the Groq model for this run. |

For a fully non-interactive run:

```bash
ark docs "…" --no-choices --no-ask-urls --no-review --yes
```

Prompts are also skipped automatically when stdin is not a terminal, so piped and CI
use needs no flags.

---

## Environment variables

Set in `.env`. Every one has a working default except the credentials.

### Credentials

| Variable | Default | Needed for |
|---|---|---|
| `GROQ_API_KEY` | — | every command that uses an LLM |
| `FIRECRAWL_API_KEY` | — | search, when `ARK_SEARCH_BACKEND=firecrawl` |
| `TAVILY_API_KEY` | — | search, when `ARK_SEARCH_BACKEND=tavily` |
| `BRIGHT_DATA_API_TOKEN` | — | scraping, either backend |
| `BRIGHT_DATA_COLLECTOR_ID` | — | scraping, **only** when `ARK_SCRAPE_BACKEND=collector` |

Each command asks only for what it actually uses — `ark plan` needs Groq alone.

### Model

| Variable | Default | Meaning |
|---|---|---|
| `ARK_MODEL` | `openai/gpt-oss-20b` | Groq model ID |
| `ARK_TEMPERATURE` | `0.1` | low, because these are extraction tasks |
| `ARK_LLM_CONCURRENCY` | `3` | parallel curation calls; lower it if you hit per-minute limits |

### Search

| Variable | Default | Meaning |
|---|---|---|
| `ARK_SEARCH_BACKEND` | `firecrawl` | `firecrawl` or `tavily` |
| `ARK_SEARCH_MAX_RESULTS` | `5` | candidate URLs per library |
| `ARK_MAX_LIBRARIES` | `8` | cap on libraries per run — the main lever on total cost |
| `ARK_FIRECRAWL_MCP_URL` | `https://mcp.firecrawl.dev/v2/mcp` | |
| `ARK_TAVILY_MCP_URL` | `https://mcp.tavily.com/mcp/` | |

### Scraping

| Variable | Default | Meaning |
|---|---|---|
| `ARK_SCRAPE_BACKEND` | `unlocker` | `unlocker` (Web Unlocker, no collector needed) or `collector` (Scraper Studio) |
| `ARK_MAX_ALTERNATES` | `2` | runner-up URLs scraped per library |
| `BRIGHT_DATA_UNLOCKER_ZONE` | `cli_unlocker` | unlocker backend only |
| `BRIGHT_DATA_CONTENT_FIELD` | *auto-detect* | set only if your collector's content field isn't found — run `scripts/check_brightdata.py` to see the real row |
| `BRIGHT_DATA_POLL_INTERVAL` | `5` | seconds between snapshot polls (collector) |
| `BRIGHT_DATA_TIMEOUT` | `600` | seconds before giving up on a snapshot |
| `BRIGHT_DATA_BASE_URL` | `https://api.brightdata.com` | override for testing against a mock |
| `ARK_DATA_DIR` | `data` | where scraped pages are written |

### Planning

| Variable | Default | Meaning |
|---|---|---|
| `ARK_DISTILL_BUDGET` | `12000` | characters of documentation per distill call. Sized for a tier that rejects requests over ~8k tokens; **raise it on a paid tier for deeper grounding** |
| `ARK_PLAN_FILENAME` | `plan.md` | |
| `ARK_OUTPUT_DIR` | `output` | |

Distillation is ~67% of the token cost, so `ARK_DISTILL_BUDGET` and
`ARK_MAX_LIBRARIES` are the two knobs that actually move the bill.

### MongoDB (optional)

| Variable | Default | Meaning |
|---|---|---|
| `MONGODB_URI` | — | unset means filesystem-only; nothing else changes |
| `MONGODB_DB` | `ark` | |
| `MONGODB_TIMEOUT_MS` | `3000` | connection timeout; an unreachable database degrades rather than failing |
| `ARK_DOC_CACHE_TTL_DAYS` | `14` | reuse a cached page only while it is younger than this |

See [mongodb.md](mongodb.md).

### Tracing (optional)

| Variable | Default | Meaning |
|---|---|---|
| `LANGSMITH_TRACING` | `false` | set `true` to record runs |
| `LANGSMITH_API_KEY` | — | |
| `LANGSMITH_PROJECT` | `ark-scrapper` | |
| `LANGSMITH_ENDPOINT` | `https://api.smith.langchain.com` | |

Traces print a URL per run. Worth knowing before pasting terminal output anywhere
public.

---

## Which credentials each command needs

| Command | Groq | Search | Bright Data |
|---|:--:|:--:|:--:|
| `ark docs` | ✓ | ✓ | only with `--scrape` / `--plan` |
| `ark chat` | ✓ | ✓ | — |
| `ark scrape` | — | — | ✓ |
| `ark plan` | ✓ | — | — |
| `ark refine` | ✓ | — | — |

---

## What each stage costs

| Stage | LLM calls | External |
|---|---|---|
| `detect_choices` | 1 | — |
| `parse_libraries` | 1 | — |
| `search_docs` | **0** | 1 search per unpinned library |
| `curate_links` | N | — |
| `scrape_docs` | **0** | 1 record per URL (0 if cached) |
| `distill` | N | — |
| `synthesize` | 1 | — |
| `render_plan` | **0** | — |

**Total `2N + 3`.** Search and scraping use no LLM: we already know what to search
for and which URLs to fetch, so a model there would add cost without adding judgment.

Ways to spend less:

- `--no-choices` saves one call
- `--max-alternates 0` roughly thirds the scrape
- pinning with `--doc-url` removes a search *and* a curation call per library
- MongoDB caching removes repeat scrapes entirely
- `ark plan` / `ark refine` reuse stored pages: `N + 1` and `1` calls respectively

## Diagnostics

```bash
uv run python scripts/check_mcp.py                                    # search backend
uv run python scripts/check_brightdata.py https://fastapi.tiangolo.com  # scrape backend
uv run python scripts/check_mongo.py                                  # store and cache
```

Each isolates one dependency, so a failure points at the responsible service rather
than at the pipeline.
