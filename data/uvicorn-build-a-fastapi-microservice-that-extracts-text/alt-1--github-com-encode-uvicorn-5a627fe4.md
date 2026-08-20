---
library: "uvicorn"
query: "Build a FastAPI microservice that extracts text from uploaded PDF resumes, embeds them with sentence-transformers, and ranks them against a job description"
url: "https://github.com/encode/uvicorn"
resolved_url: "https://github.com/Kludex/uvicorn"
role: "alternate"
rank: 1
fetched_at: "2026-08-20T15:04:04.864238+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "6828c8b40d69c9ab1352189fcd6a4219575178b273eb82ed9f453bfc0a091417"
---

[![uvicorn](https://raw.githubusercontent.com/tomchristie/uvicorn/main/docs/uvicorn.png)](https://raw.githubusercontent.com/tomchristie/uvicorn/main/docs/uvicorn.png)

*An ASGI web server, for Python.*

---

[![Build Status](https://github.com/Kludex/uvicorn/workflows/Test%20Suite/badge.svg)](https://github.com/Kludex/uvicorn/actions)   [![Package version](https://camo.githubusercontent.com/34f376e9624bcb521904ed4324929ce461f2c9eae1cd8a9ded42d33ae7c48193/68747470733a2f2f62616467652e667572792e696f2f70792f757669636f726e2e737667)](https://pypi.python.org/pypi/uvicorn)   [![Supported Python Version](https://camo.githubusercontent.com/7debbb693053bc601ba994f4f217575f73ac85262691e3199418aa25f0a98ea4/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f757669636f726e2e7376673f636f6c6f723d253233333444303538)](https://pypi.org/project/uvicorn)   [![Discord](https://camo.githubusercontent.com/00fbb2e643fa3aa94df24855b9577ee012fb9abe9ae94c57868635b20283dcd4/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313035313436383634393531383631363537363f6c6f676f3d646973636f7264266c6f676f436f6c6f723d66666666666626636f6c6f723d373338394438266c6162656c436f6c6f723d364137454332)](https://discord.gg/RxKUF5JuHs)

---

**Documentation** : <https://uvicorn.dev>

**Source Code** : <https://www.github.com/Kludex/uvicorn>

---

Uvicorn is an ASGI web server implementation for Python.

Until recently Python has lacked a minimal low-level server/application interface for async frameworks. The [ASGI specification](https://asgi.readthedocs.io/en/latest/) fills this gap, and means we're now able to start building a common set of tooling usable across all async frameworks.

Uvicorn supports HTTP/1.1 and WebSockets.

## Quickstart

Install using `pip` :

```
$ pip install uvicorn
```

This will install uvicorn with minimal (pure Python) dependencies.

```
'uvicorn[standard]'
```

This will install uvicorn with "Cython-based" dependencies (where possible) and other "optional extras".

In this context, "Cython-based" means the following:

* the event loop `uvloop` will be installed and used if possible.
* the http protocol will be handled by `httptools` if possible.

Moreover, "optional extras" means that:

* the websocket protocol will be handled by `websockets` (should you want to use `wsproto` you'd need to install it manually) if possible.
* the `--reload` flag in development mode will use `watchfiles` .
* `python-dotenv` will be installed should you want to use the `--env-file` option.
* `PyYAML` will be installed to allow you to provide a `.yaml` file to `--log-config` , if desired.

Create an application, in `example.py` :

```
async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain'),
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
```

Run the server:

```
$ uvicorn example:app
```

---

## Why ASGI?

Most well established Python Web frameworks started out as WSGI-based frameworks.

WSGI applications are a single, synchronous callable that takes a request and returns a response. This doesn’t allow for long-lived connections, like you get with long-poll HTTP or WebSocket connections, which WSGI doesn't support well.

Having an async concurrency model also allows for options such as lightweight background tasks, and can be less of a limiting factor for endpoints that have long periods being blocked on network I/O such as dealing with slow HTTP requests.

---

## Alternative ASGI servers

A strength of the ASGI protocol is that it decouples the server implementation from the application framework. This allows for an ecosystem of interoperating webservers and application frameworks.

### Daphne

The first ASGI server implementation, originally developed to power Django Channels, is [the Daphne webserver](https://github.com/django/daphne) .

It is run widely in production, and supports HTTP/1.1, HTTP/2, and WebSockets.

Any of the example applications given here can equally well be run using `daphne` instead.

```
$ pip install daphne
$ daphne app:App
```

### Hypercorn

[Hypercorn](https://github.com/pgjones/hypercorn) was initially part of the Quart web framework, before being separated out into a standalone ASGI server.

Hypercorn supports HTTP/1.1, HTTP/2, and WebSockets.

It also supports  [the excellent `trio` async framework](https://trio.readthedocs.io)  , as an alternative to `asyncio` .

```
$ pip install hypercorn
$ hypercorn app:App
```

### Mangum

[Mangum](https://github.com/jordaneremieff/mangum) is an adapter for using ASGI applications with AWS Lambda & API Gateway.

### Granian

[Granian](https://github.com/emmett-framework/granian) is an ASGI compatible Rust HTTP server which supports HTTP/2, TLS and WebSockets.

---

*Uvicorn is [BSD licensed](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md) code.
 Designed & crafted with care.*
 — 🦄 —
