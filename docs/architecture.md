# Pipeline architecture

Traced with a real run. The query:

> Build a production RAG service that ingests PDF manuals, chunks and embeds them
> into **a vector database**, and exposes a FastAPI endpoint that answers questions
> with citations back to the source page. Use pypdf for extraction, LangChain for the
> retrieval chain and Pydantic models for request and response validation. Include
> streaming responses and health checks.

Which produced 6 libraries, 11 scraped pages (100 KB), and a 17 KB plan with 11
citations — for **15 LLM calls**.

```mermaid
flowchart TD
    Q["🧑 Query<br/><i>“…embeds them into a vector database…”</i>"]

    subgraph resolve ["① Resolve ambiguity · 1 LLM call"]
        DC["detect_choices<br/><small>finds capabilities named without a package</small>"]
        ASK{{"vector database?<br/>1 qdrant-client · 2 chromadb<br/>3 weaviate · 4 pinecone-client<br/>o. type your own"}}
        DC --> ASK
    end

    subgraph discover ["② Discover · 1 + N LLM calls"]
        PL["parse_libraries<br/><small>prose → package names</small>"]
        SD["search_docs<br/><small>MCP tool, no LLM</small>"]
        CL["curate_links<br/><small>N calls · picks the official URL</small>"]
        PL --> SD --> CL
    end

    subgraph fetch ["③ Fetch · 0 LLM calls"]
        SC["scrape_docs<br/><small>one batch trigger, one poll loop</small>"]
        ST[("data/&lt;library&gt;-&lt;query&gt;/<br/>markdown + raw JSON")]
        SC --> ST
    end

    subgraph plan ["④ Plan · N + 1 LLM calls"]
        DI["distill × N<br/><small>map: docs → LibraryBrief</small>"]
        SY["synthesize<br/><small>reduce: briefs → phases</small>"]
        RE["render_plan<br/><small>formats the model's output;<br/>attaches verifiable Sources</small>"]
        DI --> SY --> RE
    end

    FC(["🔥 Firecrawl MCP<br/>firecrawl_search"])
    BD(["🌐 Bright Data<br/>Scraper Studio"])
    GQ(["🧠 Groq · gpt-oss-120b"])

    Q --> DC
    ASK -->|"user picks 4 → requirement rewritten:<br/>“Use pinecone-client for the vector database.”"| PL

    SD <-->|"5 hits per library"| FC
    SC <-->|"POST /dca/trigger · GET /dca/dataset"| BD

    CL -->|"6 doc_sources<br/>+ filtered alternates"| SC
    ST -->|"11 pages · 100 KB"| DI
    RE --> OUT["📄 plan.md<br/><small>17 KB · 78% model-written<br/>6 phases · 11 citations</small>"]

    DC -.-> GQ
    PL -.-> GQ
    CL -.-> GQ
    DI -.-> GQ
    SY -.-> GQ

    classDef llm fill:#eef2ff,stroke:#4f46e5,color:#1e1b4b
    classDef nollm fill:#ecfdf5,stroke:#059669,color:#064e3b
    classDef ext fill:#fff7ed,stroke:#ea580c,color:#7c2d12
    classDef io fill:#f8fafc,stroke:#475569,color:#0f172a

    class DC,PL,CL,DI,SY llm
    class SD,SC,RE nollm
    class FC,BD,GQ ext
    class Q,OUT,ST,ASK io
```

Blue = makes an LLM call. Green = makes none. Orange = an external service.

**The plan itself is written by the model.** `synthesize` produces the overview,
phases and tasks; `distill` produces the per-library reference. Measured on this run,
**78% of `plan.md` is model-written prose and code**. What `render_plan` adds is the
formatting and the Sources table — the part the model is deliberately not trusted with.

## What happens at each step

| Stage | Calls | Input → Output |
|---|---|---|
| `detect_choices` | 1 | requirement → open capability slots with candidate packages |
| `parse_libraries` | 1 | requirement → `fastapi, pypdf, langchain, pydantic, pinecone-client, uvicorn` |
| `search_docs` | **0** | each library → 5 candidate URLs from Firecrawl |
| `curate_links` | **N** | 5 candidates → 1 official URL + confidence + alternates |
| `scrape_docs` | **0** | 11 URLs → 100 KB of markdown in `data/` |
| `distill` | **N** | one library's pages → `LibraryBrief` (install, APIs, gotchas) |
| `synthesize` | 1 | all briefs → ordered phases with `[^key]` markers |
| `render_plan` | **0** | draft + briefs → `plan.md` markdown + Sources table |

**Total: `2N + 3`.** Six libraries → 15 calls.

## Why two stages use no LLM

`search_docs` and `scrape_docs` are deterministic. We already know what to search for
(`"<library> official documentation"`) and exactly which URLs to fetch, so a model in
the loop would add cost and nondeterminism without adding judgment. The model is used
only where judgment is genuinely needed: choosing *which* result is the real
documentation, and condensing what it says.

## Why planning is map-reduce

The corpus does not fit in one context window — this run scraped 100 KB, and wide
queries reach ~500 KB, against a ~12 KB per-request budget. So each library is
distilled independently (**map**), then one call writes the plan from the briefs alone
(**reduce**). The synthesis step never sees the raw pages.

## Who writes what

The model writes the plan; code assembles and verifies it.

| Part of `plan.md` | Written by | Share of this run |
|---|---|---|
| Overview, phases, tasks, pitfalls, API reference | **the model** | **78%** |
| `## Sources` table and footnote definitions | code | 18% |
| `## Stack` table structure (values from the model) | code | 3% |

The `[^key]` markers *inside* the prose are the model's — it decides which claim rests
on which source. The footnote **definitions** are not: `render_plan` builds them from
the documents actually stored on disk, so a marker can only ever resolve to a page that
was really scraped, and each entry carries the URL, local path and sha256 of the exact
snapshot. Unreferenced sources are dropped, so the table never overstates the grounding.

That split is the point: the model is trusted to write, and not trusted to say where
its claims came from.

## Seeing a run

With `LANGSMITH_TRACING=true`, one CLI invocation is one LangSmith trace. The stages
below map onto spans: LangGraph emits one per node, and `ark/tracing.py` fills in the
non-LangChain work (Bright Data, the store, HTML cleaning, plan rendering) so the
timeline has no gaps.

The decisions worth reading are attached as span metadata rather than logged:
`parse_libraries` records what the model proposed versus what survived deduplication,
`curate_one_library` records the URL chosen and whether a guard had to override it,
`groq.invoke` records how many retries a rate limit cost, and `distill_library` records
the budget each 413 forced it to halve. See the Tracing section of the README for the
tree and for what is redacted before upload.

## Re-running cheaply

`ark plan <artifact.json>` re-enters at stage ④ using the already-stored pages:
**N + 1 calls**, no Firecrawl credits, no Bright Data records. That is the loop to use
when tuning plan quality or recovering from a truncated run.
