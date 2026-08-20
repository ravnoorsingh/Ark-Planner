# MongoDB store

ARK currently writes everything to disk: an artifact per run, a `plan.md` per run,
and scraped pages under `data/<library>-<query>/`. That works, but the store is
**query-scoped by design** — a plan's citations point at the snapshot taken for that
project — which means asking two questions that need FastAPI's docs scrapes FastAPI
twice and bills twice.

This adds MongoDB alongside the filesystem, for two jobs:

1. **A system of record.** Runs and plans become queryable — "which runs used
   pydantic", "show every plan mentioning Milvus" — instead of being greppable files.
2. **A reuse cache.** Scraped pages are stored keyed by **URL**, not by query, so a
   later run needing the same link reads it back instead of paying to fetch it again.

The filesystem keeps working exactly as it does now. Mongo is additive: with no
`MONGODB_URI` configured, nothing changes.

## What gets stored

| Collection | One document per | Replaces / mirrors |
|---|---|---|
| `runs` | query run | `output/<run>/doc_sources.json` |
| `plans` | plan revision | `output/<run>/plan.md` |
| `documents` | **scraped URL** | `data/<library>-<query>/*.md` |

### `runs`

The artifact payload, verbatim, plus an `_id` and the run directory it came from.
Keeping the same shape means `ark plan` and `ark refine` can load from either source.

```js
{
  _id: "20260819T124811Z-build-a-rest-api-with-fastapi",
  requirement: "Build a REST API with FastAPI…",
  model: "openai/gpt-oss-120b",
  generated_at: ISODate("2026-08-19T12:48:11Z"),
  libraries:   [ { name: "fastapi", reason: "…" }, … ],
  doc_sources: [ { library, url, kind, confidence, alternates, … }, … ],
  documents:   [ { library, url, status, sha256, path, … }, … ],
  briefs:      [ … ],        // so `ark refine` costs one LLM call
  plan_draft:  { … },
  errors:      [ … ]
}
```

### `plans`

Each revision is appended rather than overwritten, so the refinement history of a
plan is inspectable.

```js
{
  run_id: "20260819T124811Z-…",
  revision: 2,
  instruction: "Add a phase on pytest tests",   // null for the first
  markdown: "# Implementation plan…",
  model: "openai/gpt-oss-120b",
  created_at: ISODate(…)
}
```

### `documents` — the part that saves money

Keyed by the **normalized URL**, which is what makes it shareable across queries.
`ark.brightdata.normalize_url` already exists for row matching and is reused here, so
`https://x.dev` and `https://x.dev/` are one cache entry rather than two.

```js
{
  _id: "fastapi.tiangolo.com/tutorial",         // normalized URL
  url: "https://fastapi.tiangolo.com/tutorial/",
  resolved_url: "",                              // set when the fetch redirected
  markdown: "# Tutorial…",                       // converted, cleaned
  raw: { … },                                    // the backend's row, for re-conversion
  sha256: "48eb5a1f…",
  bytes: 5632,
  fetched_via: "brightdata-collector:c_msx9…",
  fetched_at: ISODate("2026-08-19T12:48:23Z"),
  queries: ["Build a REST API…", "Build a RAG service…"]   // provenance, appended
}
```

`queries` records every run that used the page. It is deliberately *not* part of the
key: the cache is about the URL's content, and the same content serves any query.

## Reuse rules

Before scraping, each planned URL is looked up. A hit is used when it is **fresh** —
younger than `ARK_DOC_CACHE_TTL_DAYS` (default 14). Anything older is re-fetched,
because the entire premise of this project is that documentation goes stale.

```
planned URLs ──► cache lookup ──► hits ────────────────► written to data/ from Mongo
                      │                                   (no Bright Data call)
                      └──► misses ──► Bright Data ──► stored in Mongo ──► data/
```

Three deliberate limits:

- **`--no-cache` forces a refetch**, for when you know a page has changed.
- **Only successful pages are cached.** A `failed` or `empty` result is never stored,
  so a transient collector hiccup cannot be served back for two weeks.
- **The markdown is cached, and so is the raw row.** Keeping the raw row means a later
  improvement to `clean.py` — and there have been several — can be applied by
  re-converting, without paying to scrape again.

## Why not replace the filesystem

The files stay because they are what the citations point at. A plan's Sources table
gives a local path and a sha256 so a claim can be checked by opening a file; making
that a database lookup would trade a property that is currently one `cat` away for
one that needs a client and a connection. Mongo is the index and the cache; the files
remain the artifact.

---

## Setting up MongoDB

### Option A — Docker Compose (recommended)

`docker-compose.yml` in the repo root runs MongoDB *and* the mongo-express web UI:

```bash
docker compose up -d          # start both
docker compose ps             # check health
docker compose down           # stop; data survives in the volume
docker compose down -v        # stop and DELETE the cached documents
```

- Mongo → `mongodb://localhost:27017`
- Web UI → <http://localhost:8081>

Both ports publish to `127.0.0.1` only. Neither the database nor the UI requires a
password, so binding them to all interfaces would hand the LAN an open admin console.

The compose project is pinned to `name: ark`, so the data volume is always
`ark_ark-mongo-data`. Without that pin Compose derives the project name from the
directory, and renaming the folder points the stack at a different, empty volume.

### Option B — Homebrew, macOS

```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

### Option C — MongoDB Atlas (free tier, no local install)

1. Create a free M0 cluster at <https://cloud.mongodb.com>.
2. **Database Access** → add a user with *Read and write to any database*.
3. **Network Access** → allow your IP (or `0.0.0.0/0` while testing).
4. **Connect** → *Drivers* → *Python* → copy the `mongodb+srv://…` string.

### Point ARK at it

Add to `.env`:

```bash
# Local
MONGODB_URI=mongodb://localhost:27017
# or Atlas
# MONGODB_URI=mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

MONGODB_DB=ark
# ARK_DOC_CACHE_TTL_DAYS=14
```

That is the only switch. Leave `MONGODB_URI` unset and ARK behaves exactly as before,
writing only to disk.

### Verify

```bash
uv run python scripts/check_mongo.py
```

It reports the connection, creates the indexes, and prints how many runs, plans and
cached documents are stored.

## Browsing the store

`docker compose up -d` also starts **mongo-express** at <http://localhost:8081>.
Open it and pick the `ark` database:

| Collection | What to look at |
|---|---|
| `documents` | One row per scraped URL. `queries` lists every run that reused it — the cache paying for itself. `markdown` is what the planner reads. |
| `plans` | One row per revision. Sort by `revision` to read `instruction` and see what each `ark refine` asked for. |
| `runs` | The artifact: requirement, libraries, doc sources. |

Deletes are behind a confirmation modal (`ME_CONFIG_OPTIONS_CONFIRM_DELETE`) because
dropping `documents` throws away every cached page and the next run re-scrapes them
all at Bright Data's expense.

If you prefer a desktop client, **MongoDB Compass** (`brew install --cask
mongodb-compass`) connects to the same `mongodb://localhost:27017`.

> Installing mongo-express from npm instead is not worth the trouble: `1.0.2` pulls a
> GitHub-hosted dependency that fails to resolve, and `1.1.0-rc-4` ships without its
> built frontend assets. The Docker image is the only reliable route.

## Operating notes

**Indexes** are created on first connect: `documents.fetched_at` (for TTL sweeps and
freshness checks), `runs.generated_at`, and `plans.run_id + revision`.

**Failures never block a run.** Every Mongo write is best-effort — if the database is
unreachable mid-run, the error is recorded as a warning and the filesystem output is
still produced. Losing the cache should never lose the work.

**Growth.** A scraped page averages ~15 KB of markdown plus a raw row that can be
100 KB+ of HTML. Roughly 100 KB per cached URL, so a thousand pages is ~100 MB —
comfortable for a free Atlas tier, and trimmable by dropping `raw` if it becomes an
issue.

## Useful queries

```js
// which runs used a given library
db.runs.find({ "libraries.name": "pydantic" }, { _id: 1, requirement: 1 })

// pages the cache is serving most often
db.documents.aggregate([
  { $project: { url: 1, uses: { $size: "$queries" } } },
  { $sort: { uses: -1 } }, { $limit: 10 }
])

// how much scraping the cache has saved
db.documents.aggregate([
  { $group: { _id: null, saved: { $sum: { $subtract: [{ $size: "$queries" }, 1] } } } }
])

// a plan's revision history
db.plans.find({ run_id: "20260819T124811Z-…" }).sort({ revision: 1 })
```
