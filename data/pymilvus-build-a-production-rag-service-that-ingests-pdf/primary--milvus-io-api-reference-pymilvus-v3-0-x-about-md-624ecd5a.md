---
library: "pymilvus"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://milvus.io/api-reference/pymilvus/v3.0.x/About.md"
role: "primary"
rank: 0
fetched_at: "2026-08-19T12:36:05.238478+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "3a452791e02f4205df41029151a77f103725fb5d79af0a61c0843a7f1cb8eeea"
---

[< Docs](/docs)

* [v3.0.x](/api-reference/pymilvus/v3.0.x/About.md)
* [v2.6.x](/api-reference/pymilvus/v2.6.x/About.md)
* [v2.5.x](/api-reference/pymilvus/v2.5.x/About.md)
* [v2.4.x](/api-reference/pymilvus/v2.4.x/About.md)

* Python

  + [About](/api-reference/pymilvus/v3.0.x/About.md)
  + DataImport
  + EmbeddingModels
  + FileResource
  + MilvusClient
  + ORM
  + Rerankers
  + Volume

* [Home](/)
* [Docs](/docs)
* [API Reference](/api-reference/pymilvus/v3.0.x/About.md)
* Python
* About

# About PyMilvus

PyMilvus is a Python SDK of Milvus. Its source code is open-sourced and hosted on [GitHub](https://github.com/milvus-io/pymilvus) .

In this release, you have the flexibility to choose MilvusClient or the original ORM module to talk with Milvus.

## Compatibility

| Milvus version | Recommended PyMilvus version |
| --- | --- |
| 1.0.x | 1.0.1 |
| 1.1.x | 1.1.2 |
| 2.0.x | 2.0.2 |
| 2.1.x | 2.1.3 |
| 2.2.x | 2.2.3 |
| 2.3.x | 2.3.7 |
| 2.4.x | 2.4.15 |
| 2.5.x | 2.5.16 |
| 2.6.x | 2.6.17 |
| 3.0.x | 3.0.1 |

## Install & Update

You can run the following command to install the latest PyMilvus or update your PyMilvus to this version.

```

```

After the installation, you can check the PyMilvus version by running the following

```
from
 pymilvus import
 __version__
print(__version__)
# v3.0.1
```

To install the Model library for embedding operations, run the following command:

```

```

For details, refer to the Model library documents and examples.

## Connect to Milvus

```
from
 pymilvus import
 MilvusClient
# Authentication not enabled

client = MilvusClient("http://localhost:19530")
# Authentication enabled with the root user

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus",
    db_name="default"

)
# Authentication enabled with a non-root user

client = MilvusClient(
    uri="http://localhost:19530",
    token="user:password", # replace this with your token

    db_name="default"

)
```

## Examples

In addition to the documents, you can also refer to the example sets in our GitHub repo.

## Feedback & Issues

If you are having trouble or have questions about PyMilvus, ask your question on our PyMilvus Community Forum. Once you get an answer, it’d be great if you could work it back into this documentation and contribute!

## Contributing

We are committed to building a collaborative, exuberant open-source community for PyMilvus. Therefore, contributions to PyMilvus are welcome from everyone. Refer to [Contributing Guideline](https://github.com/milvus-io/pymilvus/blob/master/CONTRIBUTING.md) before making contributions to this project. You can [file an issue](https://github.com/milvus-io/pymilvus/issues/new/choose) or contact us on [Slack](https://github.com/milvus-io/pymilvus#readme) if you need any assistance or want to propose your ideas about PyMilvus.

## Try Managed Milvus for Free

Zilliz Cloud is hassle-free, powered by Milvus and 10x faster.

 [Get Started](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_right_card&utm_content=api-reference/pymilvus/v3.0.x/About.md)

* [Edit this page](https://github.com/milvus-io/web-content/edit/master/API_Reference/pymilvus/v3.0.x/About.md)
* [Create an issue](https://github.com/milvus-io/web-content/issues/new/choose)

##### Feedback

Was this page helpful?
