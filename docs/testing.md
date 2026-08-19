# Testing ARK Scrapper

Ordered cheapest-first, so configuration problems surface before anything is spent.

Run everything from the project root:

```bash
cd "/Users/ravnoorsingh/Downloads/ARK Scrapper"
```

| Section | Cost |
|---|---|
| [1. Offline](#1-offline) | free |
| [2. Connectivity](#2-connectivity) | 1 Bright Data record |
| [3. Discovery](#3-discovery) | Groq + Tavily |
| [4. Scraping](#4-scraping) | 1 Bright Data record per URL |
| [5. Inspect the store](#5-inspect-the-store) | free |
| [6. Idempotence](#6-idempotence) | re-scrapes, so billed |
| [7. Failure paths](#7-failure-paths) | free |
| [8. Switching backends](#8-switching-backends) | 1 record |

---

## 1. Offline

No network, no API keys.

```bash
uv run pytest -q          # 163 tests, fully mocked
uv run ruff check .
uv run ark --help         # docs / chat / scrape
uv run ark scrape --help
```

## 2. Connectivity

Isolates credential and endpoint problems before any real work.

```bash
uv run python scripts/check_mcp.py                                        # Tavily MCP
uv run python scripts/check_brightdata.py https://fastapi.tiangolo.com    # Bright Data
```

`check_brightdata.py` prints the active backend, the row keys returned, which content
field was auto-detected, and a markdown preview. **If a scrape ever misbehaves, run
this first** — it tells you immediately whether the problem is Bright Data's or ARK's.

## 3. Discovery

Groq + Tavily only. No scraping, no Bright Data credits.

```bash
# Direct: extract the libraries named
uv run ark docs "get me the latest docs for LangGraph, Tavily and FastAPI"

# Inferential: infer the whole stack from a project description
uv run ark docs "build a RAG chatbot over PDFs with FastAPI and a vector database"

# Machine-readable, nothing written to disk
uv run ark docs "latest docs for httpx" --json --no-save \
  | jq '.doc_sources[] | {library, url, confidence}'

# A stronger model — curation quality varies noticeably between them
uv run ark docs "latest docs for langgraph" --model openai/gpt-oss-120b
```

Interactive session, accumulating results across turns:

```bash
uv run ark chat
# then: /list  /save  /clear  /quit
```

## 4. Scraping

**Each URL is one billed Bright Data record.** `ark scrape` prints the URL list and
asks before triggering; `--yes` skips the prompt.

```bash
# Re-scrape an artifact produced earlier (no LLM or search calls)
uv run ark scrape output/20260817T120952Z-get-me-the-latest-docs-for-langgraph-tav/doc_sources.json

# Primary URLs only — cheapest real scrape (3 records)
uv run ark scrape output/20260817T120952Z-*/doc_sources.json --max-alternates 0 --yes

# One library, into a throwaway directory so data/ is untouched
uv run ark scrape output/20260817T120952Z-*/doc_sources.json \
  --library fastapi --max-alternates 0 --data-dir /tmp/ark-test --yes

# Discovery and scraping in a single command
uv run ark docs "latest docs for pydantic" --scrape --max-alternates 1 --yes
```

> Use `--data-dir /tmp/ark-test` whenever you're experimenting — it keeps the
> populated `data/` store intact.

## 4b. The full path, end to end

Query → Groq → Tavily MCP → curated doc links → Bright Data → `data/` store, in one
command:

```bash
uv run ark docs "build a CLI tool with typer and rich" --scrape --max-alternates 1 --yes
```

Watch the spinner move through all four nodes: `Identifying libraries` →
`Searching docs via Tavily MCP` → `Curating official links` →
`Scraping docs via Bright Data`.

Real output:

```
Libraries identified: typer, rich
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Library ┃ Documentation URL           ┃ Kind          ┃ Conf. ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━┩
│ typer   │ https://typer.tiangolo.com  │ official_docs │  0.98 │
│ rich    │ https://rich.readthedocs.io │ official_docs │  0.98 │
└─────────┴─────────────────────────────┴───────────────┴───────┘

┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Library ┃ Role    ┃ Status ┃    Size ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ typer   │ primary │ ok     │ 13.7 KB │
│ typer   │ alt 1   │ ok     │ 14.2 KB │
│ rich    │ primary │ ok     │  6.2 KB │
│ rich    │ alt 1   │ ok     │ 21.4 KB │
└─────────┴─────────┴────────┴─────────┘
4/4 pages stored.
Saved → output/20260817T145807Z-build-a-cli-tool-with-typer-and-rich/doc_sources.json
```

### Verifying each hop

```bash
# Newest run. Sorts by name, since the directories are UTC-timestamped — and
# unlike `ls -dt` this survives an `ls` aliased to colorls/exa.
RUN=$(find output -mindepth 1 -maxdepth 1 -type d | sort | tail -1)

# hop 1 — LLM identified the libraries
jq -r '.libraries[] | "\(.name)\t\(.reason)"' "$RUN/doc_sources.json"

# hop 2+3 — Tavily found candidates, the LLM curated them
jq -r '.doc_sources[] | "\(.library)\t\(.confidence)\t\(.url)"' "$RUN/doc_sources.json"
jq -r '.doc_sources[] | "\(.library): \(.rationale)"' "$RUN/doc_sources.json"

# hop 4 — Bright Data scraped them into the store
jq -r '.documents[] | "\(.library)\t\(.status)\t\(.bytes)\t\(.path)"' "$RUN/doc_sources.json"

# the stored file itself
head -12 "$(jq -r '.documents[0].path' "$RUN/doc_sources.json")"
```

The run artifact carries the whole chain — `libraries`, `doc_sources`, and
`documents` — so one file shows what each stage produced.

### Sanity checks worth making

Two things to look at, because neither shows up as an error:

```bash
# Any page suspiciously small? Under ~1 KB usually means a thin landing page
# or over-aggressive cleanup. This check is how the toctree bug was caught:
# rich.readthedocs.io's index stored as 148 B because its table of contents —
# 95% of that page — was being stripped as navigation.
jq -r '.documents[] | select(.bytes < 1000) | "\(.bytes)\t\(.url)"' "$RUN/doc_sources.json"

# Are the alternates actually documentation? Curation sometimes picks a GitHub
# issue or a blog post as a runner-up.
jq -r '.doc_sources[] | .alternates[]' "$RUN/doc_sources.json"
```

## 5. Inspect the store

```bash
tree data/

# Front matter: library, url, role, fetched_at, fetched_via, sha256
head -12 data/fastapi/primary--fastapi-tiangolo-com-6355c1ab.md

jq '.fetched_via, (.documents | length)' data/manifest.json
jq -r '.documents[] | "\(.library)\t\(.status)\t\(.bytes)\t\(.url)"' data/manifest.json
```

Did any page come from somewhere other than what was requested? Empty is good — a
non-empty result means a backend redirected or crawled, and the content is attributed
to `resolved_url` rather than silently filed under the requested URL:

```bash
jq '[.documents[] | select(.resolved_url != "")]' data/manifest.json
```

Is the chrome cleanup working? Should be at or near zero link-only lines:

```bash
grep -c '^\s*\*\?\s*\[.*\](.*)\s*$' data/langgraph/primary--*.md
```

## 6. Idempotence

Paths are a pure function of `(library, role, rank, url)`, so a re-scrape overwrites in
place and the manifest upserts rather than appends.

```bash
find data -name '*.md' | wc -l
jq '.documents | length' data/manifest.json

uv run ark scrape output/20260817T120952Z-*/doc_sources.json --max-alternates 1 --yes

find data -name '*.md' | wc -l                 # unchanged
jq '.documents | length' data/manifest.json    # unchanged
```

## 7. Failure paths

Free — none of these reach an API.

```bash
# Missing credentials → names only what THIS command needs, never Groq/Tavily.
# Set the variable empty rather than using `env -u`: an exported variable overrides
# .env, but unsetting one just lets the .env value through.
BRIGHT_DATA_API_TOKEN= uv run ark scrape /tmp/anything.json
```
```
Missing required environment variable(s): BRIGHT_DATA_API_TOKEN.
Copy .env.example to .env and fill them in, or export them in your shell.
  Bright Data token:   https://brightdata.com/cp/setting
```

```bash
# Not JSON → readable error, no traceback
echo 'not json' > /tmp/bad.json && uv run ark scrape /tmp/bad.json

# Valid JSON, wrong shape → the schema violation is named
echo '{"doc_sources":[{"library":"x"}]}' > /tmp/bad2.json && uv run ark scrape /tmp/bad2.json
#   → /tmp/bad2.json is not a valid doc_sources artifact: 1 validation error
#     for DocSource / url / Field required

# No doc_sources at all → exits cleanly rather than triggering an empty scrape
echo '{"nope": 1}' > /tmp/bad3.json && uv run ark scrape /tmp/bad3.json
#   → No doc sources to scrape.

# Abort at the confirmation prompt (answer "n")
uv run ark scrape output/20260817T120952Z-*/doc_sources.json
```

## 8. Switching backends

```bash
ARK_SCRAPE_BACKEND=collector \
  uv run python scripts/check_brightdata.py https://fastapi.tiangolo.com
```

**Expect this to misbehave.** Collector `c_msx9i6aq2bz5dznadk` returns zero rows on
Sphinx sites and flattens code blocks onto one line. The collector path is fully wired
and tested against real `/dca/trigger` responses, but the parser fix (return raw HTML,
generic selectors) was never saved to production in Scraper Studio. See the
Troubleshooting section of the [README](../README.md) for the details.

---

## What good looks like

A successful scrape of the LangGraph/Tavily/FastAPI artifact:

```
6/6 pages stored.
Store → data
```

```
library            size   nav%  first heading
fastapi           53 KB     0%  ## Tutorial
fastapi           21 KB     0%  # FastAPI
langgraph         38 KB     1%  ## LangChain Assistant
langgraph          6 KB     0%  ## Install
tavily-python      2 KB     0%  ## Introduction
tavily-python      6 KB     2%  # Build with Tavily
```

Four documentation frameworks (MkDocs Material, Sphinx/ReadTheDocs, Mintlify, GitHub),
no errors, no URL drift, and code blocks fenced with their line breaks intact:

````
```
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
```
````
