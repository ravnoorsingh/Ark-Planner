/* Index page: drive a run, answer its questions, browse the catalogue. */

const $ = (id) => document.getElementById(id);
const el = (tag, attrs = {}, ...kids) => {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key === "html") node.innerHTML = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (value !== null && value !== false) node.setAttribute(key, value);
  }
  for (const kid of kids.flat()) {
    if (kid == null) continue;
    node.append(kid.nodeType ? kid : document.createTextNode(kid));
  }
  return node;
};

const compact = (n) => n >= 1e6 ? (n / 1e6).toFixed(1) + "M"
  : n >= 1e3 ? (n / 1e3).toFixed(1) + "K" : String(n);

function toast(message) {
  const node = el("div", { class: "toast" }, message);
  document.body.append(node);
  setTimeout(() => node.remove(), 2600);
}

/* ------------------------------------------------------------------ sparkline */

function sparkline(values, width = 78, height = 24) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "spark");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("width", width);
  svg.setAttribute("height", height);
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  const top = Math.max(...values, 1);
  const step = values.length > 1 ? width / (values.length - 1) : width;
  // A plan with no downloads yet still gets a line — a missing sparkline reads as
  // broken, a flat one reads as "nothing yet", which is the truth.
  const flat = values.every((v) => v === 0);
  const points = values.map((value, index) =>
    `${(index * step).toFixed(1)},${(height - 2 - (value / top) * (height - 4)).toFixed(1)}`);
  path.setAttribute("d", "M" + points.join("L"));
  if (flat) path.setAttribute("class", "flat");
  svg.append(path);
  return svg;
}

/* ------------------------------------------------------------------ catalogue */

let sort = "trending";
let query = "";
let library = "";

async function loadPlans() {
  const params = new URLSearchParams({ sort, q: query, library });
  const box = $("plans");
  const data = await fetch(`/api/plans?${params}`).then((r) => r.json());
  box.replaceChildren();

  if (data.offline) {
    box.append(el("div", { class: "empty", html:
      "The catalogue needs MongoDB. Start it with <code>docker compose up -d</code>." }));
    return;
  }
  if (!data.plans.length) {
    box.append(el("div", { class: "empty" },
      query || library ? "Nothing matches that." : "No plans published yet — generate the first one above."));
    return;
  }

  data.plans.forEach((plan, index) => {
    const labels = plan.libraries.slice(0, 5).map((name) =>
      el("a", {
        class: "label",
        href: "#catalogue",
        onclick: (event) => { event.preventDefault(); library = name; query = ""; $("search").value = ""; loadPlans(); },
      }, name));
    if (plan.libraries.length > 5) {
      labels.push(el("span", { class: "label more" }, `+${plan.libraries.length - 5}`));
    }
    box.append(el("div", { class: "plan-row" },
      el("div", { class: "rank" }, String(index + 1)),
      el("div", {},
        el("a", { class: "name", href: `/plan/${plan.slug}` }, plan.name),
        el("div", { class: "req", title: plan.requirement }, plan.requirement),
        el("div", { class: "labels" }, labels)),
      el("div", { class: "spark-cell" }, sparkline(plan.trend)),
      el("div", { class: "installs" }, compact(plan.installs),
        el("small", {}, plan.installs === 1 ? "install" : "installs"))));
  });
}

async function loadLibraries() {
  const { libraries } = await fetch("/api/libraries").then((r) => r.json());
  const box = $("libfilter");
  box.replaceChildren();
  if (!libraries.length) return;
  box.append(el("a", {
    class: "label" + (library ? "" : " more"),
    href: "#",
    onclick: (e) => { e.preventDefault(); library = ""; loadPlans(); },
  }, "all"));
  libraries.forEach((entry) => box.append(el("a", {
    class: "label",
    href: "#",
    onclick: (e) => { e.preventDefault(); library = entry.name; query = ""; loadPlans(); },
  }, `${entry.name} ${entry.plans}`)));
}

async function loadStats() {
  const stats = await fetch("/api/stats").then((r) => r.json());
  if (stats.offline) return;
  $("stats").textContent =
    `${stats.catalog} plans · ${stats.documents} pages cached · ${stats.installs} downloads`;
}

$("tabs").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  [...$("tabs").children].forEach((b) => b.classList.toggle("on", b === button));
  sort = button.dataset.sort;
  loadPlans();
});

let searchTimer;
$("search").addEventListener("input", (event) => {
  clearTimeout(searchTimer);
  query = event.target.value.trim();
  if (query) library = "";
  searchTimer = setTimeout(loadPlans, 220);   // one request per pause, not per keypress
});

/* ------------------------------------------------------------------ the run */

let jobId = null;
const stepNodes = new Map();

function setStep(node, label, done) {
  let item = stepNodes.get(node);
  if (!item) {
    item = el("li", { class: "active" }, el("span", { class: "mark" }, "▸"), el("span", {}, label));
    stepNodes.set(node, item);
    $("steps").append(item);
  }
  if (done) {
    item.classList.remove("active");
    item.firstChild.textContent = "✓";
  }
}

async function answer(questionId, value) {
  $("question").replaceChildren();
  const response = await fetch(`/api/runs/${jobId}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question_id: questionId, answer: value }),
  });
  if (!response.ok) toast("That question already closed.");
}

function askChoices(question) {
  const picked = {};
  const groups = question.choices.map((choice) => {
    picked[choice.slot] = choice.recommended || (choice.options[0] || {}).name || "";
    const custom = el("input", { type: "text", placeholder: "…or type another package name" });
    custom.addEventListener("input", () => {
      if (!custom.value.trim()) return;
      picked[choice.slot] = custom.value.trim();
      [...options.children].forEach((l) => l.classList.remove("sel"));
    });
    const options = el("div", { class: "choice-opts" },
      choice.options.map((option) => {
        const label = el("label", {
          class: option.name === picked[choice.slot] ? "sel" : "",
          onclick: () => {
            picked[choice.slot] = option.name;
            custom.value = "";
            [...options.children].forEach((l) => l.classList.toggle("sel", l === label));
          },
        },
          el("span", { class: "nm" }, option.name),
          el("span", { class: "note" }, option.note || ""),
          option.name === choice.recommended ? el("span", { class: "tag-rec" }, "suggested") : null);
        return label;
      }));
    return el("div", { class: "choice-group" },
      el("div", { class: "slot" }, choice.slot),
      choice.reason ? el("div", { class: "q-help" }, choice.reason) : null,
      options, custom);
  });

  $("question").replaceChildren(el("div", { class: "question" },
    el("div", { class: "q-title" }, "Your requirement leaves some choices open"),
    el("div", { class: "q-help" }, "Pick the packages to plan around, or type your own."),
    groups,
    el("div", { class: "row" },
      el("button", { class: "primary", onclick: () => answer(question.id, picked) }, "Use these"),
      el("button", { class: "ghost", onclick: () => answer(question.id, {}) }, "Decide for me"))));
}

function askDocUrls(question) {
  const inputs = new Map();
  const rows = question.libraries.map((lib) => {
    const input = el("input", { type: "text", placeholder: "https://… (optional, space-separated for several)" });
    inputs.set(lib.name, input);
    return el("div", { class: "pin-row" },
      el("div", {}, el("span", { class: "lib" }, lib.name),
        el("span", { class: "why" }, lib.reason || lib.ecosystem || "")),
      input);
  });
  const extra = el("textarea", { placeholder: "Anything else? One per line. Prefix to group: auth=https://…" });

  const submit = () => {
    const picked = {};
    for (const [name, input] of inputs) {
      const urls = input.value.trim().split(/\s+/).filter((u) => u.startsWith("http"));
      if (urls.length) picked[name] = urls;
    }
    extra.value.split("\n").forEach((line) => {
      const text = line.trim();
      if (!text) return;
      const [head, ...rest] = text.split("=");
      const body = rest.join("=").trim();
      const urls = (body || text).trim().split(/\s+/).filter((u) => u.startsWith("http"));
      if (!urls.length) return;
      // A bare URL still needs a label: it becomes a library of its own downstream.
      const name = body ? head.trim() : new URL(urls[0]).hostname.replace(/^www\./, "");
      picked[name] = (picked[name] || []).concat(urls);
    });
    answer(question.id, picked);
  };

  $("question").replaceChildren(el("div", { class: "question" },
    el("div", { class: "q-title" }, "Pin documentation URLs"),
    el("div", { class: "q-help" },
      "A pinned URL is used as-is — no search, no guessing. Leave blank to let ARK find it."),
    rows,
    el("div", { style: "margin-top:14px" }, extra),
    el("div", { class: "row", style: "margin-top:12px" },
      el("button", { class: "primary", onclick: submit }, "Continue"),
      el("button", { class: "ghost", onclick: () => answer(question.id, {}) }, "Skip"))));
}

function askReview(question) {
  let rows = question.rows.map((row) => ({ ...row, dropped: false }));

  const render = () => {
    const list = rows.map((row, index) => {
      const input = el("input", {
        type: "text", value: row.url,
        oninput: (event) => { row.url = event.target.value; },
      });
      const wrapper = el("div", { class: "url-row" + (row.dropped ? " dropped" : "") },
        el("span", { class: "n" }, String(index + 1)),
        el("span", { class: "lib" }, row.library + (row.primary ? "" : " · alt")),
        input,
        el("button", {
          class: "small ghost",
          onclick: () => { row.dropped = !row.dropped; render(); },
        }, row.dropped ? "keep" : "drop"));
      return wrapper;
    });

    const newLib = el("input", { type: "text", placeholder: "library" });
    const newUrl = el("input", { type: "text", placeholder: "https://…" });
    const kept = rows.filter((row) => !row.dropped && row.url.trim());

    $("question").replaceChildren(el("div", { class: "question" },
      el("div", { class: "q-title" }, `${kept.length} page(s) will be scraped`),
      el("div", { class: "q-help" },
        "This is the last step before anything is fetched. Edit a URL, drop one, or add your own."),
      list,
      el("div", { class: "url-row", style: "margin-top:10px" },
        el("span", { class: "n" }, "+"), newLib, newUrl,
        el("button", {
          class: "small",
          onclick: () => {
            const url = newUrl.value.trim();
            if (!url.startsWith("http")) return toast("That needs to be a URL.");
            rows.push({ library: newLib.value.trim() || new URL(url).hostname, url, primary: false, dropped: false });
            render();
          },
        }, "add")),
      el("div", { class: "row", style: "margin-top:14px" },
        el("button", {
          class: "primary",
          onclick: () => answer(question.id, {
            rows: rows.filter((r) => !r.dropped && r.url.trim())
              .map(({ library, url, primary }) => ({ library, url, primary })),
          }),
        }, `Scrape ${kept.length} page(s)`),
        el("button", { class: "ghost", onclick: () => answer(question.id, { cancel: true }) }, "Cancel run"))));
  };
  render();
}

function showResult(data) {
  const labels = (data.libraries || []).map((name) => el("span", { class: "label" }, name));
  $("outcome").replaceChildren(el("div", { class: "panel", style: "margin-top:18px" },
    el("div", { class: "row between" },
      el("div", {},
        el("div", { style: "font-size:20px;font-weight:600;letter-spacing:-0.02em" }, data.name),
        el("div", { class: "labels" }, labels)),
      el("div", { class: "row" },
        el("a", { href: `/plan/${data.slug}` }, el("button", {}, "Open")),
        el("a", { href: data.published ? `/api/plans/${data.slug}/download` : `/api/runs/${jobId}/plan.md`,
                  download: `${data.slug}-plan.md` },
          el("button", { class: "primary" }, "Download .md")))),
    (data.errors || []).length
      ? el("div", { class: "q-help", style: "margin-top:12px;color:var(--warn)" },
          `${data.errors.length} warning(s): ${data.errors[0]}`)
      : null,
    !data.published
      ? el("div", { class: "q-help", style: "margin-top:12px" },
          "Not catalogued — MongoDB is offline, so this plan lives on disk only.")
      : null));
  loadPlans();
  loadStats();
}

function listen() {
  const source = new EventSource(`/api/runs/${jobId}/events`);
  source.onmessage = (message) => {
    const data = JSON.parse(message.data);
    switch (data.event) {
      case "status": setStep("start", data.step); break;
      case "step": {
        [...stepNodes.entries()].forEach(([key, node]) => {
          if (node.classList.contains("active")) setStep(key, null, true);
        });
        setStep(data.node, data.label);
        break;
      }
      case "resolved":
        $("steps").append(el("li", {}, el("span", { class: "mark" }, "·"),
          el("span", {}, "Using " + data.choices.join(", "))));
        break;
      case "note":
        $("steps").append(el("li", {}, el("span", { class: "mark" }, "·"), el("span", {}, data.text)));
        break;
      case "question":
        if (data.kind === "choices") askChoices(data);
        else if (data.kind === "doc_urls") askDocUrls(data);
        else if (data.kind === "review") askReview(data);
        break;
      case "done":
        stepNodes.forEach((node, key) => setStep(key, null, true));
        showResult(data);
        source.close();
        $("go").disabled = false;
        break;
      case "error":
        $("question").replaceChildren();
        $("outcome").replaceChildren(el("div", { class: "panel", style: "margin-top:18px;border-color:var(--danger)" },
          el("div", { style: "color:var(--danger)" }, data.message)));
        source.close();
        $("go").disabled = false;
        break;
    }
  };
  source.onerror = () => { source.close(); $("go").disabled = false; };
}

$("go").addEventListener("click", async () => {
  const requirement = $("requirement").value.trim();
  if (requirement.length < 8) return toast("Describe what you want to build first.");
  $("go").disabled = true;
  $("run").hidden = false;
  $("steps").replaceChildren();
  $("question").replaceChildren();
  $("outcome").replaceChildren();
  stepNodes.clear();
  $("running-req").textContent = requirement;

  const response = await fetch("/api/runs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      requirement,
      ask_choices: $("opt-choices").checked,
      ask_urls: $("opt-urls").checked,
      review: $("opt-review").checked,
      use_cache: $("opt-cache").checked,
      max_alternates: Number($("opt-alts").value),
    }),
  });
  if (!response.ok) {
    $("go").disabled = false;
    return toast("Could not start the run.");
  }
  jobId = (await response.json()).job_id;
  // Clear the box: the run is now shown below with its own copy of the requirement,
  // and leaving the text sitting there invites a second identical (billable) run.
  $("requirement").value = "";
  history.replaceState(null, "", `?job=${jobId}`);
  listen();
});

/* Rejoin a run already in progress (a reload, or a link someone kept). */
async function resume() {
  const wanted = new URLSearchParams(location.search).get("job");
  if (!wanted) return;
  const response = await fetch(`/api/runs/${wanted}`);
  if (!response.ok) return history.replaceState(null, "", location.pathname);

  const state = await response.json();
  jobId = wanted;
  $("run").hidden = false;
  $("running-req").textContent = state.requirement;
  setStep("resumed", `Rejoined run ${wanted}`, true);

  if (state.status === "done") return showResult(state.result);
  if (state.status === "error") {
    return $("outcome").replaceChildren(el("div", { class: "panel", style: "margin-top:18px;border-color:var(--danger)" },
      el("div", { style: "color:var(--danger)" }, state.error)));
  }
  $("go").disabled = true;
  // A question asked before this tab attached is not replayed on the stream, so it
  // is rendered from the status payload instead.
  if (state.question) {
    const question = state.question;
    if (question.kind === "choices") askChoices(question);
    else if (question.kind === "doc_urls") askDocUrls(question);
    else if (question.kind === "review") askReview(question);
  }
  listen();
}

resume();

loadPlans();
loadLibraries();
loadStats();
