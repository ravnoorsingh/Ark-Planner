---
library: "chromadb"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, LangChain for the retrieval chain, ChromaDB for storage, and Pydantic models for request and response validation. Include streaming responses and health checks. Use openai for the embedding model."
url: "https://www.trychroma.com"
role: "primary"
rank: 0
fetched_at: "2026-08-18T08:56:28.853382+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "0c56b145d8c1fcd9167535c1e6f4d2249103c3418a19a1c4ff4d5655fcabfdfc"
---

# Open-source search infrastructure for AI

## Fast, serverless, and scalable infrastructure supporting vector, full-text, regex, and metadata search. Built on object storage and trusted by millions of developers. Open-source Apache 2.0.

Or,  [get started locally](https://docs.trychroma.com/docs/overview/getting-started) .

![Capital One Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcapital-one.0k44g0j369u2l.png&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

[![Mintlify Logo](/_next/static/media/mintlify.0dw6~ty-vnd-z.svg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Read case study →](/customers/mintlify-case-study)

![UnitedHealthcare Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fuhc.018kwqkts6v0k.png&w=1920&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

![Conduit Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fconduit.04_5ewp9e~3_d.png&w=1200&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

[![Propel Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fpropel.0~5lggt__r80y.png&w=1920&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Read case study →](/customers/propel-ai-case-study)

![Cofounder Logo](/_next/static/media/cofounder.0w9-1nc5fc23b.svg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

![Weights & Biases Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fwandb.0.b5gqy_nti~v.png&w=1080&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

![Medwise Logo](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fmedwise.0ebwh~7j9~-8s.png&w=2048&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

AI App

Ask a question

Chroma

knowledge\_base -  1,277,467  records

awaiting query input

15M+ monthly downloads

Apache 2.0
 27k Github stars

Low latency  search

Fast queries over billions of multi-tenant indexes.

Up to 10x  cheaper

Built on object storage with automatic data tiering.

No engineering ops

Scales with your data and traffic. SOC 2 Type II.

Features

◇

Sparse vector search

Lexical search (BM25, SPLADE)

◆

Vector search

Semantic similarity search

●

Full-text search

Trigram and regex search

◐

Metadata search

Filtering and faceted search

◊

Forking

Dataset versioning, A/B testing, and roll-outs

▣

CLI

Command-line tools for development

```
// configure client and collection for sparse embeddings (BM25, SPLADE)

// Add documents with sparse embeddings (BM25)
await collection.add({
  ids: ["id1", "id2"],
  documents: ["Document about databases", "ML tutorial"]
})

// Query with sparse vector
const sparseRank = Knn({ query: "ML", key: "sparse_embedding" });

// Build and execute search
const search = new Search()
  .rank(sparseRank)
  .limit(10)
  .select(K.DOCUMENT, K.SCORE);

const results = await collection.search(search);
```

Terminal Output

```
$ node sparse-search.js
Connecting to Chroma...
✓ Connected successfully
Creating collection 'my_collection'...
✓ Collection created

Adding documents with sparse embeddings (BM25)...
✓ Added 2 documents

Querying with sparse vector...
✓ Query completed in 18ms

Results (ranked by BM25 score):
[
  {
    id: "id1",
    document: "Document about databases",
    score: 0.87,
    metadata: {}
  },
  {
    id: "id2",
    document: "ML tutorial",
    score: 0.45,
    metadata: {}
  }
]
```

Performance

Fast search over billions of multi-tenant indexes

Chroma's indexes are built and optimized for object-storage offering unparalleled cost and performance. State-of-the-art vector, full-text, and regex search.

Latency

Query Latency

@384 dim at 100k vectors

Warm

Cold

p50

20ms

650ms

p90

27ms

1.2s

p99

57ms

1.5s

[Contact us](/talk-with-us)  to run a POC for your specific workload.
 Dedicated clusters can be scaled to your specific requirements.

Technical specs

Write throughput (per collection) 30 MB/s (2000+ QPS)

Concurrent reads (per collection) 10 (200+ QPS)

Collections per database 1M

Records per collection 5M

Recall 90-100%

Zero-ops infra

```
┌───────────────────────────────┐
│ Query Layer                   │
│   Fast memory cache (hot)     │
│   SSD cache (warm)            │
└───────────────────────────────┘

↕ Intelligent tiering

┌───────────────────────────────┐
│ Storage Layer                 │
│   S3 / GCS (cold)             │
│     • All vectors             │
│     • All metadata            │
│     • All indexes             │
└───────────────────────────────┘
```

Unlike legacy search systems, Chroma is a database you'll want to be on-call for.

✓ Auto-scales with usage

✓ No manual tuning

✓ Serverless pricing

Chroma takes full advantage of object storage with automatic query-aware data tiering and caching.

✓ Vectors are large: 1GB text → 15GB of vectors

✓ Memory is expensive: $5/GB/mo

✓ Object storage is not: $0.02/GB/mo

Enterprise

Chroma brings the security, compliance, education and operational model enterprises need with our Apache 2.0 architecture.

BYOC in your VPC, multi-cloud/multi-region replication, point-in-time-recovery ensure a resilient and scalable search system with the same 0-ops story as Cloud.

Contact us

## Hidden

```
 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
 ▓░                                         ░▓
 ▓░  ┌──────────── YOUR VPC ─────────────┐  ░▓
 ▓░  │                                   │  ░▓
 ▓░  │   █ DATA PLANE █
                  │  ░▓
 ▓░  │                                   │  ░▓
 ▓░  │   Your data, your cloud           │  ░▓
 ▓░  │                                   │  ░▓
 ▓░  │                                   │  ░▓
 ▓░  └───────────────────────────────────┘  ░▓
 ▓░                    │
                    ░▓
 ▓░                    │
                    ░▓
 ▓░                    ▼
                    ░▓
 ▓░  ═════════════════════════════════════
  ░▓
 ▓░  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░▓
 ▓░                                         ░▓
 ▓░  ┌────────── CHROMA VPC ─────────────┐  ░▓
 ▓░  │                                   │  ░▓
 ▓░  │   █ CONTROL PLANE █
               │  ░▓
 ▓░  │                                   │  ░▓
 ▓░  │   Managed by Chroma               │  ░▓
 ▓░  │   Monitoring, backups, ops        │  ░▓
 ▓░  │                                   │  ░▓
 ▓░  └───────────────────────────────────┘  ░▓
 ▓░                                         ░▓
 ▓░  ✓ BYOC in your VPC                     ░▓
 ▓░  ✓ Multi-region replication             ░▓
 ▓░  ✓ 0-ops management                     ░▓
 ▓░                                         ░▓
 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```

[▶] Videos

[![Deep dive: Using Reranking to improve search results](/img/video_thumbs/reranking.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Deep dive: Using Reranking to improve search results

15:23](https://www.youtube.com/watch?v=FHXRWwpQYY8) [![Chroma Context-1](/img/video_thumbs/context-1.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Chroma Context-1

13:20](https://www.youtube.com/watch?v=4sAJLLWPAh4) [![Lexical Search in Chroma](/img/video_thumbs/lexical-search.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Lexical Search in Chroma

4:41](https://www.youtube.com/watch?v=XHEgXDff2xw) [![Schema() and Search() APIs](/img/video_thumbs/schema-search-apis.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Schema() and Search() APIs

9:02](https://www.youtube.com/watch?v=EtUjXsowN_4) [![Context Engineering Episode 3 - Lance Martin - LangChain](/img/video_thumbs/context-eng-ep3.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Engineering Episode 3 - Lance Martin - LangChain

1:02:36](https://www.youtube.com/watch?v=MJScoDgIcXg) [![Beyond The Embedding: Vector Indexing](/img/video_thumbs/vectorindexing.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Beyond The Embedding: Vector Indexing

11:26](https://youtu.be/1QdwYWd3S1g) [![Long live Context Engineering](/img/video_thumbs/ragisdead.png?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Long live Context Engineering

57:00](https://www.youtube.com/watch?v=pIbIZ_Bxl_g) [![Context Rot](/img/video_thumbs/context-rot.jpg?v=1&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Rot

7:55](https://youtu.be/TUjQuC4ugak) [![Context Engineering: The Outer Loop ](/img/video_thumbs/outer-loop.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Engineering: The Outer Loop

23:43](https://youtu.be/vsfbplnJyA8) [![Context Engineering for Engineers ](/img/video_thumbs/context-eng.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Engineering for Engineers

11:16](https://youtu.be/L8ZM78APDPk) [![Reliability at Scale](/img/video_thumbs/reliability.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Reliability at Scale

26:30](https://youtu.be/XVFevYxRKAE) [![Context Engineering with DSPy](/img/video_thumbs/dspy.jpg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Engineering with DSPy

12:46](https://youtu.be/1I9PoXzvWcs) [See more

Visit our YouTube channel →](https://youtube.com/@trychroma)

[●] Open source community

Open-source databases give your team the control and flexibility to build exactly what you need. No licensing limits, no vendor lock-in, just reliable performance backed by a large community.

[Github →](https://github.com/chroma-core/chroma)

Chroma has over 26k GitHub stars and is used in over 90k other open-source codebases on GitHub. It is downloaded over 11M times a month.

[Discord →](https://discord.gg/MMeYNTmh3x)

Join the Discord to see what people are building!

[Social →](https://twitter.com/trychroma)

Find the greater community on  [X](https://x.com/trychroma)  and  [YouTube.](https://www.youtube.com/@trychroma)

[Run Chroma OSS →](https://docs.trychroma.com/deployment)

Run Chroma on your own infrastructure with our open-source deployment guides.

[◆] Support

[Open-source →](https://discord.gg/MMeYNTmh3x)

Join our 10K person strong Discord community to get fast and expert help from the open-source community.

[All plans →](/pricing)

Helpful support direct from engineers on the Chroma team

[Pro plan →](/pricing)

Direct Slack communication for fast support and help designing and iterating your search system.

[Enterprise plan →](/enterprise)

Customized SLAs ensure your team gets 24/7 assistance.

[▲] Research

Our research spans both basic and applied research for search, retrieval, agents, and context engineering.

[![Context-1](/_next/image?url=%2Fimg%2Fcontext_1%2Fhero.jpg&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context-1

Training a self-editing search agent.](/research/context-1) [![Context Rot](/_next/image?url=%2Fimg%2Fcontext_rot%2Fheader_plot.jpg&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Context Rot

How increasing input tokens impacts LLM performance.](/research/context-rot) [![Generative Benchmarking](/_next/image?url=%2Fimg%2Fgenerative_benchmarking%2Fart.jpg&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Generative Benchmarking

New methods for evaluating retrieval systems.](/research/generative-benchmarking) [![Chunking Strategies](/_next/image?url=%2Fimg%2Fevaluating_chunking%2Fheader_plot.jpg&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Chunking Strategies

Evaluating chunking strategies in retrieval for AI.](/research/evaluating-chunking) [![Embedding Adapters](/_next/image?url=%2Fimg%2Fembedding_adapters%2Fheader_plot.jpg&w=3840&q=75&dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

Embedding Adapters

Lightweight transforms to boost embedding accuracy.](/research/embedding-adapters)

[■] Updates

Chroma's project is rapidly improving. Here are the latest updates.

[Chroma Cloud Sync

Serverless data ingestion for Chroma Cloud.

Mar 2026](/changelog/chroma-sync-s3-github-and-web) [Metadata Arrays

Store arrays of strings, numbers, and booleans in metadata.

Feb 2026](/changelog/metadata-arrays) [Indexing Status

Monitor real-time indexing progress of your collections.

Jan 2026](/changelog/indexingstatus) [Read Level

Control read consistency with index-only or full read modes.

Jan 2026](/changelog/readlevel) [Private Networking

Secure connectivity with AWS PrivateLink support.

Jan 2026](/changelog/private-networking) [GroupBy

Group and aggregate search results by metadata keys.

Jan 2026](/changelog/groupby) [Customer-Managed Encryption Keys

Encrypt your data with your own encryption keys.

Dec 2025](/changelog/cmek) [Chroma Web Sync

Automatically crawl, scrape, chunk and embed web pages.

Nov 2025](/changelog/chroma-web-sync) [Sparse Vector Search

First class support for BM25 and SPLADE vectors.

Oct 2025](project/sparse-vector-search) [Introducing Chroma Sync

Automatically chunk, embed, and index GitHub repos.

Oct 2025](/changelog/introducing-chroma-sync) [wal3: Chroma's Write-Ahead Log

A Write-Ahead Log for Chroma, Built on Object Storage

Sep 2025](engineering/wal3) [Package Search MCP

Query thousands of open-source repos through MCP.

Sep 2025](/changelog/package-search-mcp) [Collection Forking

Fast duplication of collections with copy-on-write.

Aug 2025](/changelog/forking) [Introducing Chroma Cloud

Chroma Cloud is now generally available.

Aug 2025](/changelog/introducing-chroma-cloud) [Designing a query execution engine

A push-based, morsel-driven execution engine in Rust.

Aug 2025](engineering/execution-engine) [70% Data Throughput Increase

Performance boost using base64 vector encoding.

Jul 2025](/changelog/base64-data-throughput) [Regex Search Support

Search using regular expressions with new operators.

Jun 2025](/changelog/regex) [JavaScript Client V3

Complete rewrite with reduced bundle size.

Jun 2025](/changelog/js-client-v3)

We’re looking for curious people who are dedicated to becoming world-class at their craft to join our team.

![separator](/img/street.jpg)

Get started

Get up and running in 30 seconds or less with $5 in free credits.

Quick Start

Python  [Python  getting started docs →](https://docs.trychroma.com/docs/overview/getting-started)

`pip install chromadb`

JavaScript / TypeScript  [JavaScript / TypeScript  getting started docs →](https://docs.trychroma.com/docs/overview/getting-started#typescript)

`npm install chromadb`

[View full documentation →](https://docs.trychroma.com/docs/overview/introduction)

![Chroma logo](/_next/static/media/chroma-wordmark.0~1c352v-zy35.svg?dpl=dpl_8qN7e7VzL2Aabhf2CmxsYzGtzgog)

©  2026

### Product

[Database](/products/chromadb) [Sync](/products/sync) [Enterprise](/enterprise) [Package Search MCP](/package-search) [Docs](https://docs.trychroma.com) [Status](https://status.trychroma.com) [Contact](mailto:hello@trychroma.com)

### Follow

[GitHub](https://github.com/chroma-core/chroma) [X](https://x.com/trychroma) [YouTube](https://www.youtube.com/@trychroma)

### Company

[About](https://docs.trychroma.com/docs/overview/introduction) [Changelog](/changelog) [Careers](/careers)

### Legal

[Privacy](/website-privacy) [Terms](/website-terms) [Security](/security) [DPA](/dpa)
