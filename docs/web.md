# The web UI

`ark serve` puts the whole pipeline behind a browser and adds the thing a CLI cannot:
a **public catalogue**, where every plan anyone generates can be searched, ranked and
downloaded by anyone else.

```bash
docker compose up -d      # MongoDB — the catalogue lives here
uv run ark serve          # → http://127.0.0.1:8000
```

Without MongoDB the site still generates plans and hands them to the tab that asked
for them; there is simply nothing to list. That is the same degradation the CLI has.

## What the page does

**Left to right through a run:**

1. **Describe the project.** Free text, the same input `ark docs` takes.
2. **Answer the open choices.** "A vector database" becomes a set of real packages
   with one-line notes and a suggested default — or a box to type a package the
   model never offered.
3. **Pin documentation URLs.** Any library can be given its docs directly, which
   skips both the search and the curation call for it. A second box takes links the
   requirement never mentioned (an internal spec, a design doc); each becomes an
   entry of its own.
4. **Review the URL list.** Every page that is about to be scraped, editable: change
   a URL, drop one, add one, or cancel the run. This is the last point where nothing
   has been spent.
5. **Read the plan.** It gets a two-or-three-word name, a library label for each
   package it is grounded in, and a page of its own that anyone can download.
6. **Refine it, as often as you like.** Every plan page carries a prompt bar docked at
   the bottom — type what to change and the plan is rewritten in place.

Each option in step 2–4 can be turned off with a checkbox before the run starts, in
which case the pipeline uses the same defaults the non-interactive CLI would.

## The catalogue

| Column | Meaning |
|---|---|
| Rank | Position under the current sort |
| Name | Generated at publish time, two or three words |
| Labels | Every library the plan is grounded in — click one to filter |
| Sparkline | Downloads per day over the last week |
| Installs | Lifetime downloads |

Three sorts: **Trending** (downloads in the last 7 days), **Most installed**
(lifetime), **Newest**. Search matches the name, the requirement and the library
list, weighted so a name match wins.

Downloads are open — no account, no key, `GET /api/plans/<slug>/download`. Each one
increments the counter and appends an event, which is what makes trending possible:
ranking by lifetime installs alone would freeze the leaderboard permanently in favour
of whatever was published first.

**Every plan lands here, however it was made.** `ark docs --plan`, `ark plan` and the
web UI all publish on completion, and `ark refine` updates the entry in place — same
slug, same name, same install count, revised text. Nothing extra to run.

`ark publish` exists for plans generated before the catalogue did:

```bash
uv run ark publish output/20260820T151423Z-*/doc_sources.json
```

Two properties this relies on:

- **A run owns one entry for life.** The slug and name are set the first time and
  never regenerated, so a shared link keeps working across revisions and a refinement
  does not spend a call renaming what it just changed.
- **Two runs that generate the same name get separate entries** (`rest-api`,
  `rest-api-2`). "Build a REST API" is common enough that overwriting would be a real
  way to lose a plan.

## Refining an open plan

The bar at the foot of every plan page (`> Modify this plan…`) revises the plan you
are reading:

```
POST /api/plans/{slug}/refine   {"instruction": "Add a phase on rate limiting"}
```

It is **one LLM call and no scraping at all**. The library briefs and the previous
draft are read back out of the stored run, synthesis is re-run from those, and the
markdown is re-assembled in code — which is why every `[^citation]` still points at a
page that was actually fetched, rather than drifting into prose the model rewrote by
hand.

What changes and what does not:

| Stays | Changes |
|---|---|
| Slug, name, install count, download history | The plan text, phase count and size |
| The libraries and their scraped pages | The stored draft, so the *next* refinement builds on this one |

Each revision is appended to `plans` with the instruction that produced it, and the
run directory on disk is updated too when it is still present — a plan revised in the
browser and a stale `plan.md` on disk is the kind of divergence that wastes an
afternoon.

Plans generated before briefs were stored can be read and downloaded but not refined;
the bar says so rather than letting the model rewrite from memory.

## How a blocking prompt becomes an HTTP round-trip

The pipeline asks its questions with callbacks that *block until answered* — fine for
`console.input()`, impossible for a request handler. The web layer keeps the pipeline
exactly as it is and changes only what the callback does:

```
browser                     server
   │  POST /api/runs          │  pipeline starts in a background task
   │ ◀── SSE: step ───────────│
   │ ◀── SSE: question ───────│  hook creates a Future and awaits it
   │  POST …/answer ─────────▶│  Future resolves → pipeline continues
   │ ◀── SSE: done ───────────│
```

Three consequences worth knowing:

- **A closed tab does not strand the run.** Each question has a 15-minute deadline,
  after which the pipeline proceeds with the default it would have used unattended.
- **A reload rejoins.** The job id goes in the URL; the page re-fetches the current
  status, re-renders any open question, and re-attaches to the stream.
- **Jobs are memory, not records.** What survives the process is the plan — on disk
  and in Mongo. Finished jobs are pruned so a long-lived server does not grow.

## API

Everything the page does is a documented endpoint (`/api/docs` for the schema).

| Endpoint | Purpose |
|---|---|
| `POST /api/runs` | Start a run. Body carries the requirement and the option toggles. |
| `GET /api/runs/{id}/events` | Server-sent events: `step`, `question`, `note`, `done`, `error`. |
| `GET /api/runs/{id}` | Current status, including any open question — used to rejoin. |
| `POST /api/runs/{id}/answer` | Answer the open question. `409` if it already closed. |
| `POST /api/runs/{id}/cancel` | Abandon a run. |
| `GET /api/plans` | The catalogue. `?q=`, `?sort=trending\|installs\|new`, `?library=`. |
| `GET /api/plans/{slug}` | One plan, with its markdown and a 14-day download series. |
| `GET /api/plans/{slug}/download` | The markdown as a file. Counts an install. |
| `POST /api/plans/{slug}/refine` | Revise the plan in place. One LLM call. `400` with a reason if it cannot be refined. |
| `GET /api/libraries` | Library facets with plan counts. |
| `GET /api/stats` | Catalogue size, cache size, total downloads. |

## Deploying it beyond localhost

`ark serve` binds `127.0.0.1` by default, and that default is deliberate: **anyone who
can reach the server can spend your Bright Data and Groq credits** by starting a run.
There is no authentication in front of `POST /api/runs`. Before exposing it, put it
behind something that authenticates writes — the catalogue half is safe to serve
publicly, the run half is not.
