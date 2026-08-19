---
library: "uvicorn"
query: "Build an MCP server in Python that exposes a company's internal wiki as searchable tools for AI coding agents. Use the official MCP Python SDK with streamable HTTP transport, httpx for the wiki's REST API, and Pydantic for tool input schemas. Support tool listing, full-text search, page fetch by ID, and bearer-token auth."
url: "https://uvicorn.dev"
role: "primary"
rank: 0
fetched_at: "2026-08-17T18:52:39.679227+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "2eb79e0a057bd7feaa67c107c4683108aece3a3e2f4c5f575de77e55fedf3005"
---

# Index

![uvicorn](../../uvicorn.png)

*An ASGI web server, for Python.*

[![Test Suite](https://github.com/Kludex/uvicorn/workflows/Test%20Suite/badge.svg)](https://github.com/Kludex/uvicorn/actions)   [![Package version](https://badge.fury.io/py/uvicorn.svg)](https://pypi.org/project/uvicorn/)   [![Supported Python versions](https://img.shields.io/pypi/pyversions/uvicorn.svg?color=%2334D058)](https://pypi.org/project/uvicorn)   [![Discord](https://img.shields.io/discord/1051468649518616576?logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/RxKUF5JuHs)

---

**Documentation** : <https://uvicorn.dev>

**Source Code** : <https://www.github.com/Kludex/uvicorn>

---

**Uvicorn** is an [ASGI](concepts/asgi/) web server implementation for Python.

Until recently Python has lacked a minimal low-level server/application interface for async frameworks. The [ASGI specification](https://asgi.readthedocs.io/en/latest/) fills this gap, and means we're now able to start building a common set of tooling usable across all async frameworks.

Uvicorn currently supports **HTTP/1.1** and **WebSockets** .

## Sponsorship

Help us keep Uvicorn maintained and sustainable by [becoming a sponsor](https://github.com/sponsors/Kludex) .

**Current sponsors:**

[![FastAPI](img/fastapi-logo.png)](https://fastapi.tiangolo.com)

## Quickstart

**Uvicorn** is available on [PyPI](https://pypi.org/project/uvicorn/) so installation is as simple as:

[pip](#__tabbed_1_1)   [uv](#__tabbed_1_2)

```
pip install uvicorn
```

```
uv add uvicorn
```

See the [installation documentation](installation/) for more information.

---

Let's create a simple ASGI application to run with Uvicorn:

main.py

```
async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain'),
            (b'content-length', b'13'),
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
```

Then we can run it with Uvicorn:

```
uvicorn main:app
```

---

## Usage

The uvicorn command line tool is the easiest way to run your application.

### Command line options

Run `uvicorn --help` to see the full set of command line options.

For more information, see the [settings documentation](settings/) .

### Running programmatically

There are several ways to run uvicorn directly from your application.

#### `uvicorn.run`

If you're looking for a programmatic equivalent of the `uvicorn` command line interface, use `uvicorn.run()` :

main.py

```
import uvicorn

async def app(scope, receive, send):
    ...

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
```

#### `Config` and `Server` instances

For more control over configuration and server lifecycle, use `uvicorn.Config` and `uvicorn.Server` :

main.py

```
import uvicorn

async def app(scope, receive, send):
    ...

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
```

If you'd like to run Uvicorn from an already running async environment, use `uvicorn.Server.serve()` instead:

main.py

```
import asyncioimport uvicorn

async def app(scope, receive, send):
    ...

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

### Running with Gunicorn

Warning

The `uvicorn.workers` module is deprecated and will be removed in a future release.

You should use the  [`uvicorn-worker`](https://github.com/Kludex/uvicorn-worker)  package instead.

```
python -m pip install uvicorn-worker
```

[Gunicorn](https://gunicorn.org/) is a mature, fully featured server and process manager.

Uvicorn includes a Gunicorn worker class allowing you to run ASGI applications, with all of Uvicorn's performance benefits, while also giving you Gunicorn's fully-featured process management.

This allows you to increase or decrease the number of worker processes on the fly, restart worker processes gracefully, or perform server upgrades without downtime.

For production deployments we recommend using gunicorn with the uvicorn worker class.

```
gunicorn example:app -w 4 -k uvicorn.workers.UvicornWorker
```

For a [PyPy](https://pypy.org/) compatible configuration use `uvicorn.workers.UvicornH11Worker` .

For more information, see the [deployment documentation](deployment/) .

### Application factories

The `--factory` flag allows loading the application from a factory function, rather than an application instance directly. The factory will be called with no arguments and should return an ASGI application.

main.py

```
def create_app():
    app = ...
    return app
```

```
uvicorn --factory main:create_app
```
