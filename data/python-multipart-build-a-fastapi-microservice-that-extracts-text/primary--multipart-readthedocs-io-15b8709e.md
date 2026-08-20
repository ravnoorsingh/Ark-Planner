---
library: "python-multipart"
query: "Build a FastAPI microservice that extracts text from uploaded PDF resumes, embeds them with sentence-transformers, and ranks them against a job description"
url: "https://multipart.readthedocs.io/"
resolved_url: "https://multipart.readthedocs.io/en/latest/"
role: "primary"
rank: 0
fetched_at: "2026-08-20T15:09:55.108803+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "b147b270fee6fede462218b2653b9f1ae6d5f50049a52219ee715ea84dcfa4ae"
---

# Python multipart/form-data parser

 [![CI Status](https://github.com/defnull/multipart/actions/workflows/test.yaml/badge.svg)](https://github.com/defnull/multipart/actions/workflows/test.yaml)   [![Latest Version](https://img.shields.io/pypi/v/multipart.svg)](https://pypi.python.org/pypi/multipart/)   [![Supported Python Version](https://img.shields.io/pypi/pyversions/multipart.svg?color=%2334D058)](https://pypi.python.org/pypi/multipart/)   [![License](https://img.shields.io/pypi/l/multipart.svg)](https://github.com/defnull/multipart/)

This module provides a fast incremental non-blocking parser for `multipart/form-data` [ [HTML5](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#multipart-form-data) , [RFC7578](https://www.rfc-editor.org/rfc/rfc7578) ], as well as blocking alternatives for easier use in [WSGI](https://peps.python.org/pep-3333) or CGI applications:

* [SansIO Parser](usage.html#push-example)  : Fast incremental and non-blocking parser suitable for [ASGI](https://asgi.readthedocs.io/en/latest/) , [asyncio](https://docs.python.org/3/library/asyncio.html) , [twisted](https://twisted.org/) and other IO, time or memory constrained environments.
* [Buffered Parser](usage.html#stream-example)  : Blocking stream parser that reads from any stream and yields memory- or disk-buffered  [`MultipartPart`](api.html#multipart.MultipartPart "multipart.MultipartPart")  instances.
* [WSGI Helper](usage.html#wsgi-example)  : High-level parser functions for [WSGI](https://peps.python.org/pep-3333) or CGI applications with support for both `multipart` and `urlencoded` form submissions.

## Features and Scope

* Pure python single file module with no dependencies.
* Highly optimized parsers for blocking and non-blocking applications.
* 100% test coverage with test data from actual browsers and HTTP clients.
* High throughput and low latency (see [benchmarks](https://github.com/defnull/multipart_bench) ).
* Predictable memory and disk resource consumption via fine grained limits.
* Strict mode: Spend less time parsing malicious or broken inputs.

**Scope:** All parsers in this module implement `multipart/form-data` as defined by [HTML5](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#multipart-form-data) and [RFC7578](https://www.rfc-editor.org/rfc/rfc7578) , supporting all modern browsers or HTTP clients in use today. Legacy browsers (e.g. IE6) are supported to some degree, but only if the required workarounds do not impact performance or security. In detail this means:

* Just `multipart/form-data` , not suitable for email parsing.
* No `multipart/mixed` support (deprecated in [RFC7578](https://www.rfc-editor.org/rfc/rfc7578) ).
* No `base64` or `quoted-printable` transfer encoding (deprecated in [RFC7578](https://www.rfc-editor.org/rfc/rfc7578) ).
* No `encoded-word` or `name=_charset_` encoding markers (deprecated in [HTML5](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#multipart-form-data) ).
* No support for clearly broken clients (e.g. invalid line breaks or headers).

## Installation

`pip install multipart` or `uv add multipart`

## Table of Contents

## License

Copyright (c) 2010-2026, Marcel Hellkamp

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
