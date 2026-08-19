---
library: "hypothesis"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://hypothesis.readthedocs.io/en/latest/quickstart.html"
role: "alternate"
rank: 1
fetched_at: "2026-08-17T19:28:29.680281+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "4333a9de88d331638eb25cff20c7e52202e12eaba068182b7c81a316601dbc5f"
---

# Quickstart

This is a lightning introduction to the most important features of Hypothesis; enough to get you started writing tests. The  [tutorial](tutorial/index.html)  introduces these features (and more) in greater detail.

## Install Hypothesis

```
pip install hypothesis
```

## Write your first test

Create a new file called `example.py` , containing a simple test:

```
# contents of example.pyfrom hypothesis import given, strategies as st

@given(st.integers())def test_integers(n):
    print(f"called with {n}")
    assert isinstance(n, int)

test_integers()
```

[`@given`](reference/api.html#hypothesis.given "hypothesis.given")  is the standard entrypoint to Hypothesis. It takes a *strategy* , which describes the type of inputs you want the decorated function to accept. When we call `test_integers` , Hypothesis will generate random integers (because we used the  [`integers()`](reference/strategies.html#hypothesis.strategies.integers "hypothesis.strategies.integers")  strategy) and pass them as `n` . Let’s see that in action now by running `python example.py` :

```
called with 0
called with -18588
called with -672780074
called with 32616
...
```

We just called `test_integers()` , without passing a value for `n` , because Hypothesis generates random values of `n` for us.

Note

By default, Hypothesis generates 100 random inputs. You can control this with the  [`max_examples`](reference/api.html#hypothesis.settings.max_examples "hypothesis.settings.max_examples")  setting.

## Running in a test suite

A Hypothesis test is still a regular python function, which means pytest or unittest will pick it up and run it in all the normal ways.

```
# contents of example.pyfrom hypothesis import given, strategies as st

@given(st.integers(0, 200))def test_integers(n):
    assert n < 50
```

This test will clearly fail, which can be confirmed by running `pytest example.py` :

```
$ pytest example.py

    ...

    @given(st.integers())
    def test_integers(n):
>       assert n < 50
E       assert 50 < 50
E       Failing test case: test_integers(
E           n=50,
E       )
```

## Arguments to [`@given`](reference/api.html#hypothesis.given "hypothesis.given")

You can pass multiple arguments to  [`@given`](reference/api.html#hypothesis.given "hypothesis.given")  :

```
@given(st.integers(), st.text())def test_integers(n, s):
    assert isinstance(n, int)
    assert isinstance(s, str)
```

Or use keyword arguments:

```
@given(n=st.integers(), s=st.text())def test_integers(n, s):
    assert isinstance(n, int)
    assert isinstance(s, str)
```

Note

See  [`@given`](reference/api.html#hypothesis.given "hypothesis.given")  for details about how  [`@given`](reference/api.html#hypothesis.given "hypothesis.given")  handles different types of arguments.

## Filtering inside a test

Sometimes, you need to remove invalid cases from your test. The best way to do this is with  [`.filter()`](reference/strategies.html#hypothesis.strategies.SearchStrategy.filter "hypothesis.strategies.SearchStrategy.filter")  :

```
@given(st.integers().filter(lambda n: n % 2 == 0))def test_integers(n):
    assert n % 2 == 0
```

For more complicated conditions, you can use  [`assume()`](reference/api.html#hypothesis.assume "hypothesis.assume")  , which tells Hypothesis to discard any  [test case](glossary.html#term-test-case)  with a false-y argument:

```
@given(st.integers(), st.integers())def test_integers(n1, n2):
    assume(n1 != n2)
    # n1 and n2 are guaranteed to be different here
```

Note

You can learn more about  [`.filter()`](reference/strategies.html#hypothesis.strategies.SearchStrategy.filter "hypothesis.strategies.SearchStrategy.filter")  and  [`assume()`](reference/api.html#hypothesis.assume "hypothesis.assume")  in the  [Adapting strategies](tutorial/adapting-strategies.html)  tutorial page.

## Dependent generation

You may want an input to depend on the value of another input. For instance, you might want to generate two integers `n1` and `n2` where `n1 <= n2` .

You can do this using the  [`@composite`](reference/strategies.html#hypothesis.strategies.composite "hypothesis.strategies.composite")  strategy.  [`@composite`](reference/strategies.html#hypothesis.strategies.composite "hypothesis.strategies.composite")  lets you define a new strategy which is itself built by drawing values from other strategies, using the automatically-passed `draw` function.

```
@st.compositedef ordered_pairs(draw):
    n1 = draw(st.integers())
    n2 = draw(st.integers(min_value=n1))
    return (n1, n2)

@given(ordered_pairs())def test_pairs_are_ordered(pair):
    n1, n2 = pair
    assert n1 <= n2
```

In more complex cases, you might need to interleave generation and test code. In this case, use  [`data()`](reference/strategies.html#hypothesis.strategies.data "hypothesis.strategies.data")  .

```
@given(st.data(), st.text(min_size=1))def test_string_characters_are_substrings(data, string):
    assert isinstance(string, str)
    index = data.draw(st.integers(0, len(string) - 1))
    assert string[index] in string
```

## Combining Hypothesis with pytest

Hypothesis works with pytest features, like  [pytest.mark.parametrize](https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-parametrize-ref "(in pytest v9.1.1)")  :

```
import pytest

from hypothesis import given, strategies as st

@pytest.mark.parametrize("operation", [reversed, sorted])@given(st.lists(st.integers()))def test_list_operation_preserves_length(operation, lst):
    assert len(lst) == len(list(operation(lst)))
```

Hypothesis also works with pytest fixtures:

```
import pytest

@pytest.fixture(scope="session")def shared_mapping():
    return {n: 0 for n in range(101)}

@given(st.integers(0, 100))def test_shared_mapping_keys(shared_mapping, n):
    assert n in shared_mapping
```
