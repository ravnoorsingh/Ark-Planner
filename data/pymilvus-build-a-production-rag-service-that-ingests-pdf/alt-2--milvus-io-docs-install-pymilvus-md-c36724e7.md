---
library: "pymilvus"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://milvus.io/docs/install-pymilvus.md"
role: "alternate"
rank: 2
fetched_at: "2026-08-19T12:36:05.483812+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "cfbff0a355d845a89de06fafebd945513ae58dfbc2d1e9d04ef771e0712753be"
---

[Home](/docs)

* [v3.0.x](/docs/install-pymilvus.md)
* [v2.6.x](/docs/v2.6.x/install-pymilvus.md)
* [v2.5.x](/docs/v2.5.x/install-pymilvus.md)
* [v2.4.x](/docs/v2.4.x/install-pymilvus.md)

* About Milvus
* Get Started

  + [Quickstart](/docs/quickstart.md)
  + Install Milvus
  + Install SDKs

    - [PyMilvus](/docs/install-pymilvus.md)
    - [Java SDK](/docs/install-java.md)
    - [Go SDK](/docs/install-go.md)
    - [Node.js SDK](/docs/install-node.md)
  + [Connect to Milvus Server](/docs/connect-to-milvus-server.md)
* Concepts
* User Guide
* Data Import
* AI Tools
* Administration Guide
* Tools
* Integrations
* Tutorials
* FAQs
* API Reference

* [Home](/)
* [Docs](/docs)
* Get Started
* Install SDKs
* PyMilvus

# Install Milvus Python SDK

This topic describes how to install Milvus python SDK pymilvus for Milvus.

Current version of Milvus supports SDKs in Python, Node.js, GO, and Java.

## Requirements

* Python 3.7 or later is required.
* Google protobuf is installed. You can install it with the command `pip3 install protobuf==3.20.0` .
* grpcio-tools is installed. You can install it with the command `pip3 install grpcio-tools` .

## Install PyMilvus via pip

PyMilvus is available in [Python Package Index](https://pypi.org/project/pymilvus/) .

It is recommended to install a PyMilvus version that matches the version of the Milvus server you installed. For more information, see [Release Notes](/docs/release_notes.md) .

```
$ python3 -m pip install pymilvus==3.0.1
```

## Verify installation

If PyMilvus is correctly installed, no exception will be raised when you run the following command.

```
$ python3 -c "from pymilvus import Collection"
```

## What’s next

Having installed PyMilvus, you can:

* Learn the basic operations of Milvus:

  + [Manage Collections](/docs/manage-collections.md)
  + [Manage Partitions](/docs/manage-partitions.md)
  + [Insert, Upsert & Delete](/docs/insert-update-delete.md)
  + [Single-Vector Search](/docs/single-vector-search.md)
  + [Hybrid Search](/docs/multi-vector-search.md)
* Explore [PyMilvus API reference](/api-reference/pymilvus/v3.0.x/About.md)

##### Table of contents

* [Install Milvus Python SDK](#Install-Milvus-Python-SDK)
* [Requirements](#Requirements)
* [Install PyMilvus via pip](#Install-PyMilvus-via-pip)
* [Verify installation](#Verify-installation)
* [What's next](#Whats-next)

## Try Managed Milvus for Free

Zilliz Cloud is hassle-free, powered by Milvus and 10x faster.

 [Get Started](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_right_card&utm_content=docs/install-pymilvus.md)

* [Edit this page](https://github.com/milvus-io/milvus-docs/edit/v3.0.x/site/en/getstarted/install_SDKs/install-pymilvus.md)
* [Create an issue](https://github.com/milvus-io/milvus-docs/issues/new/choose)

##### Feedback

Was this page helpful?
