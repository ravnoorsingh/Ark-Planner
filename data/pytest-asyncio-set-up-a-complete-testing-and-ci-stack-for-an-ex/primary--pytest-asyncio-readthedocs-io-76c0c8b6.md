---
library: "pytest-asyncio"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://pytest-asyncio.readthedocs.io"
resolved_url: "https://pytest-asyncio.readthedocs.io/en/stable/"
role: "primary"
rank: 0
fetched_at: "2026-08-17T19:28:29.118692+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "e92405bd7a86067b27a25f25ec0a195128ee0678e97b0f9381336248b44b0974"
---

# Welcome to pytest-asyncio!

pytest-asyncio is a [pytest](https://docs.pytest.org/en/latest/contents.html) plugin. It facilitates testing of code that uses the [asyncio](https://docs.python.org/3/library/asyncio.html) library.

Specifically, pytest-asyncio provides support for coroutines as test functions. This allows users to *await* code inside their tests. For example, the following code is executed as a test item by pytest:

```
@pytest.mark.asyncioasync def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

Note that test classes subclassing the standard [unittest](https://docs.python.org/3/library/unittest.html) library are not supported. Users are advised to use [unittest.IsolatedAsyncioTestCase](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase) or an async framework such as [asynctest](https://asynctest.readthedocs.io/en/latest) .

pytest-asyncio is available under the [Apache License 2.0](https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE) .
