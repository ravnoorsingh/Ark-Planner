---
library: "elasticsearch"
query: "Build a job board API with search, background email digests and a vector database for semantic matching. Use qdrant-client for the vector database. Use elasticsearch for the search. Use celery for the task queue."
url: "https://elasticsearch-py.readthedocs.io/"
resolved_url: "https://elasticsearch-py.readthedocs.io/en/stable/"
role: "primary"
rank: 0
fetched_at: "2026-08-20T18:31:23.431834+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "0b9e8dd661fab6da28cf72c842c59f71290ddb0b42727ae16af4d894477a6e18"
---

# Python Elasticsearch Client

Welcome to the API documentation of the official Python client for Elasticsearch! The goal of this client is to provide common ground for all Elasticsearch-related code in Python; because of this it tries to be opinion-free and very extendable.

High-level documentation for this client is [also available](https://www.elastic.co/docs/reference/elasticsearch/clients/python) .

* [Elasticsearch API](es_api.html)
  + [Elasticsearch](api/elasticsearch.html)
  + [Async Search](api/async-search.html)
  + [Autoscaling](api/autoscaling.html)
  + [Cat](api/cat.html)
  + [Cross-Cluster Replication (CCR)](api/ccr.html)
  + [Cluster](api/cluster.html)
  + [Connector](api/connector.html)
  + [Dangling Indices](api/dangling-indices.html)
  + [Enrich Policies](api/enrich-policies.html)
  + [Event Query Language (EQL)](api/eql.html)
  + [ES|QL](api/esql.html)
  + [Fleet](api/fleet.html)
  + [Graph Explore](api/graph-explore.html)
  + [Index Lifecycle Management (ILM)](api/index-lifecycle-management.html)
  + [Indices](api/indices.html)
  + [Inference](api/inference.html)
  + [Ingest Pipelines](api/ingest-pipelines.html)
  + [License](api/license.html)
  + [Logstash](api/logstash.html)
  + [Migration](api/migration.html)
  + [Machine Learning (ML)](api/ml.html)
  + [Monitoring](api/monitoring.html)
  + [Nodes](api/nodes.html)
  + [Project](api/project.html)
  + [Query rules](api/query-rules.html)
  + [Rollup Indices](api/rollup-indices.html)
  + [Search Applications](api/search-application.html)
  + [Searchable Snapshots](api/searchable-snapshots.html)
  + [Security](api/security.html)
  + [Shutdown](api/shutdown.html)
  + [Simulate](api/simulate.html)
  + [Snapshot Lifecycle Management (SLM)](api/snapshot-lifecycle-management.html)
  + [Snapshots](api/snapshots.html)
  + [Snapshottable Features](api/snapshottable-features.html)
  + [SQL](api/sql.html)
  + [Streams](api/streams.html)
  + [Synonyms](api/synonyms.html)
  + [TLS/SSL](api/tls-ssl.html)
  + [Tasks](api/tasks.html)
  + [Text Structure](api/text-structure.html)
  + [Transforms](api/transforms.html)
  + [Watcher](api/watcher.html)
  + [X-Pack](api/x-pack.html)
* [ES|QL Query Builder](esql.html)
  + [Commands](esql.html#commands)
  + [Functions](esql.html#module-elasticsearch.esql.functions)
* [DSL](dsl.html)
  + [Search](dsl.html#search)
  + [Multi-Search](dsl.html#multi-search)
  + [Document](dsl.html#document)
  + [Index](dsl.html#index)
  + [Mapping](dsl.html#mapping)
  + [Faceted Search](dsl.html#faceted-search)
  + [Update by Query](dsl.html#update-by-query)
* [Helpers](api_helpers.html)
  + [Streaming Bulk](api_helpers.html#streaming-bulk)
  + [Parallel Bulk](api_helpers.html#parallel-bulk)
  + [Bulk](api_helpers.html#bulk)
  + [Dense Vector packing](api_helpers.html#dense-vector-packing)
  + [Scan](api_helpers.html#scan)
  + [Reindex](api_helpers.html#reindex)
* [Exceptions & Warnings](exceptions.html)
  + [API Errors](exceptions.html#api-errors)
  + [Transport and Connection Errors](exceptions.html#transport-and-connection-errors)
  + [Warnings](exceptions.html#warnings)

Async

* [Async Elasticsearch API](async_es_api.html)
  + [Elasticsearch](async_es_api.html#elasticsearch)
* [Async DSL](async_dsl.html)
  + [Search](async_dsl.html#search)
  + [Multi-Search](async_dsl.html#multi-search)
  + [Document](async_dsl.html#document)
  + [Index](async_dsl.html#index)
  + [Mapping](async_dsl.html#mapping)
  + [Faceted Search](async_dsl.html#faceted-search)
  + [Update by Query](async_dsl.html#update-by-query)
* [Async Helpers](async_api_helpers.html)
  + [Streaming Bulk](async_api_helpers.html#streaming-bulk)
  + [Bulk](async_api_helpers.html#bulk)
  + [Scan](async_api_helpers.html#scan)
  + [Reindex](async_api_helpers.html#reindex)

## License

Copyright 2023 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.

## Indices and tables

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)
