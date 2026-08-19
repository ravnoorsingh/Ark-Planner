---
library: "pinecone-client"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, LangChain for the retrieval chain and Pydantic models for request and response validation. Include streaming responses and health checks. Use pinecone-client for the vector database."
url: "https://docs.pinecone.io/reference/sdks/python/overview"
role: "primary"
rank: 0
fetched_at: "2026-08-18T11:02:12.015424+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "bf8ce181578e5fc0d38d209d90b99c3e97900a6d399ddae1a62fd76277a2d13d"
---

For installation instructions, usage examples, and reference information, see the [Pinecone Python SDK documentation](https://sdk.pinecone.io/python/) . To report an issue or request a feature, [file an issue on GitHub](https://github.com/pinecone-io/pinecone-python-client/issues) .

 The Pinecone Python SDK is distributed on PyPI using the package name `pinecone` . By default, the `pinecone` package has a minimal set of dependencies and interacts with Pinecone via HTTP requests. However, you can install the following extras to unlock additional functionality:

* `pinecone[grpc]` adds dependencies on `grpcio` and related libraries needed to run data operations such as upserts and queries over [gRPC](https://grpc.io/) for a modest performance improvement.
* `pinecone[asyncio]` adds a dependency on `aiohttp` and enables usage of `async` methods for use with [asyncio](https://docs.python.org/3/library/asyncio.html) . For more details, see [Async requests](#async-requests) .

## [​](#requirements) Requirements

The Pinecone Python SDK requires Python 3.9 or later. It has been tested with CPython versions from 3.9 to 3.13.

## [​](#sdk-versions) SDK versions

 SDK versions are pinned to specific [API versions](/reference/api/versioning) . When a new API version is released, a new version of the SDK is also released.  The mappings between API versions and Python SDK versions are as follows:

| API version | SDK version |
| --- | --- |
| `2025-04` | v7.x |
| `2025-01` | v6.x |
| `2024-10` | v5.3.x |
| `2024-07` | v5.0.x-v5.2.x |
| `2024-04` | v4.x |

When a new stable API version is released, you should upgrade your SDK to the latest version to ensure compatibility with the latest API changes.

## [​](#install) Install

 To install the latest version of the [Python SDK](https://github.com/pinecone-io/pinecone-python-client) , run the following command:

```
# Install the latest version
pip install pinecone

# Install the latest version with gRPC extras
pip install "pinecone[grpc]"

# Install the latest version with asyncio extras
pip install "pinecone[asyncio]"
```

To install a specific version of the Python SDK, run the following command:

pip

```
# Install a specific version
pip install pinecone==<version>

# Install a specific version with gRPC extras
pip install "pinecone[grpc]"==<version>

# Install a specific version with asyncio extras
pip install "pinecone[asyncio]"==<version>
```

To check your SDK version, run the following command:

pip

```
pip show pinecone
```

To use the [Inference API](/reference/api/introduction#inference) , you must be on version 5.0.0 or later.

### [​](#install-the-pinecone-assistant-python-plugin) Install the Pinecone Assistant Python plugin

 As of Python SDK v7.0.0, the `pinecone-plugin-assistant` package is included by default. It is only necessary to install the package if you are using a version of the Python SDK prior to v7.0.0.

HTTP

```
pip install --upgrade pinecone pinecone-plugin-assistant
```

## [​](#upgrade) Upgrade

Before upgrading to `v6.0.0` , update all relevant code to account for the breaking changes explained [here](https://github.com/pinecone-io/pinecone-python-client/blob/main/docs/upgrading.md) .   Also, make sure to upgrade using the `pinecone` package name instead of `pinecone-client` ; upgrading with the latter will not work as of `v6.0.0` .

If you already have the Python SDK, upgrade to the latest version as follows:

```
# Upgrade to the latest version
pip install pinecone --upgrade

# Upgrade to the latest version with gRPC extras
pip install "pinecone[grpc]" --upgrade

# Upgrade to the latest version with asyncio extras
pip install "pinecone[asyncio]" --upgrade
```

## [​](#initialize) Initialize

 Once installed, you can import the library and then use an [API key](/guides/projects/manage-api-keys) to initialize a client instance:

```
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
```

```
from pinecone.grpc import PineconeGRPC as Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
```

 When [creating an index](/guides/index-data/create-an-index) , import the `ServerlessSpec` or `PodSpec` class as well:

```
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key="YOUR_API_KEY")

pc.create_index(
  name="docs-example",
  dimension=1536,
  metric="cosine",
  spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
  )
)
```

```
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import PodSpec

pc = Pinecone(api_key="YOUR_API_KEY")

pc.create_index(
  name="docs-example",
  dimension=1536,
  metric="cosine",
  spec=PodSpec(
    environment="us-west-1-gcp",
    pod_type="p1.x1",
    pods=1
  )
)
```

## [​](#proxy-configuration) Proxy configuration

If your network setup requires you to interact with Pinecone through a proxy, you will need to pass additional configuration using optional keyword parameters:

* `proxy_url` : The location of your proxy. This could be an HTTP or HTTPS URL depending on your proxy setup.
* `proxy_headers` : Accepts a python dictionary which can be used to pass any custom headers required by your proxy. If your proxy is protected by authentication, use this parameter to pass basic authentication headers with a digest of your username and password. The `make_headers` utility from `urllib3` can be used to help construct the dictionary. **Note:** Not supported with Asyncio.
* `ssl_ca_certs` : By default, the client will perform SSL certificate verification using the CA bundle maintained by Mozilla in the  [`certifi`](https://pypi.org/project/certifi/)  package. If your proxy is using self-signed certicates, use this parameter to specify the path to the certificate (PEM format).
* `ssl_verify` : SSL verification is enabled by default, but it is disabled when set to `False` . It is not recommened to go into production with SSL verification disabled.

```
from pinecone import Pinecone
import urllib3
from urllib3.util import make_headers

pc = Pinecone(
    api_key="YOUR_API_KEY",
    proxy_url='https://your-proxy.com',
    proxy_headers=make_headers(proxy_basic_auth='username:password'),
    ssl_ca_certs='path/to/cert-bundle.pem'
)
```

```
from pinecone.grpc import PineconeGRPC as Pinecone
import urllib3
from urllib3.util import make_headers

pc = Pinecone(
    api_key="YOUR_API_KEY",
    proxy_url='https://your-proxy.com',
    proxy_headers=make_headers(proxy_basic_auth='username:password'),
    ssl_ca_certs='path/to/cert-bundle.pem'
)
```

```
import asyncio
from pinecone import PineconeAsyncio

async def main():
    async with PineconeAsyncio(
        api_key="YOUR_API_KEY",
        proxy_url='https://your-proxy.com',
        ssl_ca_certs='path/to/cert-bundle.pem'
    ) as pc:
        # Do async things
        await pc.list_indexes()

asyncio.run(main())
```

## [​](#async-requests) Async requests

 Pinecone Python SDK versions 6.0.0 and later provide `async` methods for use with [asyncio](https://docs.python.org/3/library/asyncio.html) . Asyncio support makes it possible to use Pinecone with modern async web frameworks such as [FastAPI](https://fastapi.tiangolo.com/) , [Quart](https://quart.palletsprojects.com/en/latest/) , and [Sanic](https://sanic.dev/en/) , and should significantly increase the efficiency of running requests in parallel.   Use the  [`PineconeAsyncio`](https://sdk.pinecone.io/python/asyncio.html)  class to create and manage indexes and the  [`IndexAsyncio`](https://sdk.pinecone.io/python/asyncio.html#pinecone.db_data.IndexAsyncio)  class to read and write index data. To ensure that sessions are properly closed, use the `async with` syntax when creating `PineconeAsyncio` and `IndexAsyncio` objects.

```
# pip install "pinecone[asyncio]"
import asyncio
from pinecone import PineconeAsyncio, ServerlessSpec

async def main():
    async with PineconeAsyncio(api_key="YOUR_API_KEY") as pc:
        if not await pc.has_index(index_name):
            desc = await pc.create_index(
                name="docs-example",
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ),
                deletion_protection="disabled",
                tags={
                    "environment": "development"
                }
            )

asyncio.run(main())
```

```
# pip install "pinecone[asyncio]"
import asyncio
from pinecone import Pinecone

async def main():
    pc = Pinecone(api_key="YOUR_API_KEY")
    async with pc.IndexAsyncio(host="INDEX_HOST") as idx:
        await idx.upsert_records(
            namespace="example-namespace",
            records=[
                {
                    "id": "1",
                    "title": "The Great Gatsby",
                    "author": "F. Scott Fitzgerald",
                    "description": "The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
                    "year": 1925,
                },
                {
                    "id": "2",
                    "title": "To Kill a Mockingbird",
                    "author": "Harper Lee",
                    "description": "A young girl comes of age in the segregated American South and witnesses her father's courageous defense of an innocent black man.",
                    "year": 1960,
                },
                {
                    "id": "3",
                    "title": "1984",
                    "author": "George Orwell",
                    "description": "In a dystopian future, a totalitarian regime exercises absolute control through pervasive surveillance and propaganda.",
                    "year": 1949,
                },
            ]
        )

asyncio.run(main())
```

## [​](#query-across-namespaces) Query across namespaces

 Each query is limited to a single [namespace](/guides/index-data/indexing-overview#namespaces) . However, the Pinecone Python SDK provides a `query_namespaces` utility method to run a query in parallel across multiple namespaces in an index and then merge the result sets into a single ranked result set with the `top_k` most relevant results.   The `query_namespaces` method accepts most of the same arguments as `query` with the addition of a required `namespaces` parameter.

* Python SDK without gRPC
* Python SDK with gRPC

When using the Python SDK without gRPC extras, to get good performance, it is important to set values for the `pool_threads` and `connection_pool_maxsize` properties on the index client. The `pool_threads` setting is the number of threads available to execute requests, while `connection_pool_maxsize` is the number of cached http connections that will be held. Since these tasks are not computationally heavy and are mainly i/o bound, it should be okay to have a high ratio of threads to cpus.  The combined results include the sum of all read unit usage used to perform the underlying queries for each namespace.

Python

```
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index(
    name="docs-example",
    pool_threads=50,             # <-- make sure to set these
    connection_pool_maxsize=50,  # <-- make sure to set these
)

query_vec = [ 0.1, ...] # an embedding vector with same dimension as the index
combined_results = index.query_namespaces(
    vector=query_vec,
    namespaces=['ns1', 'ns2', 'ns3', 'ns4'],
    metric="cosine",
    top_k=10,
    include_values=False,
    include_metadata=True,
    filter={"genre": { "$eq": "comedy" }},
    show_progress=False,
)

for scored_vec in combined_results.matches:
    print(scored_vec)
print(combined_results.usage)
```

When using the Python SDK with gRPC extras, there is no need to set the `connection_pool_maxsize` because grpc makes efficient use of open connections by default.

Python

```
from pinecone.grpc import PineconeGRPC

pc = PineconeGRPC(api_key="YOUR_API_KEY")
index = pc.Index(
    name="docs-example",
    pool_threads=50, # <-- make sure to set this
)

query_vec = [ 0.1, ...] # an embedding vector with same dimension as the index
combined_results = index.query_namespaces(
    vector=query_vec,
    namespaces=['ns1', 'ns2', 'ns3', 'ns4'],
    metric="cosine",
    top_k=10,
    include_values=False,
    include_metadata=True,
    filter={"genre": { "$eq": "comedy" }},
    show_progress=False,
)

for scored_vec in combined_results.matches:
    print(scored_vec)
print(combined_results.usage)
```

## [​](#upsert-from-a-dataframe) Upsert from a dataframe

 To quickly ingest data when using the [Python SDK](/reference/sdks/python/overview) , use the `upsert_from_dataframe` method. The method includes retry logic and `batch_size` , and is performant especially with Parquet file data sets.   The following example upserts the `uora_all-MiniLM-L6-bm25` dataset as a dataframe.

Python

```
from pinecone import Pinecone, ServerlessSpec
from pinecone_datasets import list_datasets, load_dataset

pc = Pinecone(api_key="API_KEY")

dataset = load_dataset("quora_all-MiniLM-L6-bm25")

pc.create_index(
  name="docs-example",
  dimension=384,
  metric="cosine",
  spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
  )
)

# To get the unique host for an index,
# see https://docs.pinecone.io/guides/manage-data/target-an-index
index = pc.Index(host="INDEX_HOST")

index.upsert_from_dataframe(dataset.drop(columns=["blob"]))
```

Was this page helpful?

⌘  I
