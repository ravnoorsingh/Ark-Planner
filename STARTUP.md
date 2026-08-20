# Getting ARK Scrapper running

From nothing to a working web UI at <http://127.0.0.1:8000>. Roughly 10 minutes, most
of it spent collecting API keys.

---

## Step 0 — What you need first

| Thing | Why | Where |
|---|---|---|
| **uv** | Installs Python and every dependency | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Docker** | Runs MongoDB and the database UI | <https://docs.docker.com/get-docker/> |
| **Groq key** | Every LLM call in the pipeline | <https://console.groq.com/keys> |
| **Firecrawl key** | Finding documentation pages | <https://firecrawl.dev/app/api-keys> |
| **Bright Data token** | Scraping those pages | <https://brightdata.com/cp/setting> |

Python itself is *not* a prerequisite — `uv` installs the right version (3.12, pinned
in `.python-version`).

> **On costs.** Groq has a free tier that is enough to try this. Bright Data charges
> **one record per URL scraped**, so a run over 8 libraries with 1 alternate each is
> ~16 records. The defaults below keep that small, and every run shows you the URL
> list and waits for approval before spending anything.

---

## Step 1 — Install

```bash
cd "path/to/ARK Scrapper"
uv sync
```

This creates `.venv/` and installs everything. Nothing else is needed globally.

Check it worked:

```bash
uv run ark --help
```

You should see the command list: `docs`, `chat`, `scrape`, `plan`, `refine`,
`publish`, `serve`.

---

## Step 2 — Add your keys

```bash
cp .env.example .env
```

Open `.env` and fill in these three lines:

```bash
GROQ_API_KEY=gsk_...
FIRECRAWL_API_KEY=fc-...
BRIGHT_DATA_API_TOKEN=...
```

Everything else in that file is optional and already has a sensible default. Two
notes:

- **You do not need a collector ID.** The default scrape backend is Bright Data's Web
  Unlocker (`ARK_SCRAPE_BACKEND=unlocker`), which takes only the token. A collector is
  needed solely if you switch to `ARK_SCRAPE_BACKEND=collector`.
- **Tavily is an alternative to Firecrawl**, not an addition. Set `TAVILY_API_KEY` and
  `ARK_SEARCH_BACKEND=tavily` only if you prefer it.

Verify the keys are readable and the search provider answers:

```bash
uv run python scripts/check_mcp.py
```

It lists the provider's tools and runs one real search. If this fails, fix it before
going further — nothing downstream can work without it.

---

## Step 3 — Start MongoDB

The database holds three things: the scraped-page cache (so a page is never paid for
twice), the run history, and the public plan catalogue that the web UI lists.

```bash
docker compose up -d
```

That starts two containers:

| Container | Port | What it is |
|---|---|---|
| `ark-mongo` | 27017 | MongoDB 8, data in the `ark_ark-mongo-data` volume |
| `ark-mongo-express` | 8081 | Web UI for browsing the database |

Confirm both are healthy:

```bash
docker compose ps
```

Then point ARK at it — uncomment these two lines in `.env`:

```bash
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=ark
```

Verify the connection and create the indexes:

```bash
uv run python scripts/check_mongo.py
```

It prints how many runs, plans and cached documents are stored — all zeros on a fresh
install, which is correct.

> **Skipping this step is allowed.** With `MONGODB_URI` unset, ARK still runs and
> still writes plans to `output/`. You lose the page cache (every run re-scrapes) and
> the web UI's catalogue is empty. Nothing errors.

---

## Step 4 — Start the app

```bash
uv run ark serve
```

Open <http://127.0.0.1:8000>.

To use a different port, or to have the server restart when you edit the code:

```bash
uv run ark serve --port 9000 --reload
```

Leave it running — the next steps happen in the browser.

---

## Step 5 — Generate your first plan

In the page:

1. **Describe the project** in the box. Be specific about what it should do; the
   quality of the plan tracks the quality of the requirement. For example:

   > Build a FastAPI service that accepts PDF uploads, extracts their text, embeds it
   > into a vector database, and answers questions with citations back to the page.

2. **Press Generate plan.** The steps appear as they run.

3. **Answer the questions** as they come up. There are up to three:

   | Question | What it is asking | Safe answer |
   |---|---|---|
   | Open choices | Your requirement said "a vector database", not which one | Take the suggested option |
   | Pin doc URLs | Want to supply documentation links yourself? | Leave blank — ARK will find them |
   | Review URLs | Every page about to be scraped, editable | Press Scrape |

   The review step is the **last point before money is spent**. Each row is one Bright
   Data record. Drop anything that looks wrong.

4. **Wait.** Scraping and writing the plan takes one to three minutes. When it
   finishes you get the plan's generated name, its library labels, and a download
   button.

The finished plan lands in three places: `output/<timestamp>-<slug>/plan.md`, the
MongoDB catalogue, and the listing at the bottom of the page where anyone can find and
download it.

---

## Step 6 — Have a look at what it stored

**The catalogue** — scroll down the home page. Sort by Trending, Most installed or
Newest, search by name or library, or click a library label to filter.

**The database** — <http://localhost:8081>, pick the `ark` database:

| Collection | What is in it |
|---|---|
| `documents` | Every page scraped, with the markdown and a `queries` list of the runs that reused it |
| `catalog` | The public plan listing, with install counts |
| `plans` | Every plan revision, including what each `ark refine` asked for |
| `runs` | The full artifact for each run |

**On disk** — `data/` holds the scraped markdown, `output/` holds the artifact and
plan for each run.

---

## Optional — the same thing from the terminal

The web UI and the CLI are the same pipeline; nothing is exclusive to either.

```bash
# Discover, scrape and plan in one pass
uv run ark docs "build a REST API with FastAPI and Pydantic" --plan

# Revise a plan you already have (1 LLM call, no re-scraping)
uv run ark refine output/2026*-build-a-rest-api*/doc_sources.json "add a section on auth"

# Put a terminal-made plan into the web catalogue
uv run ark publish output/2026*-build-a-rest-api*/doc_sources.json
```

Every flag is listed in [docs/reference.md](docs/reference.md).

---

## If something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| `Missing required environment variable(s)` | `.env` missing or a key is blank | Check Step 2; the message names the exact variable |
| `503 Service Unavailable` from `mcp.firecrawl.dev` | Firecrawl outage — it happens | Wait and retry, or pin doc URLs so no search is needed |
| Catalogue says "The catalogue needs MongoDB" | Mongo not running, or `MONGODB_URI` unset | `docker compose up -d`, then check Step 3 |
| `Groq daily token quota (TPD) exhausted` | Free-tier daily cap | Wait for the reset, or use `--model` with a smaller model |
| Run says "no row returned for <url>" | Bright Data could not fetch that page | Usually the site blocks scraping; drop that URL at the review step |
| Plan is thin or generic | Few pages scraped | Raise `--max-alternates`, or pin better documentation URLs |

Rich failure detail for any run is in the LangSmith trace if you set
`LANGSMITH_TRACING=true` — the URL is printed after each run.

---

## Stopping and restarting

```bash
# Stop the web server
Ctrl-C in its terminal

# Stop the database (data is kept)
docker compose down

# Start everything again
docker compose up -d && uv run ark serve
```

`docker compose down -v` also **deletes the volume** — every cached page and every
catalogued plan. The plans on disk in `output/` survive it; the cache does not, so the
next run re-scrapes and re-pays for everything.

---

## Where to read more

| Document | Covers |
|---|---|
| [docs/web.md](docs/web.md) | The web UI and its HTTP API |
| [docs/reference.md](docs/reference.md) | Every command, flag and environment variable |
| [docs/mongodb.md](docs/mongodb.md) | What is stored, reuse rules, useful queries |
| [docs/architecture.md](docs/architecture.md) | How the pipeline fits together |
| [docs/example-queries.md](docs/example-queries.md) | Requirements worth trying |
| [docs/testing.md](docs/testing.md) | Running the test suite |
