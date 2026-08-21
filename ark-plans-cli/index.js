#!/usr/bin/env node
/**
 * ark-plans — pull citation-backed planning documents into a project.
 *
 * Deliberately dependency-free: `npx` downloads and extracts the package before it
 * runs, so every dependency is latency the user waits through on a cold cache. Node's
 * built-ins cover all of it.
 */

"use strict";

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");

const { version } = require("./package.json");

/**
 * Where the catalogue lives.
 *
 * Override per-invocation with `--url`, or per-shell with `ARK_URL`. This default
 * must point at a publicly reachable deployment before the package is published —
 * a localhost default means `npx ark-plans add` fails for everyone but its author.
 */
const DEFAULT_URL = "http://127.0.0.1:8000";
const PLANS_DIR = path.join(".ark", "plans");
const TIMEOUT_MS = 20000;

// Colour only when a human is watching; CI logs and pipes stay clean.
const tty = process.stdout.isTTY;
const c = {
  reset: tty ? "\x1b[0m" : "",
  dim: tty ? "\x1b[2m" : "",
  bold: tty ? "\x1b[1m" : "",
  green: tty ? "\x1b[32m" : "",
  red: tty ? "\x1b[31m" : "",
  yellow: tty ? "\x1b[33m" : "",
};

const out = (line = "") => process.stdout.write(line + "\n");
const err = (line) => process.stderr.write(line + "\n");

class CliError extends Error {}

// --- argument parsing --------------------------------------------------------------

function parseArgs(argv) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const [name, inline] = token.slice(2).split("=");
      // `--limit 5` and `--limit=5` both work; a bare flag is boolean.
      const next = argv[i + 1];
      if (inline !== undefined) flags[name] = inline;
      else if (next && !next.startsWith("--")) flags[name] = argv[++i];
      else flags[name] = true;
    } else {
      positional.push(token);
    }
  }
  return { positional, flags };
}

function baseUrl(flags) {
  const url = String(flags.url || process.env.ARK_URL || DEFAULT_URL);
  return url.replace(/\/+$/, "");
}

// --- HTTP --------------------------------------------------------------------------

function request(url, redirects = 3) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith("https:") ? https : http;
    const req = client.get(url, { headers: { "user-agent": `ark-plans/${version}` } }, (res) => {
      const { statusCode, headers } = res;

      if ([301, 302, 307, 308].includes(statusCode) && headers.location) {
        res.resume();
        if (redirects === 0) return reject(new CliError("Too many redirects."));
        return resolve(request(new URL(headers.location, url).toString(), redirects - 1));
      }

      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => resolve({ status: statusCode, headers, body }));
    });

    req.setTimeout(TIMEOUT_MS, () => {
      req.destroy();
      reject(new CliError(`Timed out after ${TIMEOUT_MS / 1000}s: ${url}`));
    });
    req.on("error", (error) => reject(describeConnection(error, url)));
  });
}

function describeConnection(error, url) {
  // ECONNREFUSED against the default is overwhelmingly the common failure, and the
  // raw Node message says nothing about what the user should do next.
  if (error.code === "ECONNREFUSED" || error.code === "ENOTFOUND") {
    return new CliError(
      `Could not reach the ARK catalogue at ${new URL(url).origin}\n` +
        `  Point it somewhere reachable:  ${c.bold}ARK_URL=https://your-ark-host ark-plans list${c.reset}\n` +
        `  Or run one locally:            ${c.bold}uv run ark serve${c.reset}`
    );
  }
  return new CliError(`${error.code || "Request failed"}: ${error.message}`);
}

async function getJson(url) {
  const res = await request(url);
  if (res.status === 404) throw new CliError("No such plan.");
  if (res.status >= 400) throw new CliError(`The catalogue returned HTTP ${res.status}.`);
  try {
    return JSON.parse(res.body);
  } catch {
    // Almost always a proxy or login page answering instead of the API.
    throw new CliError(`Expected JSON from ${url} but got something else.`);
  }
}

// --- rendering ---------------------------------------------------------------------

const compact = (n) =>
  n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}K` : String(n);

function printPlans(plans) {
  if (!plans.length) return out(`${c.dim}No plans found.${c.reset}`);
  const width = Math.max(...plans.map((p) => p.slug.length));
  for (const plan of plans) {
    const installs = `${compact(plan.installs)} ${plan.installs === 1 ? "install" : "installs"}`;
    out(
      `  ${c.bold}${plan.slug.padEnd(width)}${c.reset}  ${c.dim}${installs.padStart(12)}${c.reset}  ${plan.name}`
    );
    if (plan.libraries && plan.libraries.length) {
      out(`  ${" ".repeat(width)}  ${" ".repeat(12)}  ${c.dim}${plan.libraries.join(", ")}${c.reset}`);
    }
  }
  out();
  out(`${c.dim}Add one with:${c.reset} ark-plans add ${plans[0].slug}`);
}

// --- commands ----------------------------------------------------------------------

async function cmdList(flags) {
  const sort = flags.sort || "trending";
  const limit = Number(flags.limit) || 20;
  const data = await getJson(`${baseUrl(flags)}/api/plans?sort=${encodeURIComponent(sort)}&limit=${limit}`);
  if (data.offline) throw new CliError("The catalogue is offline (its database is unreachable).");
  out(`\n${c.bold}Plans${c.reset} ${c.dim}(${sort})${c.reset}\n`);
  printPlans(data.plans || []);
}

async function cmdSearch(query, flags) {
  if (!query) throw new CliError("Usage: ark-plans search <query>");
  const data = await getJson(`${baseUrl(flags)}/api/plans?q=${encodeURIComponent(query)}`);
  if (data.offline) throw new CliError("The catalogue is offline (its database is unreachable).");
  out(`\n${c.bold}Results for${c.reset} "${query}"\n`);
  printPlans(data.plans || []);
}

async function cmdInfo(slug, flags) {
  if (!slug) throw new CliError("Usage: ark-plans info <slug>");
  const plan = await getJson(`${baseUrl(flags)}/api/plans/${encodeURIComponent(slug)}`);
  out(`\n${c.bold}${plan.name}${c.reset}  ${c.dim}${plan.slug}${c.reset}\n`);
  out(`  ${plan.requirement}\n`);
  const row = (label, value) => out(`  ${c.dim}${label.padEnd(12)}${c.reset}${value}`);
  row("Libraries", (plan.libraries || []).join(", ") || "—");
  row("Installs", compact(plan.installs));
  row("Citations", String(plan.citations));
  row("Phases", String(plan.phases));
  row("Size", `${Math.round((plan.bytes || 0) / 1024)} KB`);
  row("Model", plan.model || "—");
  out(`\n${c.dim}Add it with:${c.reset} ark-plans add ${plan.slug}`);
}

async function cmdAdd(slug, flags) {
  if (!slug) throw new CliError("Usage: ark-plans add <slug>");
  const dir = flags.dir ? String(flags.dir) : PLANS_DIR;
  const target = path.join(dir, `${slug}.md`);

  // Checked before the request, not after: the download endpoint counts an install,
  // so fetching first would inflate the plan's count on a command that then refuses
  // to write anything.
  if (fs.existsSync(target) && !flags.force) {
    throw new CliError(`${target} already exists. Re-download it with --force.`);
  }

  const url = `${baseUrl(flags)}/api/plans/${encodeURIComponent(slug)}/download`;
  const res = await request(url);
  if (res.status === 404) {
    throw new CliError(`No plan called "${slug}". Try: ark-plans search ${slug}`);
  }
  if (res.status >= 400) throw new CliError(`The catalogue returned HTTP ${res.status}.`);

  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(target, res.body, "utf8");

  const lines = res.body.split("\n").length;
  const installs = res.headers["x-install-count"];
  out(`\n${c.green}✔${c.reset} ${c.bold}${target}${c.reset}  ${c.dim}(${lines} lines)${c.reset}`);
  if (installs) out(`  ${c.dim}install #${installs} of this plan${c.reset}`);
  out(`\nPoint your agent at it:\n  ${c.bold}@${target}${c.reset}\n`);
}

function cmdHelp() {
  out(`
${c.bold}ark-plans${c.reset} ${c.dim}v${version}${c.reset} — citation-backed plans for AI coding agents

${c.bold}USAGE${c.reset}
  npx ark-plans <command> [options]

${c.bold}COMMANDS${c.reset}
  ${c.bold}add${c.reset} <slug>       Download a plan into ./.ark/plans/
  ${c.bold}list${c.reset}             Show plans from the catalogue
  ${c.bold}search${c.reset} <query>   Search by name, requirement or library
  ${c.bold}info${c.reset} <slug>      Show a plan's stats before adding it
  ${c.bold}help${c.reset}             This message

${c.bold}OPTIONS${c.reset}
  --url <url>       Catalogue to talk to (default: $ARK_URL, else ${DEFAULT_URL})
  --sort <order>    list: trending | installs | new        (default: trending)
  --limit <n>       list: how many to show                 (default: 20)
  --dir <path>      add: where to write                    (default: ${PLANS_DIR})
  --force           add: overwrite an existing file
  --version         Print the version

${c.bold}EXAMPLES${c.reset}
  npx ark-plans list
  npx ark-plans search fastapi
  npx ark-plans add short-url-tracker
  ARK_URL=https://ark.example.com npx ark-plans list
`);
}

// --- entry point -------------------------------------------------------------------

async function main() {
  const { positional, flags } = parseArgs(process.argv.slice(2));
  const [command, argument] = positional;

  if (flags.version) return out(version);
  if (!command || command === "help" || flags.help) return cmdHelp();

  switch (command) {
    case "add":
      return cmdAdd(argument, flags);
    case "list":
      return cmdList(flags);
    case "search":
      // Everything after `search` is the query, so quoting is optional.
      return cmdSearch(positional.slice(1).join(" "), flags);
    case "info":
      return cmdInfo(argument, flags);
    default:
      throw new CliError(`Unknown command "${command}". Run: ark-plans help`);
  }
}

main().catch((error) => {
  err(`\n${c.red}✖${c.reset} ${error instanceof CliError ? error.message : error.stack}\n`);
  process.exit(1);
});
