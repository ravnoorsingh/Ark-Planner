# ARK Scrapper

Citation-backed planning documentation for AI coding agents.

AI coding agents plan against memorized, often stale API knowledge. The fix is to ground
the planning document in freshly-fetched official docs, with every claim carrying a
citation. The full pipeline:

```
user requirement → identify libraries → find official doc URLs (Firecrawl MCP)
                 → scrape docs (Bright Data) → md/json store
                 → LLM writes a planning doc grounded in + citing those docs
```

**Implemented so far**: requirement → libraries → curated official doc links (phase 1),
and scraping those pages into a local `data/` store (phase 2).

## Pipeline

```
START
  ↓
parse_libraries   ← Groq LLM (JSON mode)          → state.libraries
  ↓
search_docs       ← Firecrawl MCP `firecrawl_search` → state.hits    (concurrent)
  ↓
curate_links      ← Groq LLM ranks + classifies   → state.doc_sources
  ↓
scrape_docs       ← Bright Data (Unlocker/Studio)  → state.documents  (opt-in)
  ↓
END → Rich tables + output/<run>/doc_sources.json + data/ store
```

`search_docs` calls the MCP tool directly by name rather than letting the model
tool-call it — one deterministic search per library. The LLM's judgment is applied in
`curate_links`, where it actually matters (telling `fastapi.tiangolo.com` apart from a
Medium tutorial that ranks well).

A diagram of the whole flow, traced through a real query, is in
**[docs/architecture.md](docs/architecture.md)**.

`scrape_docs` has two Bright Data backends, chosen with `ARK_SCRAPE_BACKEND`:

- **`unlocker`** (default) — the Web Unlocker API, one request per URL. Page-exact by
  construction, nothing to build or maintain.
- **`collector`** — a Scraper Studio collector. Sends **every URL in one
  `/dca/trigger` call**, since it accepts an array of inputs and bills per record
  either way: one snapshot and one poll loop rather than a request per page. Needs
  `BRIGHT_DATA_COLLECTOR_ID`.

Both ask Bright Data for **raw HTML** and convert it here. That is deliberate: both
products' own markdown converters flatten `<pre>` blocks onto a single line, which
turns documentation code samples into syntactically broken text. `markdownify` keeps
them fenced and intact.

## Setup

Requires [uv](https://docs.astral.sh/uv/). Python 3.12 is pinned via `.python-version`.

```bash
uv sync
cp .env.example .env   # then fill in your keys
```

- Groq key: <https://console.groq.com/keys> — required for `docs` / `chat`
- Firecrawl key: <https://firecrawl.dev/app/api-keys> — required for `docs` / `chat`
- Tavily key: <https://app.tavily.com> — only when `ARK_SEARCH_BACKEND=tavily`
- Bright Data token: <https://brightdata.com/cp/setting> — required for scraping
- Collector ID: <https://brightdata.com/cp/scrapers> — only for
  `ARK_SCRAPE_BACKEND=collector`; the default `unlocker` backend needs no collector

## Usage

One-shot:

```bash
uv run ark docs "get me the latest docs for LangGraph, Tavily and FastAPI"
uv run ark docs "build a RAG chatbot over PDFs with FastAPI" --json | jq '.doc_sources'
uv run ark docs "..." --model openai/gpt-oss-120b --out ./artifacts --no-save
```

Interactive:

```bash
uv run ark chat
```

REPL commands: `/list`, `/save`, `/clear`, `/quit`.

If the requirement names a capability rather than a package — "a vector database", "an
ORM" — ARK asks which one before researching, offering real candidates and accepting
anything you type instead. See
[docs/example-queries.md](docs/example-queries.md#when-you-leave-a-choice-open).
Non-interactive runs take the recommended option and say so; `--no-choices` skips it.

Scrape the discovered pages into `data/`:

```bash
# Scrape an artifact you already produced (no LLM or search calls)
uv run ark scrape output/20260817T120952Z-*/doc_sources.json --max-alternates 1

# Only certain libraries
uv run ark scrape output/*/doc_sources.json --library fastapi --library langgraph

# Or discover and scrape in one pass
uv run ark docs "build a RAG chatbot over PDFs with FastAPI" --scrape
```

`ark scrape` prints the URL list and asks before triggering, since **each URL is one
billed Bright Data record**. `--yes` skips the prompt; a non-TTY stdin proceeds
automatically. `--max-alternates 0` scrapes primary URLs only.

Check connectivity without spending tokens or credits:

```bash
uv run python scripts/check_mcp.py                              # search MCP
uv run python scripts/check_brightdata.py https://fastapi.tiangolo.com   # Bright Data
```

## Output contract

`output/<UTC-timestamp>-<slug>/doc_sources.json`:

```json
{
  "requirement": "...",
  "model": "openai/gpt-oss-20b",
  "generated_at": "2026-08-17T12:00:00+00:00",
  "libraries": [{"name": "fastapi", "ecosystem": "python", "version_hint": null, "reason": "..."}],
  "doc_sources": [{
    "library": "fastapi",
    "url": "https://fastapi.tiangolo.com/",
    "title": "FastAPI",
    "kind": "official_docs",
    "confidence": 0.95,
    "rationale": "...",
    "alternates": ["https://github.com/fastapi/fastapi"]
  }],
  "errors": []
}
```

`doc_sources` is what the scrape phase consumes — `ark scrape` takes this file directly.
When scraping ran, the artifact also carries a `documents` array mirroring the manifest.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `GROQ_API_KEY` | — | required for `docs` / `chat` |
| `FIRECRAWL_API_KEY` | — | required for `docs` / `chat` (default search backend) |
| `TAVILY_API_KEY` | — | required only when `ARK_SEARCH_BACKEND=tavily` |
| `ARK_SEARCH_BACKEND` | `firecrawl` | `firecrawl` or `tavily` |
| `BRIGHT_DATA_API_TOKEN` | — | required for `scrape` / `--scrape` |
| `ARK_SCRAPE_BACKEND` | `unlocker` | `unlocker` (Web Unlocker) or `collector` (Scraper Studio) |
| `BRIGHT_DATA_UNLOCKER_ZONE` | `cli_unlocker` | unlocker backend only |
| `BRIGHT_DATA_COLLECTOR_ID` | — | **collector backend only**; starts with `c_` |
| `BRIGHT_DATA_CONTENT_FIELD` | *auto-detect* | set only if detection picks the wrong field |
| `ARK_DATA_DIR` | `data` | where the doc store is written |
| `ARK_MAX_ALTERNATES` | `2` | alternate URLs scraped per library |
| `BRIGHT_DATA_POLL_INTERVAL` | `5` | seconds between snapshot polls |
| `BRIGHT_DATA_TIMEOUT` | `600` | seconds before giving up on a snapshot |
| `ARK_MODEL` | `openai/gpt-oss-20b` | Groq model ID |
| `ARK_TEMPERATURE` | `0.1` | |
| `ARK_MAX_LIBRARIES` | `8` | cap per run |
| `ARK_SEARCH_MAX_RESULTS` | `5` | Tavily results per library |
| `ARK_LLM_CONCURRENCY` | `3` | parallel curation calls; lower it if you hit rate limits |
| `ARK_OUTPUT_DIR` | `output` | |
| `ARK_TAVILY_MCP_URL` | `https://mcp.tavily.com/mcp/` | |
| `LANGSMITH_TRACING` | `false` | set to `true` to trace runs to LangSmith |
| `LANGSMITH_API_KEY` | — | required when tracing is on; tracing stays off without it |
| `LANGSMITH_PROJECT` | `ark-scrapper` | project traces are filed under |
| `LANGSMITH_ENDPOINT` | `https://api.smith.langchain.com` | self-hosted LangSmith |
| `ARK_TRACE_MAX_CHARS` | `2000` | per-value truncation before upload |

## Tracing

Off by default. Turn it on with two lines in `.env`:

```ini
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_...
```

Every command then prints its trace URL to **stderr** (so `--json` output stays
pipeable) and the whole run lands in LangSmith as a single tree:

```
ark docs
├── load_mcp_tools                  which tools the search server exposed
└── docs-research                   the LangGraph run
    ├── parse_libraries             → kept, names
    │   └── structured → groq.invoke → ChatGroq
    ├── search_docs                 → hits_per_library, failed
    │   └── search_one_library      → the exact query sent
    │       ├── firecrawl_search
    │       └── normalize_search_results
    └── curate_links                → curated, failed
        ├── curate_one_library      → chosen, kind, confidence
        └── finalize_doc_source     → hallucinated_url, if the model invented one
```

`--scrape` adds `scrape_urls` and per-URL Bright Data spans; `--plan` (and
`ark plan`) adds `build_plan` with one `distill_library` per library.

Two layers produce that tree. LangGraph, ChatGroq and the MCP tools trace
themselves as soon as the environment is configured; `ark/tracing.py` adds
`@traced` to the code LangChain knows nothing about — Bright Data, the document
store, HTML cleaning, citation assembly, plan rendering — so those stop showing up
as unexplained gaps between two model calls.

**What is uploaded.** Every traced value passes through `tracing.safe()` first,
which redacts anything whose key looks like a credential, dumps Pydantic models
and truncates long strings to `ARK_TRACE_MAX_CHARS`. This matters because nodes
take a `Settings` object holding every API key in the process, and a scraped page
runs to hundreds of kilobytes. Prompts, search results and doc excerpts *are*
uploaded — which is why tracing is opt-in rather than on whenever a key happens to
be in the shell.

**Cost.** Runs are billed per span ingested. A three-library discovery run is ~40
spans; a scrape-and-plan run over eight libraries is several hundred.

### A note on structured output

Groq's strict `json_schema` response format is only supported on the `openai/gpt-oss-*`
models. JSON Object Mode *is* supported on every Groq model, so `ark.llm.structured()`
takes the universal route: request a JSON object, inject the Pydantic schema into the
prompt, validate, and repair once on failure. That is why the code does not use
LangChain's `with_structured_output()` default path.

The default model (`openai/gpt-oss-20b`) happens to support strict mode, but keeping the
single json_mode path means swapping `ARK_MODEL` to any other Groq model — Qwen,
Llama, MiniMax — works without touching code.

## Troubleshooting

**`model ... is blocked at the organization level`** — Groq gates preview models per
org, and `qwen/qwen3.6-27b` is blocked by default. Enable it at
<https://console.groq.com/settings/limits> before setting `ARK_MODEL=qwen/qwen3.6-27b`.

**Rate limits** — the free tier caps tokens per minute. `structured()` reads the wait
Groq states in its 429 and retries, and curation runs at most `ARK_LLM_CONCURRENCY`
calls at once. Lower that value if you still see 429s.

**No collector needed** on the default `unlocker` backend — only
`BRIGHT_DATA_API_TOKEN`, plus a Web Unlocker zone (`bdata login` creates
`cli_unlocker` automatically).

**Collector returns the wrong page, or zero rows** — Scraper Studio's AI tends to
generate a two-stage *crawler* (`next_stage()` over discovered links) rather than a
single-page fetch, and hard-codes one theme's CSS selectors. Symptoms: a different
page than you requested, hundreds of billed rows for one input URL, or nothing at all
on a site using a different docs framework. Fix the collector to be single-stage
(`collect(parse())`), or just use the default `unlocker` backend.

**`no content field found in the row`** — a collector's output schema is whatever you
defined when you built it, so the field holding page content can't be known in advance.
Run `scripts/check_brightdata.py <url>`; it prints the real row keys and which field
auto-detection chose. Set `BRIGHT_DATA_CONTENT_FIELD` if it guessed wrong. HTML content
is converted to markdown automatically.

**`422 Unprocessable Entity`** — this client sends `[{"url": ...}]`. Check your
collector's Inputs tab expects a `url` field.

**Tavily tool naming** — the published docs write the tools hyphenated
(`tavily-search`), but the live server exposes them underscored (`tavily_search`).
`require_tool` normalizes both, so either convention resolves. `scripts/check_mcp.py`
prints what the server actually offers.

## Tests

```bash
uv run pytest
```

Fully mocked — no network, no API keys needed. Covers Tavily response normalization,
the structured-output repair retry, Bright Data's poll loop and error mapping, content-field
detection, URL slug collisions, chrome stripping, and manifest idempotence.

For manual end-to-end checks — connectivity probes, real scrapes, store inspection,
idempotence and failure paths, ordered cheapest-first — see
**[docs/testing.md](docs/testing.md)**.

## The `data/` store

```
data/
├─ manifest.json                                  ← index of every stored page
├─ fastapi/
│   ├─ primary--fastapi-tiangolo-com-6355c1ab.md  ← markdown + YAML front matter
│   ├─ primary--fastapi-tiangolo-com-6355c1ab.json ← raw Bright Data row
│   └─ alt-1--github-com-fastapi-fastapi-f9ecc9a5.md
└─ langgraph/
    └─ primary--docs-langchain-com-langgraph-0bd806a5.md
```

Paths are a pure function of `(library, role, rank, url)`, so **re-scraping overwrites in
place** — "latest docs" stays latest, and a future RAG index gets stable identifiers.
Freshness lives in the manifest and each file's front matter, never in the path. The
8-character hash suffix prevents distinct URLs (long doc paths, `?version=` query
strings) from colliding after slug truncation.

`manifest.json` is keyed on `(library, url)` and merged across runs, so a re-scrape
updates an entry instead of appending a duplicate. URLs the collector never returned are
recorded with `status: "failed"` rather than silently dropped.

