---
library: "pytest-asyncio"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://github.com/pytest-dev/pytest-asyncio"
role: "alternate"
rank: 1
fetched_at: "2026-08-17T19:28:29.201799+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "6f6cd29b950a3662708b5a5002b40ab67c218a334c76024b3cedca8f3b66fb71"
---

# pytest-asyncio

 [!](https://pypi.python.org/pypi/pytest-asyncio)   [!](https://github.com/pytest-dev/pytest-asyncio/actions?workflow=CI)   [!](https://codecov.io/gh/pytest-dev/pytest-asyncio)   [![Supported Python versions](https://camo.githubusercontent.com/1bf95d4462bbe7b2a451f8d8152c362f7ba83968254ad368abdfda401ee99e2f/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7079746573742d6173796e63696f2e737667)](https://github.com/pytest-dev/pytest-asyncio)   [![Matrix chat room: #pytest-asyncio](https://camo.githubusercontent.com/8b08cb123f2ea6b85d0daf4c499ec94e302dc0fa0570d037b3dcea4921aca88a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d61747269782d2532337079746573742d2d6173796e63696f2d627269676874677265656e)](https://matrix.to/#/#pytest-asyncio:matrix.org)

[pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/stable/) is a [pytest](https://docs.pytest.org/en/latest/contents.html) plugin. It facilitates testing of code that uses the [asyncio](https://docs.python.org/3/library/asyncio.html) library.

Specifically, pytest-asyncio provides support for coroutines as test functions. This allows users to *await* code inside their tests. For example, the following code is executed as a test item by pytest:

```
@pytest.mark.asyncio

async def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

More details can be found in the [documentation](https://pytest-asyncio.readthedocs.io/en/stable/) .

Note that test classes subclassing the standard [unittest](https://docs.python.org/3/library/unittest.html) library are not supported. Users are advised to use [unittest.IsolatedAsyncioTestCase](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase) or an async framework such as [asynctest](https://asynctest.readthedocs.io/en/latest) .

pytest-asyncio is available under the [Apache License 2.0](https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE) .

## Installation

To install pytest-asyncio, simply:

```
$ pip install pytest-asyncio
```

This is enough for pytest to pick up pytest-asyncio.

## Contributing

Contributions are very welcome. Tests can be run with `tox` , please ensure the coverage at least stays the same before you submit a pull request.
