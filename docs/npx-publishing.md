# Publishing `npx ark-plans`

The package lives in [`ark-plans-cli/`](../ark-plans-cli). It is a separate npm package
from the Python app — three files, no dependencies — whose only job is to fetch a plan
from a running ARK catalogue and drop it in `./.ark/plans/`.

```bash
npx ark-plans add short-url-tracker
```

---

## Step 1 — Deploy the backend first (this is the blocker)

**`npx ark-plans` is useless until the catalogue is reachable from the public
internet.** The CLI is a thin client; it holds no plans of its own. Publishing before
deploying ships a command that fails with connection-refused for everybody except
whoever has `ark serve` running locally.

What has to be true:

| Requirement | Why |
|---|---|
| A public HTTPS URL serving the FastAPI app | The CLI calls `/api/plans*` on it |
| MongoDB reachable from it | The catalogue *is* the database; without it `/api/plans` returns `offline` |
| `GROQ_API_KEY` and the scrape keys set | Only if you want the deployed instance to *generate* plans too |

Any container host works — the app is a normal ASGI app:

```bash
uvicorn ark.web.app:app --host 0.0.0.0 --port ${PORT:-8000}
```

> **Bind `0.0.0.0` deliberately, and read the warning in [web.md](web.md) first.**
> Nothing authenticates `POST /api/runs`, so anyone who can reach the deployment can
> spend your Groq and Bright Data credits. Put auth in front of the run endpoints, or
> deploy a catalogue-only instance, before it is public.

Confirm it before going further:

```bash
curl https://your-ark-host/api/plans | head -c 200
```

You want JSON with `"offline": false`. If it says `"offline": true`, the app is up but
its database is not — fix that first, or every `npx ark-plans` command will report an
offline catalogue.

---

## Step 2 — Point the CLI at that deployment

Open `ark-plans-cli/index.js` and set the default:

```js
const DEFAULT_URL = "https://your-ark-host";   // was http://127.0.0.1:8000
```

This is the single line that decides whether the published package works out of the
box. Users can still override it with `--url` or `$ARK_URL`, but almost nobody will.

Test it locally exactly as a user gets it — `npm pack` builds the real tarball, and
`npx` on that tarball exercises the `bin` entry, the shebang and the file list:

```bash
cd ark-plans-cli
npm pack                              # → ark-plans-0.1.0.tgz
cd /tmp && mkdir try && cd try
npx --yes /path/to/ark-plans-0.1.0.tgz list
npx --yes /path/to/ark-plans-0.1.0.tgz add <some-slug>
```

If `list` prints plans and `add` writes `.ark/plans/<slug>.md`, it is ready.

---

## Step 3 — Publish

The name `ark-plans` was unclaimed as of August 2026. Check it is still free:

```bash
npm view ark-plans     # "404 Not Found" means it is yours to take
```

Then:

```bash
cd ark-plans-cli
npm login              # opens a browser; do this yourself
npm publish --access public
```

`--access public` matters only for scoped names (`@you/ark-plans`), but it is harmless
and saves a confusing failure if you ever scope it.

Verify from a clean machine or a fresh cache:

```bash
npx --yes ark-plans@latest list
```

---

## Step 4 — Releasing updates

```bash
cd ark-plans-cli
npm version patch      # 0.1.0 → 0.1.1, and creates a git tag
npm publish
```

Use `minor` for new commands, `major` for anything that changes existing behaviour.

**npm versions are immutable.** You cannot re-publish `0.1.1` with a fix; you publish
`0.1.2`. `npm unpublish` is only allowed within 72 hours and breaks anyone who already
depends on it, so treat every publish as permanent.

Users are largely insulated from mistakes anyway, because the CLI is a thin client: if
the API changes shape, fix the server and everyone's existing `npx ark-plans` follows
along without upgrading.

---

## What is in the package

```
ark-plans-cli/
├── package.json     the "bin" field is what makes `npx ark-plans` work
├── index.js         the CLI; starts with #!/usr/bin/env node
└── README.md        what npmjs.com shows on the package page
```

`npm pack --dry-run` prints the exact file list — 3 files, ~5 kB. The `files` field in
`package.json` is an allowlist, so nothing from the Python project can leak into the
tarball by accident.

Two properties worth preserving in any change:

- **No dependencies.** `npx` downloads and extracts the package before running it, so
  every dependency is latency the user waits through on a cold cache. Node's built-ins
  cover HTTP, redirects, files and argument parsing.
- **`add` counts an install, so it checks for an existing file *before* fetching.**
  Fetching first would inflate a plan's download count on a command that then refuses
  to write anything.

---

## How the pieces connect

```
npx ark-plans add short-url-tracker
        │
        ├─ npx resolves "ark-plans" from the npm registry (or its cache)
        ├─ reads package.json "bin" → index.js
        └─ runs it with stdio inherited
                │
                ▼
        GET https://your-ark-host/api/plans/short-url-tracker/download
                │
                ├─ MongoDB: $inc installs, append an install event
                └─ returns the markdown
                │
                ▼
        .ark/plans/short-url-tracker.md
```

That download endpoint is the same one the website's **Download .md** button uses, so
installs from the terminal and the browser land in the same counter and the same
trending window.
