# Example queries — full project builds

Long, specific requirements that exercise the whole pipeline: library inference →
Firecrawl MCP → curation → **Bright Data Scraper Studio** → `data/` → citation-backed
`plan.md`.

Every command below pins `ARK_SCRAPE_BACKEND=collector`, so scraping always goes
through Scraper Studio's `/dca/trigger` + `/dca/dataset` regardless of what `.env`
says.

## How to read the cost

Each URL is one billed Scraper Studio record. With `--max-alternates N` a run scrapes
`libraries × (1 + N)` URLs. The estimates below assume the library counts ARK actually
inferred in testing; a wide query can hit the `ARK_MAX_LIBRARIES` cap of 8.

| Flag | Effect |
|---|---|
| *(default)* | primary docs **plus up to 2 alternates** per library |
| `--max-alternates 1` | one fallback page per library |
| `--max-alternates 0` | primary docs only — cheapest |
| `--plan` | implies `--scrape`, then writes `plan.md` |
| `--yes` | skips the confirmation prompt |

Alternates are scraped and cited like any other page, so curation is held to the same
standard for them: another section of the library's docs, its API reference, or its
GitHub repo root. Issue threads, blog posts and same-named-but-different projects are
filtered out structurally, and a library may legitimately end up with none.

> Detail helps. Naming concrete versions, deployment targets and constraints gives
> `parse_libraries` far more to work with than "build a web app" — and the resulting
> plan is grounded in the docs for the stack you actually meant.

## When you leave a choice open

You don't have to name every library. Say "a vector database" and ARK asks before
researching anything:

```
3 choice(s) left open by the requirement. Press enter to accept the default.

vector database — stores embeddings
  1. qdrant-client (recommended)  lightweight, easy local deployment
  2. chromadb                     simple, no server needed
  3. weaviate-client              supports hybrid search
  4. pymilvus                     high-performance, distributed
  o. other — type a package name
› (qdrant-client)
```

Enter takes the recommendation, a number picks an option, `o` (or just typing a name)
uses anything you like — `pgvector`, `lancedb`, an internal package. The pick is folded
into the requirement as an explicit sentence, so the artifact, the plan's goal line and
the `data/` folder names all show the stack that was actually researched.

This is generic: it fires for any capability named without a package — an ORM, a task
queue, a frontend framework. A requirement that already names everything produces no
questions at all.

In a non-interactive run (piped, CI, `--json`) the recommended option is used and
printed with a `(default)` marker, so a scripted run stays reproducible and honest
about what it assumed. `--no-choices` skips the check entirely and saves one LLM call.

## Pinning your own documentation URLs

If you already know where a library's docs are — or you want a specific version,
an internal fork, or a deep page rather than a landing page — pin it. A pinned
library skips **both** the Firecrawl search and the curation LLM call, and lands in
the plan at confidence 1.00.

### A. Interactive — asks after it detects the libraries

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a REST API with FastAPI and Pydantic, served by uvicorn" --no-choices
```

```
Paste a documentation URL to use it directly, or press enter to search for one.
  fastapi (provides the REST API framework) › https://fastapi.tiangolo.com/tutorial/
  pydantic (validates request models)       ›
  uvicorn (runs the ASGI app)               ›
```

Enter skips a library and it searches as before. Ctrl-D stops the questions without
aborting the run.

### B. Pin one, search the rest

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a REST API with FastAPI and Pydantic, served by uvicorn" \
  --doc-url "fastapi=https://fastapi.tiangolo.com/tutorial/" \
  --no-choices --no-ask-urls
```

Expect `fastapi` at **1.00** with your exact URL, the others at their usual 0.9x.

### C. Pin a specific version — the case search cannot serve

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a data pipeline with pandas and pydantic" \
  --doc-url "pydantic=https://docs.pydantic.dev/1.10/" \
  --doc-url "pandas=https://pandas.pydata.org/pandas-docs/version/2.1/" \
  --no-choices --no-ask-urls --plan --yes
```

Search will always favour "latest"; pinning is how you plan against the version you
actually run.

### D. Pin everything — no search credits at all

```bash
uv run ark docs "Build a CLI with typer and rich" \
  --doc-url "typer=https://typer.tiangolo.com/tutorial/" \
  --doc-url "rich=https://rich.readthedocs.io/en/stable/console.html" \
  --no-choices --no-ask-urls --no-save
```

If every detected library is pinned, the search backend is never contacted.

### E. Internal or unsearchable docs

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a service using our internal auth SDK and FastAPI" \
  --doc-url "acme-auth=https://docs.internal.acme.example/auth/" \
  --no-choices --no-ask-urls
```

The point of the feature: a library public search cannot find at all.

### Checking it worked

```bash
RUN=$(find output -mindepth 1 -maxdepth 1 -type d | sort | tail -1)

# pinned libraries read "supplied by the user" and sit at 1.0
jq -r '.doc_sources[] | "\(.confidence)\t\(.library)\t\(.url)\t\(.rationale)"' \
  "$RUN/doc_sources.json"

# and carry no alternates, because you named the page you wanted
jq -r '.doc_sources[] | select(.confidence == 1.0) | {library, alternates}' \
  "$RUN/doc_sources.json"
```

| Flag | Effect |
|---|---|
| `--doc-url lib=URL` | pin one library; repeatable |
| `--no-ask-urls` | never prompt per library |
| *(neither)* | prompt interactively when stdin is a terminal |

Names match case-insensitively, so `--doc-url fastapi=…` pins a library the model
named `FastAPI`. A name that matches nothing detected is ignored rather than
silently creating a library.

---

## 1. RAG service over PDFs

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a production RAG service that ingests PDF manuals, chunks and embeds them \
into a vector database, and exposes a FastAPI endpoint that answers questions with \
citations back to the source page. Use pypdf for extraction, LangChain for the \
retrieval chain, ChromaDB for storage, and Pydantic models for request and response \
validation. Include streaming responses and health checks." \
  --plan --yes
```

Exercises the deepest library graph — extraction, embeddings, vector store, API layer.
Expect 5–7 libraries, so 10–14 records. This is the query that first surfaced Groq's
8000 TPM ceiling during distillation.

## 2. Agentic CLI tool

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a command-line coding assistant in Python that takes a natural-language task, \
plans it with an LLM, and executes shell commands with user confirmation. Use Typer \
for the command interface with subcommands and shell completion, Rich for streaming \
output, syntax-highlighted diffs and progress bars, LangGraph for the plan-execute \
loop with checkpointing, and httpx for async API calls. Package it as an installable \
console script." \
  --plan --yes
```

Four libraries across four doc frameworks (MkDocs Material, Sphinx, Mintlify, GitHub) —
the best single test of the `clean.py` extraction paths.

## 3. Real-time collaborative backend

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a real-time collaborative document editor backend. FastAPI serves WebSocket \
connections, Redis pub/sub broadcasts operational-transform patches between clients, \
SQLModel persists document snapshots to a Database, and Alembic manages migrations. \
Include JWT authentication, per-document access control, and graceful reconnection \
with missed-update replay." \
  --plan --yes
```

Stresses library *inference*: only some of the stack is named outright, so
`parse_libraries` has to derive the rest (`uvicorn`, `psycopg`, an auth library) from
the description.

## 4. Data pipeline with orchestration

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build a nightly ETL pipeline that pulls transaction data from a REST API, validates \
it with Pydantic, transforms it with Polars, and loads it into DuckDB for analytics. \
Orchestrate with Prefect including retries and failure alerting, and expose a Typer \
CLI to trigger backfills for an arbitrary date range." \
  --plan --yes
```

Deliberately outside the web-framework space, where a coding agent's memorized API
knowledge is weakest — Polars and Prefect both moved fast. Good demonstration of why
freshly scraped docs matter.

## 5. MCP server

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Build an MCP server in Python that exposes a company's internal wiki as searchable \
tools for AI coding agents. Use the official MCP Python SDK with streamable HTTP \
transport, httpx for the wiki's REST API, and Pydantic for tool input schemas. Support \
tool listing, full-text search, page fetch by ID, and bearer-token auth." \
  --plan --yes
```

The strongest argument for this whole project: MCP is new enough that most models'
training data predates the current SDK, so an ungrounded plan is likely to invent APIs.

## 6. Testing and CI for an existing service

```bash
ARK_SCRAPE_BACKEND=collector uv run ark docs \
  "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest \
with async fixtures, httpx's ASGI transport for endpoint tests without a live server, \
pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the \
validation layer, and ruff for linting. Wire it into GitHub Actions running against a \
Postgres service container." \
  --plan --yes
```

Tooling rather than application code — plans here are only as good as the docs, since
config formats and CLI flags change frequently.

---

## Working with the store

Documents land in `data/<library>-<query-slug>/`, so each run's docs stay together:

```
data/
├── manifest.json
├── fastapi-build-a-rest-api-with-fastapi-and-pydantic/
│   ├── primary--fastapi-tiangolo-com-6355c1ab.md
│   └── primary--fastapi-tiangolo-com-6355c1ab.json
└── typer-build-a-cli-tool-with-typer-and-rich/
    └── ...
```

```bash
# Everything scraped for one project
ls -d data/*-build-a-rest-api-*

# Every page of a library, across projects
ls -d data/fastapi-*

jq -r '.documents[] | "\(.query)\t\(.library)\t\(.status)\t\(.bytes)"' data/manifest.json
```

Re-running the same query overwrites in place. A *different* query re-scrapes the same
pages into its own folder — deliberate, so a plan's citations always point at the
snapshot taken for that project, but it does mean paying again for shared libraries.
Drop to `--max-alternates 1` or `0` when you expect heavy overlap.

## Iterating without re-scraping

Plan quality is worth tuning; scraping is not worth repeating. Once a run has scraped,
regenerate the plan for free as often as you like:

```bash
RUN=$(find output -mindepth 1 -maxdepth 1 -type d | sort | tail -1)

uv run ark plan "$RUN/doc_sources.json"                              # rewrite plan.md
uv run ark plan "$RUN/doc_sources.json" --model openai/gpt-oss-120b  # stronger model
uv run ark plan "$RUN/doc_sources.json" --stdout | less              # preview only
```

`ark plan` needs only `GROQ_API_KEY` — no Bright Data credits, no search calls.

## Reviewing links before paying

For an expensive query, split discovery from scraping and read the URLs first:

```bash
uv run ark docs "<your long requirement>"          # discovery only

RUN=$(find output -mindepth 1 -maxdepth 1 -type d | sort | tail -1)
jq -r '.doc_sources[] | "\(.confidence)\t\(.library)\t\(.url)"' "$RUN/doc_sources.json"

# then scrape only what looks right
ARK_SCRAPE_BACKEND=collector uv run ark scrape "$RUN/doc_sources.json" \
  --library fastapi --library pydantic --max-alternates 0
```

Worth doing on wide queries: curation picks excellent primary URLs but its *alternates*
sometimes drift to GitHub issues or third-party pages, and those get cited in the plan.

## Judging a plan

```bash
grep '^### Phase' plan.md                                   # ordered, executable?
grep -c '\[\^' plan.md                                      # claims carrying citations
sed -n '/## Sources/,$p' plan.md                            # every marker resolves?
```

The signal that grounding worked is a plan containing current API surfaces a model
would otherwise misremember — `uv add "fastapi[standard]"` rather than
`pip install fastapi uvicorn`, or `uv run fastapi dev` rather than a raw
`uvicorn main:app` invocation.
