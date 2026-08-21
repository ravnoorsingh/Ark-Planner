# ark-plans

Pull **citation-backed planning documents** into your project, for your AI coding
agent to follow.

Each plan is written from documentation that was actually scraped at generation time —
every claim carries a `[^citation]` back to the page it came from, so the agent is
following the library's real API rather than the model's memory of it.

```bash
npx ark-plans list
npx ark-plans add short-url-tracker
```

```
✔ .ark/plans/short-url-tracker.md  (260 lines)
  install #43 of this plan

Point your agent at it:
  @.ark/plans/short-url-tracker.md
```

Then reference that file in Claude Code, Cursor, or whatever you use.

## Commands

| Command | What it does |
|---|---|
| `npx ark-plans add <slug>` | Download a plan into `./.ark/plans/` |
| `npx ark-plans list` | Show plans from the catalogue |
| `npx ark-plans search <query>` | Search by name, requirement or library |
| `npx ark-plans info <slug>` | Stats for one plan before you add it |
| `npx ark-plans help` | Usage |

## Options

| Flag | Applies to | Meaning |
|---|---|---|
| `--url <url>` | all | Catalogue to talk to. Also read from `$ARK_URL`. |
| `--sort <order>` | `list` | `trending` (default), `installs`, or `new` |
| `--limit <n>` | `list` | How many to show. Default 20. |
| `--dir <path>` | `add` | Where to write. Default `.ark/plans`. |
| `--force` | `add` | Overwrite a file that is already there |

## Pointing at your own catalogue

Plans are served by an [ARK Scrapper](https://github.com/) instance. To use your own:

```bash
export ARK_URL=https://ark.your-company.com
npx ark-plans list
```

Or run one locally — `uv run ark serve` — and leave `ARK_URL` unset.

## Notes

- **No dependencies.** `npx` extracts the package before it runs, so every dependency
  is latency you would wait through. This uses Node built-ins only.
- **Requires Node 18+.**
- `add` refuses to overwrite an existing file unless you pass `--force`, so a plan you
  have edited is safe.

MIT licensed.
