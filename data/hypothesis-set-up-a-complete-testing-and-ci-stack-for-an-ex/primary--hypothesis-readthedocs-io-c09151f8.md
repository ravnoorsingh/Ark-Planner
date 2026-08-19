---
library: "hypothesis"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://hypothesis.readthedocs.io"
resolved_url: "https://hypothesis.readthedocs.io/en/latest/"
role: "primary"
rank: 0
fetched_at: "2026-08-17T19:28:29.416225+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "04be3a08d0cb3fcd31daa9850d0acd754c3b1a116d87bd076ffb0531deae708b"
---

# Welcome to Hypothesis!

Hypothesis is the property-based testing library for Python. With Hypothesis, you write tests which should pass for all inputs in whatever range you describe, and let Hypothesis randomly choose which of those inputs to check - including edge cases you might not have thought about. For example:

```
from hypothesis import given, strategies as st

@given(st.lists(st.integers() | st.floats()))def test_sort_correctness_using_properties(lst):
    result = my_sort(lst)
    assert set(lst) == set(result)
    assert all(a <= b for a, b in zip(result, result[1:]))
```

You should start with the  [tutorial](tutorial/index.html)  , or alternatively the more condensed  [quickstart](quickstart.html)  .

## [Tutorial](tutorial/index.html)

An introduction to Hypothesis.

New users should start here, or with the more condensed  [quickstart](quickstart.html)  .

## [How-to guides](how-to/index.html)

Practical guides for applying Hypothesis in specific scenarios.

## [Explanations](explanation/index.html)

Commentary oriented towards deepening your understanding of Hypothesis.

## [API Reference](reference/index.html)

Technical API reference.
