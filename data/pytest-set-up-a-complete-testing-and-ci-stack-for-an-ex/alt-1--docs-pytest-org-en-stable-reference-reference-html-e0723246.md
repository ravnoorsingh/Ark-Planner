---
library: "pytest"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://docs.pytest.org/en/stable/reference/reference.html"
role: "alternate"
rank: 1
fetched_at: "2026-08-17T19:28:28.596787+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "6e6423d5dbfe969323bccf6792c5f23e467a90bc5273f710b28fadcc2ee944dc"
---

# API Reference

This page contains the full reference to pytest’s API.

## Constants

### pytest.\_\_version\_\_

The current pytest version, as a string:

```
>>> import pytest>>> pytest.__version__'9.0.2'
```

### pytest.HIDDEN\_PARAM

Added in version 8.4.

Can be passed to `ids` of  [`Metafunc.parametrize`](#pytest.Metafunc.parametrize "pytest.Metafunc.parametrize")  or to `id` of  [`pytest.param()`](#pytest.param "pytest.param")  to hide a parameter set from the test name. Can only be used at most 1 time, as test names need to be unique.

### pytest.version\_tuple

Added in version 7.0.

The current pytest version, as a tuple:

```
>>> import pytest>>> pytest.version_tuple(7, 0, 0)
```

For pre-releases, the last component will be a string with the prerelease version:

```
>>> import pytest>>> pytest.version_tuple(7, 0, '0rc1')
```

## Functions

### pytest.approx

approx ( *expected* , *rel = None* , *abs = None* , *nan\_ok = False* ) [[source]](../_modules/_pytest/python_api.html#approx)
:   Assert that two numbers (or two ordered sequences of numbers) are equal to each other within some tolerance.

    Due to the  [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html "(in Python v3.14)")  , numbers that we would intuitively expect to be equal are not always so:

    ```
    >>> 0.1 + 0.2 == 0.3False
    ```

    This problem is commonly encountered when writing tests, e.g. when making sure that floating-point values are what you expect them to be. One way to deal with this problem is to assert that two floating-point numbers are equal to within some appropriate tolerance:

    ```
    >>> abs((0.1 + 0.2) - 0.3) < 1e-6True
    ```

    However, comparisons like this are tedious to write and difficult to understand. Furthermore, absolute comparisons like the one above are usually discouraged because there’s no tolerance that works well for all situations. `1e-6` is good for numbers around `1` , but too small for very big numbers and too big for very small ones. It’s better to express the tolerance as a fraction of the expected value, but relative comparisons like that are even more difficult to write correctly and concisely.

    The `approx` class performs floating-point comparisons using a syntax that’s as intuitive as possible:

    ```
    >>> from pytest import approx>>> 0.1 + 0.2 == approx(0.3)True
    ```

    The same syntax also works for ordered sequences of numbers:

    ```
    >>> (0.1 + 0.2, 0.2 + 0.4) == approx((0.3, 0.6))True
    ```

    `numpy` arrays:

    ```
    >>> import numpy as np>>> np.array([0.1, 0.2]) + np.array([0.2, 0.4]) == approx(np.array([0.3, 0.6]))True
    ```

    And for a `numpy` array against a scalar:

    ```
    >>> import numpy as np>>> np.array([0.1, 0.2]) + np.array([0.2, 0.1]) == approx(0.3)True
    ```

    Only ordered sequences are supported, because `approx` needs to infer the relative position of the sequences without ambiguity. This means `sets` and other unordered sequences are not supported.

    Finally, dictionary *values* can also be compared:

    ```
    >>> {'a': 0.1 + 0.2, 'b': 0.2 + 0.4} == approx({'a': 0.3, 'b': 0.6})True
    ```

    The comparison will be true if both mappings have the same keys and their respective values match the expected tolerances.

    **Tolerances**

    By default, `approx` considers numbers within a relative tolerance of `1e-6` (i.e. one part in a million) of its expected value to be equal. This treatment would lead to surprising results if the expected value was `0.0` , because nothing but `0.0` itself is relatively close to `0.0` . To handle this case less surprisingly, `approx` also considers numbers within an absolute tolerance of `1e-12` of its expected value to be equal. Infinity and NaN are special cases. Infinity is only considered equal to itself, regardless of the relative tolerance. NaN is not considered equal to anything by default, but you can make it be equal to itself by setting the `nan_ok` argument to True. (This is meant to facilitate comparing arrays that use NaN to mean “no data”.)

    Both the relative and absolute tolerances can be changed by passing arguments to the `approx` constructor:

    ```
    >>> 1.0001 == approx(1)False>>> 1.0001 == approx(1, rel=1e-3)True>>> 1.0001 == approx(1, abs=1e-3)True
    ```

    If you specify `abs` but not `rel` , the comparison will not consider the relative tolerance at all. In other words, two numbers that are within the default relative tolerance of `1e-6` will still be considered unequal if they exceed the specified absolute tolerance. If you specify both `abs` and `rel` , the numbers will be considered equal if either tolerance is met:

    ```
    >>> 1 + 1e-8 == approx(1)True>>> 1 + 1e-8 == approx(1, abs=1e-12)False>>> 1 + 1e-8 == approx(1, rel=1e-6, abs=1e-12)True
    ```

    **Non-numeric types**

    You can also use `approx` to compare non-numeric types, or dicts and sequences containing non-numeric types, in which case it falls back to strict equality. This can be useful for comparing dicts and sequences that can contain optional values:

    ```
    >>> {"required": 1.0000005, "optional": None} == approx({"required": 1, "optional": None})True>>> [None, 1.0000005] == approx([None,1])True>>> ["foo", 1.0000005] == approx([None,1])False
    ```

    **datetime and timedelta**

    You can also use `approx` to compare  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")  and  [`timedelta`](https://docs.python.org/3/library/datetime.html#datetime.timedelta "(in Python v3.14)")  objects by specifying an absolute tolerance as a  [`timedelta`](https://docs.python.org/3/library/datetime.html#datetime.timedelta "(in Python v3.14)")  :

    ```
    >>> from datetime import datetime, timedelta>>> dt1 = datetime(2024, 1, 1, 12, 0, 0)>>> dt2 = datetime(2024, 1, 1, 12, 0, 0, 500000)>>> dt1 == approx(dt2, abs=timedelta(seconds=1))True
    ```

    Note that `rel` is not supported for datetime comparisons. For timedelta comparisons, `rel` is a number (not a timedelta) that represents a relative tolerance – a fraction of the expected value. `abs` must be a `timedelta` object in both cases.

    Added in version 8.4.

    If you’re thinking about using `approx` , then you might want to know how it compares to other good ways of comparing floating-point numbers. All of these algorithms are based on relative and absolute tolerances and should agree for the most part, but they do have meaningful differences:

    * `math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)` : True if the relative tolerance is met w.r.t. either `a` or `b` or if the absolute tolerance is met. Because the relative tolerance is calculated w.r.t. both `a` and `b` , this test is symmetric (i.e. neither `a` nor `b` is a “reference value”). You have to specify an absolute tolerance if you want to compare to `0.0` because there is no tolerance by default. More information:  [`math.isclose()`](https://docs.python.org/3/library/math.html#math.isclose "(in Python v3.14)")  .
    * `numpy.isclose(a, b, rtol=1e-5, atol=1e-8)` : True if the difference between `a` and `b` is less that the sum of the relative tolerance w.r.t. `b` and the absolute tolerance. Because the relative tolerance is only calculated w.r.t. `b` , this test is asymmetric and you can think of `b` as the reference value. Support for comparing sequences is provided by  [`numpy.allclose()`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html#numpy.allclose "(in NumPy v2.4)")  . More information:  [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html "(in NumPy v2.4)")  .
    * `unittest.TestCase.assertAlmostEqual(a, b)` : True if `a` and `b` are within an absolute tolerance of `1e-7` . No relative tolerance is considered , so this function is not appropriate for very large or very small numbers. Also, it’s only available in subclasses of `unittest.TestCase` and it’s ugly because it doesn’t follow PEP8. More information:  [`unittest.TestCase.assertAlmostEqual()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual "(in Python v3.14)")  .
    * `a == pytest.approx(b, rel=1e-6, abs=1e-12)` : True if the relative tolerance is met w.r.t. `b` or if the absolute tolerance is met. Because the relative tolerance is only calculated w.r.t. `b` , this test is asymmetric and you can think of `b` as the reference value. In the special case that you explicitly specify an absolute tolerance but not a relative tolerance, only the absolute tolerance is considered.

    Note

    `approx` can handle numpy arrays, but we recommend the specialised test helpers in  [Test support](https://numpy.org/doc/stable/reference/routines.testing.html "(in NumPy v2.4)")  if you need support for comparisons, NaNs, or ULP-based tolerances.

    To match strings using regex, you can use [Matches](https://github.com/asottile/re-assert#re_assertmatchespattern-str-args-kwargs) from the [re\_assert package](https://github.com/asottile/re-assert) .

    Note

    Unlike built-in equality, this function considers booleans unequal to numeric zero or one. For example:

    ```
    >>> 1 == approx(True)False
    ```

    Warning

    Changed in version 3.2.

    In order to avoid inconsistent behavior,  [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)")  is raised for `>` , `>=` , `<` and `<=` comparisons. The example below illustrates the problem:

    ```
    assert approx(0.1) > 0.1 + 1e-10  # calls approx(0.1).__gt__(0.1 + 1e-10)assert 0.1 + 1e-10 > approx(0.1)  # calls approx(0.1).__lt__(0.1 + 1e-10)
    ```

    In the second example one expects `approx(0.1).__le__(0.1 + 1e-10)` to be called. But instead, `approx(0.1).__lt__(0.1 + 1e-10)` is used to comparison. This is because the call hierarchy of rich comparisons follows a fixed behavior. More information:  [`object.__ge__()`](https://docs.python.org/3/reference/datamodel.html#object.__ge__ "(in Python v3.14)")

    Changed in version 3.7.1:  `approx` raises `TypeError` when it encounters a dict value or sequence element of non-numeric type.

    Changed in version 6.1.0:  `approx` falls back to strict equality for non-numeric types instead of raising `TypeError` .

### pytest.fail

**Tutorial** :  [How to use skip and xfail to deal with tests that cannot succeed](../how-to/skipping.html#skipping)

fail ( *reason* [ , *pytrace = True* ] )
:   Explicitly fail an executing test with the given message.

    Parameters :
    :   * **reason** – The message to show the user as reason for the failure.
        * **pytrace** – If False, msg represents the full failure information and no python traceback will be reported.

    Raises :
    :   [**pytest.fail.Exception**](#pytest.fail.Exception "pytest.fail.Exception")  – The exception that is raised.

class pytest.fail. Exception
:   The exception raised by  [`pytest.fail()`](#pytest.fail "pytest.fail")  .

### pytest.skip

skip ( *reason* [ , *allow\_module\_level = False* ] )
:   Skip an executing test with the given message.

    This function should be called only during testing (setup, call or teardown) or during collection by using the `allow_module_level` flag. This function can be called in doctests as well.

    Parameters :
    :   * **reason** – The message to show the user as reason for the skip.
        * **allow\_module\_level** –

          Allows this function to be called at module level. Raising the skip exception at module level will stop the execution of the module and prevent the collection of all tests in the module, even those defined before the `skip` call.

          Defaults to False.

    Raises :
    :   [**pytest.skip.Exception**](#pytest.skip.Exception "pytest.skip.Exception")  – The exception that is raised.

    Note

    It is better to use the  [pytest.mark.skipif](#pytest-mark-skipif-ref)  marker when possible to declare a test to be skipped under certain conditions like mismatching platforms or dependencies. Similarly, use the `# doctest: +SKIP` directive (see  [`doctest.SKIP`](https://docs.python.org/3/library/doctest.html#doctest.SKIP "(in Python v3.14)")  ) to skip a doctest statically.

class pytest.skip. Exception
:   The exception raised by  [`pytest.skip()`](#pytest.skip "pytest.skip")  .

### pytest.importorskip

importorskip ( *modname* , *minversion = None* , *reason = None* , *\** , *exc\_type = None* ) [[source]](../_modules/_pytest/outcomes.html#importorskip)
:   Import and return the requested module `modname` , or skip the current test if the module cannot be imported.

    Parameters :
    :   * **modname** – The name of the module to import.
        * **minversion** – If given, the imported module’s `__version__` attribute must be at least this minimal version, otherwise the test is still skipped.
        * **reason** – If given, this reason is shown as the message when the module cannot be imported.
        * **exc\_type** –

          The exception that should be captured in order to skip modules. Must be  [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError "(in Python v3.14)")  or a subclass.

          Defaults to  [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError "(in Python v3.14)")  when not given, which means the module must be missing for the test to be skipped. Pass `exc_type=ImportError` to also skip modules that raise  [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError "(in Python v3.14)")  during import.

          See  [pytest.importorskip default behavior regarding ImportError](../deprecations.html#import-or-skip-import-error)  for details.

    Returns :
    :   The imported module. This should be assigned to its canonical name.

    Raises :
    :   [**pytest.skip.Exception**](#pytest.skip.Exception "pytest.skip.Exception")  – If the module cannot be imported.

    Example:

    ```
    docutils = pytest.importorskip("docutils")
    ```

    Added in version 8.2:  The `exc_type` parameter.

    Changed in version 9.1:  The default for `exc_type` is now  [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError "(in Python v3.14)")  .

### pytest.xfail

xfail ( *reason = ''* )
:   Imperatively xfail an executing test or setup function with the given reason.

    This function should be called only during testing (setup, call or teardown).

    No other code is executed after using `xfail()` (it is implemented internally by raising an exception).

    Parameters :
    :   **reason** – The message to show the user as reason for the xfail.

    Note

    It is better to use the  [pytest.mark.xfail](#pytest-mark-xfail-ref)  marker when possible to declare a test to be xfailed under certain conditions like known bugs or missing features.

    Raises :
    :   [**pytest.xfail.Exception**](#pytest.xfail.Exception "pytest.xfail.Exception")  – The exception that is raised.

class pytest.xfail. Exception
:   The exception raised by  [`pytest.xfail()`](#pytest.xfail "pytest.xfail")  .

### pytest.exit

exit ( *reason* [ , *returncode = None* ] )
:   Exit testing process.

    Parameters :
    :   * **reason** – The message to show as the reason for exiting pytest. reason has a default value only because `msg` is deprecated.
        * **returncode** – Return code to be used when exiting pytest. None means the same as `0` (no error), same as  [`sys.exit()`](https://docs.python.org/3/library/sys.html#sys.exit "(in Python v3.14)")  .

    Raises :
    :   [**pytest.exit.Exception**](#pytest.exit.Exception "pytest.exit.Exception")  – The exception that is raised.

class pytest.exit. Exception
:   The exception raised by  [`pytest.exit()`](#pytest.exit "pytest.exit")  .

### pytest.main

**Tutorial** :  [Calling pytest from Python code](../how-to/usage.html#pytest-main-usage)

main ( *args = None* , *plugins = None* ) [[source]](../_modules/_pytest/config.html#main)
:   Perform an in-process test run.

    Parameters :
    :   * **args** – List of command line arguments. If `None` or not given, defaults to reading arguments directly from the process command line (  [`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv "(in Python v3.14)")  ).
        * **plugins** – List of plugin objects to be auto-registered during initialization.

    Returns :
    :   An exit code.

### pytest.param

param ( *\*values* [ , *id* ] [ , *marks* ] ) [[source]](../_modules/_pytest/mark.html#param)
:   Specify a parameter in [pytest.mark.parametrize](#pytest-mark-parametrize) calls or  [parametrized fixtures](../how-to/fixtures.html#fixture-parametrize-marks)  .

    ```
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("3+5", 8),
            pytest.param("6*9", 42, marks=pytest.mark.xfail),
        ],)def test_eval(test_input, expected):
        assert eval(test_input) == expected
    ```

    Parameters :
    :   * **values** – Variable args of the values of the parameter set, in order.
        * **marks** –

          A single mark or a list of marks to be applied to this parameter set.

          [pytest.mark.usefixtures](#pytest-mark-usefixtures-ref)  cannot be added via this parameter.
        * **id** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *Literal* *[* *pytest.HIDDEN\_PARAM* *]*  *|*  *None* ) –

          The id to attribute to this parameter set.

          Added in version 8.4:   [pytest.HIDDEN\_PARAM](#hidden-param)  means to hide the parameter set from the test name. Can only be used at most 1 time, as test names need to be unique.

### pytest.raises

**Tutorial** :  [Assertions about expected exceptions](../how-to/assert.html#assertraises)

with raises ( *expected\_exception : [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ E ] | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ E ] , ... ]* , *\** , *match : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [Pattern](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = ...* , *check : Callable [ [ E ] , [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") ] = ...* ) → [RaisesExc](#pytest.RaisesExc "pytest.RaisesExc") [ E ] as excinfo [[source]](../_modules/_pytest/raises.html#raises)

with raises ( *\** , *match : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [Pattern](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]* , *check : Callable [ [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] , [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") ] = ...* ) → [RaisesExc](#pytest.RaisesExc "_pytest.raises.RaisesExc") [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] as excinfo

with raises ( *\** , *check : Callable [ [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] , [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") ]* ) → [RaisesExc](#pytest.RaisesExc "_pytest.raises.RaisesExc") [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] as excinfo

with raises ( *expected\_exception : [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ E ] | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ E ] , ... ]* , *func : Callable [ P , [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ]* , *\* args : P.args* , *\*\* kwargs : P.kwargs* ) → [ExceptionInfo](#pytest.ExceptionInfo "pytest.ExceptionInfo") [ E ] as excinfo
:   Assert that a code block/function call raises an exception type, or one of its subclasses.

    Parameters :
    :   * **expected\_exception** –

          The expected exception type, or a tuple if one of multiple possible exception types are expected. Note that subclasses of the passed exceptions will also match.

          This is not a required parameter, you may opt to only use `match` and/or `check` for verifying the raised exception.
        * **match** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*re.Pattern*](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]*  *|*  *None* ) –

          If specified, a string containing a regular expression, or a regular expression object, that is tested against the string representation of the exception and its   [**PEP 678**](https://peps.python.org/pep-0678/)  `__notes__` using  [`re.search()`](https://docs.python.org/3/library/re.html#re.search "(in Python v3.14)")  .

          To match a literal string that may contain  [special characters](https://docs.python.org/3/library/re.html#re-syntax "(in Python v3.14)")  , the pattern can first be escaped with  [`re.escape()`](https://docs.python.org/3/library/re.html#re.escape "(in Python v3.14)")  .

          (This is only used when `pytest.raises` is used as a context manager, and passed through to the function otherwise. When using `pytest.raises` as a function, you can use: `pytest.raises(Exc, func, match="passed on").match("my pattern")` .)
        * **check** ( *Callable* *[* *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *,*   [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  *]* ) –

          Added in version 8.4.

          If specified, a callable that will be called with the exception as a parameter after checking the type and the match regex if specified. If it returns `True` it will be considered a match, if not it will be considered a failed match.

    Use `pytest.raises` as a context manager, which will capture the exception of the given type, or any of its subclasses:

    ```
    >>> import pytest>>> with pytest.raises(ZeroDivisionError):...    1/0
    ```

    If the code block does not raise the expected exception (  [`ZeroDivisionError`](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError "(in Python v3.14)")  in the example above), or no exception at all, the check will fail instead.

    You can also use the keyword argument `match` to assert that the exception matches a text or regex:

    ```
    >>> with pytest.raises(ValueError, match='must be 0 or None'):...     raise ValueError("value must be 0 or None")

    >>> with pytest.raises(ValueError, match=r'must be \d+$'):...     raise ValueError("value must be 42")
    ```

    The `match` argument searches the formatted exception string, which includes any [PEP-678](https://peps.python.org/pep-0678/) `__notes__` :

    ```
    >>> with pytest.raises(ValueError, match=r"had a note added"):...     e = ValueError("value must be 42")...     e.add_note("had a note added")...     raise e
    ```

    The `check` argument, if provided, must return True when passed the raised exception for the match to be successful, otherwise an  [`AssertionError`](https://docs.python.org/3/library/exceptions.html#AssertionError "(in Python v3.14)")  is raised.

    ```
    >>> import errno>>> with pytest.raises(OSError, check=lambda e: e.errno == errno.EACCES):...     raise OSError(errno.EACCES, "no permission to view")
    ```

    The context manager produces an  [`ExceptionInfo`](#pytest.ExceptionInfo "pytest.ExceptionInfo")  object which can be used to inspect the details of the captured exception:

    ```
    >>> with pytest.raises(ValueError) as exc_info:...     raise ValueError("value must be 42")>>> assert exc_info.type is ValueError>>> assert exc_info.value.args[0] == "value must be 42"
    ```

    Warning

    Given that `pytest.raises` matches subclasses, be wary of using it to match  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")  like this:

    ```
    # Careful, this will catch ANY exception raised.with pytest.raises(Exception):
        some_function()
    ```

    Because  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")  is the base class of almost all exceptions, it is easy for this to hide real bugs, where the user wrote this expecting a specific exception, but some other exception is being raised due to a bug introduced during a refactoring.

    Avoid using `pytest.raises` to catch  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")  unless certain that you really want to catch **any** exception raised.

    Note

    When using `pytest.raises` as a context manager, it’s worthwhile to note that normal context manager rules apply and that the exception raised *must* be the final line in the scope of the context manager. Lines of code after that, within the scope of the context manager will not be executed. For example:

    ```
    >>> value = 15>>> with pytest.raises(ValueError) as exc_info:...     if value > 10:...         raise ValueError("value must be <= 10")...     assert exc_info.type is ValueError  # This will not execute.
    ```

    Instead, the following approach must be taken (note the difference in scope):

    ```
    >>> with pytest.raises(ValueError) as exc_info:...     if value > 10:...         raise ValueError("value must be <= 10")...>>> assert exc_info.type is ValueError
    ```

    **Expecting exception groups**

    When expecting exceptions wrapped in  [`BaseExceptionGroup`](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup "(in Python v3.14)")  or  [`ExceptionGroup`](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)")  , you should instead use  [`pytest.RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")  .

    **Using with** `pytest.mark.parametrize`

    When using  [pytest.mark.parametrize](#pytest-mark-parametrize-ref)  it is possible to parametrize tests such that some runs raise an exception and others do not.

    See  [Parametrizing conditional raising](../example/parametrize.html#parametrizing-conditional-raising)  for an example.

    See also

    [Assertions about expected exceptions](../how-to/assert.html#assertraises)  for more examples and detailed discussion.

    Note

    Similar to caught exception objects in Python, explicitly clearing local references to returned `ExceptionInfo` objects can help the Python interpreter speed up its garbage collection.

    Clearing those references breaks a reference cycle ( `ExceptionInfo` –> caught exception –> frame stack raising the exception –> current frame stack –> local variables –> `ExceptionInfo` ) which makes Python keep all objects referenced from that cycle (including all local variables in the current frame) alive until the next cyclic garbage collection run. More detailed information can be found in the official Python documentation for  [the try statement](https://docs.python.org/3/reference/compound_stmts.html#try "(in Python v3.14)")  .

### pytest.deprecated\_call

**Tutorial** :  [Ensuring code triggers a deprecation warning](../how-to/capture-warnings.html#ensuring-function-triggers)

with deprecated\_call ( *\** , *match : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [Pattern](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = ...* ) → [WarningsRecorder](#pytest.WarningsRecorder "_pytest.recwarn.WarningsRecorder") [[source]](../_modules/_pytest/recwarn.html#deprecated_call)

with deprecated\_call ( *func : Callable [ P , T ]* , *\* args : P.args* , *\*\* kwargs : P.kwargs* ) → T
:   Assert that code produces a `DeprecationWarning` or `PendingDeprecationWarning` or `FutureWarning` .

    This function can be used as a context manager:

    ```
    >>> import warnings>>> def api_call_v2():...     warnings.warn('use v3 of this api', DeprecationWarning)...     return 200

    >>> import pytest>>> with pytest.deprecated_call():...    assert api_call_v2() == 200>>> with pytest.deprecated_call(match="^use v3 of this api$") as warning_messages:...    assert api_call_v2() == 200
    ```

    You may use the keyword argument `match` to assert that the warning matches a text or regex.

    The return value is a list of `warnings.WarningMessage` objects, one for each warning emitted (regardless of whether it is an `expected_warning` or not).

### pytest.register\_assert\_rewrite

**Tutorial** :  [Assertion Rewriting](../how-to/writing_plugins.html#assertion-rewriting)

register\_assert\_rewrite ( *\* names* ) [[source]](../_modules/_pytest/assertion.html#register_assert_rewrite)
:   Register one or more module names to be rewritten on import.

    This function will make sure that this module or all modules inside the package will get their assert statements rewritten. Thus you should make sure to call this before the module is actually imported, usually in your \_\_init\_\_.py if you are a plugin using a package.

    Parameters :
    :   **names** – The module names to register.

### pytest.register\_fixture

register\_fixture ( *\** , *name* , *func* , *node* , *scope = 'function'* , *params = None* , *ids = None* , *autouse = False* ) [[source]](../_modules/_pytest/fixtures.html#register_fixture)
:   Register a fixture imperatively.

    This is an advanced function intended for use by plugins.

    Normally, fixtures should be registered declaratively using the  [`@pytest.fixture`](#pytest.fixture "pytest.fixture")  decorator. Pytest looks for these fixture definitions during the collection phase and registers them automatically. For some plugin usecases the declarative interface can be cumbersome or nonviable, in which case the imperative interface can be used.

    Fixture registration is expected to happen during the collection phase, and this is the only sanctioned use. However, to allow for more creative uses, this is not enforced. But do so at your own risk!

    Parameters :
    :   * **name** – The fixture’s name.
        * **func** – The fixture’s implementation function.
        * **node** –

          The visibility of the fixture.

          Only items that are descendents of this node in the collection tree will be able to request this fixture. You can think of this as the place where you would put the `@pytest.fixture` .

          For global visibility, pass the  [`session`](#pytest.Session "pytest.Session")  node, which is the root of the collection tree.
        * **scope** – The fixture’s scope.
        * **params** – The fixture’s parametrization params.
        * **ids** – The fixture’s IDs.
        * **autouse** – Whether this is an autouse fixture.

### pytest.warns

**Tutorial** :  [Asserting warnings with the warns function](../how-to/capture-warnings.html#assertwarnings)

with warns ( *expected\_warning: type[Warning] | tuple[type[Warning], ...] = <class 'Warning'>, \*, match: str | ~re.Pattern[str] | None = ...* ) → WarningsChecker [[source]](../_modules/_pytest/recwarn.html#warns)

with warns ( *expected\_warning : [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ [Warning](https://docs.python.org/3/library/exceptions.html#Warning "(in Python v3.14)") ] | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ [Warning](https://docs.python.org/3/library/exceptions.html#Warning "(in Python v3.14)") ] , ... ]* , *func : Callable [ P , T ]* , *\* args : P.args* , *\*\* kwargs : P.kwargs* ) → T
:   Assert that code raises a particular class of warning.

    Specifically, the parameter `expected_warning` can be a warning class or tuple of warning classes, and the code inside the `with` block must issue at least one warning of that class or classes.

    This helper produces a list of `warnings.WarningMessage` objects, one for each warning emitted (regardless of whether it is an `expected_warning` or not). Since pytest 8.0, unmatched warnings are also re-emitted when the context closes.

    This function should be used as a context manager:

    ```
    >>> import pytest>>> with pytest.warns(RuntimeWarning):...    warnings.warn("my warning", RuntimeWarning)
    ```

    The `match` keyword argument can be used to assert that the warning matches a text or regex:

    ```
    >>> with pytest.warns(UserWarning, match='must be 0 or None'):...     warnings.warn("value must be 0 or None", UserWarning)

    >>> with pytest.warns(UserWarning, match=r'must be \d+$'):...     warnings.warn("value must be 42", UserWarning)

    >>> with pytest.warns(UserWarning):  # catch re-emitted warning...     with pytest.warns(UserWarning, match=r'must be \d+$'):...         warnings.warn("this is not here", UserWarning)Traceback (most recent call last):  ...Failed: Regex pattern did not match any of the 1 warnings emitted. Regex: ... Emitted warnings: ...UserWarning...
    ```

    **Using with** `pytest.mark.parametrize`

    When using  [pytest.mark.parametrize](#pytest-mark-parametrize-ref)  it is possible to parametrize tests such that some runs raise a warning and others do not.

    This could be achieved in the same way as with exceptions, see  [Parametrizing conditional raising](../example/parametrize.html#parametrizing-conditional-raising)  for an example.

### pytest.freeze\_includes

**Tutorial** :  [Freezing pytest](../example/simple.html#freezing-pytest)

freeze\_includes ( ) [[source]](../_modules/_pytest/freeze_support.html#freeze_includes)
:   Return a list of module names used by pytest that should be included by cx\_freeze.

## Marks

Marks can be used to apply metadata to *test functions* (but not fixtures), which can then be accessed by fixtures or plugins.

### pytest.mark.filterwarnings

**Tutorial** :  [@pytest.mark.filterwarnings](../how-to/capture-warnings.html#filterwarnings)

Add warning filters to marked test items.

pytest.mark. filterwarnings ( *filter* )
:   Parameters :
    :   **filter** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) –

        A *warning specification string* , which is composed of contents of the tuple `(action, message, category, module, lineno)` as specified in  [The Warnings Filter](https://docs.python.org/3/library/warnings.html#warning-filter "(in Python v3.14)")  section of the Python documentation, separated by `":"` . Optional fields can be omitted. Module names passed for filtering are not regex-escaped.

        For example:

        ```
        @pytest.mark.filterwarnings(r"ignore:.*usage will be deprecated.*:DeprecationWarning")def test_foo(): ...
        ```

### pytest.mark.parametrize

**Tutorial** :  [How to parametrize fixtures and test functions](../how-to/parametrize.html#parametrize)

This mark has the same signature as  [`pytest.Metafunc.parametrize()`](#pytest.Metafunc.parametrize "pytest.Metafunc.parametrize")  ; see there.

### pytest.mark.skip

**Tutorial** :  [Skipping test functions](../how-to/skipping.html#skip)

Unconditionally skip a test function.

pytest.mark. skip ( *reason = None* )
:   Parameters :
    :   **reason** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Reason why the test function is being skipped.

### pytest.mark.skipif

**Tutorial** :  [Skipping test functions](../how-to/skipping.html#skipif)

Skip a test function if a condition is `True` .

pytest.mark. skipif ( *condition* , *\** , *reason = None* )
:   Parameters :
    :   * **condition** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")   *or*   [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – `True/False` if the condition should be skipped or a  [condition string](../historical-notes.html#string-conditions)  .
        * **reason** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Reason why the test function is being skipped.

### pytest.mark.usefixtures

**Tutorial** :  [Use fixtures in classes and modules with usefixtures](../how-to/fixtures.html#usefixtures)

Mark a test function as using the given fixture names.

pytest.mark. usefixtures ( *\* names* )
:   Parameters :
    :   **args** – The names of the fixture to use, as strings.

Note

When using `usefixtures` in hooks, it can only load fixtures when applied to a test function before test setup (for example in the `pytest_collection_modifyitems` hook).

Also note that this mark has no effect when applied to **fixtures** .

### pytest.mark.xfail

**Tutorial** :  [XFail: mark test functions as expected to fail](../how-to/skipping.html#xfail)

Marks a test function as *expected to fail* .

pytest.mark. xfail ( *condition = False* , *\** , *reason = None* , *raises = None* , *run = True* , *strict = strict\_xfail* )
:   Parameters :
    :   * **condition** ( *Union* *[*  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  *,*   [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – Condition for marking the test function as xfail ( `True/False` or a  [condition string](../historical-notes.html#string-conditions)  ). If a `bool` , you also have to specify `reason` (see  [condition string](../historical-notes.html#string-conditions)  ).
        * **reason** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Reason why the test function is marked as xfail.
        * **raises** (Type[  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")  ]) – Exception class (or tuple of classes) expected to be raised by the test function; other exceptions will fail the test. Note that subclasses of the classes passed will also result in a match (similar to how the `except` statement works).
        * **run** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether the test function should actually be executed. If `False` , the function will always xfail and will not be executed (useful if a function is segfaulting).
        * **strict** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) –

          + If `False` the function will be shown in the terminal output as `xfailed` if it fails and as `xpass` if it passes. In both cases this will not cause the test suite to fail as a whole. This is particularly useful to mark *flaky* tests (tests that fail at random) to be tackled later.
          + If `True` , the function will be shown in the terminal output as `xfailed` if it fails, but if it unexpectedly passes then it will **fail** the test suite. This is particularly useful to mark functions that are always failing and there should be a clear indication if they unexpectedly start to pass (for example a new release of a library fixes a known bug).

          Defaults to  [`strict_xfail`](#confval-strict_xfail)  , which is `False` by default.

### Custom marks

Marks are created dynamically using the factory object `pytest.mark` and applied as a decorator.

For example:

```
@pytest.mark.timeout(10, "slow", method="thread")def test_function(): ...
```

Will create and attach a  [`Mark`](#pytest.Mark "pytest.Mark")  object to the collected  [`Item`](#pytest.Item "pytest.Item")  , which can then be accessed by fixtures or hooks with  [`Node.iter_markers`](#pytest.nodes.Node.iter_markers "_pytest.nodes.Node.iter_markers")  . The `mark` object will have the following attributes:

```
mark.args == (10, "slow")mark.kwargs == {"method": "thread"}
```

Example for using multiple custom markers:

```
@pytest.mark.timeout(10, "slow", method="thread")@pytest.mark.slowdef test_function(): ...
```

When  [`Node.iter_markers`](#pytest.nodes.Node.iter_markers "_pytest.nodes.Node.iter_markers")  or  [`Node.iter_markers_with_node`](#pytest.nodes.Node.iter_markers_with_node "_pytest.nodes.Node.iter_markers_with_node")  is used with multiple markers, the marker closest to the function will be iterated over first. The above example will result in `@pytest.mark.slow` followed by `@pytest.mark.timeout(...)` .

## Fixtures

**Tutorial** :  [Fixtures reference](fixtures.html#fixture)

Fixtures are requested by test functions or other fixtures by declaring them as argument names.

Example of a test requiring a fixture:

```
def test_output(capsys):
    print("hello")
    out, err = capsys.readouterr()
    assert out == "hello\n"
```

Example of a fixture requiring another fixture:

```
@pytest.fixturedef db_session(tmp_path):
    fn = tmp_path / "db.file"
    return connect(fn)
```

For more details, consult the full  [fixtures docs](fixtures.html#fixture)  .

### @pytest.fixture

@ fixture ( *fixture\_function : [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)") [ [ ... ] , [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ]* , *\** , *scope : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ] | [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)") [ [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Config](#pytest.Config "_pytest.config.Config") ] , [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ] ] = 'function'* , *params : [Iterable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") [ [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *autouse : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = False* , *ids : [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") ] | [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)") [ [ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ] , [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* ) → FixtureFunctionDefinition [[source]](../_modules/_pytest/fixtures.html#fixture)

@ fixture ( *fixture\_function : [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *\** , *scope : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ] | [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)") [ [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Config](#pytest.Config "_pytest.config.Config") ] , [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ] ] = 'function'* , *params : [Iterable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") [ [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *autouse : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = False* , *ids : [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") ] | [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)") [ [ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ] , [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* ) → FixtureFunctionMarker
:   Decorator to mark a fixture factory function.

    This decorator can be used, with or without parameters, to define a fixture function.

    The name of the fixture function can later be referenced to cause its invocation ahead of running tests: test modules or classes can use the `pytest.mark.usefixtures(fixturename)` marker.

    Test functions can directly use fixture names as input arguments in which case the fixture instance returned from the fixture function will be injected.

    Fixtures can provide their values to test functions using `return` or `yield` statements. When using `yield` the code block after the `yield` statement is executed as teardown code regardless of the test outcome, and must yield exactly once.

    Parameters :
    :   * **scope** –

          The scope for which this fixture is shared; one of `"function"` (default), `"class"` , `"module"` , `"package"` or `"session"` .

          This parameter may also be a callable which receives `(fixture_name, config)` as parameters, and must return a `str` with one of the values mentioned above.

          See  [Dynamic scope](../how-to/fixtures.html#dynamic-scope)  in the docs for more information.
        * **params** – An optional list of parameters which will cause multiple invocations of the fixture function and all of the tests using it. The current parameter is available in `request.param` .
        * **autouse** – If True, the fixture func is activated for all tests that can see it. If False (the default), an explicit reference is needed to activate the fixture.
        * **ids** – Sequence of ids each corresponding to the params so that they are part of the test id. If no ids are provided they will be generated automatically from the params.
        * **name** – The name of the fixture. This defaults to the name of the decorated function. If a fixture is used in the same module in which it is defined, the function name of the fixture will be shadowed by the function arg that requests the fixture; one way to resolve this is to name the decorated function `fixture_<fixturename>` and then use `@pytest.fixture(name='<fixturename>')` .

### capfd

**Tutorial** :  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)

capfd ( ) [[source]](../_modules/_pytest/capture.html#capfd)
:   Enable text capturing of writes to file descriptors `1` and `2` .

    The captured output is made available via `capfd.readouterr()` method calls, which return a `(out, err)` namedtuple. `out` and `err` will be `text` objects.

    Returns an instance of  [`CaptureFixture[str]`](#pytest.CaptureFixture "pytest.CaptureFixture")  .

    Example:

    ```
    def test_system_echo(capfd):
        os.system('echo "hello"')
        captured = capfd.readouterr()
        assert captured.out == "hello\n"
    ```

### capfdbinary

**Tutorial** :  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)

capfdbinary ( ) [[source]](../_modules/_pytest/capture.html#capfdbinary)
:   Enable bytes capturing of writes to file descriptors `1` and `2` .

    The captured output is made available via `capfd.readouterr()` method calls, which return a `(out, err)` namedtuple. `out` and `err` will be `byte` objects.

    Returns an instance of  [`CaptureFixture[bytes]`](#pytest.CaptureFixture "pytest.CaptureFixture")  .

    Example:

    ```
    def test_system_echo(capfdbinary):
        os.system('echo "hello"')
        captured = capfdbinary.readouterr()
        assert captured.out == b"hello\n"
    ```

### caplog

**Tutorial** :  [How to manage logging](../how-to/logging.html#logging)

caplog ( ) [[source]](../_modules/_pytest/logging.html#caplog)
:   Access and control log capturing.

    Captured logs are available through the following properties/methods:

    ```
    * caplog.messages        -> list of format-interpolated log messages* caplog.text            -> string containing formatted log output* caplog.records         -> list of logging.LogRecord instances* caplog.record_tuples   -> list of (logger_name, level, message) tuples* caplog.clear()         -> clear captured records and formatted log output string
    ```

    Returns a  [`pytest.LogCaptureFixture`](#pytest.LogCaptureFixture "pytest.LogCaptureFixture")  instance.

final class LogCaptureFixture [[source]](../_modules/_pytest/logging.html#LogCaptureFixture)
:   Provides access and control of log capturing.

    property handler : LogCaptureHandler
    :   Get the logging handler used by the fixture.

    get\_records ( *when* ) [[source]](../_modules/_pytest/logging.html#LogCaptureFixture.get_records)
    :   Get the logging records for one of the possible test phases.

        Parameters :
        :   **when** (  [*Literal*](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)")  *[* *'setup'* *,*  *'call'* *,*  *'teardown'* *]* ) – Which test phase to obtain the records from. Valid values are: “setup”, “call” and “teardown”.

        Returns :
        :   The list of captured records at the given stage.

        Return type :
        :   [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [  [*LogRecord*](https://docs.python.org/3/library/logging.html#logging.LogRecord "(in Python v3.14)")  ]

        Added in version 3.4.

    property text : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   The formatted log text.

    property records : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [LogRecord](https://docs.python.org/3/library/logging.html#logging.LogRecord "(in Python v3.14)") ]
    :   The list of log records.

    property record\_tuples : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] ]
    :   A list of a stripped down version of log records intended for use in assertion comparison.

        The format of the tuple is:

        > (logger\_name, log\_level, message)

    property messages : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]
    :   A list of format-interpolated log messages.

        Unlike ‘records’, which contains the format string and parameters for interpolation, log messages in this list are all interpolated.

        Unlike ‘text’, which contains the output from the handler, log messages in this list are unadorned with levels, timestamps, etc, making exact comparisons more reliable.

        Note that traceback or stack info (from  [`logging.exception()`](https://docs.python.org/3/library/logging.html#logging.exception "(in Python v3.14)")  or the `exc_info` or `stack_info` arguments to the logging functions) is not included, as this is added by the formatter in the handler.

        Added in version 3.7.

    clear ( ) [[source]](../_modules/_pytest/logging.html#LogCaptureFixture.clear)
    :   Reset the list of log records and the captured log text.

    set\_level ( *level* , *logger = None* ) [[source]](../_modules/_pytest/logging.html#LogCaptureFixture.set_level)
    :   Set the threshold level of a logger for the duration of a test.

        Logging messages which are less severe than this level will not be captured.

        Changed in version 3.4:  The levels of the loggers changed by this function will be restored to their initial values at the end of the test.

        Will enable the requested logging level if it was disabled via  [`logging.disable()`](https://docs.python.org/3/library/logging.html#logging.disable "(in Python v3.14)")  .

        Parameters :
        :   * **level** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")   *|*   [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The level.
            * **logger** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – The logger to update. If not given, the root logger.

    at\_level ( *level* , *logger = None* ) [[source]](../_modules/_pytest/logging.html#LogCaptureFixture.at_level)
    :   Context manager that sets the level for capturing of logs. After the end of the ‘with’ statement the level is restored to its original value.

        Will enable the requested logging level if it was disabled via  [`logging.disable()`](https://docs.python.org/3/library/logging.html#logging.disable "(in Python v3.14)")  .

        Parameters :
        :   * **level** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")   *|*   [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The level.
            * **logger** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – The logger to update. If not given, the root logger.

    filtering ( *filter\_* ) [[source]](../_modules/_pytest/logging.html#LogCaptureFixture.filtering)
    :   Context manager that temporarily adds the given filter to the caplog’s  [`handler()`](#pytest.LogCaptureFixture.handler "pytest.LogCaptureFixture.handler")  for the ‘with’ statement block, and removes that filter at the end of the block.

        Parameters :
        :   **filter** – A custom  [`logging.Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "(in Python v3.14)")  object.

        Added in version 7.5.

### capsys

**Tutorial** :  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)

capsys ( ) [[source]](../_modules/_pytest/capture.html#capsys)
:   Enable text capturing of writes to `sys.stdout` and `sys.stderr` .

    The captured output is made available via `capsys.readouterr()` method calls, which return a `(out, err)` namedtuple. `out` and `err` will be `text` objects.

    Returns an instance of  [`CaptureFixture[str]`](#pytest.CaptureFixture "pytest.CaptureFixture")  .

    Example:

    ```
    def test_output(capsys):
        print("hello")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"
    ```

class CaptureFixture [[source]](../_modules/_pytest/capture.html#CaptureFixture)
:   Object returned by the  [`capsys`](#std-fixture-capsys)  ,  [`capsysbinary`](#std-fixture-capsysbinary)  ,  [`capfd`](#std-fixture-capfd)  and  [`capfdbinary`](#std-fixture-capfdbinary)  fixtures.

    readouterr ( ) [[source]](../_modules/_pytest/capture.html#CaptureFixture.readouterr)
    :   Read and return the captured output so far, resetting the internal buffer.

        Returns :
        :   The captured content as a namedtuple with `out` and `err` string attributes.

        Return type :
        :   *CaptureResult*

    disabled ( ) [[source]](../_modules/_pytest/capture.html#CaptureFixture.disabled)
    :   Temporarily disable capturing while inside the `with` block.

### capteesys

**Tutorial** :  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)

capteesys ( ) [[source]](../_modules/_pytest/capture.html#capteesys)
:   Enable simultaneous text capturing and pass-through of writes to `sys.stdout` and `sys.stderr` as defined by `--capture=` .

    The captured output is made available via `capteesys.readouterr()` method calls, which return a `(out, err)` namedtuple. `out` and `err` will be `text` objects.

    The output is also passed-through, allowing it to be “live-printed”, reported, or both as defined by `--capture=` .

    Returns an instance of  [`CaptureFixture[str]`](#pytest.CaptureFixture "pytest.CaptureFixture")  .

    Example:

    ```
    def test_output(capteesys):
        print("hello")
        captured = capteesys.readouterr()
        assert captured.out == "hello\n"
    ```

### capsysbinary

**Tutorial** :  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)

capsysbinary ( ) [[source]](../_modules/_pytest/capture.html#capsysbinary)
:   Enable bytes capturing of writes to `sys.stdout` and `sys.stderr` .

    The captured output is made available via `capsysbinary.readouterr()` method calls, which return a `(out, err)` namedtuple. `out` and `err` will be `bytes` objects.

    Returns an instance of  [`CaptureFixture[bytes]`](#pytest.CaptureFixture "pytest.CaptureFixture")  .

    Example:

    ```
    def test_output(capsysbinary):
        print("hello")
        captured = capsysbinary.readouterr()
        assert captured.out == b"hello\n"
    ```

### config.cache

**Tutorial** :  [How to re-run failed tests and maintain state between test runs](../how-to/cache.html#cache)

The `config.cache` object allows other plugins and fixtures to store and retrieve values across test runs. To access it from fixtures request `pytestconfig` into your fixture and get it with `pytestconfig.cache` .

Under the hood, the cache plugin uses the simple `dumps` / `loads` API of the  [`json`](https://docs.python.org/3/library/json.html#module-json "(in Python v3.14)")  stdlib module.

`config.cache` is an instance of  [`pytest.Cache`](#pytest.Cache "pytest.Cache")  :

final class Cache [[source]](../_modules/_pytest/cacheprovider.html#Cache)
:   Instance of the `cache` fixture.

    mkdir ( *name* ) [[source]](../_modules/_pytest/cacheprovider.html#Cache.mkdir)
    :   Return a directory path object with the given name.

        If the directory does not yet exist, it will be created. You can use it to manage files to e.g. store/retrieve database dumps across test sessions.

        Added in version 7.0.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Must be a string not containing a `/` separator. Make sure the name contains your plugin or application identifiers to prevent clashes with other cache users.

    get ( *key* , *default* ) [[source]](../_modules/_pytest/cacheprovider.html#Cache.get)
    :   Return the cached value for the given key.

        If no value was yet cached or the value cannot be read, the specified default is returned.

        Parameters :
        :   * **key** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Must be a `/` separated value. Usually the first name is the name of your plugin or your application.
            * **default** – The value to return in case of a cache-miss or invalid cache value.

    set ( *key* , *value* ) [[source]](../_modules/_pytest/cacheprovider.html#Cache.set)
    :   Save value for the given key.

        Parameters :
        :   * **key** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Must be a `/` separated value. Usually the first name is the name of your plugin or your application.
            * **value** (  [*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")  ) – Must be of any combination of basic python types, including nested types like lists of dictionaries.

### doctest\_namespace

**Tutorial** :  [How to run doctests](../how-to/doctest.html#doctest)

doctest\_namespace ( ) [[source]](../_modules/_pytest/doctest.html#doctest_namespace)
:   Fixture that returns a  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  that will be injected into the namespace of doctests.

    Usually this fixture is used in conjunction with another `autouse` fixture:

    ```
    @pytest.fixture(autouse=True)def add_np(doctest_namespace):
        doctest_namespace["np"] = numpy
    ```

    For more details:  [‘doctest\_namespace’ fixture](../how-to/doctest.html#doctest-namespace)  .

### monkeypatch

**Tutorial** :  [How to monkeypatch/mock modules and environments](../how-to/monkeypatch.html#monkeypatching)

monkeypatch ( ) [[source]](../_modules/_pytest/monkeypatch.html#monkeypatch)
:   A convenient fixture for monkey-patching.

    The fixture provides these methods to modify objects, dictionaries, or  [`os.environ`](https://docs.python.org/3/library/os.html#os.environ "(in Python v3.14)")  :

    * [`monkeypatch.setattr(obj, name, value, raising=True)`](#pytest.MonkeyPatch.setattr "pytest.MonkeyPatch.setattr")
    * [`monkeypatch.delattr(obj, name, raising=True)`](#pytest.MonkeyPatch.delattr "pytest.MonkeyPatch.delattr")
    * [`monkeypatch.setitem(mapping, name, value)`](#pytest.MonkeyPatch.setitem "pytest.MonkeyPatch.setitem")
    * [`monkeypatch.delitem(obj, name, raising=True)`](#pytest.MonkeyPatch.delitem "pytest.MonkeyPatch.delitem")
    * [`monkeypatch.setenv(name, value, prepend=None)`](#pytest.MonkeyPatch.setenv "pytest.MonkeyPatch.setenv")
    * [`monkeypatch.delenv(name, raising=True)`](#pytest.MonkeyPatch.delenv "pytest.MonkeyPatch.delenv")
    * [`monkeypatch.syspath_prepend(path)`](#pytest.MonkeyPatch.syspath_prepend "pytest.MonkeyPatch.syspath_prepend")
    * [`monkeypatch.chdir(path)`](#pytest.MonkeyPatch.chdir "pytest.MonkeyPatch.chdir")
    * [`monkeypatch.context()`](#pytest.MonkeyPatch.context "pytest.MonkeyPatch.context")

    All modifications will be undone after the requesting test function or fixture has finished. The `raising` parameter determines if a  [`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError "(in Python v3.14)")  or  [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "(in Python v3.14)")  will be raised if the set/deletion operation does not have the specified target.

    To undo modifications done by the fixture in a contained scope, use  [`context()`](#pytest.MonkeyPatch.context "pytest.MonkeyPatch.context")  .

    Returns a  [`MonkeyPatch`](#pytest.MonkeyPatch "pytest.MonkeyPatch")  instance.

final class MonkeyPatch [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch)
:   Helper to conveniently monkeypatch attributes/items/environment variables/syspath.

    Returned by the  [`monkeypatch`](#std-fixture-monkeypatch)  fixture.

    Changed in version 6.2:  Can now also be used directly as `pytest.MonkeyPatch()` , for when the fixture is not available. In this case, use  [`with MonkeyPatch.context() as mp:`](#pytest.MonkeyPatch.context "pytest.MonkeyPatch.context")  or remember to call  [`undo()`](#pytest.MonkeyPatch.undo "pytest.MonkeyPatch.undo")  explicitly.

    classmethod context ( ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.context)
    :   Context manager that returns a new  [`MonkeyPatch`](#pytest.MonkeyPatch "pytest.MonkeyPatch")  object which undoes any patching done inside the `with` block upon exit.

        Example:

        ```
        import functools

        def test_partial(monkeypatch):
            with monkeypatch.context() as m:
                m.setattr(functools, "partial", 3)
        ```

        Useful in situations where it is desired to undo some patches before the test ends, such as mocking `stdlib` functions that might break pytest itself if mocked (for examples of this see [#3290](https://github.com/pytest-dev/pytest/issues/3290) ).

    setattr ( *target : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")* , *name : [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")* , *value : NotSetType = NotSetType.token* , *raising : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = True* ) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.setattr)

    setattr ( *target : [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")* , *name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")* , *value : [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")* , *raising : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = True* ) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
    :   Set attribute value on target, memorizing the old value.

        For example:

        ```
        import os

        monkeypatch.setattr(os, "getcwd", lambda: "/")
        ```

        The code above replaces the  [`os.getcwd()`](https://docs.python.org/3/library/os.html#os.getcwd "(in Python v3.14)")  function by a `lambda` which always returns `"/"` .

        For convenience, you can specify a string as `target` which will be interpreted as a dotted import path, with the last part being the attribute name:

        ```
        monkeypatch.setattr("os.getcwd", lambda: "/")
        ```

        Raises  [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "(in Python v3.14)")  if the attribute does not exist, unless `raising` is set to False.

        **Where to patch**

        `monkeypatch.setattr` works by (temporarily) changing the object that a name points to with another one. There can be many names pointing to any individual object, so for patching to work you must ensure that you patch the name used by the system under test.

        See the section  [Where to patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch "(in Python v3.14)")  in the  [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock "(in Python v3.14)")  docs for a complete explanation, which is meant for  [`unittest.mock.patch()`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch "(in Python v3.14)")  but applies to `monkeypatch.setattr` as well.

    delattr ( *target* , *name = NotSetType.token* , *raising = True* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.delattr)
    :   Delete attribute `name` from `target` .

        If no `name` is specified and `target` is a string it will be interpreted as a dotted import path with the last part being the attribute name.

        Raises AttributeError it the attribute does not exist, unless `raising` is set to False.

    setitem ( *dic* , *name* , *value* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.setitem)
    :   Set dictionary entry `name` to value.

    delitem ( *dic* , *name* , *raising = True* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.delitem)
    :   Delete `name` from dict.

        Raises `KeyError` if it doesn’t exist, unless `raising` is set to False.

    setenv ( *name* , *value* , *prepend = None* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.setenv)
    :   Set environment variable `name` to `value` .

        If `prepend` is a character, read the current environment variable value and prepend the `value` adjoined with the `prepend` character.

    delenv ( *name* , *raising = True* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.delenv)
    :   Delete `name` from the environment.

        Raises `KeyError` if it does not exist, unless `raising` is set to False.

    syspath\_prepend ( *path* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.syspath_prepend)
    :   Prepend `path` to `sys.path` list of import locations.

    chdir ( *path* ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.chdir)
    :   Change the current working directory to the specified path.

        Parameters :
        :   **path** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The path to change into.

    undo ( ) [[source]](../_modules/_pytest/monkeypatch.html#MonkeyPatch.undo)
    :   Undo previous changes.

        This call consumes the undo stack. Calling it a second time has no effect unless you do more monkeypatching after the undo call.

        There is generally no need to call `undo()` , since it is called automatically during tear-down.

        Note

        The same `monkeypatch` fixture is used across a single test function invocation. If `monkeypatch` is used both by the test function itself and one of the test fixtures, calling `undo()` will undo all of the changes made in both functions.

        Prefer to use  [`context()`](#pytest.MonkeyPatch.context "pytest.MonkeyPatch.context")  instead.

### pytestconfig

pytestconfig ( ) [[source]](../_modules/_pytest/fixtures.html#pytestconfig)
:   Session-scoped fixture that returns the session’s  [`pytest.Config`](#pytest.Config "pytest.Config")  object.

    Example:

    ```
    def test_foo(pytestconfig):
        if pytestconfig.get_verbosity() > 0:
            ...
    ```

### pytester

Added in version 6.2.

Provides a  [`Pytester`](#pytest.Pytester "pytest.Pytester")  instance that can be used to run and test pytest itself.

It provides an empty directory where pytest can be executed in isolation, and contains facilities to write tests, configuration files, and match against expected output.

To use it, include in your topmost `conftest.py` file:

```
pytest_plugins = "pytester"
```

final class Pytester [[source]](../_modules/_pytest/pytester.html#Pytester)
:   Facilities to write tests/configuration files, execute pytest in isolation, and match against expected output, perfect for black-box testing of pytest plugins.

    It attempts to isolate the test run from external factors as much as possible, modifying the current working directory to  [`path`](#pytest.Pytester.path "pytest.Pytester.path")  and environment variables during initialization.

    exception TimeoutExpired [[source]](../_modules/_pytest/pytester.html#Pytester.TimeoutExpired)

    plugins : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ]
    :   A list of plugins to use with  [`parseconfig()`](#pytest.Pytester.parseconfig "pytest.Pytester.parseconfig")  and  [`runpytest()`](#pytest.Pytester.runpytest "pytest.Pytester.runpytest")  . Initially this is an empty list but plugins can be added to the list.

        When running in subprocess mode, specify plugins by name (str) - adding plugin objects directly is not supported.

    property path : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
    :   Temporary directory path used to create files/run tests from, etc.

    make\_hook\_recorder ( *pluginmanager* ) [[source]](../_modules/_pytest/pytester.html#Pytester.make_hook_recorder)
    :   Create a new  [`HookRecorder`](#pytest.HookRecorder "pytest.HookRecorder")  for a  [`PytestPluginManager`](#pytest.PytestPluginManager "pytest.PytestPluginManager")  .

    chdir ( ) [[source]](../_modules/_pytest/pytester.html#Pytester.chdir)
    :   Cd into the temporary directory.

        This is done automatically upon instantiation.

    makefile ( *ext* , *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.makefile)
    :   Create new text file(s) in the test directory.

        Parameters :
        :   * **ext** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The extension the file(s) should use, including the dot, e.g. `.py` .
            * **args** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – All args are treated as strings and joined using newlines. The result is written as contents to the file. The name of the file is based on the test function requesting this fixture.
            * **kwargs** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Each keyword is the name of a file, while the value of it will be written as contents of the file.

        Returns :
        :   The first created file.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

        Examples:

        ```
        pytester.makefile(".txt", "line1", "line2")

        pytester.makefile(".ini", pytest="[pytest]\naddopts=-rs\n")
        ```

        To create binary files, use  [`pathlib.Path.write_bytes()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_bytes "(in Python v3.14)")  directly:

        ```
        filename = pytester.path.joinpath("foo.bin")filename.write_bytes(b"...")
        ```

    makeconftest ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.makeconftest)
    :   Write a conftest.py file.

        Parameters :
        :   **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The contents.

        Returns :
        :   The conftest.py file.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

    makeini ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.makeini)
    :   Write a tox.ini file.

        Parameters :
        :   **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The contents.

        Returns :
        :   The tox.ini file.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

    maketoml ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.maketoml)
    :   Write a pytest.toml file.

        Parameters :
        :   **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The contents.

        Returns :
        :   The pytest.toml file.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

        Added in version 9.0.

    getinicfg ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getinicfg)
    :   Return the pytest section from the tox.ini config file.

    makepyprojecttoml ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.makepyprojecttoml)
    :   Write a pyproject.toml file.

        Parameters :
        :   **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The contents.

        Returns :
        :   The pyproject.ini file.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

        Added in version 6.0.

    makepyfile ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.makepyfile)
    :   Shortcut for .makefile() with a .py extension.

        Defaults to the test name with a ‘.py’ extension, e.g test\_foobar.py, overwriting existing files.

        Examples:

        ```
        def test_something(pytester):
            # Initial file is created test_something.py.
            pytester.makepyfile("foobar")
            # To create multiple files, pass kwargs accordingly.
            pytester.makepyfile(custom="foobar")
            # At this point, both 'test_something.py' & 'custom.py' exist in the test directory.
        ```

    maketxtfile ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.maketxtfile)
    :   Shortcut for .makefile() with a .txt extension.

        Defaults to the test name with a ‘.txt’ extension, e.g test\_foobar.txt, overwriting existing files.

        Examples:

        ```
        def test_something(pytester):
            # Initial file is created test_something.txt.
            pytester.maketxtfile("foobar")
            # To create multiple files, pass kwargs accordingly.
            pytester.maketxtfile(custom="foobar")
            # At this point, both 'test_something.txt' & 'custom.txt' exist in the test directory.
        ```

    syspathinsert ( *path = None* ) [[source]](../_modules/_pytest/pytester.html#Pytester.syspathinsert)
    :   Prepend a directory to sys.path, defaults to  [`path`](#pytest.Pytester.path "pytest.Pytester.path")  .

        This is undone automatically when this object dies at the end of each test.

        Parameters :
        :   **path** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]*  *|*  *None* ) – The path.

    mkdir ( *name* ) [[source]](../_modules/_pytest/pytester.html#Pytester.mkdir)
    :   Create a new (sub)directory.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The name of the directory, relative to the pytester path.

        Returns :
        :   The created directory.

        Return type :
        :   [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

    mkpydir ( *name* ) [[source]](../_modules/_pytest/pytester.html#Pytester.mkpydir)
    :   Create a new python package.

        This creates a (sub)directory with an empty `__init__.py` file so it gets recognised as a Python package.

    copy\_example ( *name = None* ) [[source]](../_modules/_pytest/pytester.html#Pytester.copy_example)
    :   Copy file from project’s directory into the testdir.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – The name of the file to copy.

        Returns :
        :   Path to the copied directory (inside `self.path` ).

        Return type :
        :   [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

    getnode ( *config* , *arg* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getnode)
    :   Get the collection node of a file.

        Parameters :
        :   * **config** (  [*Config*](#pytest.Config "_pytest.config.Config")  ) – A pytest config. See  [`parseconfig()`](#pytest.Pytester.parseconfig "pytest.Pytester.parseconfig")  and  [`parseconfigure()`](#pytest.Pytester.parseconfigure "pytest.Pytester.parseconfigure")  for creating it.
            * **arg** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – Path to the file.

        Returns :
        :   The node.

        Return type :
        :   [*Collector*](#pytest.Collector "_pytest.nodes.Collector")  |  [*Item*](#pytest.Item "_pytest.nodes.Item")

    getpathnode ( *path* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getpathnode)
    :   Return the collection node of a file.

        This is like  [`getnode()`](#pytest.Pytester.getnode "pytest.Pytester.getnode")  but uses  [`parseconfigure()`](#pytest.Pytester.parseconfigure "pytest.Pytester.parseconfigure")  to create the (configured) pytest Config instance.

        Parameters :
        :   **path** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – Path to the file.

        Returns :
        :   The node.

        Return type :
        :   [*Collector*](#pytest.Collector "_pytest.nodes.Collector")  |  [*Item*](#pytest.Item "_pytest.nodes.Item")

    genitems ( *colitems* ) [[source]](../_modules/_pytest/pytester.html#Pytester.genitems)
    :   Generate all test items from a collection node.

        This recurses into the collection node and returns a list of all the test items contained within.

        Parameters :
        :   **colitems** (  [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*Item*](#pytest.Item "_pytest.nodes.Item")   *|*   [*Collector*](#pytest.Collector "_pytest.nodes.Collector")  *]* ) – The collection nodes.

        Returns :
        :   The collected items.

        Return type :
        :   [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [  [*Item*](#pytest.Item "_pytest.nodes.Item")  ]

    runitem ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runitem)
    :   Run the “test\_func” Item.

        The calling test instance (class containing the test method) must provide a `.getrunner()` method which should return a runner which can run the test protocol for a single item, e.g. `_pytest.runner.runtestprotocol` .

    inline\_runsource ( *source* , *\* cmdlineargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.inline_runsource)
    :   Run a test module in process using `pytest.main()` .

        This run writes “source” into a temporary file and runs `pytest.main()` on it, returning a  [`HookRecorder`](#pytest.HookRecorder "pytest.HookRecorder")  instance for the result.

        Parameters :
        :   * **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The source code of the test module.
            * **cmdlineargs** – Any extra command line arguments to use.

    inline\_genitems ( *\* args* ) [[source]](../_modules/_pytest/pytester.html#Pytester.inline_genitems)
    :   Run `pytest.main(['--collect-only'])` in-process.

        Runs the  [`pytest.main()`](#pytest.main "pytest.main")  function to run all of pytest inside the test process itself like  [`inline_run()`](#pytest.Pytester.inline_run "pytest.Pytester.inline_run")  , but returns a tuple of the collected items and a  [`HookRecorder`](#pytest.HookRecorder "pytest.HookRecorder")  instance.

    inline\_run ( *\* args* , *plugins = ()* , *no\_reraise\_ctrlc = False* ) [[source]](../_modules/_pytest/pytester.html#Pytester.inline_run)
    :   Run `pytest.main()` in-process, returning a HookRecorder.

        Runs the  [`pytest.main()`](#pytest.main "pytest.main")  function to run all of pytest inside the test process itself. This means it can return a  [`HookRecorder`](#pytest.HookRecorder "pytest.HookRecorder")  instance which gives more detailed results from that run than can be done by matching stdout/stderr from  [`runpytest()`](#pytest.Pytester.runpytest "pytest.Pytester.runpytest")  .

        Parameters :
        :   * **args** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – Command line arguments to pass to  [`pytest.main()`](#pytest.main "pytest.main")  .
            * **plugins** – Extra plugin instances the `pytest.main()` instance should use.
            * **no\_reraise\_ctrlc** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Typically we reraise keyboard interrupts from the child run. If True, the KeyboardInterrupt exception is captured.

    runpytest\_inprocess ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runpytest_inprocess)
    :   Return result of running pytest in-process, providing a similar interface to what self.runpytest() provides.

    runpytest ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runpytest)
    :   Run pytest inline or in a subprocess, depending on the command line option “–runpytest” and return a  [`RunResult`](#pytest.RunResult "pytest.RunResult")  .

    parseconfig ( *\* args* ) [[source]](../_modules/_pytest/pytester.html#Pytester.parseconfig)
    :   Return a new pytest  [`pytest.Config`](#pytest.Config "pytest.Config")  instance from given commandline args.

        This invokes the pytest bootstrapping code in \_pytest.config to create a new  [`pytest.PytestPluginManager`](#pytest.PytestPluginManager "pytest.PytestPluginManager")  and call the  [`pytest_cmdline_parse`](#std-hook-pytest_cmdline_parse)  hook to create a new  [`pytest.Config`](#pytest.Config "pytest.Config")  instance.

        If  [`plugins`](#pytest.Pytester.plugins "pytest.Pytester.plugins")  has been populated they should be plugin modules to be registered with the plugin manager.

    parseconfigure ( *\* args* ) [[source]](../_modules/_pytest/pytester.html#Pytester.parseconfigure)
    :   Return a new pytest configured Config instance.

        Returns a new  [`pytest.Config`](#pytest.Config "pytest.Config")  instance like  [`parseconfig()`](#pytest.Pytester.parseconfig "pytest.Pytester.parseconfig")  , but also calls the  [`pytest_configure`](#std-hook-pytest_configure)  hook.

    getitem ( *source* , *funcname = 'test\_func'* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getitem)
    :   Return the test item for a test function.

        Writes the source to a python file and runs pytest’s collection on the resulting module, returning the test item for the requested function name.

        Parameters :
        :   * **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The module source.
            * **funcname** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The name of the test function for which to return a test item.

        Returns :
        :   The test item.

        Return type :
        :   [*Item*](#pytest.Item "_pytest.nodes.Item")

    getitems ( *source* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getitems)
    :   Return all test items collected from the module.

        Writes the source to a Python file and runs pytest’s collection on the resulting module, returning all test items contained within.

    getmodulecol ( *source* , *configargs = ()* , *\** , *withinit = False* ) [[source]](../_modules/_pytest/pytester.html#Pytester.getmodulecol)
    :   Return the module collection node for `source` .

        Writes `source` to a file using  [`makepyfile()`](#pytest.Pytester.makepyfile "pytest.Pytester.makepyfile")  and then runs the pytest collection on it, returning the collection node for the test module.

        Parameters :
        :   * **source** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The source code of the module to collect.
            * **configargs** – Any extra arguments to pass to  [`parseconfigure()`](#pytest.Pytester.parseconfigure "pytest.Pytester.parseconfigure")  .
            * **withinit** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether to also write an `__init__.py` file to the same directory to ensure it is a package.

    collect\_by\_name ( *modcol* , *name* ) [[source]](../_modules/_pytest/pytester.html#Pytester.collect_by_name)
    :   Return the collection node for name from the module collection.

        Searches a module collection node for a collection node matching the given name.

        Parameters :
        :   * **modcol** (  [*Collector*](#pytest.Collector "_pytest.nodes.Collector")  ) – A module collection node; see  [`getmodulecol()`](#pytest.Pytester.getmodulecol "pytest.Pytester.getmodulecol")  .
            * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The name of the node to return.

    popen ( *cmdargs* , *stdout = -1* , *stderr = -1* , *stdin = NotSetType.token* , *\*\* kw* ) [[source]](../_modules/_pytest/pytester.html#Pytester.popen)
    :   Invoke  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  .

        Calls  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  making sure the current working directory is in `PYTHONPATH` .

        You probably want to use  [`run()`](#pytest.Pytester.run "pytest.Pytester.run")  instead.

    run ( *\* cmdargs* , *timeout = None* , *stdin = NotSetType.token* ) [[source]](../_modules/_pytest/pytester.html#Pytester.run)
    :   Run a command with arguments.

        Run a process using  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  saving the stdout and stderr.

        Parameters :
        :   * **cmdargs** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The sequence of arguments to pass to  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  , with path-like objects being converted to  [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  automatically.
            * **timeout** (  [*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")   *|*  *None* ) – The period in seconds after which to timeout and raise  [`Pytester.TimeoutExpired`](#pytest.Pytester.TimeoutExpired "pytest.Pytester.TimeoutExpired")  .
            * **stdin** ( *\_pytest.compat.NotSetType*  *|*   [*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")   *|*  *IO* *[* *Any* *]*  *|*   [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) –

              Optional standard input.

              + If it is `CLOSE_STDIN` (Default), then this method calls  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  with `stdin=subprocess.PIPE` , and the standard input is closed immediately after the new command is started.
              + If it is of type  [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")  , these bytes are sent to the standard input of the command.
              + Otherwise, it is passed through to  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  . For further information in this case, consult the document of the `stdin` parameter in  [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen "(in Python v3.14)")  .

        Returns :
        :   The result.

        Return type :
        :   [*RunResult*](#pytest.RunResult "_pytest.pytester.RunResult")

    runpython ( *script* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runpython)
    :   Run a python script using sys.executable as interpreter.

    runpython\_c ( *command* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runpython_c)
    :   Run `python -c "command"` .

    runpytest\_subprocess ( *\* args* , *timeout = None* ) [[source]](../_modules/_pytest/pytester.html#Pytester.runpytest_subprocess)
    :   Run pytest as a subprocess with given arguments.

        Any plugins added to the  [`plugins`](#pytest.Pytester.plugins "pytest.Pytester.plugins")  list will be added using the `-p` command line option. Additionally `--basetemp` is used to put any temporary files and directories in a numbered directory prefixed with “runpytest-” to not conflict with the normal numbered pytest location for temporary files and directories.

        Parameters :
        :   * **args** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*PathLike*](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – The sequence of arguments to pass to the pytest subprocess.
            * **timeout** (  [*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")   *|*  *None* ) – The period in seconds after which to timeout and raise  [`Pytester.TimeoutExpired`](#pytest.Pytester.TimeoutExpired "pytest.Pytester.TimeoutExpired")  .

        Returns :
        :   The result.

        Return type :
        :   [*RunResult*](#pytest.RunResult "_pytest.pytester.RunResult")

    spawn\_pytest ( *string* , *expect\_timeout = 10.0* ) [[source]](../_modules/_pytest/pytester.html#Pytester.spawn_pytest)
    :   Run pytest using pexpect.

        This makes sure to use the right pytest and sets up the temporary directory locations.

        The pexpect child is returned.

    spawn ( *cmd* , *expect\_timeout = 10.0* ) [[source]](../_modules/_pytest/pytester.html#Pytester.spawn)
    :   Run a command using pexpect.

        The pexpect child is returned.

final class RunResult [[source]](../_modules/_pytest/pytester.html#RunResult)
:   The result of running a command from  [`Pytester`](#pytest.Pytester "pytest.Pytester")  .

    ret : [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") | [ExitCode](#pytest.ExitCode "pytest.ExitCode")
    :   The return value.

    outlines
    :   List of lines captured from stdout.

    errlines
    :   List of lines captured from stderr.

    stdout
    :   [`LineMatcher`](#pytest.LineMatcher "pytest.LineMatcher")  of stdout.

        Use e.g.  [`str(stdout)`](#pytest.LineMatcher.__str__ "pytest.LineMatcher.__str__")  to reconstruct stdout, or the commonly used  [`stdout.fnmatch_lines()`](#pytest.LineMatcher.fnmatch_lines "pytest.LineMatcher.fnmatch_lines")  method.

    stderr
    :   [`LineMatcher`](#pytest.LineMatcher "pytest.LineMatcher")  of stderr.

    duration
    :   Duration in seconds.

    parseoutcomes ( ) [[source]](../_modules/_pytest/pytester.html#RunResult.parseoutcomes)
    :   Return a dictionary of outcome noun -> count from parsing the terminal output that the test process produced.

        The returned nouns will always be in plural form:

        ```
        ======= 1 failed, 1 passed, 1 warning, 1 error in 0.13s ====
        ```

        Will return `{"failed": 1, "passed": 1, "warnings": 1, "errors": 1}` .

    classmethod parse\_summary\_nouns ( *lines* ) [[source]](../_modules/_pytest/pytester.html#RunResult.parse_summary_nouns)
    :   Extract the nouns from a pytest terminal summary line.

        It always returns the plural noun for consistency:

        ```
        ======= 1 failed, 1 passed, 1 warning, 1 error in 0.13s ====
        ```

        Will return `{"failed": 1, "passed": 1, "warnings": 1, "errors": 1}` .

    assert\_outcomes ( *passed = 0* , *skipped = 0* , *failed = 0* , *errors = 0* , *xpassed = 0* , *xfailed = 0* , *warnings = None* , *deselected = None* ) [[source]](../_modules/_pytest/pytester.html#RunResult.assert_outcomes)
    :   Assert that the specified outcomes appear with the respective numbers (0 means it didn’t occur) in the text output from a test run.

        `warnings` and `deselected` are only checked if not None.

class LineMatcher [[source]](../_modules/_pytest/pytester.html#LineMatcher)
:   Flexible matching of text.

    This is a convenience class to test large texts like the output of commands.

    The constructor takes a list of lines without their trailing newlines, i.e. `text.splitlines()` .

    \_\_str\_\_ ( ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.__str__)
    :   Return the entire original text.

        Added in version 6.2:  You can use  [`str()`](#pytest.LineMatcher.str "pytest.LineMatcher.str")  in older versions.

    fnmatch\_lines\_random ( *lines2* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.fnmatch_lines_random)
    :   Check lines exist in the output in any order (using  [`fnmatch.fnmatch()`](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch "(in Python v3.14)")  ).

    re\_match\_lines\_random ( *lines2* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.re_match_lines_random)
    :   Check lines exist in the output in any order (using  [`re.match()`](https://docs.python.org/3/library/re.html#re.match "(in Python v3.14)")  ).

    get\_lines\_after ( *fnline* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.get_lines_after)
    :   Return all lines following the given line in the text.

        The given line can contain glob wildcards.

    fnmatch\_lines ( *lines2* , *\** , *consecutive = False* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.fnmatch_lines)
    :   Check lines exist in the output (using  [`fnmatch.fnmatch()`](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch "(in Python v3.14)")  ).

        The argument is a list of lines which have to match and can use glob wildcards. If they do not match a pytest.fail() is called. The matches and non-matches are also shown as part of the error message.

        Parameters :
        :   * **lines2** (  [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – String patterns to match.
            * **consecutive** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Match lines consecutively?

    re\_match\_lines ( *lines2* , *\** , *consecutive = False* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.re_match_lines)
    :   Check lines exist in the output (using  [`re.match()`](https://docs.python.org/3/library/re.html#re.match "(in Python v3.14)")  ).

        The argument is a list of lines which have to match using `re.match` . If they do not match a pytest.fail() is called.

        The matches and non-matches are also shown as part of the error message.

        Parameters :
        :   * **lines2** (  [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – string patterns to match.
            * **consecutive** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – match lines consecutively?

    no\_fnmatch\_line ( *pat* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.no_fnmatch_line)
    :   Ensure captured lines do not match the given pattern, using `fnmatch.fnmatch` .

        Parameters :
        :   **pat** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The pattern to match lines.

    no\_re\_match\_line ( *pat* ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.no_re_match_line)
    :   Ensure captured lines do not match the given pattern, using `re.match` .

        Parameters :
        :   **pat** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The regular expression to match lines.

    str ( ) [[source]](../_modules/_pytest/pytester.html#LineMatcher.str)
    :   Return the entire original text.

final class HookRecorder [[source]](../_modules/_pytest/pytester.html#HookRecorder)
:   Record all hooks called in a plugin manager.

    Hook recorders are created by  [`Pytester`](#pytest.Pytester "pytest.Pytester")  .

    This wraps all the hook calls in the plugin manager, recording each call before propagating the normal calls.

    getcalls ( *names* ) [[source]](../_modules/_pytest/pytester.html#HookRecorder.getcalls)
    :   Get all recorded calls to hooks with the given names (or name).

    matchreport ( *inamepart = ''* , *names = ('pytest\_runtest\_logreport', 'pytest\_collectreport')* , *when = None* ) [[source]](../_modules/_pytest/pytester.html#HookRecorder.matchreport)
    :   Return a testreport whose dotted import path matches.

final class RecordedHookCall [[source]](../_modules/_pytest/pytester.html#RecordedHookCall)
:   A recorded call to a hook.

    The arguments to the hook call are set as attributes. For example:

    ```
    calls = hook_recorder.getcalls("pytest_runtest_setup")# Suppose pytest_runtest_setup was called once with `item=an_item`.assert calls[0].item is an_item
    ```

### record\_property

**Tutorial** :  [record\_property](../how-to/output.html#record-property-example)

record\_property ( ) [[source]](../_modules/_pytest/junitxml.html#record_property)
:   Add extra properties to the calling test.

    User properties become part of the test report and are available to the configured reporters, like JUnit XML.

    The fixture is callable with `name, value` . The value is automatically XML-encoded.

    Example:

    ```
    def test_function(record_property):
        record_property("example_key", 1)
    ```

### record\_testsuite\_property

**Tutorial** :  [record\_testsuite\_property](../how-to/output.html#record-testsuite-property-example)

record\_testsuite\_property ( ) [[source]](../_modules/_pytest/junitxml.html#record_testsuite_property)
:   Record a new `<property>` tag as child of the root `<testsuite>` .

    This is suitable to writing global information regarding the entire test suite, and is compatible with `xunit2` JUnit family.

    This is a `session` -scoped fixture which is called with `(name, value)` . Example:

    ```
    def test_foo(record_testsuite_property):
        record_testsuite_property("ARCH", "PPC")
        record_testsuite_property("STORAGE_TYPE", "CEPH")
    ```

    Parameters :
    :   * **name** – The property name.
        * **value** – The property value. Will be converted to a string.

    Warning

    Currently this fixture **does not work** with the [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) plugin. See [#7767](https://github.com/pytest-dev/pytest/issues/7767) for details.

### recwarn

**Tutorial** :  [Recording warnings](../how-to/capture-warnings.html#recwarn)

recwarn ( ) [[source]](../_modules/_pytest/recwarn.html#recwarn)
:   Return a  [`WarningsRecorder`](#pytest.WarningsRecorder "_pytest.recwarn.WarningsRecorder")  instance that records all warnings emitted by test functions.

    See  [How to capture warnings](../how-to/capture-warnings.html#warnings)  for information on warning categories.

class WarningsRecorder [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder)
:   A context manager to record raised warnings.

    Each recorded warning is an instance of `warnings.WarningMessage` .

    Adapted from `warnings.catch_warnings` .

    Note

    `DeprecationWarning` and `PendingDeprecationWarning` are treated differently; see  [Ensuring code triggers a deprecation warning](../how-to/capture-warnings.html#ensuring-function-triggers)  .

    property list : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ WarningMessage ]
    :   The list of recorded warnings.

    \_\_getitem\_\_ ( *i* ) [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder.__getitem__)
    :   Get a recorded warning by index.

    \_\_iter\_\_ ( ) [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder.__iter__)
    :   Iterate through the recorded warnings.

    \_\_len\_\_ ( ) [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder.__len__)
    :   The number of recorded warnings.

    pop ( *cls = <class 'Warning'>* ) [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder.pop)
    :   Pop the first recorded warning which is an instance of `cls` , but not an instance of a child class of any other match. Raises `AssertionError` if there is no match.

    clear ( ) [[source]](../_modules/_pytest/recwarn.html#WarningsRecorder.clear)
    :   Clear the list of recorded warnings.

### request

**Example** :  [Pass different values to a test function, depending on command line options](../example/simple.html#request-example)

The `request` fixture is a special fixture providing information of the requesting test function.

class FixtureRequest [[source]](../_modules/_pytest/fixtures.html#FixtureRequest)
:   The type of the `request` fixture.

    A request object gives access to the requesting test context and has a `param` attribute in case the fixture is parametrized.

    fixturename : [Final](https://docs.python.org/3/library/typing.html#typing.Final "(in Python v3.14)")
    :   Fixture for which this request is being performed.

    property scope : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ]
    :   Scope string, one of “function”, “class”, “module”, “package”, “session”.

    property fixturenames : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]
    :   Names of all active fixtures in this request.

    abstract property node
    :   Underlying collection node (depends on current request scope).

    property config : [Config](#pytest.Config "_pytest.config.Config")
    :   The pytest config object associated with this request.

    property function
    :   Test function object if the request has a per-function scope.

    property cls
    :   Class (can be None) where the test function was collected.

    property instance
    :   Instance (can be None) on which test function was collected.

    property module
    :   Python module object where the test function was collected.

    property path : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
    :   Path where the test function was collected.

    property keywords : [MutableMapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ]
    :   Keywords/markers dictionary for the underlying node.

    property session : [Session](#pytest.Session "_pytest.main.Session")
    :   Pytest session object.

    abstractmethod addfinalizer ( *finalizer* ) [[source]](../_modules/_pytest/fixtures.html#FixtureRequest.addfinalizer)
    :   Add finalizer/teardown function to be called without arguments after the last test within the requesting test context finished execution.

    applymarker ( *marker* ) [[source]](../_modules/_pytest/fixtures.html#FixtureRequest.applymarker)
    :   Apply a marker to a single test function invocation.

        This method is useful if you don’t want to have a keyword/marker on all function invocations.

        Parameters :
        :   **marker** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*MarkDecorator*](#pytest.MarkDecorator "_pytest.mark.structures.MarkDecorator")  ) – An object created by a call to `pytest.mark.NAME(...)` .

    raiseerror ( *msg* ) [[source]](../_modules/_pytest/fixtures.html#FixtureRequest.raiseerror)
    :   Raise a FixtureLookupError exception.

        Parameters :
        :   **msg** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – An optional custom error message.

    getfixturevalue ( *argname* ) [[source]](../_modules/_pytest/fixtures.html#FixtureRequest.getfixturevalue)
    :   Dynamically run a named fixture function.

        Declaring fixtures via function argument is recommended where possible. But if you can only decide whether to use another fixture at test setup time, you may use this function to retrieve it inside a fixture or test function body.

        This method can be used during the test setup phase or the test run phase. Avoid using it during the teardown phase.

        Changed in version 9.1:  Calling `request.getfixturevalue()` during teardown to request a fixture that was not already requested  [is deprecated](../deprecations.html#dynamic-fixture-request-during-teardown)  .

        Parameters :
        :   **argname** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The fixture name.

        Raises :
        :   [**pytest.FixtureLookupError**](#pytest.FixtureLookupError "pytest.FixtureLookupError")  – If the given fixture could not be found.

### subtests

The `subtests` fixture enables declaring subtests inside test functions.

**Tutorial** :  [How to use subtests](../how-to/subtests.html#subtests)

class Subtests [[source]](../_modules/_pytest/subtests.html#Subtests)
:   Subtests fixture, enables declaring subtests inside test functions via the  [`test()`](#pytest.Subtests.test "pytest.Subtests.test")  method.

    test ( *msg = None* , *\*\* kwargs* ) [[source]](../_modules/_pytest/subtests.html#Subtests.test)
    :   Context manager for subtests, capturing exceptions raised inside the subtest scope and reporting assertion failures and errors individually.

        #### Usage

        ```
        def test(subtests):
            for i in range(5):
                with subtests.test("custom message", i=i):
                    assert i % 2 == 0
        ```

        param msg :
        :   If given, the message will be shown in the test report in case of subtest failure.

        param kwargs :
        :   Arbitrary values that are also added to the subtest report.

### testdir

Identical to  [`pytester`](#std-fixture-pytester)  , but provides an instance whose methods return legacy `py.path.local` objects instead when applicable.

New code should avoid using  [`testdir`](#std-fixture-testdir)  in favor of  [`pytester`](#std-fixture-pytester)  .

final class Testdir [[source]](../_modules/_pytest/legacypath.html#Testdir)
:   Similar to  [`Pytester`](#pytest.Pytester "pytest.Pytester")  , but this class works with legacy legacy\_path objects instead.

    All methods just forward to an internal  [`Pytester`](#pytest.Pytester "pytest.Pytester")  instance, converting results to `legacy_path` objects as necessary.

    exception TimeoutExpired

    property tmpdir : LocalPath
    :   Temporary directory where tests are executed.

    make\_hook\_recorder ( *pluginmanager* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.make_hook_recorder)
    :   See  [`Pytester.make_hook_recorder()`](#pytest.Pytester.make_hook_recorder "pytest.Pytester.make_hook_recorder")  .

    chdir ( ) [[source]](../_modules/_pytest/legacypath.html#Testdir.chdir)
    :   See  [`Pytester.chdir()`](#pytest.Pytester.chdir "pytest.Pytester.chdir")  .

    makefile ( *ext* , *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.makefile)
    :   See  [`Pytester.makefile()`](#pytest.Pytester.makefile "pytest.Pytester.makefile")  .

    makeconftest ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.makeconftest)
    :   See  [`Pytester.makeconftest()`](#pytest.Pytester.makeconftest "pytest.Pytester.makeconftest")  .

    makeini ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.makeini)
    :   See  [`Pytester.makeini()`](#pytest.Pytester.makeini "pytest.Pytester.makeini")  .

    getinicfg ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getinicfg)
    :   See  [`Pytester.getinicfg()`](#pytest.Pytester.getinicfg "pytest.Pytester.getinicfg")  .

    makepyprojecttoml ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.makepyprojecttoml)
    :   See  [`Pytester.makepyprojecttoml()`](#pytest.Pytester.makepyprojecttoml "pytest.Pytester.makepyprojecttoml")  .

    makepyfile ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.makepyfile)
    :   See  [`Pytester.makepyfile()`](#pytest.Pytester.makepyfile "pytest.Pytester.makepyfile")  .

    maketxtfile ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.maketxtfile)
    :   See  [`Pytester.maketxtfile()`](#pytest.Pytester.maketxtfile "pytest.Pytester.maketxtfile")  .

    syspathinsert ( *path = None* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.syspathinsert)
    :   See  [`Pytester.syspathinsert()`](#pytest.Pytester.syspathinsert "pytest.Pytester.syspathinsert")  .

    mkdir ( *name* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.mkdir)
    :   See  [`Pytester.mkdir()`](#pytest.Pytester.mkdir "pytest.Pytester.mkdir")  .

    mkpydir ( *name* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.mkpydir)
    :   See  [`Pytester.mkpydir()`](#pytest.Pytester.mkpydir "pytest.Pytester.mkpydir")  .

    copy\_example ( *name = None* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.copy_example)
    :   See  [`Pytester.copy_example()`](#pytest.Pytester.copy_example "pytest.Pytester.copy_example")  .

    getnode ( *config* , *arg* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getnode)
    :   See  [`Pytester.getnode()`](#pytest.Pytester.getnode "pytest.Pytester.getnode")  .

    getpathnode ( *path* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getpathnode)
    :   See  [`Pytester.getpathnode()`](#pytest.Pytester.getpathnode "pytest.Pytester.getpathnode")  .

    genitems ( *colitems* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.genitems)
    :   See  [`Pytester.genitems()`](#pytest.Pytester.genitems "pytest.Pytester.genitems")  .

    runitem ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runitem)
    :   See  [`Pytester.runitem()`](#pytest.Pytester.runitem "pytest.Pytester.runitem")  .

    inline\_runsource ( *source* , *\* cmdlineargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.inline_runsource)
    :   See  [`Pytester.inline_runsource()`](#pytest.Pytester.inline_runsource "pytest.Pytester.inline_runsource")  .

    inline\_genitems ( *\* args* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.inline_genitems)
    :   See  [`Pytester.inline_genitems()`](#pytest.Pytester.inline_genitems "pytest.Pytester.inline_genitems")  .

    inline\_run ( *\* args* , *plugins = ()* , *no\_reraise\_ctrlc = False* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.inline_run)
    :   See  [`Pytester.inline_run()`](#pytest.Pytester.inline_run "pytest.Pytester.inline_run")  .

    runpytest\_inprocess ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runpytest_inprocess)
    :   See  [`Pytester.runpytest_inprocess()`](#pytest.Pytester.runpytest_inprocess "pytest.Pytester.runpytest_inprocess")  .

    runpytest ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runpytest)
    :   See  [`Pytester.runpytest()`](#pytest.Pytester.runpytest "pytest.Pytester.runpytest")  .

    parseconfig ( *\* args* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.parseconfig)
    :   See  [`Pytester.parseconfig()`](#pytest.Pytester.parseconfig "pytest.Pytester.parseconfig")  .

    parseconfigure ( *\* args* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.parseconfigure)
    :   See  [`Pytester.parseconfigure()`](#pytest.Pytester.parseconfigure "pytest.Pytester.parseconfigure")  .

    getitem ( *source* , *funcname = 'test\_func'* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getitem)
    :   See  [`Pytester.getitem()`](#pytest.Pytester.getitem "pytest.Pytester.getitem")  .

    getitems ( *source* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getitems)
    :   See  [`Pytester.getitems()`](#pytest.Pytester.getitems "pytest.Pytester.getitems")  .

    getmodulecol ( *source* , *configargs = ()* , *withinit = False* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.getmodulecol)
    :   See  [`Pytester.getmodulecol()`](#pytest.Pytester.getmodulecol "pytest.Pytester.getmodulecol")  .

    collect\_by\_name ( *modcol* , *name* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.collect_by_name)
    :   See  [`Pytester.collect_by_name()`](#pytest.Pytester.collect_by_name "pytest.Pytester.collect_by_name")  .

    popen ( *cmdargs* , *stdout = -1* , *stderr = -1* , *stdin = NotSetType.token* , *\*\* kw* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.popen)
    :   See  [`Pytester.popen()`](#pytest.Pytester.popen "pytest.Pytester.popen")  .

    run ( *\* cmdargs* , *timeout = None* , *stdin = NotSetType.token* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.run)
    :   See  [`Pytester.run()`](#pytest.Pytester.run "pytest.Pytester.run")  .

    runpython ( *script* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runpython)
    :   See  [`Pytester.runpython()`](#pytest.Pytester.runpython "pytest.Pytester.runpython")  .

    runpython\_c ( *command* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runpython_c)
    :   See  [`Pytester.runpython_c()`](#pytest.Pytester.runpython_c "pytest.Pytester.runpython_c")  .

    runpytest\_subprocess ( *\* args* , *timeout = None* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.runpytest_subprocess)
    :   See  [`Pytester.runpytest_subprocess()`](#pytest.Pytester.runpytest_subprocess "pytest.Pytester.runpytest_subprocess")  .

    spawn\_pytest ( *string* , *expect\_timeout = 10.0* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.spawn_pytest)
    :   See  [`Pytester.spawn_pytest()`](#pytest.Pytester.spawn_pytest "pytest.Pytester.spawn_pytest")  .

    spawn ( *cmd* , *expect\_timeout = 10.0* ) [[source]](../_modules/_pytest/legacypath.html#Testdir.spawn)
    :   See  [`Pytester.spawn()`](#pytest.Pytester.spawn "pytest.Pytester.spawn")  .

### tmp\_path

**Tutorial** :  [How to use temporary directories and files in tests](../how-to/tmp_path.html#tmp-path)

tmp\_path ( ) [[source]](../_modules/_pytest/tmpdir.html#tmp_path)
:   Return a temporary directory (as  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  object) which is unique to each test function invocation. The temporary directory is created as a subdirectory of the base temporary directory, with configurable retention, as discussed in  [Temporary directory location and retention](../how-to/tmp_path.html#temporary-directory-location-and-retention)  .

### tmp\_path\_factory

**Tutorial** :  [The tmp\_path\_factory fixture](../how-to/tmp_path.html#tmp-path-factory-example)

`tmp_path_factory` is an instance of  [`TempPathFactory`](#pytest.TempPathFactory "pytest.TempPathFactory")  :

final class TempPathFactory [[source]](../_modules/_pytest/tmpdir.html#TempPathFactory)
:   Factory for temporary directories under the common base temp directory, as discussed at  [Temporary directory location and retention](../how-to/tmp_path.html#temporary-directory-location-and-retention)  .

    mktemp ( *basename* , *numbered = True* ) [[source]](../_modules/_pytest/tmpdir.html#TempPathFactory.mktemp)
    :   Create a new temporary directory managed by the factory.

        Parameters :
        :   * **basename** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Directory base name, must be a relative path.
            * **numbered** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If `True` , ensure the directory is unique by adding a numbered suffix greater than any existing one: `basename="foo-"` and `numbered=True` means that this function will create directories named `"foo-0"` , `"foo-1"` , `"foo-2"` and so on.

        Returns :
        :   The path to the new directory.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

    getbasetemp ( ) [[source]](../_modules/_pytest/tmpdir.html#TempPathFactory.getbasetemp)
    :   Return the base temporary directory, creating it if needed.

        Returns :
        :   The base temporary directory.

        Return type :
        :   [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")

### tmpdir

**Tutorial** :  [The tmpdir and tmpdir\_factory fixtures](../how-to/tmp_path.html#tmpdir-and-tmpdir-factory)

tmpdir ( )
:   Return a temporary directory (as [legacy\_path](https://py.readthedocs.io/en/latest/path.html) object) which is unique to each test function invocation. The temporary directory is created as a subdirectory of the base temporary directory, with configurable retention, as discussed in  [Temporary directory location and retention](../how-to/tmp_path.html#temporary-directory-location-and-retention)  .

    Note

    These days, it is preferred to use `tmp_path` .

    [About the tmpdir and tmpdir\_factory fixtures](../how-to/tmp_path.html#tmpdir-and-tmpdir-factory)  .

### tmpdir\_factory

**Tutorial** :  [The tmpdir and tmpdir\_factory fixtures](../how-to/tmp_path.html#tmpdir-and-tmpdir-factory)

`tmpdir_factory` is an instance of  [`TempdirFactory`](#pytest.TempdirFactory "pytest.TempdirFactory")  :

final class TempdirFactory [[source]](../_modules/_pytest/legacypath.html#TempdirFactory)
:   Backward compatibility wrapper that implements `py.path.local` for  [`TempPathFactory`](#pytest.TempPathFactory "pytest.TempPathFactory")  .

    Note

    These days, it is preferred to use `tmp_path_factory` .

    [About the tmpdir and tmpdir\_factory fixtures](../how-to/tmp_path.html#tmpdir-and-tmpdir-factory)  .

    mktemp ( *basename* , *numbered = True* ) [[source]](../_modules/_pytest/legacypath.html#TempdirFactory.mktemp)
    :   Same as  [`TempPathFactory.mktemp()`](#pytest.TempPathFactory.mktemp "pytest.TempPathFactory.mktemp")  , but returns a `py.path.local` object.

    getbasetemp ( ) [[source]](../_modules/_pytest/legacypath.html#TempdirFactory.getbasetemp)
    :   Same as  [`TempPathFactory.getbasetemp()`](#pytest.TempPathFactory.getbasetemp "pytest.TempPathFactory.getbasetemp")  , but returns a `py.path.local` object.

## Hooks

**Tutorial** :  [Writing plugins](../how-to/writing_plugins.html#writing-plugins)

Reference to all hooks which can be implemented by  [conftest.py files](../how-to/writing_plugins.html#localplugin)  and  [plugins](../how-to/writing_plugins.html#plugins)  .

### @pytest.hookimpl

@ pytest. hookimpl
:   pytest’s decorator for marking functions as hook implementations.

    See  [Writing hook functions](../how-to/writing_hook_functions.html#writinghooks)  and  [`pluggy.HookimplMarker()`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.HookimplMarker "(in pluggy v0.1)")  .

### @pytest.hookspec

@ pytest. hookspec
:   pytest’s decorator for marking functions as hook specifications.

    See  [Declaring new hooks](../how-to/writing_hook_functions.html#declaringhooks)  and  [`pluggy.HookspecMarker()`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.HookspecMarker "(in pluggy v0.1)")  .

### Bootstrapping hooks

Bootstrapping hooks called for plugins registered early enough (internal and third-party plugins).

pytest\_load\_initial\_conftests ( *early\_config* , *parser* , *args* ) [[source]](../_modules/_pytest/hookspec.html#pytest_load_initial_conftests)
:   Called to implement the loading of  [initial conftest files](../how-to/writing_plugins.html#pluginorder)  ahead of command line option parsing.

    Parameters :
    :   * **early\_config** – The pytest config object.
        * **args** – Arguments passed on the command line.
        * **parser** – To add command line options.

    #### Use in conftest plugins

    This hook is not called for conftest files.

pytest\_cmdline\_parse ( *pluginmanager* , *args* ) [[source]](../_modules/_pytest/hookspec.html#pytest_cmdline_parse)
:   Return an initialized  [`Config`](#pytest.Config "pytest.Config")  , parsing the specified args.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Note

    This hook is only called for plugin classes passed to the `plugins` arg when using [pytest.main](#pytest-main) to perform an in-process test run.

    Parameters :
    :   * **pluginmanager** – The pytest plugin manager.
        * **args** – List of arguments passed on the command line.

    Returns :
    :   A pytest config object.

    #### Use in conftest plugins

    This hook is not called for conftest files.

pytest\_cmdline\_main ( *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_cmdline_main)
:   Called for performing the main command line action.

    The default implementation will invoke the configure hooks and  [`pytest_runtestloop`](#std-hook-pytest_runtestloop)  .

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   **config** – The pytest config object.

    Returns :
    :   The exit code.

    #### Use in conftest plugins

    This hook is only called for  [initial conftests](../how-to/writing_plugins.html#pluginorder)  .

### Initialization hooks

Initialization hooks called for plugins and `conftest.py` files.

pytest\_addoption ( *parser* , *pluginmanager* ) [[source]](../_modules/_pytest/hookspec.html#pytest_addoption)
:   Register argparse-style options and config-style config values, called once at the beginning of a test run.

    Parameters :
    :   * **parser** – To add command line options, call  [`parser.addoption(...)`](#pytest.Parser.addoption "pytest.Parser.addoption")  . To add config-file values call  [`parser.addini(...)`](#pytest.Parser.addini "pytest.Parser.addini")  .
        * **pluginmanager** – The pytest plugin manager, which can be used to install  [`hookspec()`](#pytest.hookspec "pytest.hookspec")  ’s or  [`hookimpl()`](#pytest.hookimpl "pytest.hookimpl")  ’s and allow one plugin to call another plugin’s hooks to change how command line options are added.

    Options can later be accessed through the  [`config`](#pytest.Config "pytest.Config")  object, respectively:

    * [`config.getoption(name)`](#pytest.Config.getoption "pytest.Config.getoption")  to retrieve the value of a command line option.
    * [`config.getini(name)`](#pytest.Config.getini "pytest.Config.getini")  to retrieve a value read from a configuration file.

    The config object is passed around on many internal objects via the `.config` attribute or can be retrieved as the `pytestconfig` fixture.

    Note

    This hook is incompatible with hook wrappers.

    #### Use in conftest plugins

    If a conftest plugin implements this hook, it will be called immediately when the conftest is registered.

    This hook is only called for  [initial conftests](../how-to/writing_plugins.html#pluginorder)  .

pytest\_addhooks ( *pluginmanager* ) [[source]](../_modules/_pytest/hookspec.html#pytest_addhooks)
:   Called at plugin registration time to allow adding new hooks via a call to  [`pluginmanager.add_hookspecs(module_or_class, prefix)`](#pytest.PytestPluginManager.add_hookspecs "pytest.PytestPluginManager.add_hookspecs")  .

    Parameters :
    :   **pluginmanager** – The pytest plugin manager.

    Note

    This hook is incompatible with hook wrappers.

    #### Use in conftest plugins

    If a conftest plugin implements this hook, it will be called immediately when the conftest is registered.

pytest\_configure ( *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_configure)
:   Allow plugins and conftest files to perform initial configuration.

    Note

    This hook is incompatible with hook wrappers.

    Parameters :
    :   **config** – The pytest config object.

    #### Use in conftest plugins

    This hook is called for every  [initial conftest](../how-to/writing_plugins.html#pluginorder)  file after command line options have been parsed. After that, the hook is called for other conftest files as they are registered.

pytest\_unconfigure ( *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_unconfigure)
:   Called before test process is exited.

    Parameters :
    :   **config** – The pytest config object.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

pytest\_sessionstart ( *session* ) [[source]](../_modules/_pytest/hookspec.html#pytest_sessionstart)
:   Called after the `Session` object has been created and before performing collection and entering the run test loop.

    Parameters :
    :   **session** – The pytest session object.

    #### Use in conftest plugins

    This hook is only called for  [initial conftests](../how-to/writing_plugins.html#pluginorder)  .

pytest\_sessionfinish ( *session* , *exitstatus* ) [[source]](../_modules/_pytest/hookspec.html#pytest_sessionfinish)
:   Called after whole test run finished, right before returning the exit status to the system.

    Parameters :
    :   * **session** – The pytest session object.
        * **exitstatus** – The status which pytest will return to the system.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

pytest\_plugin\_registered ( *plugin* , *plugin\_name* , *manager* ) [[source]](../_modules/_pytest/hookspec.html#pytest_plugin_registered)
:   A new pytest plugin got registered.

    Parameters :
    :   * **plugin** – The plugin module or instance.
        * **plugin\_name** – The name by which the plugin is registered.
        * **manager** – The pytest plugin manager.

    Note

    This hook is incompatible with hook wrappers.

    #### Use in conftest plugins

    If a conftest plugin implements this hook, it will be called immediately when the conftest is registered, once for each plugin registered thus far (including itself!), and for all plugins thereafter when they are registered.

### Collection hooks

`pytest` calls the following hooks for collecting files and directories:

pytest\_collection ( *session* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collection)
:   Perform the collection phase for the given session.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  . The return value is not used, but only stops further processing.

    The default collection phase is this (see individual hooks for full details):

    1. Starting from `session` as the initial collector:

    > 1. `pytest_collectstart(collector)`
    > 2. `report = pytest_make_collect_report(collector)`
    > 3. `pytest_exception_interact(collector, call, report)` if an interactive exception occurred
    > 4. For each collected node:
    >
    > > 1. If an item, `pytest_itemcollected(item)`
    > > 2. If a collector, recurse into it.
    >
    > 5. `pytest_collectreport(report)`

    2. `pytest_collection_modifyitems(session, config, items)`

    > 1. `pytest_deselected(items)` for any deselected items (may be called multiple times)

    3. Set `session.items` to the list of collected items
    4. `pytest_collection_finish(session)`
    5. Set `session.testscollected` to the number of collected items

    You can implement this hook to only perform some action before collection, for example the terminal plugin uses it to start displaying the collection counter (and returns `None` ).

    Parameters :
    :   **session** – The pytest session object.

    #### Use in conftest plugins

    This hook is only called for  [initial conftests](../how-to/writing_plugins.html#pluginorder)  .

pytest\_ignore\_collect ( *collection\_path* , *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_ignore_collect)
:   Return `True` to ignore this path for collection.

    Return `None` to let other plugins ignore the path for collection.

    Returning `False` will forcefully *not* ignore this path for collection, without giving a chance for other plugins to ignore this path.

    This hook is consulted for all files and directories prior to calling more specific hooks.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   * **collection\_path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The path to analyze.
        * **config** – The pytest config object.

    Changed in version 7.0.0:  The `collection_path` parameter was added as a  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  equivalent of the `path` parameter. The `path` parameter has been deprecated and removed in pytest 9.0.0.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collection path, only conftest files in parent directories of the collection path are consulted (if the path is a directory, its own conftest file is *not* consulted - a directory cannot ignore itself!).

pytest\_collect\_directory ( *path* , *parent* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collect_directory)
:   Create a  [`Collector`](#pytest.Collector "pytest.Collector")  for the given directory, or None if not relevant.

    Added in version 8.0.

    For best results, the returned collector should be a subclass of  [`Directory`](#pytest.Directory "pytest.Directory")  , but this is not required.

    The new node needs to have the specified `parent` as a parent.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   **path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The path to analyze.

    See  [Using a custom directory collector](../example/customdirectory.html#custom-directory-collectors)  for a simple example of use of this hook.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collection path, only conftest files in parent directories of the collection path are consulted (if the path is a directory, its own conftest file is *not* consulted - a directory cannot collect itself!).

pytest\_collect\_file ( *file\_path* , *parent* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collect_file)
:   Create a  [`Collector`](#pytest.Collector "pytest.Collector")  for the given path, or None if not relevant.

    For best results, the returned collector should be a subclass of  [`File`](#pytest.File "pytest.File")  , but this is not required.

    The new node needs to have the specified `parent` as a parent.

    Parameters :
    :   **file\_path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The path to analyze.

    Changed in version 7.0.0:  The `file_path` parameter was added as a  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  equivalent of the `path` parameter. The `path` parameter has been deprecated and removed in pytest 9.0.0.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given file path, only conftest files in parent directories of the file path are consulted.

pytest\_pycollect\_makemodule ( *module\_path* , *parent* ) [[source]](../_modules/_pytest/hookspec.html#pytest_pycollect_makemodule)
:   Return a  [`pytest.Module`](#pytest.Module "pytest.Module")  collector or None for the given path.

    This hook will be called for each matching test module path. The  [`pytest_collect_file`](#std-hook-pytest_collect_file)  hook needs to be used if you want to create test modules for files that do not match as a test module.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   **module\_path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The path of the module to collect.

    Changed in version 7.0.0:  The `module_path` parameter was added as a  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  equivalent of the `path` parameter. The `path` parameter has been deprecated in favor of `module_path` and removed in pytest 9.0.0.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given parent collector, only conftest files in the collector’s directory and its parent directories are consulted.

For influencing the collection of objects in Python modules you can use the following hook:

pytest\_pycollect\_makeitem ( *collector* , *name* , *obj* ) [[source]](../_modules/_pytest/hookspec.html#pytest_pycollect_makeitem)
:   Return a custom item/collector for a Python object in a module, or None.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   * **collector** – The module/class collector.
        * **name** – The name of the object in the module/class.
        * **obj** – The object.

    Returns :
    :   The created items/collectors.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collector, only conftest files in the collector’s directory and its parent directories are consulted.

pytest\_generate\_tests ( *metafunc* ) [[source]](../_modules/_pytest/hookspec.html#pytest_generate_tests)
:   Generate (multiple) parametrized calls to a test function.

    Parameters :
    :   **metafunc** – The  [`Metafunc`](#pytest.Metafunc "pytest.Metafunc")  helper for the test function.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given function definition, only conftest files in the functions’s directory and its parent directories are consulted.

pytest\_make\_parametrize\_id ( *config* , *val* , *argname* ) [[source]](../_modules/_pytest/hookspec.html#pytest_make_parametrize_id)
:   Return a user-friendly string representation of the given `val` that will be used by @pytest.mark.parametrize calls, or None if the hook doesn’t know about `val` .

    The parameter name is available as `argname` , if required.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   * **config** – The pytest config object.
        * **val** – The parametrized value.
        * **argname** – The automatic parameter name produced by pytest.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

Hooks for influencing test skipping:

pytest\_markeval\_namespace ( *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_markeval_namespace)
:   Called when constructing the globals dictionary used for evaluating string conditions in xfail/skipif markers.

    This is useful when the condition for a marker requires objects that are expensive or impossible to obtain during collection time, which is required by normal boolean conditions.

    Added in version 6.2.

    Parameters :
    :   **config** – The pytest config object.

    Returns :
    :   A dictionary of additional globals to add.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in parent directories of the item are consulted.

After collection is complete, you can modify the order of items, delete or otherwise amend the test items:

pytest\_collection\_modifyitems ( *session* , *config* , *items* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collection_modifyitems)
:   Called after collection has been performed. May filter or re-order the items in-place.

    When items are deselected (filtered out from `items` ), the hook  [`pytest_deselected`](#std-hook-pytest_deselected)  must be called explicitly with the deselected items to properly notify other plugins, e.g. with `config.hook.pytest_deselected(items=deselected_items)` .

    Parameters :
    :   * **session** – The pytest session object.
        * **config** – The pytest config object.
        * **items** – List of item objects.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

Note

If this hook is implemented in `conftest.py` files, it always receives all collected items, not only those under the `conftest.py` where it is implemented.

pytest\_collection\_finish ( *session* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collection_finish)
:   Called after collection has been performed and modified.

    Parameters :
    :   **session** – The pytest session object.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

### Test running (runtest) hooks

All runtest related hooks receive a  [`pytest.Item`](#pytest.Item "pytest.Item")  object.

pytest\_runtestloop ( *session* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtestloop)
:   Perform the main runtest loop (after collection finished).

    The default hook implementation performs the runtest protocol for all items collected in the session ( `session.items` ), unless the collection failed or the `collectonly` pytest option is set.

    If at any point  [`pytest.exit()`](#pytest.exit "pytest.exit")  is called, the loop is terminated immediately.

    If at any point `session.shouldfail` or `session.shouldstop` are set, the loop is terminated after the runtest protocol for the current item is finished.

    Parameters :
    :   **session** – The pytest session object.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  . The return value is not used, but only stops further processing.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

pytest\_runtest\_protocol ( *item* , *nextitem* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_protocol)
:   Perform the runtest protocol for a single test item.

    The default runtest protocol is this (see individual hooks for full details):

    * `pytest_runtest_logstart(nodeid, location)`
    * Setup phase:
      :   + `call = pytest_runtest_setup(item)` (wrapped in `CallInfo(when="setup")` )
          + `report = pytest_runtest_makereport(item, call)`
          + `pytest_runtest_logreport(report)`
          + `pytest_exception_interact(call, report)` if an interactive exception occurred
    * Call phase, if the setup passed and the `setuponly` pytest option is not set:
      :   + `call = pytest_runtest_call(item)` (wrapped in `CallInfo(when="call")` )
          + `report = pytest_runtest_makereport(item, call)`
          + `pytest_runtest_logreport(report)`
          + `pytest_exception_interact(call, report)` if an interactive exception occurred
    * Teardown phase:
      :   + `call = pytest_runtest_teardown(item, nextitem)` (wrapped in `CallInfo(when="teardown")` )
          + `report = pytest_runtest_makereport(item, call)`
          + `pytest_runtest_logreport(report)`
          + `pytest_exception_interact(call, report)` if an interactive exception occurred
    * `pytest_runtest_logfinish(nodeid, location)`

    Parameters :
    :   * **item** – Test item for which the runtest protocol is performed.
        * **nextitem** – The scheduled-to-be-next test item (or None if this is the end my friend).

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  . The return value is not used, but only stops further processing.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

pytest\_runtest\_logstart ( *nodeid* , *location* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_logstart)
:   Called at the start of running the runtest protocol for a single item.

    See  [`pytest_runtest_protocol`](#std-hook-pytest_runtest_protocol)  for a description of the runtest protocol.

    Parameters :
    :   * **nodeid** – Full node ID of the item.
        * **location** – A tuple of `(filename, lineno, testname)` where `filename` is a file path relative to `config.rootpath` and `lineno` is 0-based.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_runtest\_logfinish ( *nodeid* , *location* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_logfinish)
:   Called at the end of running the runtest protocol for a single item.

    See  [`pytest_runtest_protocol`](#std-hook-pytest_runtest_protocol)  for a description of the runtest protocol.

    Parameters :
    :   * **nodeid** – Full node ID of the item.
        * **location** – A tuple of `(filename, lineno, testname)` where `filename` is a file path relative to `config.rootpath` and `lineno` is 0-based.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_runtest\_setup ( *item* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_setup)
:   Called to perform the setup phase for a test item.

    The default implementation runs `setup()` on `item` and all of its parents (which haven’t been setup yet). This includes obtaining the values of fixtures required by the item (which haven’t been obtained yet).

    Parameters :
    :   **item** – The item.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_runtest\_call ( *item* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_call)
:   Called to run the test for test item (the call phase).

    The default implementation calls `item.runtest()` .

    Parameters :
    :   **item** – The item.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_runtest\_teardown ( *item* , *nextitem* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_teardown)
:   Called to perform the teardown phase for a test item.

    The default implementation runs the finalizers and calls `teardown()` on `item` and all of its parents (which need to be torn down). This includes running the teardown phase of fixtures required by the item (if they go out of scope).

    Parameters :
    :   * **item** – The item.
        * **nextitem** – The scheduled-to-be-next test item (None if no further test item is scheduled). This argument is used to perform exact teardowns, i.e. calling just enough finalizers so that nextitem only needs to call setup functions.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_runtest\_makereport ( *item* , *call* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_makereport)
:   Called to create a  [`TestReport`](#pytest.TestReport "pytest.TestReport")  for each of the setup, call and teardown runtest phases of a test item.

    See  [`pytest_runtest_protocol`](#std-hook-pytest_runtest_protocol)  for a description of the runtest protocol.

    Parameters :
    :   * **item** – The item.
        * **call** – The  [`CallInfo`](#pytest.CallInfo "pytest.CallInfo")  for the phase.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

For deeper understanding you may look at the default implementation of these hooks in `_pytest.runner` and maybe also in `_pytest.pdb` which interacts with `_pytest.capture` and its input/output capturing in order to immediately drop into interactive debugging when a test failure occurs.

pytest\_pyfunc\_call ( *pyfuncitem* ) [[source]](../_modules/_pytest/hookspec.html#pytest_pyfunc_call)
:   Call underlying test function.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   **pyfuncitem** – The function item.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

### Reporting hooks

Session related reporting hooks:

pytest\_collectstart ( *collector* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collectstart)
:   Collector starts collecting.

    Parameters :
    :   **collector** – The collector.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collector, only conftest files in the collector’s directory and its parent directories are consulted.

pytest\_make\_collect\_report ( *collector* ) [[source]](../_modules/_pytest/hookspec.html#pytest_make_collect_report)
:   Perform  [`collector.collect()`](#pytest.Collector.collect "pytest.Collector.collect")  and return a  [`CollectReport`](#pytest.CollectReport "pytest.CollectReport")  .

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Parameters :
    :   **collector** – The collector.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collector, only conftest files in the collector’s directory and its parent directories are consulted.

pytest\_itemcollected ( *item* ) [[source]](../_modules/_pytest/hookspec.html#pytest_itemcollected)
:   We just collected a test item.

    Parameters :
    :   **item** – The item.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_collectreport ( *report* ) [[source]](../_modules/_pytest/hookspec.html#pytest_collectreport)
:   Collector finished collecting.

    Parameters :
    :   **report** – The collect report.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given collector, only conftest files in the collector’s directory and its parent directories are consulted.

pytest\_deselected ( *items* ) [[source]](../_modules/_pytest/hookspec.html#pytest_deselected)
:   Called for deselected test items, e.g. by keyword.

    Note that this hook has two integration aspects for plugins:

    * it can be *implemented* to be notified of deselected items
    * it must be *called* from  [`pytest_collection_modifyitems`](#std-hook-pytest_collection_modifyitems)  implementations when items are deselected (to properly notify other plugins).

    May be called multiple times.

    Parameters :
    :   **items** – The items.

    #### Use in conftest plugins

    Any conftest file can implement this hook.

pytest\_report\_header ( *config* , *start\_path* ) [[source]](../_modules/_pytest/hookspec.html#pytest_report_header)
:   Return a string or list of strings to be displayed as header info for terminal reporting.

    Parameters :
    :   * **config** – The pytest config object.
        * **start\_path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The starting dir.

    Note

    Lines returned by a plugin are displayed before those of plugins which ran before it. If you want to have your line(s) displayed first, use  [trylast=True](../how-to/writing_hook_functions.html#plugin-hookorder)  .

    Changed in version 7.0.0:  The `start_path` parameter was added as a  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  equivalent of the `startdir` parameter. The `startdir` parameter has been deprecated and removed in pytest 9.0.0.

    #### Use in conftest plugins

    This hook is only called for  [initial conftests](../how-to/writing_plugins.html#pluginorder)  .

pytest\_report\_collectionfinish ( *config* , *start\_path* , *items* ) [[source]](../_modules/_pytest/hookspec.html#pytest_report_collectionfinish)
:   Return a string or list of strings to be displayed after collection has finished successfully.

    These strings will be displayed after the standard “collected X items” message.

    Added in version 3.2.

    Parameters :
    :   * **config** – The pytest config object.
        * **start\_path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The starting dir.
        * **items** – List of pytest items that are going to be executed; this list should not be modified.

    Note

    Lines returned by a plugin are displayed before those of plugins which ran before it. If you want to have your line(s) displayed first, use  [trylast=True](../how-to/writing_hook_functions.html#plugin-hookorder)  .

    Changed in version 7.0.0:  The `start_path` parameter was added as a  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  equivalent of the `startdir` parameter. The `startdir` parameter has been deprecated and removed in pytest 9.0.0.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_report\_teststatus ( *report* , *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_report_teststatus)
:   Return result-category, shortletter and verbose word for status reporting.

    The result-category is a category in which to count the result, for example “passed”, “skipped”, “error” or the empty string.

    The shortletter is shown as testing progresses, for example “.”, “s”, “E” or the empty string.

    The verbose word is shown as testing progresses in verbose mode, for example “PASSED”, “SKIPPED”, “ERROR” or the empty string.

    pytest may style these implicitly according to the report outcome. To provide explicit styling, return a tuple for the verbose word, for example `"rerun", "R", ("RERUN", {"yellow": True})` .

    Parameters :
    :   * **report** – The report object whose status is to be returned.
        * **config** – The pytest config object.

    Returns :
    :   The test status.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_report\_to\_serializable ( *config* , *report* ) [[source]](../_modules/_pytest/hookspec.html#pytest_report_to_serializable)
:   Serialize the given report object into a data structure suitable for sending over the wire, e.g. converted to JSON.

    Parameters :
    :   * **config** – The pytest config object.
        * **report** – The report.

    #### Use in conftest plugins

    Any conftest file can implement this hook. The exact details may depend on the plugin which calls the hook.

pytest\_report\_from\_serializable ( *config* , *data* ) [[source]](../_modules/_pytest/hookspec.html#pytest_report_from_serializable)
:   Restore a report object previously serialized with  [`pytest_report_to_serializable`](#std-hook-pytest_report_to_serializable)  .

    Parameters :
    :   **config** – The pytest config object.

    #### Use in conftest plugins

    Any conftest file can implement this hook. The exact details may depend on the plugin which calls the hook.

pytest\_terminal\_summary ( *terminalreporter* , *exitstatus* , *config* ) [[source]](../_modules/_pytest/hookspec.html#pytest_terminal_summary)
:   Add a section to terminal summary reporting.

    Parameters :
    :   * **terminalreporter** – The internal terminal reporter object.
        * **exitstatus** – The exit status that will be reported back to the OS.
        * **config** – The pytest config object.

    Added in version 4.2:  The `config` parameter.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_fixture\_setup ( *fixturedef* , *request* ) [[source]](../_modules/_pytest/hookspec.html#pytest_fixture_setup)
:   Perform fixture setup execution.

    Parameters :
    :   * **fixturedef** – The fixture definition object.
        * **request** – The fixture request object.

    Returns :
    :   The return value of the call to the fixture function.

    Stops at first non-None result, see  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  .

    Note

    If the fixture function returns None, other implementations of this hook function will continue to be called, according to the behavior of the  [firstresult: stop at first non-None result](../how-to/writing_hook_functions.html#firstresult)  option.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given fixture, only conftest files in the fixture scope’s directory and its parent directories are consulted.

pytest\_fixture\_post\_finalizer ( *fixturedef* , *request* ) [[source]](../_modules/_pytest/hookspec.html#pytest_fixture_post_finalizer)
:   Called after fixture teardown, but before the cache is cleared, so the fixture result `fixturedef.cached_result` is still available (not `None` ).

    Parameters :
    :   * **fixturedef** – The fixture definition object.
        * **request** – The fixture request object.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given fixture, only conftest files in the fixture scope’s directory and its parent directories are consulted.

pytest\_warning\_recorded ( *warning\_message* , *when* , *nodeid* , *location* ) [[source]](../_modules/_pytest/hookspec.html#pytest_warning_recorded)
:   Process a warning captured by the internal pytest warnings plugin.

    Parameters :
    :   * **warning\_message** – The captured warning. This is the same object produced by  [`warnings.catch_warnings`](https://docs.python.org/3/library/warnings.html#warnings.catch_warnings "(in Python v3.14)")  , and contains the same attributes as the parameters of  [`warnings.showwarning()`](https://docs.python.org/3/library/warnings.html#warnings.showwarning "(in Python v3.14)")  .
        * **when** –

          Indicates when the warning was captured. Possible values:

          + `"config"` : during pytest configuration/initialization stage.
          + `"collect"` : during test collection.
          + `"runtest"` : during test execution.
        * **nodeid** – Full id of the item. Empty string for warnings that are not specific to a particular node.
        * **location** – When available, holds information about the execution context of the captured warning (filename, linenumber, function). `function` evaluates to <module> when the execution context is at the module level.

    Added in version 6.0.

    #### Use in conftest plugins

    Any conftest file can implement this hook. If the warning is specific to a particular node, only conftest files in parent directories of the node are consulted.

Central hook for reporting about test execution:

pytest\_runtest\_logreport ( *report* ) [[source]](../_modules/_pytest/hookspec.html#pytest_runtest_logreport)
:   Process the  [`TestReport`](#pytest.TestReport "pytest.TestReport")  produced for each of the setup, call and teardown runtest phases of an item.

    See  [`pytest_runtest_protocol`](#std-hook-pytest_runtest_protocol)  for a description of the runtest protocol.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

Assertion related hooks:

pytest\_assertrepr\_compare ( *config* , *op* , *left* , *right* ) [[source]](../_modules/_pytest/hookspec.html#pytest_assertrepr_compare)
:   Return explanation for comparisons in failing assert expressions.

    Return None for no custom explanation, otherwise return a list of strings. The strings will be joined by newlines but any newlines *in* a string will be escaped. Note that all but the first line will be indented slightly, the intention is for the first line to be a summary.

    Parameters :
    :   * **config** – The pytest config object.
        * **op** – The operator, e.g. `"=="` , `"!="` , `"not in"` .
        * **left** – The left operand.
        * **right** – The right operand.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

pytest\_assertion\_pass ( *item* , *lineno* , *orig* , *expl* ) [[source]](../_modules/_pytest/hookspec.html#pytest_assertion_pass)
:   Called whenever an assertion passes.

    Added in version 5.0.

    Use this hook to do some processing after a passing assertion. The original assertion information is available in the `orig` string and the pytest introspected assertion information is available in the `expl` string.

    This hook must be explicitly enabled by the  [`enable_assertion_pass_hook`](#confval-enable_assertion_pass_hook)  configuration option:

    toml

    ```
    [pytest]enable_assertion_pass_hook = true
    ```

     ini

    ```
    [pytest]enable_assertion_pass_hook = true
    ```

    You need to **clean the .pyc** files in your project directory and interpreter libraries when enabling this option, as assertions will require to be re-written.

    Parameters :
    :   * **item** – pytest item object of current test.
        * **lineno** – Line number of the assert statement.
        * **orig** – String with the original assertion.
        * **expl** – String with the assert explanation.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given item, only conftest files in the item’s directory and its parent directories are consulted.

### Debugging/Interaction hooks

There are few hooks which can be used for special reporting or interaction with exceptions:

pytest\_internalerror ( *excrepr* , *excinfo* ) [[source]](../_modules/_pytest/hookspec.html#pytest_internalerror)
:   Called for internal errors.

    Return True to suppress the fallback handling of printing an INTERNALERROR message directly to sys.stderr.

    Parameters :
    :   * **excrepr** – The exception repr object.
        * **excinfo** – The exception info.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_keyboard\_interrupt ( *excinfo* ) [[source]](../_modules/_pytest/hookspec.html#pytest_keyboard_interrupt)
:   Called for keyboard interrupt.

    Parameters :
    :   **excinfo** – The exception info.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_exception\_interact ( *node* , *call* , *report* ) [[source]](../_modules/_pytest/hookspec.html#pytest_exception_interact)
:   Called when an exception was raised which can potentially be interactively handled.

    May be called during collection (see  [`pytest_make_collect_report`](#std-hook-pytest_make_collect_report)  ), in which case `report` is a  [`CollectReport`](#pytest.CollectReport "pytest.CollectReport")  .

    May be called during runtest of an item (see  [`pytest_runtest_protocol`](#std-hook-pytest_runtest_protocol)  ), in which case `report` is a  [`TestReport`](#pytest.TestReport "pytest.TestReport")  .

    This hook is not called if the exception that was raised is an internal exception like `skip.Exception` .

    Parameters :
    :   * **node** – The item or collector.
        * **call** – The call information. Contains the exception.
        * **report** – The collection or test report.

    #### Use in conftest plugins

    Any conftest file can implement this hook. For a given node, only conftest files in parent directories of the node are consulted.

pytest\_enter\_pdb ( *config* , *pdb* ) [[source]](../_modules/_pytest/hookspec.html#pytest_enter_pdb)
:   Called upon pdb.set\_trace().

    Can be used by plugins to take special action just before the python debugger enters interactive mode.

    Parameters :
    :   * **config** – The pytest config object.
        * **pdb** – The Pdb instance.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

pytest\_leave\_pdb ( *config* , *pdb* ) [[source]](../_modules/_pytest/hookspec.html#pytest_leave_pdb)
:   Called when leaving pdb (e.g. with continue after pdb.set\_trace()).

    Can be used by plugins to take special action just after the python debugger leaves interactive mode.

    Parameters :
    :   * **config** – The pytest config object.
        * **pdb** – The Pdb instance.

    #### Use in conftest plugins

    Any conftest plugin can implement this hook.

## Collection tree objects

These are the collector and item classes (collectively called “nodes”) which make up the collection tree.

### Node

class Node [[source]](../_modules/_pytest/nodes.html#Node)
:   Bases:  [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)")

    Base class of  [`Collector`](#pytest.Collector "_pytest.nodes.Collector")  and  [`Item`](#pytest.Item "_pytest.nodes.Item")  , the components of the test collection tree.

    `Collector` 's are the internal nodes of the tree, and `Item` 's are the leaf nodes.

    fspath : LEGACY\_PATH
    :   A `LEGACY_PATH` copy of the  [`path`](#pytest.nodes.Node.path "_pytest.nodes.Node.path")  attribute. Intended for usage for methods not migrated to `pathlib.Path` yet, such as  [`Item.reportinfo`](#pytest.Item.reportinfo "pytest.Item.reportinfo")  . Will be deprecated in a future release, prefer using  [`path`](#pytest.nodes.Node.path "_pytest.nodes.Node.path")  instead.

    name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    config : [Config](#pytest.Config "pytest.Config")
    :   The pytest config object.

    session : [Session](#pytest.Session "pytest.Session")
    :   The pytest session this node is part of.

    path : [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
    :   Filesystem path where this node was collected from.

    keywords : MutableMapping [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , Any ]
    :   Keywords/markers collected from all scopes.

    own\_markers : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [Mark](#pytest.Mark "pytest.Mark") ]
    :   The marker objects belonging to this node.

    extra\_keyword\_matches : [set](https://docs.python.org/3/library/stdtypes.html#set "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]
    :   Allow adding of extra keywords to use for matching.

    stash : [Stash](#pytest.Stash "pytest.Stash")
    :   A place where plugins can store information on the node for their own use.

    classmethod from\_parent ( *parent* , *\*\* kw* ) [[source]](../_modules/_pytest/nodes.html#Node.from_parent)
    :   Public constructor for Nodes.

        This indirection got introduced in order to enable removing the fragile logic from the node constructors.

        Subclasses can use `super().from_parent(...)` when overriding the construction.

        Parameters :
        :   **parent** (  [*Node*](#pytest.nodes.Node "_pytest.nodes.Node")  ) – The parent node of this Node.

    property ihook : [HookRelay](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.HookRelay "(in pluggy v0.1)")
    :   Path-sensitive hook proxy used to call pytest hooks.

    warn ( *warning* ) [[source]](../_modules/_pytest/nodes.html#Node.warn)
    :   Issue a warning for this Node.

        Warnings will be displayed after the test session, unless explicitly suppressed.

        Parameters :
        :   **warning** (  [*Warning*](https://docs.python.org/3/library/exceptions.html#Warning "(in Python v3.14)")  ) – The warning instance to issue.

        Raises :
        :   [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)")  – If `warning` instance is not a subclass of Warning.

        Example usage:

        ```
        node.warn(PytestWarning("some message"))node.warn(UserWarning("some message"))
        ```

        Changed in version 6.2:  Any subclass of  [`Warning`](https://docs.python.org/3/library/exceptions.html#Warning "(in Python v3.14)")  is now accepted, rather than only  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")  subclasses.

    property nodeid : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   A ::-separated string denoting its collection tree address.

    iter\_parents ( ) [[source]](../_modules/_pytest/nodes.html#Node.iter_parents)
    :   Iterate over all parent collectors starting from and including self up to the root of the collection tree.

        Added in version 8.1.

    listchain ( ) [[source]](../_modules/_pytest/nodes.html#Node.listchain)
    :   Return a list of all parent collectors starting from the root of the collection tree down to and including self.

    add\_marker ( *marker* , *append = True* ) [[source]](../_modules/_pytest/nodes.html#Node.add_marker)
    :   Dynamically add a marker object to the node.

        Parameters :
        :   * **marker** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*MarkDecorator*](#pytest.MarkDecorator "_pytest.mark.structures.MarkDecorator")  ) – The marker.
            * **append** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether to append the marker, or prepend it.

    iter\_markers ( *name = None* ) [[source]](../_modules/_pytest/nodes.html#Node.iter_markers)
    :   Iterate over all markers of the node.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – If given, filter the results by the name attribute.

        Returns :
        :   An iterator of the markers of the node.

        Return type :
        :   [*Iterator*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "(in Python v3.14)")  [  [*Mark*](#pytest.Mark "_pytest.mark.structures.Mark")  ]

    iter\_markers\_with\_node ( *name = None* ) [[source]](../_modules/_pytest/nodes.html#Node.iter_markers_with_node)
    :   Iterate over all markers of the node.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – If given, filter the results by the name attribute.

        Returns :
        :   An iterator of (node, mark) tuples.

        Return type :
        :   [*Iterator*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "(in Python v3.14)")  [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [  [*Node*](#pytest.nodes.Node "_pytest.nodes.Node")  ,  [*Mark*](#pytest.Mark "_pytest.mark.structures.Mark")  ]]

    get\_closest\_marker ( *name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")* ) → [Mark](#pytest.Mark "_pytest.mark.structures.Mark") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/_pytest/nodes.html#Node.get_closest_marker)

    get\_closest\_marker ( *name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")* , *default : [Mark](#pytest.Mark "_pytest.mark.structures.Mark")* ) → [Mark](#pytest.Mark "_pytest.mark.structures.Mark")
    :   Return the first marker matching the name, from closest (for example function) to farther level (for example module level).

        Parameters :
        :   * **default** (  [*Mark*](#pytest.Mark "_pytest.mark.structures.Mark")   *|*  *None* ) – Fallback return value if no marker was found.
            * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Name to filter by.

    listextrakeywords ( ) [[source]](../_modules/_pytest/nodes.html#Node.listextrakeywords)
    :   Return a set of all extra keywords in self and any parents.

    addfinalizer ( *fin* ) [[source]](../_modules/_pytest/nodes.html#Node.addfinalizer)
    :   Register a function to be called without arguments when this node is finalized.

        This method can only be called when this node is active in a setup chain, for example during self.setup().

    getparent ( *cls* ) [[source]](../_modules/_pytest/nodes.html#Node.getparent)
    :   Get the closest parent node (including self) which is an instance of the given class.

        Parameters :
        :   **cls** (  [*type*](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type")  *[* *\_NodeType* *]* ) – The node class to search for.

        Returns :
        :   The node, if found.

        Return type :
        :   *\_NodeType* | None

    repr\_failure ( *excinfo* , *style = None* ) [[source]](../_modules/_pytest/nodes.html#Node.repr_failure)
    :   Return a representation of a collection or test failure.

        See also

        [Working with non-python tests](../example/nonpython.html#non-python-tests)

        Parameters :
        :   **excinfo** (  [*ExceptionInfo*](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* ) – Exception information for the failure.

### Collector

class Collector [[source]](../_modules/_pytest/nodes.html#Collector)
:   Bases:  [`Node`](#pytest.nodes.Node "_pytest.nodes.Node")  ,  [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)")

    Base class of all collectors.

    Collector create children through `collect()` and thus iteratively build the collection tree.

    exception CollectError [[source]](../_modules/_pytest/nodes.html#Collector.CollectError)
    :   Bases:  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")

        An error during collection, contains a custom message.

    abstractmethod collect ( ) [[source]](../_modules/_pytest/nodes.html#Collector.collect)
    :   Collect children (items and collectors) for this collector.

    repr\_failure ( *excinfo* ) [[source]](../_modules/_pytest/nodes.html#Collector.repr_failure)
    :   Return a representation of a collection failure.

        Parameters :
        :   **excinfo** (  [*ExceptionInfo*](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* ) – Exception information for the failure.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Item

class Item [[source]](../_modules/_pytest/nodes.html#Item)
:   Bases:  [`Node`](#pytest.nodes.Node "_pytest.nodes.Node")  ,  [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)")

    Base class of all test invocation items.

    Note that for a single function there might be multiple test invocation items.

    user\_properties : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ] ]
    :   A list of tuples (name, value) that holds user defined properties for this test.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

    abstractmethod runtest ( ) [[source]](../_modules/_pytest/nodes.html#Item.runtest)
    :   Run the test case for this item.

        Must be implemented by subclasses.

        See also

        [Working with non-python tests](../example/nonpython.html#non-python-tests)

    add\_report\_section ( *when* , *key* , *content* ) [[source]](../_modules/_pytest/nodes.html#Item.add_report_section)
    :   Add a new report section, similar to what’s done internally to add stdout and stderr captured output:

        ```
        item.add_report_section("call", "stdout", "report section contents")
        ```

        Parameters :
        :   * **when** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – One of the possible capture states, `"setup"` , `"call"` , `"teardown"` .
            * **key** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Name of the section, can be customized at will. Pytest uses `"stdout"` and `"stderr"` internally.
            * **content** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The full contents as a string.

    reportinfo ( ) [[source]](../_modules/_pytest/nodes.html#Item.reportinfo)
    :   Get location information for this item for test reports.

        Returns a tuple with three elements:

        * The path of the test (default `self.path` )
        * The 0-based line number of the test (default `None` )
        * A name of the test to be shown (default `""` )

        See also

        [Working with non-python tests](../example/nonpython.html#non-python-tests)

    property location : [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] [[source]](../_modules/_pytest/nodes.html#Item.location)
    :   Returns a tuple of `(relfspath, lineno, testname)` for this item where `relfspath` is file path relative to `config.rootpath` and lineno is a 0-based line number.

### File

class File [[source]](../_modules/_pytest/nodes.html#File)
:   Bases:  [`FSCollector`](#pytest.nodes.FSCollector "_pytest.nodes.FSCollector")  ,  [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)")

    Base class for collecting tests from a file.

    [Working with non-python tests](../example/nonpython.html#non-python-tests)  .

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### FSCollector

class FSCollector [[source]](../_modules/_pytest/nodes.html#FSCollector)
:   Bases:  [`Collector`](#pytest.Collector "_pytest.nodes.Collector")  ,  [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)")

    Base class for filesystem collectors.

    path
    :   Filesystem path where this node was collected from.

    classmethod from\_parent ( *parent* , *\** , *fspath = None* , *path = None* , *\*\* kw* ) [[source]](../_modules/_pytest/nodes.html#FSCollector.from_parent)
    :   The public constructor.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    session
    :   The pytest session this node is part of.

### Session

final class Session [[source]](../_modules/_pytest/main.html#Session)
:   Bases:  [`Collector`](#pytest.Collector "_pytest.nodes.Collector")

    The root of the collection tree.

    `Session` collects the initial paths given as arguments to pytest.

    exception Interrupted
    :   Bases:  [`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt "(in Python v3.14)")

        Signals that the test run was interrupted.

    exception Failed
    :   Bases:  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")

        Signals a stop as failed test run.

    property startpath : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
    :   The path from which pytest was invoked.

        Added in version 7.0.0.

    isinitpath ( *path* , *\** , *with\_parents = False* ) [[source]](../_modules/_pytest/main.html#Session.isinitpath)
    :   Is path an initial path?

        An initial path is a path explicitly given to pytest on the command line.

        Parameters :
        :   **with\_parents** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If set, also return True if the path is a parent of an initial path.

        Changed in version 8.0:  Added the `with_parents` parameter.

    perform\_collect ( *args : [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *genitems : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ True ] = True* ) → [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [Item](#pytest.Item "_pytest.nodes.Item") ] [[source]](../_modules/_pytest/main.html#Session.perform_collect)

    perform\_collect ( *args : [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None* , *genitems : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = True* ) → [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [Item](#pytest.Item "_pytest.nodes.Item") | [Collector](#pytest.Collector "_pytest.nodes.Collector") ]
    :   Perform the collection phase for this session.

        This is called by the default  [`pytest_collection`](#std-hook-pytest_collection)  hook implementation; see the documentation of this hook for more details. For testing purposes, it may also be called directly on a fresh `Session` .

        This function normally recursively expands any collectors collected from the session to their items, and only items are returned. For testing purposes, this may be suppressed by passing `genitems=False` , in which case the return value contains these collectors unexpanded, and `session.items` is empty.

    collect ( ) [[source]](../_modules/_pytest/main.html#Session.collect)
    :   Collect children (items and collectors) for this collector.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Package

class Package [[source]](../_modules/_pytest/python.html#Package)
:   Bases:  [`Directory`](#pytest.Directory "_pytest.nodes.Directory")

    Collector for files and directories in a Python packages – directories with an `__init__.py` file.

    Note

    Directories without an `__init__.py` file are instead collected by  [`Dir`](#pytest.Dir "pytest.Dir")  by default. Both are  [`Directory`](#pytest.Directory "pytest.Directory")  collectors.

    Changed in version 8.0:  Now inherits from  [`Directory`](#pytest.Directory "pytest.Directory")  .

    collect ( ) [[source]](../_modules/_pytest/python.html#Package.collect)
    :   Collect children (items and collectors) for this collector.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Module

class Module [[source]](../_modules/_pytest/python.html#Module)
:   Bases:  [`File`](#pytest.File "_pytest.nodes.File")  , `PyCollector`

    Collector for test classes and functions in a Python module.

    collect ( ) [[source]](../_modules/_pytest/python.html#Module.collect)
    :   Collect children (items and collectors) for this collector.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Class

class Class [[source]](../_modules/_pytest/python.html#Class)
:   Bases: `PyCollector`

    Collector for test methods (and nested classes) in a Python class.

    classmethod from\_parent ( *parent* , *\** , *name* , *obj = None* , *\*\* kw* ) [[source]](../_modules/_pytest/python.html#Class.from_parent)
    :   The public constructor.

    collect ( ) [[source]](../_modules/_pytest/python.html#Class.collect)
    :   Collect children (items and collectors) for this collector.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Function

class Function [[source]](../_modules/_pytest/python.html#Function)
:   Bases: `PyobjMixin` ,  [`Item`](#pytest.Item "_pytest.nodes.Item")

    Item responsible for setting up and executing a Python test function.

    Parameters :
    :   * **name** – The full function name, including any decorations like those added by parametrization ( `my_func[my_param]` ).
        * **parent** – The parent Node.
        * **config** – The pytest Config object.
        * **callspec** – If given, this function has been parametrized and the callspec contains meta information about the parametrization.
        * **callobj** – If given, the object which will be called when the Function is invoked, otherwise the callobj will be obtained from `parent` using `originalname` .
        * **keywords** – Keywords bound to the function object for “-k” matching.
        * **session** – The pytest Session object.
        * **fixtureinfo** – Fixture information already resolved at this fixture node..
        * **originalname** – The attribute name to use for accessing the underlying function object. Defaults to `name` . Set this if name is different from the original name, for example when it contains decorations like those added by parametrization ( `my_func[my_param]` ).

    originalname
    :   Original function name, without any decorations (for example parametrization adds a `"[...]"` suffix to function names), used to access the underlying function object from `parent` (in case `callobj` is not given explicitly).

        Added in version 3.0.

    classmethod from\_parent ( *parent* , *\*\* kw* ) [[source]](../_modules/_pytest/python.html#Function.from_parent)
    :   The public constructor.

    property function
    :   Underlying python ‘function’ object.

    property instance
    :   Python instance object the function is bound to.

        Returns None if not a test method, e.g. for a standalone test function, a class or a module.

    runtest ( ) [[source]](../_modules/_pytest/python.html#Function.runtest)
    :   Execute the underlying test function.

    repr\_failure ( *excinfo* ) [[source]](../_modules/_pytest/python.html#Function.repr_failure)
    :   Return a representation of a collection or test failure.

        See also

        [Working with non-python tests](../example/nonpython.html#non-python-tests)

        Parameters :
        :   **excinfo** (  [*ExceptionInfo*](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* ) – Exception information for the failure.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### FunctionDefinition

class FunctionDefinition [[source]](../_modules/_pytest/python.html#FunctionDefinition)
:   Bases:  [`Function`](#pytest.Function "_pytest.python.Function")

    This class is a stop gap solution until we evolve to have actual function definition nodes and manage to get rid of `metafunc` .

    runtest ( ) [[source]](../_modules/_pytest/python.html#FunctionDefinition.runtest)
    :   Execute the underlying test function.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

    setup ( )
    :   Execute the underlying test function.

## Objects

Objects accessible from  [fixtures](fixtures.html#fixture)  or  [hooks](#hook-reference)  or importable from `pytest` .

### CallInfo

final class CallInfo [[source]](../_modules/_pytest/runner.html#CallInfo)
:   Result/Exception info of a function invocation.

    excinfo : [ExceptionInfo](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo") [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
    :   The captured exception of the call, if it raised.

    start : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   The system time when the call started, in seconds since the epoch.

    stop : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   The system time when the call ended, in seconds since the epoch.

    duration : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   The call duration, in seconds.

    when : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'collect' , 'setup' , 'call' , 'teardown' ]
    :   The context of invocation: “collect”, “setup”, “call” or “teardown”.

    property result : TResult
    :   The return value of the call, if it didn’t raise.

        Can only be accessed if excinfo is None.

    classmethod from\_call ( *func* , *when* , *reraise = None* ) [[source]](../_modules/_pytest/runner.html#CallInfo.from_call)
    :   Call func, wrapping the result in a CallInfo.

        Parameters :
        :   * **func** ( *Callable* *[* *[* *]* *,*  *\_pytest.runner.TResult* *]* ) – The function to call. Called without arguments.
            * **when** (  [*Literal*](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)")  *[* *'collect'* *,*  *'setup'* *,*  *'call'* *,*  *'teardown'* *]* ) – The phase in which the function is called.
            * **reraise** (  [*type*](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]*  *|*   [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")  *[*  [*type*](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *,*  *...* *]*  *|*  *None* ) – Exception or exceptions that shall propagate if raised by the function, instead of being wrapped in the CallInfo.

### CollectReport

final class CollectReport [[source]](../_modules/_pytest/reports.html#CollectReport)
:   Bases: `BaseReport`

    Collection report object.

    Reports can contain arbitrary extra attributes.

    nodeid : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Normalized collection nodeid.

    outcome : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'passed' , 'failed' , 'skipped' ]
    :   Test outcome, always one of “passed”, “failed”, “skipped”.

    longrepr : [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [ExceptionInfo](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo") [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | TerminalRepr
    :   None or a failure representation.

    result
    :   The collected items and collection nodes.

    sections : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] ]
    :   Tuples of str `(heading, content)` with extra information for the test report. Used by pytest to add text captured from `stdout` , `stderr` , and intercepted logging events. May be used by other plugins to add arbitrary information to reports.

    property caplog : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured log lines, if log capturing is enabled.

        Added in version 3.5.

    property capstderr : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured text from stderr, if capturing is enabled.

        Added in version 3.0.

    property capstdout : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured text from stdout, if capturing is enabled.

        Added in version 3.0.

    property count\_towards\_summary : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   **Experimental** Whether this report should be counted towards the totals shown at the end of the test session: “1 passed, 1 failure, etc”.

        Note

        This function is considered **experimental** , so beware that it is subject to changes even in patch releases.

    property failed : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is failed.

    property fspath : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   The path portion of the reported node, as a string.

    property head\_line : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
    :   **Experimental** The head line shown with longrepr output for this report, more commonly during traceback representation during failures:

        ```
        ________ Test.foo ________
        ```

        In the example above, the head\_line is “Test.foo”.

        Note

        This function is considered **experimental** , so beware that it is subject to changes even in patch releases.

    property longreprtext : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Read-only property that returns the full string representation of `longrepr` .

        Added in version 3.0.

    property passed : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is passed.

    property skipped : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is skipped.

### Config

final class Config [[source]](../_modules/_pytest/config.html#Config)
:   Access to configuration values, pluginmanager and plugin hooks.

    Parameters :
    :   * **pluginmanager** (  [*PytestPluginManager*](#pytest.PytestPluginManager "pytest.PytestPluginManager")  ) – A pytest PluginManager.
        * **invocation\_params** (  [*InvocationParams*](#pytest.Config.InvocationParams "pytest.Config.InvocationParams")  ) – Object containing parameters regarding the  [`pytest.main()`](#pytest.main "pytest.main")  invocation.

    final class InvocationParams ( *\** , *args* , *plugins* , *dir* ) [[source]](../_modules/_pytest/config.html#Config.InvocationParams)
    :   Holds parameters passed during  [`pytest.main()`](#pytest.main "pytest.main")  .

        The object attributes are read-only.

        Added in version 5.1.

        Note

        Note that the environment variable `PYTEST_ADDOPTS` and the `addopts` configuration option are handled by pytest, not being included in the `args` attribute.

        Plugins accessing `InvocationParams` must be aware of that.

        args : [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , ... ]
        :   The command-line arguments as passed to  [`pytest.main()`](#pytest.main "pytest.main")  .

        plugins : [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") ] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
        :   Extra plugins, might be `None` .

        dir : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
        :   The directory from which  [`pytest.main()`](#pytest.main "pytest.main")  was invoked.

    class ArgsSource ( *\* values* ) [[source]](../_modules/_pytest/config.html#Config.ArgsSource)
    :   Indicates the source of the test arguments.

        Added in version 7.2.

        ARGS = 1
        :   Command line arguments.

        INVOCATION\_DIR = 2
        :   Invocation directory.

        TESTPATHS = 3
        :   ‘testpaths’ configuration value.

    option
    :   Access to command line option as attributes.

        Type :
        :   [argparse.Namespace](https://docs.python.org/3/library/argparse.html#argparse.Namespace "(in Python v3.14)")

    invocation\_params
    :   The parameters with which pytest was invoked.

        Type :
        :   [InvocationParams](#pytest.Config.InvocationParams "pytest.Config.InvocationParams")

    pluginmanager
    :   The plugin manager handles plugin registration and hook invocation.

        Type :
        :   [PytestPluginManager](#pytest.PytestPluginManager "pytest.PytestPluginManager")

    stash
    :   A place where plugins can store information on the config for their own use.

        Type :
        :   [Stash](#pytest.Stash "pytest.Stash")

    property rootpath : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
    :   The path to the  [rootdir](customize.html#rootdir)  .

        Added in version 6.1.

    property inipath : [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
    :   The path to the  [configfile](customize.html#configfiles)  .

        Added in version 6.1.

    add\_cleanup ( *func* ) [[source]](../_modules/_pytest/config.html#Config.add_cleanup)
    :   Add a function to be called when the config object gets out of use (usually coinciding with pytest\_unconfigure).

    classmethod fromdictargs ( *option\_dict* , *args* ) [[source]](../_modules/_pytest/config.html#Config.fromdictargs)
    :   Constructor usable for subprocesses.

    issue\_config\_time\_warning ( *warning* , *stacklevel* ) [[source]](../_modules/_pytest/config.html#Config.issue_config_time_warning)
    :   Issue and handle a warning during the “configure” stage.

        During `pytest_configure` we can’t capture warnings using the `catch_warnings_for_item` function because it is not possible to have hook wrappers around `pytest_configure` .

        This function is mainly intended for plugins that need to issue warnings during `pytest_configure` (or similar stages).

        Parameters :
        :   * **warning** (  [*Warning*](https://docs.python.org/3/library/exceptions.html#Warning "(in Python v3.14)")  ) – The warning instance.
            * **stacklevel** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) – stacklevel forwarded to warnings.warn.

    addinivalue\_line ( *name* , *line* ) [[source]](../_modules/_pytest/config.html#Config.addinivalue_line)
    :   Add a line to a configuration option. The option must have been declared but might not yet be set in which case the line becomes the first line in its value.

    getini ( *name* ) [[source]](../_modules/_pytest/config.html#Config.getini)
    :   Return configuration value the an  [configuration file](customize.html#configfiles)  .

        If a configuration value is not defined in a  [configuration file](customize.html#configfiles)  , then the `default` value provided while registering the configuration through  [`parser.addini`](#pytest.Parser.addini "pytest.Parser.addini")  will be returned. Please note that you can even provide `None` as a valid default value.

        If `default` is not provided while registering using  [`parser.addini`](#pytest.Parser.addini "pytest.Parser.addini")  , then a default value based on the `type` parameter passed to  [`parser.addini`](#pytest.Parser.addini "pytest.Parser.addini")  will be returned. The default values based on `type` are: `paths` , `pathlist` , `args` and `linelist` : empty list `[]` `bool` : `False` `string` : empty string `""` `int` : `0` `float` : `0.0`

        If neither the `default` nor the `type` parameter is passed while registering the configuration through  [`parser.addini`](#pytest.Parser.addini "pytest.Parser.addini")  , then the configuration is treated as a string and a default empty string ‘’ is returned.

        If the specified name hasn’t been registered through a prior  [`parser.addini`](#pytest.Parser.addini "pytest.Parser.addini")  call (usually from a plugin), a ValueError is raised.

    getoption ( *name* , *default = NotSetType.token* , *skip = False* ) [[source]](../_modules/_pytest/config.html#Config.getoption)
    :   Return command line option value.

        Parameters :
        :   * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Name of the option. You may also specify the literal `--OPT` option instead of the “dest” option name.
            * **default** (  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")  ) – Fallback value if no option of that name is **declared** via  [`pytest_addoption`](#std-hook-pytest_addoption)  . Note this parameter will be ignored when the option is **declared** even if the option’s value is `None` .
            * **skip** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If `True` , raise  [`pytest.skip()`](#pytest.skip "pytest.skip")  if option is undeclared or has a `None` value. Note that even if `True` , if a default was specified it will be returned instead of a skip.

    getvalue ( *name* , *path = None* ) [[source]](../_modules/_pytest/config.html#Config.getvalue)
    :   Deprecated, use getoption() instead.

    getvalueorskip ( *name* , *path = None* ) [[source]](../_modules/_pytest/config.html#Config.getvalueorskip)
    :   Deprecated, use getoption(skip=True) instead.

    VERBOSITY\_ASSERTIONS : Final = 'assertions'
    :   Verbosity type for failed assertions (see  [`verbosity_assertions`](#confval-verbosity_assertions)  ).

    VERBOSITY\_TEST\_CASES : Final = 'test\_cases'
    :   Verbosity type for test case execution (see  [`verbosity_test_cases`](#confval-verbosity_test_cases)  ).

    VERBOSITY\_SUBTESTS : Final = 'subtests'
    :   Verbosity type for failed subtests (see  [`verbosity_subtests`](#confval-verbosity_subtests)  ).

    get\_verbosity ( *verbosity\_type = None* ) [[source]](../_modules/_pytest/config.html#Config.get_verbosity)
    :   Retrieve the verbosity level for a fine-grained verbosity type.

        Parameters :
        :   **verbosity\_type** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – Verbosity type to get level for. If a level is configured for the given type, that value will be returned. If the given type is not a known verbosity type, the global verbosity level will be returned. If the given type is None (default), the global verbosity level will be returned.

        To configure a level for a fine-grained verbosity type, the configuration file should have a setting for the configuration name and a numeric value for the verbosity level. A special value of “auto” can be used to explicitly use the global verbosity level.

        Example:

        toml

        ```
        [tool.pytest]verbosity_assertions = 2
        ```

         ini

        ```
        [pytest]verbosity_assertions = 2
        ```

        ```
        pytest -v
        ```

        ```
        print(config.get_verbosity())  # 1print(config.get_verbosity(Config.VERBOSITY_ASSERTIONS))  # 2
        ```

### Dir

final class Dir [[source]](../_modules/_pytest/main.html#Dir)
:   Collector of files in a file system directory.

    Added in version 8.0.

    Note

    Python directories with an `__init__.py` file are instead collected by  [`Package`](#pytest.Package "pytest.Package")  by default. Both are  [`Directory`](#pytest.Directory "pytest.Directory")  collectors.

    classmethod from\_parent ( *parent* , *\** , *path* ) [[source]](../_modules/_pytest/main.html#Dir.from_parent)
    :   The public constructor.

        Parameters :
        :   * **parent** (  [*nodes.Collector*](#pytest.Collector "_pytest.nodes.Collector")  ) – The parent collector of this Dir.
            * **path** (  [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The directory’s path.

    collect ( ) [[source]](../_modules/_pytest/main.html#Dir.collect)
    :   Collect children (items and collectors) for this collector.

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### Directory

class Directory [[source]](../_modules/_pytest/nodes.html#Directory)
:   Base class for collecting files from a directory.

    A basic directory collector does the following: goes over the files and sub-directories in the directory and creates collectors for them by calling the hooks  [`pytest_collect_directory`](#std-hook-pytest_collect_directory)  and  [`pytest_collect_file`](#std-hook-pytest_collect_file)  , after checking that they are not ignored using  [`pytest_ignore_collect`](#std-hook-pytest_ignore_collect)  .

    The default directory collectors are  [`Dir`](#pytest.Dir "pytest.Dir")  and  [`Package`](#pytest.Package "pytest.Package")  .

    Added in version 8.0.

    [Using a custom directory collector](../example/customdirectory.html#custom-directory-collectors)  .

    config
    :   The pytest config object.

    name
    :   A unique name within the scope of the parent node.

    parent
    :   The parent collector node.

    path
    :   Filesystem path where this node was collected from.

    session
    :   The pytest session this node is part of.

### ExceptionInfo

final class ExceptionInfo [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo)
:   Wraps sys.exc\_info() objects and offers help for navigating the traceback.

    classmethod from\_exception ( *exception* , *exprinfo = None* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.from_exception)
    :   Return an ExceptionInfo for an existing exception.

        The exception must have a non- `None` `__traceback__` attribute, otherwise this function fails with an assertion error. This means that the exception must have been raised, or added a traceback with the  [`with_traceback()`](https://docs.python.org/3/library/exceptions.html#BaseException.with_traceback "(in Python v3.14)")  method.

        Parameters :
        :   **exprinfo** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – A text string helping to determine if we should strip `AssertionError` from the output. Defaults to the exception message/ `__str__()` .

        Added in version 7.4.

    classmethod from\_exc\_info ( *exc\_info* , *exprinfo = None* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.from_exc_info)
    :   Like  [`from_exception()`](#pytest.ExceptionInfo.from_exception "pytest.ExceptionInfo.from_exception")  , but using old-style exc\_info tuple.

    classmethod from\_current ( *exprinfo = None* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.from_current)
    :   Return an ExceptionInfo matching the current traceback.

        Warning

        Experimental API

        Parameters :
        :   **exprinfo** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – A text string helping to determine if we should strip `AssertionError` from the output. Defaults to the exception message/ `__str__()` .

    classmethod for\_later ( ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.for_later)
    :   Return an unfilled ExceptionInfo.

    fill\_unfilled ( *exc\_info* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.fill_unfilled)
    :   Fill an unfilled ExceptionInfo created with `for_later()` .

    property type : [type](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type") [ E ]
    :   The exception class.

    property value : E
    :   The exception value.

    property tb : [TracebackType](https://docs.python.org/3/library/types.html#types.TracebackType "(in Python v3.14)")
    :   The exception raw traceback.

    property typename : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   The type name of the exception.

    property traceback : Traceback
    :   The traceback.

    exconly ( *tryshort = False* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.exconly)
    :   Return the exception as a string.

        This is usually a single line “<exception type>: <exception str>”, but may also include additional lines for the exception notes, and detailed information for SyntaxError’s.

        Parameters :
        :   **tryshort** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If true, and the exception is an AssertionError, strip ‘AssertionError: ‘ from the beginning.

    errisinstance ( *exc* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.errisinstance)
    :   Return True if the exception is an instance of exc.

        Consider using `isinstance(excinfo.value, exc)` instead.

    getrepr ( *showlocals = False* , *style = 'long'* , *abspath = False* , *tbfilter = True* , *funcargs = False* , *truncate\_locals = True* , *truncate\_args = True* , *chain = True* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.getrepr)
    :   Return str()able representation of this exception info.

        The formatting parameters are ineffective if `style="native"` , since in this case the native formatting is used.

        Parameters :
        :   * **showlocals** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Show locals per traceback entry.
            * **style** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – long|short|line|no|native|value traceback style.
            * **abspath** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If paths should be changed to absolute or left unchanged.
            * **tbfilter** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")   *|*   [*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")  *[* *[*  [*ExceptionInfo*](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *]* *,*  *Traceback* *]* ) –

              A filter for traceback entries.

              + If false, don’t hide any entries.
              + If true, hide internal entries and entries that contain a local variable `__tracebackhide__ = True` .
              + If a callable, delegates the filtering to the callable.
            * **funcargs** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Show function arguments per traceback entry.
            * **truncate\_locals** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether to show a size-limited `repr()` of locals, or a full pretty-printing.
            * **truncate\_args** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether to show a size-limited truncated `repr()` of function arguments, or a full pretty-printing.
            * **chain** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – If chained exceptions should be shown.

        Changed in version 3.9:  Added the `chain` parameter.

    match ( *regexp* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.match)
    :   Check whether the regular expression `regexp` matches the string representation of the exception using  [`re.search()`](https://docs.python.org/3/library/re.html#re.search "(in Python v3.14)")  .

        If it matches `True` is returned, otherwise an `AssertionError` is raised.

    group\_contains ( *expected\_exception* , *\** , *match = None* , *depth = None* ) [[source]](../_modules/_pytest/_code/code.html#ExceptionInfo.group_contains)
    :   Check whether a captured exception group contains a matching exception.

        Parameters :
        :   * **expected\_exception** ( *Type* *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]*  *|*  *Tuple* *[* *Type* *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *]* ) – The expected exception type, or a tuple if one of multiple possible exception types are expected.
            * **match** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*re.Pattern*](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]*  *|*  *None* ) –

              If specified, a string containing a regular expression, or a regular expression object, that is tested against the string representation of the exception and its `PEP-678 <https://peps.python.org/pep-0678/>` `__notes__` using  [`re.search()`](https://docs.python.org/3/library/re.html#re.search "(in Python v3.14)")  .

              To match a literal string that may contain  [special characters](https://docs.python.org/3/library/re.html#re-syntax "(in Python v3.14)")  , the pattern can first be escaped with  [`re.escape()`](https://docs.python.org/3/library/re.html#re.escape "(in Python v3.14)")  .
            * **depth** ( *Optional* *[*  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  *]* ) – If `None` , will search for a matching exception at any nesting depth. If >= 1, will only match an exception if it’s at the specified depth (depth = 1 being the exceptions contained within the topmost exception group).

        Added in version 8.0.

        Warning

        This helper makes it easy to check for the presence of specific exceptions, but it is very bad for checking that the group does *not* contain *any other exceptions* . You should instead consider using  [`pytest.RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")

### ExitCode

class ExitCode ( *\* values* )
:   Encodes the valid exit codes by pytest.

    Currently users and plugins may supply other exit codes as well.

    Added in version 5.0.

### FixtureDef

class FixtureDef [[source]](../_modules/_pytest/fixtures.html#FixtureDef)
:   Bases:  [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic "(in Python v3.14)")  [ `FixtureValue` ]

    A container for a fixture definition.

    Note: At this time, only explicitly documented fields and methods are considered public stable API.

    property scope : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'session' , 'package' , 'module' , 'class' , 'function' ]
    :   Scope string, one of “function”, “class”, “module”, “package”, “session”.

    execute ( *request* ) [[source]](../_modules/_pytest/fixtures.html#FixtureDef.execute)
    :   Return the value of this fixture, executing it if not cached.

### MarkDecorator

class MarkDecorator [[source]](../_modules/_pytest/mark/structures.html#MarkDecorator)
:   A decorator for applying a mark on test functions and classes.

    `MarkDecorators` are created with `pytest.mark` :

    ```
    mark1 = pytest.mark.NAME  # Simple MarkDecoratormark2 = pytest.mark.NAME(name1=value)  # Parametrized MarkDecorator
    ```

    and can then be applied as decorators to test functions:

    ```
    @mark2def test_function():
        pass
    ```

    When a `MarkDecorator` is called, it does the following:

    1. If called with a single class as its only positional argument and no additional keyword arguments, it attaches the mark to the class so it gets applied automatically to all test cases found in that class.
    2. If called with a single function as its only positional argument and no additional keyword arguments, it attaches the mark to the function, containing all the arguments already stored internally in the `MarkDecorator` .
    3. When called in any other case, it returns a new `MarkDecorator` instance with the original `MarkDecorator` ’s content updated with the arguments passed to this call.

    Note: The rules above prevent a `MarkDecorator` from storing only a single function or class reference as its positional argument with no additional keyword or positional arguments. You can work around this by using `with_args()` .

    property name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Alias for mark.name.

    property args : [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") , ... ]
    :   Alias for mark.args.

    property kwargs : [Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ]
    :   Alias for mark.kwargs.

    with\_args ( *\* args* , *\*\* kwargs* ) [[source]](../_modules/_pytest/mark/structures.html#MarkDecorator.with_args)
    :   Return a MarkDecorator with extra arguments added.

        Unlike calling the MarkDecorator, with\_args() can be used even if the sole argument is a callable/class.

### MarkGenerator

final class MarkGenerator [[source]](../_modules/_pytest/mark/structures.html#MarkGenerator)
:   Factory for  [`MarkDecorator`](#pytest.MarkDecorator "pytest.MarkDecorator")  objects - exposed as a `pytest.mark` singleton instance.

    Example:

    ```
    import pytest

    @pytest.mark.slowtestdef test_function():
        pass
    ```

    applies a ‘slowtest’  [`Mark`](#pytest.Mark "pytest.Mark")  on `test_function` .

### Mark

final class Mark [[source]](../_modules/_pytest/mark/structures.html#Mark)
:   A pytest mark.

    name : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Name of the mark.

    args : [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") , ... ]
    :   Positional arguments of the mark decorator.

    kwargs : [Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ]
    :   Keyword arguments of the mark decorator.

    combined\_with ( *other* ) [[source]](../_modules/_pytest/mark/structures.html#Mark.combined_with)
    :   Return a new Mark which is a combination of this Mark and another Mark.

        Combines by appending args and merging kwargs.

        Parameters :
        :   **other** (  [*Mark*](#pytest.Mark "pytest.Mark")  ) – The mark to combine with.

        Return type :
        :   [Mark](#pytest.Mark "pytest.Mark")

### Metafunc

final class Metafunc [[source]](../_modules/_pytest/python.html#Metafunc)
:   Objects passed to the  [`pytest_generate_tests`](#std-hook-pytest_generate_tests)  hook.

    They help to inspect a test function and to generate tests according to test configuration or values specified in the class or module where a test function is defined.

    definition
    :   Access to the underlying  [`_pytest.python.FunctionDefinition`](#pytest.python.FunctionDefinition "_pytest.python.FunctionDefinition")  .

    config
    :   Access to the  [`pytest.Config`](#pytest.Config "pytest.Config")  object for the test session.

    module
    :   The module object where the test function is defined in.

    function
    :   Underlying Python test function.

    fixturenames
    :   Set of fixture names required by the test function.

    cls
    :   Class object where the test function is defined in or `None` .

    parametrize ( *argnames* , *argvalues* , *indirect = False* , *ids = None* , *scope = None* , *\** , *\_param\_mark = None* ) [[source]](../_modules/_pytest/python.html#Metafunc.parametrize)
    :   Add new invocations to the underlying test function using the list of argvalues for the given argnames. Parametrization is performed during the collection phase. If you need to setup expensive resources see about setting `indirect` to do it at test setup time instead.

        Can be called multiple times per test function (but only on different argument names), in which case each call parametrizes all previous parametrizations, e.g.

        ```
        unparametrized:         tparametrize ["x", "y"]: t[x], t[y]parametrize [1, 2]:     t[x-1], t[x-2], t[y-1], t[y-2]
        ```

        Parameters :
        :   * **argnames** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – A comma-separated string denoting one or more argument names, or a list/tuple of argument strings.
            * **argvalues** (  [*Iterable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)")  *[* *ParameterSet*  *|*   [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")  *]*  *|*   [*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")  *]* ) –

              The list of argvalues determines how often a test is invoked with different argument values.

              If only one argname was specified argvalues is a list of values. If N argnames were specified, argvalues must be a list of N-tuples, where each tuple-element specifies a value for its respective argname.

              Changed in version 9.1:  Passing a non-  [`Collection`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Collection "(in Python v3.14)")  iterable (such as a generator or iterator) is deprecated. See  [Non-Collection iterables in @pytest.mark.parametrize](../deprecations.html#parametrize-iterators)  for details.
            * **indirect** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")   *|*   [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – A list of arguments’ names (subset of argnames) or a boolean. If True the list contains all names from the argnames. Each argvalue corresponding to an argname in this list will be passed as request.param to its respective argname fixture function so that it can perform more expensive setups during the setup phase of a test rather than at collection time.
            * **ids** (  [*Iterable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)")  *[*  [*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")   *|*  *None* *]*  *|*   [*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")  *[* *[*  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")  *]* *,*   [*object*](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")   *|*  *None* *]*  *|*  *None* ) –

              Sequence of (or generator for) ids for `argvalues` , or a callable to return part of the id for each argvalue.

              With sequences (and generators like `itertools.count()` ) the returned ids should be of type `string` , `int` , `float` , `bool` , or `None` . They are mapped to the corresponding index in `argvalues` . `None` means to use the auto-generated id.

              Added in version 8.4:   [pytest.HIDDEN\_PARAM](#hidden-param)  means to hide the parameter set from the test name. Can only be used at most 1 time, as test names need to be unique.

              If it is a callable it will be called for each entry in `argvalues` , and the return value is used as part of the auto-generated id for the whole set (where parts are joined with dashes (“-“)). This is useful to provide more specific ids for certain items, e.g. dates. Returning `None` will use an auto-generated id.

              If no ids are provided they will be generated automatically from the argvalues.
            * **scope** (  [*Literal*](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)")  *[* *'session'* *,*  *'package'* *,*  *'module'* *,*  *'class'* *,*  *'function'* *]*  *|*  *None* ) – If specified it denotes the scope of the parameters. The scope is used for grouping tests by parameter instances. It will also override any fixture-function defined scope, allowing to set a dynamic scope using test context or configuration.

### Parser

final class Parser [[source]](../_modules/_pytest/config/argparsing.html#Parser)
:   Parser for command line arguments and config-file values.

    Variables :
    :   **extra\_info** – Dict of generic param -> value to display in case there’s an error processing the command line arguments.

    getgroup ( *name* , *description = ''* , *after = None* ) [[source]](../_modules/_pytest/config/argparsing.html#Parser.getgroup)
    :   Get (or create) a named option Group.

        Parameters :
        :   * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Name of the option group.
            * **description** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Long description for –help output.
            * **after** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – Name of another group, used for ordering –help output.

        Returns :
        :   The option group.

        Return type :
        :   [*OptionGroup*](#pytest.OptionGroup "_pytest.config.argparsing.OptionGroup")

        The returned group object has an `addoption` method with the same signature as  [`parser.addoption`](#pytest.Parser.addoption "pytest.Parser.addoption")  but will be shown in the respective group in the output of `pytest --help` .

    addoption ( *\* opts* , *\*\* attrs* ) [[source]](../_modules/_pytest/config/argparsing.html#Parser.addoption)
    :   Register a command line option.

        Parameters :
        :   * **opts** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Option names, can be short or long options.
            * **attrs** (  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")  ) – Same attributes as the argparse library’s  [`add_argument()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument "(in Python v3.14)")  function accepts.

        After command line parsing, options are available on the pytest config object via `config.option.NAME` where `NAME` is usually set by passing a `dest` attribute, for example `addoption("--long", dest="NAME", ...)` .

    parse\_known\_args ( *args* , *namespace = None* ) [[source]](../_modules/_pytest/config/argparsing.html#Parser.parse_known_args)
    :   Parse the known arguments at this point.

        Returns :
        :   An argparse namespace object.

        Return type :
        :   [*Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace "(in Python v3.14)")

    parse\_known\_and\_unknown\_args ( *args* , *namespace = None* ) [[source]](../_modules/_pytest/config/argparsing.html#Parser.parse_known_and_unknown_args)
    :   Parse the known arguments at this point, and also return the remaining unknown flag arguments.

        Returns :
        :   A tuple containing an argparse namespace object for the known arguments, and a list of unknown flag arguments.

        Return type :
        :   [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [  [*Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace "(in Python v3.14)")  , [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]]

    addini ( *name* , *help* , *type = None* , *default = NotSetType.token* , *\** , *aliases = ()* ) [[source]](../_modules/_pytest/config/argparsing.html#Parser.addini)
    :   Register a configuration file option.

        Parameters :
        :   * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Name of the configuration.
            * **type** (  [*Literal*](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)")  *[* *'string'* *,*  *'paths'* *,*  *'pathlist'* *,*  *'args'* *,*  *'linelist'* *,*  *'bool'* *,*  *'int'* *,*  *'float'* *]*  *|*  *None* ) –

              Type of the configuration. Can be:

              > + `string` : a string
              > + `bool` : a boolean
              > + `args` : a list of strings, separated as in a shell
              > + `linelist` : a list of strings, separated by line breaks
              > + `paths` : a list of  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  , separated as in a shell
              > + `pathlist` : a list of `py.path` , separated as in a shell
              > + `int` : an integer
              > + `float` : a floating-point number
              >
              > Added in version 8.4:  The `float` and `int` types.

              For `paths` and `pathlist` types, they are considered relative to the config-file. In case the execution is happening without a config-file defined, they will be considered relative to the current working directory (for example with `--override-ini` ).

              Added in version 7.0:  The `paths` variable type.

              Added in version 8.1:  Use the current working directory to resolve `paths` and `pathlist` in the absence of a config-file.

              Defaults to `string` if `None` or not passed.
            * **default** (  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")  ) – Default value if no config-file option exists but is queried.
            * **aliases** (  [*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) –

              Additional names by which this option can be referenced. Aliases resolve to the canonical name.

              Added in version 9.0:  The `aliases` parameter.

        The value of configuration keys can be retrieved via a call to  [`config.getini(name)`](#pytest.Config.getini "pytest.Config.getini")  .

### OptionGroup

class OptionGroup [[source]](../_modules/_pytest/config/argparsing.html#OptionGroup)
:   A group of options shown in its own section.

    addoption ( *\* opts* , *\*\* attrs* ) [[source]](../_modules/_pytest/config/argparsing.html#OptionGroup.addoption)
    :   Add an option to this group.

        If a shortened version of a long option is specified, it will be suppressed in the help. `addoption('--twowords', '--two-words')` results in help showing `--two-words` only, but `--twowords` gets accepted **and** the automatic destination is in `args.twowords` .

        Parameters :
        :   * **opts** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Option names, can be short or long options. Note that lower-case short options (e.g. `-x` ) are reserved.
            * **attrs** (  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")  ) – Same attributes as the argparse library’s  [`add_argument()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument "(in Python v3.14)")  function accepts.

### PytestPluginManager

final class PytestPluginManager [[source]](../_modules/_pytest/config.html#PytestPluginManager)
:   Bases:  [`PluginManager`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluginManager "(in pluggy v0.1)")

    A  [`pluggy.PluginManager`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluginManager "(in pluggy v0.1)")  with additional pytest-specific functionality:

    * Loading plugins from the command line, `PYTEST_PLUGINS` env variable and `pytest_plugins` global variables found in plugins being loaded.
    * `conftest.py` loading during start-up.

    skipped\_plugins : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] ]

    rewrite\_hook : RewriteHook

    register ( *plugin* , *name = None* ) [[source]](../_modules/_pytest/config.html#PytestPluginManager.register)
    :   Register a plugin and return its name.

        Parameters :
        :   **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – The name under which to register the plugin. If not specified, a name is generated using  [`get_canonical_name()`](#pytest.PytestPluginManager.get_canonical_name "pytest.PytestPluginManager.get_canonical_name")  .

        Returns :
        :   The plugin name. If the name is blocked from registering, returns `None` .

        Return type :
        :   [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | None

        If the plugin is already registered, raises a  [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)")  .

    getplugin ( *name* ) [[source]](../_modules/_pytest/config.html#PytestPluginManager.getplugin)

    hasplugin ( *name* ) [[source]](../_modules/_pytest/config.html#PytestPluginManager.hasplugin)
    :   Return whether a plugin with the given name is registered.

    import\_plugin ( *modname* , *consider\_entry\_points = False* ) [[source]](../_modules/_pytest/config.html#PytestPluginManager.import_plugin)
    :   Import a plugin with `modname` .

        If `consider_entry_points` is True, entry point names are also considered to find a plugin.

    add\_hookcall\_monitoring ( *before* , *after* )
    :   Add before/after tracing functions for all hooks.

        Returns an undo function which, when called, removes the added tracers.

        `before(hook_name, hook_impls, kwargs)` will be called ahead of all hook calls and receive a hookcaller instance, a list of HookImpl instances and the keyword arguments for the hook call.

        `after(outcome, hook_name, hook_impls, kwargs)` receives the same arguments as `before` but also a  [`Result`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.Result "(in pluggy v0.1)")  object which represents the result of the overall hook call.

    add\_hookspecs ( *module\_or\_class* )
    :   Add new hook specifications defined in the given `module_or_class` .

        Functions are recognized as hook specifications if they have been decorated with a matching `HookspecMarker` .

    check\_pending ( )
    :   Verify that all hooks which have not been verified against a hook specification are optional, otherwise raise `PluginValidationError` .

    enable\_tracing ( )
    :   Enable tracing of hook calls.

        Returns an undo function which, when called, removes the added tracing.

    get\_canonical\_name ( *plugin* )
    :   Return a canonical name for a plugin object.

        Note that a plugin may be registered under a different name specified by the caller of  [`register(plugin, name)`](#pytest.PytestPluginManager.register "pytest.PytestPluginManager.register")  . To obtain the name of a registered plugin use  [`get_name(plugin)`](#pytest.PytestPluginManager.get_name "pytest.PytestPluginManager.get_name")  instead.

    get\_hookcallers ( *plugin* )
    :   Get all hook callers for the specified plugin.

        Returns :
        :   The hook callers, or `None` if `plugin` is not registered in this plugin manager.

        Return type :
        :   [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [  [*HookCaller*](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.HookCaller "(in pluggy v0.1)")  ] | None

    get\_name ( *plugin* )
    :   Return the name the plugin is registered under, or `None` if is isn’t.

    get\_plugin ( *name* )
    :   Return the plugin registered under the given name, if any.

    get\_plugins ( )
    :   Return a set of all registered plugin objects.

    has\_plugin ( *name* )
    :   Return whether a plugin with the given name is registered.

    is\_blocked ( *name* )
    :   Return whether the given plugin name is blocked.

    is\_registered ( *plugin* )
    :   Return whether the plugin is already registered.

    list\_name\_plugin ( )
    :   Return a list of (name, plugin) pairs for all registered plugins.

    list\_plugin\_distinfo ( )
    :   Return a list of (plugin, distinfo) pairs for all setuptools-registered plugins.

    load\_setuptools\_entrypoints ( *group* , *name = None* )
    :   Load modules from querying the specified setuptools `group` .

        Parameters :
        :   * **group** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Entry point group to load plugins.
            * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *None* ) – If given, loads only plugins with the given `name` .

        Returns :
        :   The number of plugins loaded by this call.

        Return type :
        :   [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")

    set\_blocked ( *name* )
    :   Block registrations of the given name, unregister if already registered.

    subset\_hook\_caller ( *name* , *remove\_plugins* )
    :   Return a proxy  [`HookCaller`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.HookCaller "(in pluggy v0.1)")  instance for the named method which manages calls to all registered plugins except the ones from remove\_plugins.

    unblock ( *name* )
    :   Unblocks a name.

        Returns whether the name was actually blocked.

    unregister ( *plugin = None* , *name = None* )
    :   Unregister a plugin and all of its hook implementations.

        The plugin can be specified either by the plugin object or the plugin name. If both are specified, they must agree.

        Returns the unregistered plugin, or `None` if not found.

    project\_name
    :   The project name.

    hook
    :   The “hook relay”, used to call a hook on all registered plugins. See  [Calling hooks](https://pluggy.readthedocs.io/en/stable/index.html#calling "(in pluggy v0.1)")  .

    trace
    :   The tracing entry point. See  [Built-in tracing](https://pluggy.readthedocs.io/en/stable/index.html#tracing "(in pluggy v0.1)")  .

### RaisesExc

final class RaisesExc [[source]](../_modules/_pytest/raises.html#RaisesExc)
:   Added in version 8.4.

    This is the class constructed when calling  [`pytest.raises()`](#pytest.raises "pytest.raises")  , but may be used directly as a helper class with  [`RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")  when you want to specify requirements on sub-exceptions.

    You don’t need this if you only want to specify the type, since  [`RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")  accepts `type[BaseException]` .

    Parameters :
    :   * **expected\_exception** (  [*type*](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]*  *|*   [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")  *[*  [*type*](#pytest.ExceptionInfo.type "pytest.ExceptionInfo.type")  *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *]*  *|*  *None* ) –

          The expected type, or one of several possible types. May be `None` in order to only make use of `match` and/or `check`

          The type is checked with  [`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance "(in Python v3.14)")  , and does not need to be an exact match. If that is wanted you can use the `check` parameter.
        * **match** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*  *Pattern* *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]* ) – A regex to match.
        * **check** ( *Callable* *[* *[*  [*BaseException*](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)")  *]* *,*   [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  *]* ) – If specified, a callable that will be called with the exception as a parameter after checking the type and the match regex if specified. If it returns `True` it will be considered a match, if not it will be considered a failed match.

    [`RaisesExc.matches()`](#pytest.RaisesExc.matches "pytest.RaisesExc.matches")  can also be used standalone to check individual exceptions.

    Examples:

    ```
    with RaisesGroup(RaisesExc(ValueError, match="string"))
        ...with RaisesGroup(RaisesExc(check=lambda x: x.args == (3, "hello"))):
        ...with RaisesGroup(RaisesExc(check=lambda x: type(x) is ValueError)):
        ...
    ```

    fail\_reason
    :   Set after a call to  [`matches()`](#pytest.RaisesExc.matches "pytest.RaisesExc.matches")  to give a human-readable reason for why the match failed. When used as a context manager the string will be printed as the reason for the test failing.

    matches ( *exception* ) [[source]](../_modules/_pytest/raises.html#RaisesExc.matches)
    :   Check if an exception matches the requirements of this  [`RaisesExc`](#pytest.RaisesExc "pytest.RaisesExc")  . If it fails,  [`RaisesExc.fail_reason`](#pytest.RaisesExc.fail_reason "pytest.RaisesExc.fail_reason")  will be set.

        Examples:

        ```
        assert RaisesExc(ValueError).matches(my_exception):# is equivalent toassert isinstance(my_exception, ValueError)

        # this can be useful when checking e.g. the ``__cause__`` of an exception.with pytest.raises(ValueError) as excinfo:
            ...assert RaisesExc(SyntaxError, match="foo").matches(excinfo.value.__cause__)# above line is equivalent toassert isinstance(excinfo.value.__cause__, SyntaxError)assert re.search("foo", str(excinfo.value.__cause__)
        ```

### RaisesGroup

**Tutorial** :  [Assertions about expected exception groups](../how-to/assert.html#assert-matching-exception-groups)

final class RaisesGroup [[source]](../_modules/_pytest/raises.html#RaisesGroup)
:   Added in version 8.4.

    Contextmanager for checking for an expected  [`ExceptionGroup`](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)")  . This works similar to  [`pytest.raises()`](#pytest.raises "pytest.raises")  , but allows for specifying the structure of an  [`ExceptionGroup`](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)")  .  [`ExceptionInfo.group_contains()`](#pytest.ExceptionInfo.group_contains "pytest.ExceptionInfo.group_contains")  also tries to handle exception groups, but it is very bad at checking that you *didn’t* get unexpected exceptions.

    The catching behaviour differs from  [except\*](https://docs.python.org/3/reference/compound_stmts.html#except-star "(in Python v3.14)")  , being much stricter about the structure by default. By using `allow_unwrapped=True` and `flatten_subgroups=True` you can match  [except\*](https://docs.python.org/3/reference/compound_stmts.html#except-star "(in Python v3.14)")  fully when expecting a single exception.

    Parameters :
    :   * **args** –

          Any number of exception types,  [`RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")  or  [`RaisesExc`](#pytest.RaisesExc "pytest.RaisesExc")  to specify the exceptions contained in this exception. All specified exceptions must be present in the raised group, *and no others* .

          If you expect a variable number of exceptions you need to use  [`pytest.raises(ExceptionGroup)`](#pytest.raises "pytest.raises")  and manually check the contained exceptions. Consider making use of  [`RaisesExc.matches()`](#pytest.RaisesExc.matches "pytest.RaisesExc.matches")  .

          It does not care about the order of the exceptions, so `RaisesGroup(ValueError, TypeError)` is equivalent to `RaisesGroup(TypeError, ValueError)` .
        * **match** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *|*   [*re.Pattern*](https://docs.python.org/3/library/re.html#re.Pattern "(in Python v3.14)")  *[*  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  *]*  *|*  *None* ) –

          If specified, a string containing a regular expression, or a regular expression object, that is tested against the string representation of the exception group and its   [**PEP 678**](https://peps.python.org/pep-0678/)  `__notes__` using  [`re.search()`](https://docs.python.org/3/library/re.html#re.search "(in Python v3.14)")  .

          To match a literal string that may contain  [special characters](https://docs.python.org/3/library/re.html#re-syntax "(in Python v3.14)")  , the pattern can first be escaped with  [`re.escape()`](https://docs.python.org/3/library/re.html#re.escape "(in Python v3.14)")  .

          Note that “ (5 subgroups)” will be stripped from the `repr` before matching.
        * **check** ( *Callable* *[* *[* *E* *]* *,*   [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  *]* ) – If specified, a callable that will be called with the group as a parameter after successfully matching the expected exceptions. If it returns `True` it will be considered a match, if not it will be considered a failed match.
        * **allow\_unwrapped** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) –

          If expecting a single exception or  [`RaisesExc`](#pytest.RaisesExc "pytest.RaisesExc")  it will match even if the exception is not inside an exceptiongroup.

          Using this together with `match` , `check` or expecting multiple exceptions will raise an error.
        * **flatten\_subgroups** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – “flatten” any groups inside the raised exception group, extracting all exceptions inside any nested groups, before matching. Without this it expects you to fully specify the nesting structure by passing  [`RaisesGroup`](#pytest.RaisesGroup "pytest.RaisesGroup")  as expected parameter.

    Examples:

    ```
    with RaisesGroup(ValueError):
        raise ExceptionGroup("", (ValueError(),))# matchwith RaisesGroup(
        ValueError,
        ValueError,
        RaisesExc(TypeError, match="^expected int$"),
        match="^my group$",):
        raise ExceptionGroup(
            "my group",
            [
                ValueError(),
                TypeError("expected int"),
                ValueError(),
            ],
        )# checkwith RaisesGroup(
        KeyboardInterrupt,
        match="^hello$",
        check=lambda x: isinstance(x.__cause__, ValueError),):
        raise BaseExceptionGroup("hello", [KeyboardInterrupt()]) from ValueError# nested groupswith RaisesGroup(RaisesGroup(ValueError)):
        raise ExceptionGroup("", (ExceptionGroup("", (ValueError(),)),))

    # flatten_subgroupswith RaisesGroup(ValueError, flatten_subgroups=True):
        raise ExceptionGroup("", (ExceptionGroup("", (ValueError(),)),))

    # allow_unwrappedwith RaisesGroup(ValueError, allow_unwrapped=True):
        raise ValueError
    ```

    [`RaisesGroup.matches()`](#pytest.RaisesGroup.matches "pytest.RaisesGroup.matches")  can also be used directly to check a standalone exception group.

    The matching algorithm is greedy, which means cases such as this may fail:

    ```
    with RaisesGroup(ValueError, RaisesExc(ValueError, match="hello")):
        raise ExceptionGroup("", (ValueError("hello"), ValueError("goodbye")))
    ```

    even though it generally does not care about the order of the exceptions in the group. To avoid the above you should specify the first  [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)")  with a  [`RaisesExc`](#pytest.RaisesExc "pytest.RaisesExc")  as well.

    Note

    When raised exceptions don’t match the expected ones, you’ll get a detailed error message explaining why. This includes `repr(check)` if set, which in Python can be overly verbose, showing memory locations etc etc.

    If installed and imported (in e.g. `conftest.py` ), the `hypothesis` library will monkeypatch this output to provide shorter & more readable repr’s.

    fail\_reason
    :   Set after a call to  [`matches()`](#pytest.RaisesGroup.matches "pytest.RaisesGroup.matches")  to give a human-readable reason for why the match failed. When used as a context manager the string will be printed as the reason for the test failing.

    matches ( *exception : [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")* ) → TypeGuard [ [ExceptionGroup](https://docs.python.org/3/library/exceptions.html#ExceptionGroup "(in Python v3.14)") [ ExcT\_1 ] ] [[source]](../_modules/_pytest/raises.html#RaisesGroup.matches)

    matches ( *exception : [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")* ) → TypeGuard [ [BaseExceptionGroup](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup "(in Python v3.14)") [ BaseExcT\_1 ] ]
    :   Check if an exception matches the requirements of this RaisesGroup. If it fails, `RaisesGroup.fail_reason` will be set.

        Example:

        ```
        with pytest.raises(TypeError) as excinfo:
            ...assert RaisesGroup(ValueError).matches(excinfo.value.__cause__)# the above line is equivalent tomyexc = excinfo.value.__causeassert isinstance(myexc, BaseExceptionGroup)assert len(myexc.exceptions) == 1assert isinstance(myexc.exceptions[0], ValueError)
        ```

### TerminalReporter

final class TerminalReporter ( *config* , *file = None* ) [[source]](../_modules/_pytest/terminal.html#TerminalReporter)
:   wrap\_write ( *content* , *\** , *flush = False* , *margin = 8* , *line\_sep = '\n'* , *\*\* markup* ) [[source]](../_modules/_pytest/terminal.html#TerminalReporter.wrap_write)
    :   Wrap message with margin for progress info.

    rewrite ( *line* , *\*\* markup* ) [[source]](../_modules/_pytest/terminal.html#TerminalReporter.rewrite)
    :   Rewinds the terminal cursor to the beginning and writes the given line.

        Parameters :
        :   **erase** – If True, will also add spaces until the full terminal width to ensure previous lines are properly erased.

        The rest of the keyword arguments are markup instructions.

    build\_summary\_stats\_line ( ) [[source]](../_modules/_pytest/terminal.html#TerminalReporter.build_summary_stats_line)
    :   Build the parts used in the last summary stats line.

        The summary stats line is the line shown at the end, “=== 12 passed, 2 errors in Xs===”.

        This function builds a list of the “parts” that make up for the text in that line, in the example above it would be:

        ```
        [
            ("12 passed", {"green": True}),
            ("2 errors", {"red": True}]
        ```

        That last dict for each line is a “markup dictionary”, used by TerminalWriter to color output.

        The final color of the line is also determined by this function, and is the second element of the returned tuple.

### TestReport

class TestReport [[source]](../_modules/_pytest/reports.html#TestReport)
:   Bases: `BaseReport`

    Basic test report object (also used for setup and teardown calls if they fail).

    Reports can contain arbitrary extra attributes.

    nodeid : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Normalized collection nodeid.

    location : [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ]
    :   A (filesystempath, lineno, domaininfo) tuple indicating the actual location of a test item - it might be different from the collected one e.g. if a method is inherited from a different module. The filesystempath may be relative to `config.rootdir` . The line number is 0-based.

    keywords : [Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") ]
    :   A name -> value dictionary containing all keywords and markers associated with a test invocation.

    outcome : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'passed' , 'failed' , 'skipped' ]
    :   Test outcome, always one of “passed”, “failed”, “skipped”.

    longrepr : [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [ExceptionInfo](#pytest.ExceptionInfo "_pytest._code.code.ExceptionInfo") [ [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException "(in Python v3.14)") ] | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | TerminalRepr
    :   None or a failure representation.

    when : [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "(in Python v3.14)") [ 'setup' , 'call' , 'teardown' ]
    :   One of ‘setup’, ‘call’, ‘teardown’ to indicate runtest phase.

    user\_properties
    :   User properties is a list of tuples (name, value) that holds user defined properties of the test.

    sections : [list](#pytest.WarningsRecorder.list "pytest.WarningsRecorder.list") [ [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") ] ]
    :   Tuples of str `(heading, content)` with extra information for the test report. Used by pytest to add text captured from `stdout` , `stderr` , and intercepted logging events. May be used by other plugins to add arbitrary information to reports.

    duration : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   Time it took to run just the test.

    start : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   The system time when the call started, in seconds since the epoch.

    stop : [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")
    :   The system time when the call ended, in seconds since the epoch.

    classmethod from\_item\_and\_call ( *item* , *call* ) [[source]](../_modules/_pytest/reports.html#TestReport.from_item_and_call)
    :   Create and fill a TestReport with standard item and call info.

        Parameters :
        :   * **item** (  [*Item*](#pytest.Item "pytest.Item")  ) – The item.
            * **call** (  [*CallInfo*](#pytest.CallInfo "pytest.CallInfo")  *[* *None* *]* ) – The call info.

    property caplog : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured log lines, if log capturing is enabled.

        Added in version 3.5.

    property capstderr : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured text from stderr, if capturing is enabled.

        Added in version 3.0.

    property capstdout : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Return captured text from stdout, if capturing is enabled.

        Added in version 3.0.

    property count\_towards\_summary : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   **Experimental** Whether this report should be counted towards the totals shown at the end of the test session: “1 passed, 1 failure, etc”.

        Note

        This function is considered **experimental** , so beware that it is subject to changes even in patch releases.

    property failed : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is failed.

    property fspath : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   The path portion of the reported node, as a string.

    property head\_line : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
    :   **Experimental** The head line shown with longrepr output for this report, more commonly during traceback representation during failures:

        ```
        ________ Test.foo ________
        ```

        In the example above, the head\_line is “Test.foo”.

        Note

        This function is considered **experimental** , so beware that it is subject to changes even in patch releases.

    property longreprtext : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Read-only property that returns the full string representation of `longrepr` .

        Added in version 3.0.

    property passed : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is passed.

    property skipped : [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    :   Whether the outcome is skipped.

### TestShortLogReport

class TestShortLogReport [[source]](../_modules/_pytest/terminal.html#TestShortLogReport)
:   Used to store the test status result category, shortletter and verbose word. For example `"rerun", "R", ("RERUN", {"yellow": True})` .

    Variables :
    :   * **category** – The class of result, for example `“passed”` , `“skipped”` , `“error”` , or the empty string.
        * **letter** – The short letter shown as testing progresses, for example `"."` , `"s"` , `"E"` , or the empty string.
        * **word** – Verbose word is shown as testing progresses in verbose mode, for example `"PASSED"` , `"SKIPPED"` , `"ERROR"` , or the empty string.

    category : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Alias for field number 0

    letter : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
    :   Alias for field number 1

    word : [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") [ [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") , [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") ] ]
    :   Alias for field number 2

### Result

Result object used within  [hook wrappers](../how-to/writing_hook_functions.html#hookwrapper)  , see  [`Result in the pluggy documentation`](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.Result "(in pluggy v0.1)")  for more information.

### Stash

class Stash [[source]](../_modules/_pytest/stash.html#Stash)
:   `Stash` is a type-safe heterogeneous mutable mapping that allows keys and value types to be defined separately from where it (the `Stash` ) is created.

    Usually you will be given an object which has a `Stash` , for example  [`Config`](#pytest.Config "pytest.Config")  or a  [`Node`](#pytest.nodes.Node "_pytest.nodes.Node")  :

    ```
    stash: Stash = some_object.stash
    ```

    If a module or plugin wants to store data in this `Stash` , it creates  [`StashKey`](#pytest.StashKey "pytest.StashKey")  s for its keys (at the module level):

    ```
    # At the top-level of the modulesome_str_key = StashKey[str]()some_bool_key = StashKey[bool]()
    ```

    To store information:

    ```
    # Value type must match the key.stash[some_str_key] = "value"stash[some_bool_key] = True
    ```

    To retrieve the information:

    ```
    # The static type of some_str is str.some_str = stash[some_str_key]# The static type of some_bool is bool.some_bool = stash[some_bool_key]
    ```

    Added in version 7.0.

    \_\_setitem\_\_ ( *key* , *value* ) [[source]](../_modules/_pytest/stash.html#Stash.__setitem__)
    :   Set a value for key.

    \_\_getitem\_\_ ( *key* ) [[source]](../_modules/_pytest/stash.html#Stash.__getitem__)
    :   Get the value for key.

        Raises `KeyError` if the key wasn’t set before.

    get ( *key* , *default* ) [[source]](../_modules/_pytest/stash.html#Stash.get)
    :   Get the value for key, or return default if the key wasn’t set before.

    setdefault ( *key* , *default* ) [[source]](../_modules/_pytest/stash.html#Stash.setdefault)
    :   Return the value of key if already set, otherwise set the value of key to default and return default.

    \_\_delitem\_\_ ( *key* ) [[source]](../_modules/_pytest/stash.html#Stash.__delitem__)
    :   Delete the value for key.

        Raises `KeyError` if the key wasn’t set before.

    \_\_contains\_\_ ( *key* ) [[source]](../_modules/_pytest/stash.html#Stash.__contains__)
    :   Return whether key was set.

    \_\_len\_\_ ( ) [[source]](../_modules/_pytest/stash.html#Stash.__len__)
    :   Return how many items exist in the stash.

class StashKey [[source]](../_modules/_pytest/stash.html#StashKey)
:   Bases:  [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic "(in Python v3.14)")  [ `T` ]

    `StashKey` is an object used as a key to a  [`Stash`](#pytest.Stash "pytest.Stash")  .

    A `StashKey` is associated with the type `T` of the value of the key.

    A `StashKey` is unique and cannot conflict with another key.

    Added in version 7.0.

## Global Variables

pytest treats some global variables in a special manner when defined in a test module or `conftest.py` files.

collect\_ignore

**Tutorial** :  [Customizing test collection](../example/pythoncollection.html#customizing-test-collection)

Can be declared in *conftest.py files* to exclude test directories or modules. Needs to be a list of paths ( `str` ,  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  or any  [`os.PathLike`](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")  ).

```
collect_ignore = ["setup.py"]
```

collect\_ignore\_glob

**Tutorial** :  [Customizing test collection](../example/pythoncollection.html#customizing-test-collection)

Can be declared in *conftest.py files* to exclude test directories or modules with Unix shell-style wildcards. Needs to be `list[str]` where `str` can contain glob patterns.

```
collect_ignore_glob = ["*_ignore.py"]
```

pytest\_plugins

**Tutorial** :  [Requiring/Loading plugins in a test module or conftest file](../how-to/plugins.html#available-installable-plugins)

Can be declared at the **global** level in *test modules* and *conftest.py files* to register additional plugins. Can be either a `str` or `Sequence[str]` .

```
pytest_plugins = "myapp.testsupport.myplugin"
```

```
pytest_plugins = ("myapp.testsupport.tools", "myapp.testsupport.regression")
```

pytestmark

**Tutorial** :  [Marking whole classes or modules](../example/markers.html#scoped-marking)

Can be declared at the **global** level in *test modules* to apply one or more  [marks](#marks-ref)  to all test functions and methods. Can be either a single mark or a list of marks (applied in left-to-right order).

```
import pytest

pytestmark = pytest.mark.webtest
```

```
import pytest

pytestmark = [pytest.mark.integration, pytest.mark.slow]
```

## Environment Variables

Environment variables that can be used to change pytest’s behavior.

CI
:   When set to a non-empty value, pytest acknowledges that it is running in a CI process. See also  [CI Pipelines](../explanation/ci.html#ci-pipelines)  .

BUILD\_NUMBER
:   When set to a non-empty value, pytest acknowledges that it is running in a CI process. Alternative to   [`CI`](#envvar-CI)  . See also  [CI Pipelines](../explanation/ci.html#ci-pipelines)  .

PYTEST\_ADDOPTS
:   This contains a command-line (parsed by the py:mod: `shlex` module) that will be **prepended** to the command line given by the user, see  [Builtin configuration file options](customize.html#adding-default-options)  for more information.

PYTEST\_VERSION
:   This environment variable is defined at the start of the pytest session and is undefined afterwards. It contains the value of `pytest.__version__` , and among other things can be used to easily check if a code is running from within a pytest run.

PYTEST\_CURRENT\_TEST
:   This is not meant to be set by users, but is set by pytest internally with the name of the current test so other processes can inspect it, see  [PYTEST\_CURRENT\_TEST environment variable](../example/simple.html#pytest-current-test-env)  for more information.

PYTEST\_DEBUG
:   When set, pytest will print tracing and debug information.

PYTEST\_DEBUG\_TEMPROOT
:   Root for temporary directories produced by fixtures like  [`tmp_path`](#std-fixture-tmp_path)  as discussed in  [Temporary directory location and retention](../how-to/tmp_path.html#temporary-directory-location-and-retention)  .

PYTEST\_DISABLE\_PLUGIN\_AUTOLOAD
:   When set, disables plugin auto-loading through  [entry point packaging metadata](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/ "(in Python Packaging User Guide)")  . Only plugins explicitly specified in   [`PYTEST_PLUGINS`](#envvar-PYTEST_PLUGINS)  or with  [`-p`](#cmdoption-p)  will be loaded. See also  [–disable-plugin-autoload](../how-to/plugins.html#disable-plugin-autoload)  .

PYTEST\_PLUGINS
:   Contains comma-separated list of modules that should be loaded as plugins:

    ```
    export PYTEST_PLUGINS=mymodule.plugin,xdist
    ```

    See also  [`-p`](#cmdoption-p)  .

PYTEST\_THEME
:   Sets a [pygment style](https://pygments.org/docs/styles/) to use for the code output.

PYTEST\_THEME\_MODE
:   Sets the   [`PYTEST_THEME`](#envvar-PYTEST_THEME)  to be either *dark* or *light* .

PY\_COLORS
:   When set to `1` , pytest will use color in terminal output. When set to `0` , pytest will not use color. `PY_COLORS` takes precedence over `NO_COLOR` and `FORCE_COLOR` .

NO\_COLOR
:   When set to a non-empty string (regardless of value), pytest will not use color in terminal output. `PY_COLORS` takes precedence over `NO_COLOR` , which takes precedence over `FORCE_COLOR` . See [no-color.org](https://no-color.org/) for other libraries supporting this community standard.

FORCE\_COLOR
:   When set to a non-empty string (regardless of value), pytest will use color in terminal output. `PY_COLORS` and `NO_COLOR` take precedence over `FORCE_COLOR` .

## Exceptions

exception UsageError
:   Bases:  [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")

    Error in pytest usage or invocation.

final exception FixtureLookupError [[source]](../_modules/_pytest/fixtures.html#FixtureLookupError)
:   Bases:  [`LookupError`](https://docs.python.org/3/library/exceptions.html#LookupError "(in Python v3.14)")

    Could not return a requested fixture (missing or invalid).

## Warnings

Custom warnings generated in some situations such as improper usage or deprecated features.

class PytestWarning
:   Bases:  [`UserWarning`](https://docs.python.org/3/library/exceptions.html#UserWarning "(in Python v3.14)")

    Base class for all warnings emitted by pytest.

class PytestAssertRewriteWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted by the pytest assert rewrite module.

class PytestCacheWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted by the cache plugin in various situations.

class PytestCollectionWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted when pytest is not able to collect a file or symbol in a module.

class PytestConfigWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted for configuration issues.

class PytestDeprecationWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")  ,  [`DeprecationWarning`](https://docs.python.org/3/library/exceptions.html#DeprecationWarning "(in Python v3.14)")

    Warning class for features that will be removed in a future version.

class PytestExperimentalApiWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")  ,  [`FutureWarning`](https://docs.python.org/3/library/exceptions.html#FutureWarning "(in Python v3.14)")

    Warning category used to denote experiments in pytest.

    Use sparingly as the API might change or even be removed completely in a future version.

class PytestReturnNotNoneWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted when a test function returns a value other than `None` .

    See  [Returning non-None value in test functions](../how-to/assert.html#return-not-none)  for details.

class PytestRemovedIn10Warning
:   Bases:  [`PytestDeprecationWarning`](#pytest.PytestDeprecationWarning "pytest.PytestDeprecationWarning")

    Warning class for features that will be removed in pytest 10.

class PytestUnknownMarkWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    Warning emitted on use of unknown markers.

    See  [How to mark test functions with attributes](../how-to/mark.html#mark)  for details.

class PytestUnraisableExceptionWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    An unraisable exception was reported.

    Unraisable exceptions are exceptions raised in  [`__del__`](https://docs.python.org/3/reference/datamodel.html#object.__del__ "(in Python v3.14)")  implementations and similar situations when the exception cannot be raised as normal.

class PytestUnhandledThreadExceptionWarning
:   Bases:  [`PytestWarning`](#pytest.PytestWarning "pytest.PytestWarning")

    An unhandled exception occurred in a  [`Thread`](https://docs.python.org/3/library/threading.html#threading.Thread "(in Python v3.14)")  .

    Such exceptions don’t propagate normally.

Consult the  [Internal pytest warnings](../how-to/capture-warnings.html#internal-warnings)  section in the documentation for more information.

## Configuration Options

Here is a list of builtin configuration options that may be written in a `pytest.ini` (or `.pytest.ini` ), `pyproject.toml` , `tox.ini` , or `setup.cfg` file, usually located at the root of your repository.

To see each file format in detail, see  [Configuration file formats](customize.html#config-file-formats)  .

Warning

Usage of `setup.cfg` is not recommended except for very simple use cases. `.cfg` files use a different parser than `pytest.ini` and `tox.ini` which might cause hard to track down problems. When possible, it is recommended to use the latter files, or `pytest.toml` or `pyproject.toml` , to hold your pytest configuration.

Configuration options may be overwritten in the command-line by using `-o/--override-ini` , which can also be passed multiple times. The expected format is `name=value` . For example:

```
pytest -o console_output_style=classic -o cache_dir=/tmp/mycache
```

addopts
:   Type :
    :   `list[str]`

    Add the specified `OPTS` to the set of command line arguments as if they had been specified by the user. Example: if you have this configuration file content:

    ```
    # content of pytest.toml[pytest]addopts = ["--maxfail=2", "-rf"]  # exit after 2 failures, report fail info
    ```

    issuing `pytest test_hello.py` actually means:

    ```
    pytest --maxfail=2 -rf test_hello.py
    ```

cache\_dir
:   Type :
    :   `str`

    Default :
    :   `".pytest_cache"`

    Sets the directory where the cache plugin’s content is stored. Directory may be relative or absolute path. If setting relative path, then directory is created relative to  [rootdir](customize.html#rootdir)  . Additionally, a path may contain environment variables, that will be expanded. For more information about cache plugin please refer to  [How to re-run failed tests and maintain state between test runs](../how-to/cache.html#cache-provider)  .

collect\_imported\_tests
:   Type :
    :   `bool`

    Default :
    :   `true`

    Added in version 8.4.

    Setting this to `false` will make pytest collect classes/functions from test files **only** if they are defined in that file (as opposed to imported there).

    toml

    ```
    [pytest]collect_imported_tests = false
    ```

     ini

    ```
    [pytest]collect_imported_tests = false
    ```

    pytest traditionally collects classes/functions in the test module namespace even if they are imported from another file.

    For example:

    ```
    # contents of src/domain.pyclass Testament: ...

    # contents of tests/test_testament.pyfrom domain import Testament

    def test_testament(): ...
    ```

    In this scenario, with the default options, pytest will collect the class `Testament` from `tests/test_testament.py` because it starts with `Test` , even though in this case it is a production class being imported in the test module namespace.

    Set `collected_imported_tests` to `false` in the configuration file prevents that.

consider\_namespace\_packages
:   Type :
    :   `bool`

    Default :
    :   `false`

    Controls if pytest should attempt to identify [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages) when collecting Python modules.

    Set to `True` if the package you are testing is part of a namespace package. Namespace packages are also supported as  [`--pyargs`](#cmdoption-pyargs)  target.

    Only [native namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#native-namespace-packages) are supported, with no plans to support [legacy namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#legacy-namespace-packages) .

    For best results when using `consider_namespace_packages` , pytest needs to be able to import your namespace packages. This is best achieved by installing the packages in your environment, most commonly in [“editable” mode](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode) . If you can’t install the packages, consider adding the namespace root paths to  [`pythonpath`](#confval-pythonpath)  .

    Added in version 8.1.

console\_output\_style
:   Type :
    :   `str`

    Default :
    :   `"progress"`

    Sets the console output style while running tests:

    * `classic` : classic pytest output.
    * `progress` : like classic pytest output, but with a progress indicator.
    * `progress-even-when-capture-no` : allows the use of the progress indicator even when `capture=no` .
    * `count` : like progress, but shows progress as the number of tests completed instead of a percent.
    * `times` : show tests duration.

    You can fallback to `classic` if you prefer or the new mode is causing unexpected problems:

    toml

    ```
    [pytest]console_output_style = "classic"
    ```

     ini

    ```
    [pytest]console_output_style = classic
    ```

disable\_test\_id\_escaping\_and\_forfeit\_all\_rights\_to\_community\_support
:   Type :
    :   `bool`

    Default :
    :   `false`

    Added in version 4.4.

    pytest by default escapes any non-ascii characters used in unicode strings for the parametrization because it has several downsides. If however you would like to use unicode strings in parametrization and see them in the terminal as is (non-escaped), use this option in your configuration file:

    toml

    ```
    [pytest]disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true
    ```

     ini

    ```
    [pytest]disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true
    ```

    Keep in mind however that this might cause unwanted side effects and even bugs depending on the OS used and plugins currently installed, so use it at your own risk.

    See  [@pytest.mark.parametrize: parametrizing test functions](../how-to/parametrize.html#parametrizemark)  .

doctest\_encoding
:   Type :
    :   `str`

    Default :
    :   `"utf-8"`

    Default encoding to use to decode text files with docstrings.  [See how pytest handles doctests](../how-to/doctest.html#doctest)  .

doctest\_optionflags
:   Type :
    :   `list[str]`

    One or more doctest flag names from the standard `doctest` module.  [See how pytest handles doctests](../how-to/doctest.html#doctest)  .

empty\_parameter\_set\_mark
:   Type :
    :   `str`

    Default :
    :   `"skip"`

    Allows to pick the action for empty parametersets in parameterization

    * `skip` skips tests with an empty parameterset
    * `xfail` marks tests with an empty parameterset as xfail(run=False)
    * `fail_at_collect` raises an exception if parametrize collects an empty parameter set

    toml

    ```
    [pytest]empty_parameter_set_mark = "xfail"
    ```

     ini

    ```
    [pytest]empty_parameter_set_mark = xfail
    ```

    Note

    The default value of this option is planned to change to `xfail` in future releases as this is considered less error prone, see [#3155](https://github.com/pytest-dev/pytest/issues/3155) for more details.

enable\_assertion\_pass\_hook
:   Type :
    :   `bool`

    Default :
    :   `false`

    Enables the  [`pytest_assertion_pass`](#std-hook-pytest_assertion_pass)  hook. Make sure to delete any previously generated `.pyc` cache files.

    toml

    ```
    [pytest]enable_assertion_pass_hook = true
    ```

     ini

    ```
    [pytest]enable_assertion_pass_hook = true
    ```

faulthandler\_exit\_on\_timeout
:   Type :
    :   `bool`

    Default :
    :   `false`

    Exit the pytest process after the per-test timeout is reached by passing `exit=True` to the  [`faulthandler.dump_traceback_later()`](https://docs.python.org/3/library/faulthandler.html#faulthandler.dump_traceback_later "(in Python v3.14)")  function. This is particularly useful to avoid wasting CI resources for test suites that are prone to putting the main Python interpreter into a deadlock state.

    toml

    ```
    [pytest]faulthandler_timeout = 5faulthandler_exit_on_timeout = true
    ```

     ini

    ```
    [pytest]faulthandler_timeout = 5faulthandler_exit_on_timeout = true
    ```

faulthandler\_timeout
:   Type :
    :   `float`

    Default :
    :   `0` (disabled)

    Dumps the tracebacks of all threads if a test takes longer than `X` seconds to run (including fixture setup and teardown). Implemented using the  [`faulthandler.dump_traceback_later()`](https://docs.python.org/3/library/faulthandler.html#faulthandler.dump_traceback_later "(in Python v3.14)")  function, so all caveats there apply.

    toml

    ```
    [pytest]faulthandler_timeout = 5
    ```

     ini

    ```
    [pytest]faulthandler_timeout = 5
    ```

    For more information please refer to  [Fault Handler](../how-to/failures.html#faulthandler)  .

filterwarnings
:   Type :
    :   `list[str]`

    Sets a list of filters and actions that should be taken for matched warnings. By default all warnings emitted during the test session will be displayed in a summary at the end of the test session.

    toml

    ```
    [pytest]filterwarnings = [    'error',    'ignore::DeprecationWarning',    # Note the use of single quote below to denote "raw" strings in TOML.    'ignore:function ham\(\) should not be used:UserWarning',]
    ```

     ini

    ```
    [pytest]filterwarnings =    error    ignore::DeprecationWarning    ignore:function ham\(\) should not be used:UserWarning
    ```

    This tells pytest to ignore deprecation warnings and turn all other warnings into errors. For more information please refer to  [How to capture warnings](../how-to/capture-warnings.html#warnings)  .

max\_warnings
:   Type :
    :   `int`

    Added in version 9.1.

    Maximum number of warnings allowed before the test run is considered a failure. When all tests pass, but the total number of warnings exceeds this value, pytest exits with  [`pytest.ExitCode`](#pytest.ExitCode "pytest.ExitCode")  `MAX_WARNINGS_ERROR` (code `6` ).

    toml

    ```
    [pytest]max_warnings = 10
    ```

     ini

    ```
    [pytest]max_warnings = 10
    ```

    Note that  [`filtered warnings`](#confval-filterwarnings)  do not count toward this maximum total.

    Can also be set via the  [`--max-warnings`](#cmdoption-max-warnings)  command-line option.

junit\_duration\_report
:   Type :
    :   `str`

    Default :
    :   `"total"`

    Added in version 4.1.

    Configures how durations are recorded into the JUnit XML report:

    * `total` : duration times reported include setup, call, and teardown times.
    * `call` : duration times reported include only call times, excluding setup and teardown.

    toml

    ```
    [pytest]junit_duration_report = "call"
    ```

     ini

    ```
    [pytest]junit_duration_report = call
    ```

junit\_family
:   Type :
    :   `str`

    Default :
    :   `"xunit2"`

    Added in version 4.2.

    Changed in version 6.1:  Default changed to `xunit2` .

    Configures the format of the generated JUnit XML file. The possible options are:

    * `xunit1` (or `legacy` ): produces old style output, compatible with the xunit 1.0 format.
    * `xunit2` : produces [xunit 2.0 style output](https://github.com/jenkinsci/xunit-plugin/blob/xunit-2.3.2/src/main/resources/org/jenkinsci/plugins/xunit/types/model/xsd/junit-10.xsd) , which should be more compatible with latest Jenkins versions.

    toml

    ```
    [pytest]junit_family = "xunit2"
    ```

     ini

    ```
    [pytest]junit_family = xunit2
    ```

junit\_log\_passing\_tests
:   Type :
    :   `bool`

    Default :
    :   `true`

    Added in version 4.6.

    If `junit_logging != "no"` , configures if the captured output should be written to the JUnit XML file for **passing** tests.

    toml

    ```
    [pytest]junit_log_passing_tests = false
    ```

     ini

    ```
    [pytest]junit_log_passing_tests = False
    ```

junit\_logging
:   Type :
    :   `str`

    Default :
    :   `"no"`

    Added in version 3.5.

    Changed in version 5.4:  `log` , `all` , `out-err` options added.

    Configures if captured output should be written to the JUnit XML file. Valid values are:

    * `log` : write only `logging` captured output.
    * `system-out` : write captured `stdout` contents.
    * `system-err` : write captured `stderr` contents.
    * `out-err` : write both captured `stdout` and `stderr` contents.
    * `all` : write captured `logging` , `stdout` and `stderr` contents.
    * `no` : no captured output is written.

    toml

    ```
    [pytest]junit_logging = "system-out"
    ```

     ini

    ```
    [pytest]junit_logging = system-out
    ```

junit\_suite\_name
:   Type :
    :   `str`

    Default :
    :   `"pytest"`

    To set the name of the root test suite xml item, you can configure the `junit_suite_name` option in your config file:

    toml

    ```
    [pytest]junit_suite_name = "my_suite"
    ```

     ini

    ```
    [pytest]junit_suite_name = my_suite
    ```

log\_auto\_indent
:   Type :
    :   `str`

    Default :
    :   `"false"`

    Allow selective auto-indentation of multiline log messages.

    Supports command line option  [`--log-auto-indent=[value]`](#cmdoption-log-auto-indent)  and config option `log_auto_indent = [value]` to set the auto-indentation behavior for all logging.

    `[value]` can be:
    :   * “True” or “On” - Dynamically auto-indent multiline log messages
        * “False” or “Off” or “0” - Do not auto-indent multiline log messages
        * “[positive integer]” - auto-indent multiline log messages by [value] spaces

    toml

    ```
    [pytest]log_auto_indent = "false"
    ```

     ini

    ```
    [pytest]log_auto_indent = false
    ```

    Supports passing kwarg `extra={"auto_indent": [value]}` to calls to `logging.log()` to specify auto-indentation behavior for a specific entry in the log. `extra` kwarg overrides the value specified on the command line or in the config.

log\_cli
:   Type :
    :   `bool`

    Default :
    :   `false`

    Enable log display during test run (also known as  [“live logging”](../how-to/logging.html#live-logs)  ).

    toml

    ```
    [pytest]log_cli = true
    ```

     ini

    ```
    [pytest]log_cli = true
    ```

log\_cli\_date\_format
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_date_format`

    Sets a  [`time.strftime()`](https://docs.python.org/3/library/time.html#time.strftime "(in Python v3.14)")  -compatible string that will be used when formatting dates for live logging.

    toml

    ```
    [pytest]log_cli_date_format = "%Y-%m-%d %H:%M:%S"
    ```

     ini

    ```
    [pytest]log_cli_date_format = %Y-%m-%d %H:%M:%S
    ```

    For more information, see  [Live Logs](../how-to/logging.html#live-logs)  .

log\_cli\_format
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_format`

    Sets a  [`logging`](https://docs.python.org/3/library/logging.html#module-logging "(in Python v3.14)")  -compatible string used to format live logging messages.

    toml

    ```
    [pytest]log_cli_format = "%(asctime)s %(levelname)s %(message)s"
    ```

     ini

    ```
    [pytest]log_cli_format = %(asctime)s %(levelname)s %(message)s
    ```

    For more information, see  [Live Logs](../how-to/logging.html#live-logs)  .

log\_cli\_level
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_level`

    Sets the minimum log message level that should be captured for live logging. The integer value or the names of the levels can be used. Note in TOML the integer must be quoted, as there is no support for config parameters of mixed type.

    toml

    ```
    [pytest]log_cli_level = "INFO"log_cli_level = "10"
    ```

     ini

    ```
    [pytest]log_cli_level = INFOlog_cli_level = 10
    ```

    For more information, see  [Live Logs](../how-to/logging.html#live-logs)  .

log\_date\_format
:   Type :
    :   `str`

    Default :
    :   `"%H:%M:%S"`

    Sets a  [`time.strftime()`](https://docs.python.org/3/library/time.html#time.strftime "(in Python v3.14)")  -compatible string that will be used when formatting dates for logging capture.

    toml

    ```
    [pytest]log_date_format = "%Y-%m-%d %H:%M:%S"
    ```

     ini

    ```
    [pytest]log_date_format = %Y-%m-%d %H:%M:%S
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_file
:   Type :
    :   `str`

    Sets a file name relative to the current working directory where log messages should be written to, in addition to the other logging facilities that are active.

    toml

    ```
    [pytest]log_file = "logs/pytest-logs.txt"
    ```

     ini

    ```
    [pytest]log_file = logs/pytest-logs.txt
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_file\_date\_format
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_date_format`

    Sets a  [`time.strftime()`](https://docs.python.org/3/library/time.html#time.strftime "(in Python v3.14)")  -compatible string that will be used when formatting dates for the logging file.

    toml

    ```
    [pytest]log_file_date_format = "%Y-%m-%d %H:%M:%S"
    ```

     ini

    ```
    [pytest]log_file_date_format = %Y-%m-%d %H:%M:%S
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_file\_format
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_format`

    Sets a  [`logging`](https://docs.python.org/3/library/logging.html#module-logging "(in Python v3.14)")  -compatible string used to format logging messages redirected to the logging file.

    toml

    ```
    [pytest]log_file_format = "%(asctime)s %(levelname)s %(message)s"
    ```

     ini

    ```
    [pytest]log_file_format = %(asctime)s %(levelname)s %(message)s
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_file\_level
:   Type :
    :   `str`

    Default :
    :   Fallback to `log_level`

    Sets the minimum log message level that should be captured for the logging file. The integer value (in TOML, as a string) or the names of the levels can be used.

    toml

    ```
    [pytest]log_file_level = "INFO"log_cli_level = "10"
    ```

     ini

    ```
    [pytest]log_file_level = INFOlog_cli_level = 10
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_file\_mode
:   Type :
    :   `str`

    Default :
    :   `"w"`

    Sets the mode that the logging file is opened with. The options are `"w"` to recreate the file or `"a"` to append to the file.

    toml

    ```
    [pytest]log_file_mode = "a"
    ```

     ini

    ```
    [pytest]log_file_mode = a
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_format
:   Type :
    :   `str`

    Default :
    :   `%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s`

    Sets a  [`logging`](https://docs.python.org/3/library/logging.html#module-logging "(in Python v3.14)")  -compatible string used to format captured logging messages.

    toml

    ```
    [pytest]log_format = "%(asctime)s %(levelname)s %(message)s"
    ```

     ini

    ```
    [pytest]log_format = %(asctime)s %(levelname)s %(message)s
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

log\_level
:   Type :
    :   `str`

    Sets the minimum log message level that should be captured for logging capture. Not set by default, so it depends on the root/parent log handler’s effective level, where it is `"WARNING"` by default. The integer value (in TOML, as a string) or the names of the levels can be used.

    toml

    ```
    [pytest]log_level = "INFO"log_cli_level = "10"
    ```

     ini

    ```
    [pytest]log_level = INFOlog_cli_level = 10
    ```

    For more information, see  [How to manage logging](../how-to/logging.html#logging)  .

markers
:   Type :
    :   `list[str]`

    When the  [`strict_markers`](#confval-strict_markers)  configuration option is set, only known markers - defined in code by core pytest or some plugin - are allowed.

    You can list additional markers in this setting to add them to the whitelist, in which case you probably want to set  [`strict_markers`](#confval-strict_markers)  to `true` to avoid future regressions:

    toml

    ```
    [pytest]addopts = ["--strict-markers"]markers = ["slow", "serial"]
    ```

     ini

    ```
    [pytest]strict_markers = truemarkers =    slow    serial
    ```

minversion
:   Type :
    :   `str`

    Specifies a minimal pytest version required for running tests.

    toml

    ```
    [pytest]minversion = 3.0  # will fail if we run with pytest-2.8
    ```

     ini

    ```
    [pytest]minversion = 3.0  # will fail if we run with pytest-2.8
    ```

norecursedirs
:   Type :
    :   `list[str]`

    Default :
    :   `["*.egg", ".*", "_darcs", "build", "CVS", "dist", "node_modules", "venv", "{arch}"]`

    Set the directory basename patterns to avoid when recursing for test discovery. The individual (fnmatch-style) patterns are applied to the basename of a directory to decide if to recurse into it. Pattern matching characters:

    ```
    *       matches everything
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq
    ```

    Setting a `norecursedirs` replaces the default. Here is an example of how to avoid certain directories:

    toml

    ```
    [pytest]norecursedirs = [".svn", "_build", "tmp*"]
    ```

     ini

    ```
    [pytest]norecursedirs = .svn _build tmp*
    ```

    This would tell `pytest` to not look into typical subversion or sphinx-build directories or into any `tmp` prefixed directory.

    Additionally, `pytest` will attempt to intelligently identify and ignore a virtualenv. Any directory deemed to be the root of a virtual environment will not be considered during test collection unless  [`--collect-in-virtualenv`](#cmdoption-collect-in-virtualenv)  is given. Note also that `norecursedirs` takes precedence over `--collect-in-virtualenv` ; e.g. if you intend to run tests in a virtualenv with a base directory that matches `'.*'` you *must* override `norecursedirs` in addition to using the `--collect-in-virtualenv` flag.

python\_classes
:   Type :
    :   `list[str]`

    Default :
    :   `["Test"]`

    One or more name prefixes or glob-style patterns determining which classes are considered for test collection. Search for multiple glob patterns by adding a space between patterns. By default, pytest will consider any class prefixed with `Test` as a test collection. Here is an example of how to collect tests from classes that end in `Suite` :

    toml

    ```
    [pytest]python_classes = ["*Suite"]
    ```

     ini

    ```
    [pytest]python_classes = *Suite
    ```

    Note that `unittest.TestCase` derived classes are always collected regardless of this option, as `unittest` ’s own collection framework is used to collect those tests.

python\_files
:   Type :
    :   `list[str]`

    Default :
    :   `["test_*.py", "*_test.py"]`

    One or more Glob-style file patterns determining which python files are considered as test modules. Search for multiple glob patterns by adding a space between patterns:

    toml

    ```
    [pytest]python_files = ["test_*.py", "check_*.py", "example_*.py"]
    ```

     ini

    ```
    [pytest]python_files = test_*.py check_*.py example_*.py
    ```

    Or one per line:

    ```
    [pytest]python_files =    test_*.py    check_*.py    example_*.py
    ```

python\_functions
:   Type :
    :   `list[str]`

    Default :
    :   `["test"]`

    One or more name prefixes or glob-patterns determining which test functions and methods are considered tests. Search for multiple glob patterns by adding a space between patterns. By default, pytest will consider any function prefixed with `test` as a test. Here is an example of how to collect test functions and methods that end in `_test` :

    toml

    ```
    [pytest]python_functions = ["*_test"]
    ```

     ini

    ```
    [pytest]python_functions = *_test
    ```

    Note that this has no effect on methods that live on a `unittest.TestCase` derived class, as `unittest` ’s own collection framework is used to collect those tests.

    See  [Changing naming conventions](../example/pythoncollection.html#change-naming-conventions)  for more detailed examples.

pythonpath
:   Type :
    :   `list[str]`

    Sets list of directories that should be added to the python search path. Directories will be added to the head of  [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path "(in Python v3.14)")  . Similar to the   [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH "(in Python v3.14)")  environment variable, the directories will be included in where Python will look for imported modules. Paths are relative to the  [rootdir](customize.html#rootdir)  directory. Directories remain in path for the duration of the test session.

    toml

    ```
    [pytest]pythonpath = ["src1", "src2"]
    ```

     ini

    ```
    [pytest]pythonpath = src1 src2
    ```

required\_plugins
:   Type :
    :   `list[str]`

    A space separated list of plugins that must be present for pytest to run. Plugins can be listed with or without version specifiers directly following their name. Whitespace between different version specifiers is not allowed. If any one of the plugins is not found, emit an error.

    toml

    ```
    [pytest]required_plugins = ["pytest-django>=3.0.0,<4.0.0", "pytest-html", "pytest-xdist>=1.0.0"]
    ```

     ini

    ```
    [pytest]required_plugins = pytest-django>=3.0.0,<4.0.0 pytest-html pytest-xdist>=1.0.0
    ```

strict
:   Type :
    :   `bool`

    Default :
    :   `false`

    If set to `true` , enable “strict mode”, which enables the following options:

    * [`strict_config`](#confval-strict_config)
    * [`strict_markers`](#confval-strict_markers)
    * [`strict_parametrization_ids`](#confval-strict_parametrization_ids)
    * [`strict_xfail`](#confval-strict_xfail)

    Plugins may also enable their own strictness options.

    If you explicitly set an individual strictness option, it takes precedence over `strict` .

    Note

    If pytest adds new strictness options in the future, they will also be enabled in strict mode. Therefore, you should only enable strict mode if you use a pinned/locked version of pytest, or if you want to proactively adopt new strictness options as they are added.

    toml

    ```
    [pytest]strict = true
    ```

     ini

    ```
    [pytest]strict = true
    ```

    Added in version 9.0.

strict\_config
:   Type :
    :   `bool`

    Default :
    :   `false`

    If set to `true` , any warnings encountered while parsing the `pytest` section of the configuration file will raise errors.

    toml

    ```
    [pytest]strict_config = true
    ```

     ini

    ```
    [pytest]strict_config = true
    ```

    You can also enable this option via the  [`strict`](#confval-strict)  option.

strict\_markers
:   Type :
    :   `bool`

    Default :
    :   `false`

    If set to `true` , markers not registered in the `markers` section of the configuration file will raise errors.

    toml

    ```
    [pytest]strict_markers = true
    ```

     ini

    ```
    [pytest]strict_markers = true
    ```

    You can also enable this option via the  [`strict`](#confval-strict)  option.

strict\_parametrization\_ids
:   Type :
    :   `bool`

    Default :
    :   `false`

    If set to `true` , pytest emits an error if it detects non-unique parameter set IDs.

    If not set, pytest automatically handles this by adding `0` , `1` , … to duplicate IDs, making them unique.

    toml

    ```
    [pytest]strict_parametrization_ids = true
    ```

     ini

    ```
    [pytest]strict_parametrization_ids = true
    ```

    You can also enable this option via the  [`strict`](#confval-strict)  option.

    For example,

    ```
    import pytest

    @pytest.mark.parametrize("letter", ["a", "a"])def test_letter_is_ascii(letter):
        assert letter.isascii()
    ```

    will emit an error because both cases (parameter sets) have the same auto-generated ID “a”.

    To fix the error, if you decide to keep the duplicates, explicitly assign unique IDs:

    ```
    import pytest

    @pytest.mark.parametrize("letter", ["a", "a"], ids=["a0", "a1"])def test_letter_is_ascii(letter):
        assert letter.isascii()
    ```

    See  [`parametrize`](#pytest.Metafunc.parametrize "pytest.Metafunc.parametrize")  and  [`pytest.param()`](#pytest.param "pytest.param")  for other ways to set IDs.

strict\_xfail
:   Type :
    :   `bool`

    Default :
    :   `false`

    If set to `true` , tests marked with `@pytest.mark.xfail` that actually succeed will by default fail the test suite. For more information, see  [strict parameter](../how-to/skipping.html#xfail-strict-tutorial)  .

    toml

    ```
    [pytest]strict_xfail = true
    ```

     ini

    ```
    [pytest]strict_xfail = true
    ```

    You can also enable this option via the  [`strict`](#confval-strict)  option.

    Changed in version 9.0:  Renamed from `xfail_strict` to `strict_xfail` . `xfail_strict` is accepted as an alias for `strict_xfail` .

testpaths
:   Type :
    :   `list[str]`

    Sets list of directories that should be searched for tests when no specific directories, files or test ids are given in the command line when executing pytest from the  [rootdir](customize.html#rootdir)  directory. File system paths may use shell-style wildcards, including the recursive `**` pattern.

    Useful when all project tests are in a known location to speed up test collection and to avoid picking up undesired tests by accident.

    toml

    ```
    [pytest]testpaths = ["testing", "doc"]
    ```

     ini

    ```
    [pytest]testpaths = testing doc
    ```

    This configuration means that executing:

    ```
    pytest
    ```

    has the same practical effects as executing:

    ```
    pytest testing doc
    ```

tmp\_path\_retention\_count
:   Type :
    :   `str`

    Default :
    :   `"3"`

    How many sessions should pytest keep the `tmp_path` directories, according to  [`tmp_path_retention_policy`](#confval-tmp_path_retention_policy)  .

    toml

    ```
    [pytest]tmp_path_retention_count = "3"
    ```

     ini

    ```
    [pytest]tmp_path_retention_count = 3
    ```

tmp\_path\_retention\_policy
:   Type :
    :   `str`

    Default :
    :   `"all"`

    Controls which directories created by the `tmp_path` fixture are kept around, based on test outcome.

    > * `all` : retains directories for all tests, regardless of the outcome.
    > * `failed` : retains directories only for tests with outcome `error` or `failed` .
    > * `none` : directories are always removed after each test ends, regardless of the outcome.

    toml

    ```
    [pytest]tmp_path_retention_policy = "all"
    ```

     ini

    ```
    [pytest]tmp_path_retention_policy = all
    ```

truncation\_limit\_chars
:   Type :
    :   `int`

    Default :
    :   `640`

    Controls maximum number of characters to truncate assertion message contents.

    Setting value to `0` disables the character limit for truncation.

    toml

    ```
    [pytest]truncation_limit_chars = 640
    ```

     ini

    ```
    [pytest]truncation_limit_chars = 640
    ```

    pytest truncates the assert messages to a certain limit by default to prevent comparison with large data to overload the console output.

    Note

    If pytest detects it is  [running on CI](../explanation/ci.html#ci-pipelines)  , truncation is disabled automatically.

truncation\_limit\_lines
:   Type :
    :   `int`

    Default :
    :   `8`

    Controls maximum number of lines to truncate assertion message contents.

    Setting value to `0` disables the lines limit for truncation.

    toml

    ```
    [pytest]truncation_limit_lines = 8
    ```

     ini

    ```
    [pytest]truncation_limit_lines = 8
    ```

    pytest truncates the assert messages to a certain limit by default to prevent comparison with large data to overload the console output.

    Note

    If pytest detects it is  [running on CI](../explanation/ci.html#ci-pipelines)  , truncation is disabled automatically.

usefixtures
:   Type :
    :   `list[str]`

    List of fixtures that will be applied to all test functions; this is semantically the same to apply the `@pytest.mark.usefixtures` marker to all test functions.

    toml

    ```
    [pytest]usefixtures = ["clean_db"]
    ```

     ini

    ```
    [pytest]usefixtures =    clean_db
    ```

verbosity\_assertions
:   Type :
    :   `str`

    Default :
    :   `"auto"`

    Set a verbosity level specifically for assertion related output, overriding the application wide level.

    toml

    ```
    [pytest]verbosity_assertions = "2"
    ```

     ini

    ```
    [pytest]verbosity_assertions = 2
    ```

    A special value of `"auto"` can be used to explicitly use the global verbosity level.

assertion\_text\_diff\_style
:   Type :
    :   `str`

    Default :
    :   `"ndiff"`

    Set how pytest renders diffs for string equality assertions.

    Supported values are:

    * `ndiff` : use the inline diff rendering markers.
    * `block` : render each string in separate `Left:` and `Right:` blocks.

    toml

    ```
    [pytest]assertion_text_diff_style = "block"
    ```

     ini

    ```
    [pytest]assertion_text_diff_style = block
    ```

verbosity\_subtests
:   Type :
    :   `str`

    Default :
    :   `"auto"`

    Set the verbosity level specifically for **passed** subtests.

    toml

    ```
    [pytest]verbosity_subtests = "1"
    ```

     ini

    ```
    [pytest]verbosity_subtests = 1
    ```

    A value of `1` or higher will show output for **passed** subtests ( **failed** subtests are always reported). Passed subtests output can be suppressed with the value `0` , which overwrites the  [`-v`](#cmdoption-v)  command-line option.

    A special value of `"auto"` can be used to explicitly use the global verbosity level.

    See also:  [How to use subtests](../how-to/subtests.html#subtests)  .

verbosity\_test\_cases
:   Type :
    :   `str`

    Default :
    :   `"auto"`

    Set a verbosity level specifically for test case execution related output, overriding the application wide level.

    toml

    ```
    [pytest]verbosity_test_cases = "2"
    ```

     ini

    ```
    [pytest]verbosity_test_cases = 2
    ```

    A special value of `"auto"` can be used to explicitly use the global verbosity level.

## Command-line Flags

This section documents all command-line options provided by pytest’s core plugins.

Note

External plugins can add their own command-line options. This reference documents only the options from pytest’s core plugins. To see all available options including those from installed plugins, run `pytest --help` .

### Test Selection

-k EXPRESSION
:   Only run tests which match the given substring expression. An expression is a Python evaluable expression where all names are substring-matched against test names and their parent classes.

    Examples:

    ```
    pytest -k "test_method or test_other"  # matches names containing 'test_method' OR 'test_other'pytest -k "not test_method"            # matches names NOT containing 'test_method'pytest -k "not test_method and not test_other"  # excludes both
    ```

    The matching is case-insensitive. Keywords are also matched to classes and functions containing extra names in their `extra_keyword_matches` set.

    See  [Specifying which tests to run](../how-to/usage.html#select-tests)  for more information and examples.

-m MARKEXPR
:   Only run tests matching given mark expression. Supports `and` , `or` , and `not` operators.

    Examples:

    ```
    pytest -m slow                  # run tests marked with @pytest.mark.slowpytest -m "not slow"            # run tests NOT marked slowpytest -m "mark1 and not mark2" # run tests marked mark1 but not mark2
    ```

    See  [How to mark test functions with attributes](../how-to/mark.html#mark)  for more information on markers.

--markers
:   Show all available markers (builtin, plugin, and per-project markers defined in configuration).

### Test Execution Control

-x , --exitfirst
:   Exit instantly on first error or failed test.

--maxfail =NUM
:   Exit after first `num` failures or errors. Useful for CI environments where you want to fail fast but see a few failures.

--last-failed , --lf
:   Rerun only the tests that failed at the last run. If no tests failed (or no cached data exists), all tests are run. See also  [`cache_dir`](#confval-cache_dir)  and  [How to re-run failed tests and maintain state between test runs](../how-to/cache.html#cache)  .

--failed-first , --ff
:   Run all tests, but run the last failures first. This may re-order tests and thus lead to repeated fixture setup/teardown.

--new-first , --nf
:   Run tests from new files first, then the rest of the tests sorted by file modification time.

--stepwise , --sw
:   Exit on test failure and continue from last failing test next time. Useful for fixing multiple test failures one at a time.

    See  [Stepwise](../how-to/cache.html#cache-stepwise)  for more information.

--stepwise-skip , --sw-skip
:   Ignore the first failing test but stop on the next failing test. Implicitly enables  [`--stepwise`](#cmdoption-stepwise)  .

--stepwise-reset , --sw-reset
:   Resets stepwise state, restarting the stepwise workflow. Implicitly enables  [`--stepwise`](#cmdoption-stepwise)  .

--last-failed-no-failures , --lfnf
:   With  [`--last-failed`](#cmdoption-last-failed)  , determines whether to execute tests when there are no previously known failures or when no cached `lastfailed` data was found.

    * `all` (default): runs the full test suite again
    * `none` : just emits a message about no known failures and exits successfully

--runxfail
:   Report the results of xfail tests as if they were not marked. Useful for debugging xfailed tests. See  [XFail: mark test functions as expected to fail](../how-to/skipping.html#xfail)  .

### Collection

--collect-only , --co
:   Only collect tests, don’t execute them. Shows which tests would be collected and run.

--pyargs
:   Try to interpret all arguments as Python packages. Useful for running tests of installed packages:

    ```
    pytest --pyargs pkg.testing
    ```

--ignore =PATH
:   Ignore path during collection (multi-allowed). Can be specified multiple times.

--ignore-glob =PATTERN
:   Ignore path pattern during collection (multi-allowed). Supports glob patterns.

--deselect =NODEID\_PREFIX
:   Deselect item (via node id prefix) during collection (multi-allowed).

--confcutdir =DIR
:   Only load `conftest.py` files relative to specified directory.

--noconftest
:   Don’t load any `conftest.py` files.

--keep-duplicates
:   Keep duplicate tests. By default, pytest removes duplicate test items.

--collect-in-virtualenv
:   Don’t ignore tests in a local virtualenv directory. By default, pytest skips tests in virtualenv directories.

--continue-on-collection-errors
:   Force test execution even if collection errors occur.

--import-mode
:   Prepend/append to sys.path when importing test modules and conftest files.

    * `prepend` (default): prepend to sys.path
    * `append` : append to sys.path
    * `importlib` : use importlib to import test modules

    See  [pytest import mechanisms and sys.path/PYTHONPATH](../explanation/pythonpath.html#pythonpath)  for more information.

### Fixtures

--fixtures , --funcargs
:   Show available fixtures, sorted by plugin appearance. Fixtures with leading `_` are only shown with  [`--verbose`](#cmdoption-v)  .

--fixtures-per-test
:   Show fixtures per test.

--setup-only
:   Only setup fixtures, do not execute tests. See  [How to use fixtures](../how-to/fixtures.html#how-to-fixtures)  .

--setup-show
:   Show setup of fixtures while executing tests.

--setup-plan
:   Show what fixtures and tests would be executed but don’t execute anything.

### Debugging

--pdb
:   Start the interactive Python debugger on errors or KeyboardInterrupt. See  [Using python:library/pdb with pytest](../how-to/failures.html#pdb-option)  .

--pdbcls =MODULENAME:CLASSNAME
:   Specify a custom interactive Python debugger for use with  [`--pdb`](#cmdoption-pdb)  .

    Example:

    ```
    pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
    ```

--trace
:   Immediately break when running each test.

    See  [Dropping to pdb at the start of a test](../how-to/failures.html#trace-option)  for more information.

--full-trace
:   Don’t cut any tracebacks (default is to cut).

    See  [Modifying Python traceback printing](../how-to/output.html#how-to-modifying-python-tb-printing)  for more information.

--debug , --debug =DEBUG\_FILE\_NAME
:   Store internal tracing debug information in this log file. This file is opened with `'w'` and truncated as a result, care advised. Default file name if not specified: `pytestdebug.log` .

--trace-config
:   Trace considerations of conftest.py files.

### Output and Reporting

-v , --verbose
:   Increase verbosity. Can be specified multiple times (e.g., `-vv` ) for even more verbose output.

    See  [Fine-grained verbosity](../how-to/output.html#pytest-fine-grained-verbosity)  for fine-grained control over verbosity.

-q , --quiet
:   Decrease verbosity.

--verbosity =NUM
:   Set verbosity level explicitly. Default: 0.

-r CHARS , --report-chars =CHARS
:   Show extra test summary info as specified by chars:

    * `f` : failed
    * `E` : error
    * `s` : skipped
    * `x` : xfailed
    * `X` : xpassed
    * `p` : passed
    * `P` : passed with output
    * `a` : all except passed (p/P)
    * `A` : all
    * `w` : warnings (enabled by default)
    * `N` : resets the list

    Default: `'fE'`

    Examples:

    ```
    pytest -rA           # show all outcomespytest -rfE          # show only failed and errors (default)pytest -rfs          # show failed and skipped
    ```

    See  [Producing a detailed summary report](../how-to/output.html#pytest-detailed-failed-tests-usage)  for more information.

--no-header
:   Disable header.

--no-summary
:   Disable summary.

--no-fold-skipped
:   Do not fold skipped tests in short summary.

--force-short-summary
:   Force condensed summary output regardless of verbosity level.

-l , --showlocals
:   Show locals in tracebacks (disabled by default).

--no-showlocals
:   Hide locals in tracebacks (negate  [`--showlocals`](#cmdoption-l)  passed through addopts).

--tb =STYLE
:   Traceback print mode:

    * `auto` : intelligent traceback formatting (default)
    * `long` : exhaustive, informative traceback formatting
    * `short` : shorter traceback format
    * `line` : only the failing line
    * `native` : Python’s standard traceback
    * `no` : no traceback

    See  [Modifying Python traceback printing](../how-to/output.html#how-to-modifying-python-tb-printing)  for examples.

--xfail-tb
:   Show tracebacks for xfail (as long as  [`--tb`](#cmdoption-tb)  != `no` ).

--show-capture
:   Controls how captured stdout/stderr/log is shown on failed tests.

    * `no` : don’t show captured output
    * `stdout` : show captured stdout
    * `stderr` : show captured stderr
    * `log` : show captured logging
    * `all` (default): show all captured output

--color =WHEN
:   Color terminal output:

    * `yes` : always use color
    * `no` : never use color
    * `auto` (default): use color if terminal supports it

--code-highlight ={yes,no}
:   Whether code should be highlighted (only if  [`--color`](#cmdoption-color)  is also enabled). Default: `yes` .

--pastebin =MODE
:   Send failed|all info to bpaste.net pastebin service.

--durations =NUM
:   Show N slowest setup/test durations (N=0 for all). See  [Profiling test execution duration](../how-to/usage.html#durations)  .

--durations-min =NUM
:   Minimal duration in seconds for inclusion in slowest list. Default: 0.005 (or 0.0 if `-vv` is given).

### Output Capture

--capture =METHOD
:   Per-test capturing method:

    * `fd` : capture at file descriptor level (default)
    * `sys` : capture at sys level
    * `no` : don’t capture output
    * `tee-sys` : capture but also show output on terminal

    See  [How to capture stdout/stderr output](../how-to/capture-stdout-stderr.html#captures)  .

-s
:   Shortcut for  [`--capture=no`](#cmdoption-capture)  .

### JUnit XML

--junit-xml =PATH , --junitxml =PATH
:   Create junit-xml style report file at given path.

--junit-prefix =STR , --junitprefix =STR
:   Prepend prefix to classnames in junit-xml output.

### Cache

--cache-show [=PATTERN]
:   Show cache contents, don’t perform collection or tests. Default glob pattern: `'*'` .

--cache-clear
:   Remove all cache contents at start of test run. See  [How to re-run failed tests and maintain state between test runs](../how-to/cache.html#cache)  .

### Warnings

--disable-pytest-warnings , --disable-warnings
:   Disable warnings summary.

-W WARNING , --pythonwarnings =WARNING
:   Set which warnings to report, see `-W` option of Python itself. Can be specified multiple times.

--max-warnings =NUM
:   Exit with  [`pytest.ExitCode`](#pytest.ExitCode "pytest.ExitCode")  `MAX_WARNINGS_ERROR` (code `6` ) if all the tests pass, but the number of warnings exceeds the given threshold. By default there is no limit. Can also be set via the  [`max_warnings`](#confval-max_warnings)  configuration option.

### Doctest

--doctest-modules
:   Run doctests in all .py modules.

    See  [How to run doctests](../how-to/doctest.html#doctest)  for more information on using doctests with pytest.

--doctest-report
:   Choose another output format for diffs on doctest failure:

    * `none`
    * `cdiff`
    * `ndiff`
    * `udiff`
    * `only_first_failure`

--doctest-glob =PATTERN
:   Doctests file matching pattern. Default: `test*.txt` .

--doctest-ignore-import-errors
:   Ignore doctest collection errors.

--doctest-continue-on-failure
:   For a given doctest, continue to run after the first failure.

### Configuration

-c FILE , --config-file =FILE
:   Load configuration from `FILE` instead of trying to locate one of the implicit configuration files.

--rootdir =ROOTDIR
:   Define root directory for tests. Can be relative path: `'root_dir'` , `'./root_dir'` , `'root_dir/another_dir/'` ; absolute path: `'/home/user/root_dir'` ; path with variables: `'$HOME/root_dir'` .

--basetemp =DIR
:   Base temporary directory for this test run. Warning: this directory is removed if it exists.

    See  [Temporary directory location and retention](../how-to/tmp_path.html#temporary-directory-location-and-retention)  for more information.

-o OPTION=VALUE , --override-ini =OPTION=VALUE
:   Override configuration option with `option=value` style. Can be specified multiple times.

    Example:

    ```
    pytest -o strict_xfail=true -o cache_dir=cache
    ```

--strict-config
:   Enables the  [`strict_config`](#confval-strict_config)  option.

--strict-markers
:   Enables the  [`strict_markers`](#confval-strict_markers)  option.

--strict
:   Enables the  [`strict`](#confval-strict)  option (which enables all strictness options).

--assert =MODE
:   Control assertion debugging tools:

    * `plain` : performs no assertion debugging
    * `rewrite` (default): rewrites assert statements in test modules on import to provide assert expression information

### Logging

See  [How to manage logging](../how-to/logging.html#logging)  for a guide on using these flags.

--log-level =LEVEL
:   Level of messages to catch/display. Not set by default, so it depends on the root/parent log handler’s effective level, where it is `WARNING` by default.

--log-format =FORMAT
:   Log format used by the logging module.

--log-date-format =FORMAT
:   Log date format used by the logging module.

--log-cli-level =LEVEL
:   CLI logging level. See  [Live Logs](../how-to/logging.html#live-logs)  .

--log-cli-format =FORMAT
:   Log format used by the logging module for CLI output.

--log-cli-date-format =FORMAT
:   Log date format used by the logging module for CLI output.

--log-file =PATH
:   Path to a file logging will be written to.

--log-file-mode
:   Log file open mode:

    * `w` (default): recreate the file
    * `a` : append to the file

--log-file-level =LEVEL
:   Log file logging level.

--log-file-format =FORMAT
:   Log format used by the logging module for the log file.

--log-file-date-format =FORMAT
:   Log date format used by the logging module for the log file.

--log-auto-indent =VALUE
:   Auto-indent multiline messages passed to the logging module. Accepts `true|on` , `false|off` or an integer.

--log-disable =LOGGER
:   Disable a logger by name. Can be passed multiple times.

### Plugin and Extension Management

-p NAME
:   Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the `no:` prefix, e.g. `no:doctest` . See also  [`--disable-plugin-autoload`](#cmdoption-disable-plugin-autoload)  .

--disable-plugin-autoload
:   Disable plugin auto-loading through entry point packaging metadata. Only plugins explicitly specified in  [`-p`](#cmdoption-p)  or env var   [`PYTEST_PLUGINS`](#envvar-PYTEST_PLUGINS)  will be loaded.

### Version and Help

-V , --version
:   Display pytest version and information about plugins. When given twice, also display information about plugins.

-h , --help
:   Show help message and configuration info.

### Complete Help Output

All the command-line flags can also be obtained by running `pytest --help` :

```
$ pytest --help
usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         Only run tests which match the given substring
                        expression. An expression is a Python evaluable
                        expression where all names are substring-matched
                        against test names and their parent classes.
                        Example: -k 'test_method or test_other' matches all
                        test functions and classes whose name contains
                        'test_method' or 'test_other', while -k 'not
                        test_method' matches those that don't contain
                        'test_method' in their names. -k 'not test_method
                        and not test_other' will eliminate the matches.
                        Additionally keywords are matched to classes and
                        functions containing extra names in their
                        'extra_keyword_matches' set, as well as functions
                        which have names assigned directly to them. The
                        matching is case-insensitive.
  -m MARKEXPR           Only run tests matching given mark expression. For
                        example: -m 'mark1 and not mark2'.
  --markers             show markers (builtin, plugin and per-project ones).
  -x, --exitfirst       Exit instantly on first error or failed test
  --maxfail=num         Exit after first num failures or errors
  --strict-config       Enables the strict_config option
  --strict-markers      Enables the strict_markers option
  --strict              Enables the strict option
  --fixtures, --funcargs
                        Show available fixtures, sorted by plugin appearance
                        (fixtures with leading '_' are only shown with '-v')
  --fixtures-per-test   Show fixtures per test
  --pdb                 Start the interactive Python debugger on errors or
                        KeyboardInterrupt
  --pdbcls=modulename:classname
                        Specify a custom interactive Python debugger for use
                        with --pdb.For example:
                        --pdbcls=IPython.terminal.debugger:TerminalPdb
  --trace               Immediately break when running each test
  --capture=method      Per-test capturing method: one of fd|sys|no|tee-sys
  -s                    Shortcut for --capture=no
  --runxfail            Report the results of xfail tests as if they were
                        not marked
  --lf, --last-failed   Rerun only the tests that failed at the last run (or
                        all if none failed)
  --ff, --failed-first  Run all tests, but run the last failures first. This
                        may re-order tests and thus lead to repeated fixture
                        setup/teardown.
  --nf, --new-first     Run tests from new files first, then the rest of the
                        tests sorted by file mtime
  --cache-show=[CACHESHOW]
                        Show cache contents, don't perform collection or
                        tests. Optional argument: glob (default: '*').
  --cache-clear         Remove all cache contents at start of test run
  --lfnf, --last-failed-no-failures={all,none}
                        With ``--lf``, determines whether to execute tests
                        when there are no previously (known) failures or
                        when no cached ``lastfailed`` data was found.
                        ``all`` (the default) runs the full test suite
                        again. ``none`` just emits a message about no known
                        failures and exits successfully.
  --sw, --stepwise      Exit on test failure and continue from last failing
                        test next time
  --sw-skip, --stepwise-skip
                        Ignore the first failing test but stop on the next
                        failing test. Implicitly enables --stepwise.
  --sw-reset, --stepwise-reset
                        Resets stepwise state, restarting the stepwise
                        workflow. Implicitly enables --stepwise.

Reporting:
  --durations=N         Show N slowest setup/test durations (N=0 for all)
  --durations-min=N     Minimal duration in seconds for inclusion in slowest
                        list. Default: 0.005 (or 0.0 if -vv is given).
  -v, --verbose         Increase verbosity
  --no-header           Disable header
  --no-summary          Disable summary
  --no-fold-skipped     Do not fold skipped tests in short summary.
  --force-short-summary
                        Force condensed summary output regardless of
                        verbosity level.
  -q, --quiet           Decrease verbosity
  --verbosity=VERBOSE   Set verbosity. Default: 0.
  -r, --report-chars chars
                        Show extra test summary info as specified by chars:
                        (f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed,
                        (p)assed, (P)assed with output, (a)ll except passed
                        (p/P), or (A)ll. (w)arnings are enabled by default
                        (see --disable-warnings), 'N' can be used to reset
                        the list. (default: 'fE').
  --disable-warnings, --disable-pytest-warnings
                        Disable warnings summary
  -l, --showlocals      Show locals in tracebacks (disabled by default)
  --no-showlocals       Hide locals in tracebacks (negate --showlocals
                        passed through addopts)
  --tb=style            Traceback print mode
                        (auto/long/short/line/native/no)
  --xfail-tb            Show tracebacks for xfail (as long as --tb != no)
  --show-capture={no,stdout,stderr,log,all}
                        Controls how captured stdout/stderr/log is shown on
                        failed tests. Default: all.
  --full-trace          Don't cut any tracebacks (default is to cut)
  --color=color         Color terminal output (yes/no/auto)
  --code-highlight={yes,no}
                        Whether code should be highlighted (only if --color
                        is also enabled). Default: yes.
  --pastebin=mode       Send failed|all info to bpaste.net pastebin service
  --junitxml, --junit-xml=path
                        Create junit-xml style report file at given path
  --junitprefix, --junit-prefix=str
                        Prepend prefix to classnames in junit-xml output

pytest-warnings:
  -W, --pythonwarnings PYTHONWARNINGS
                        Set which warnings to report, see -W option of
                        Python itself
  --max-warnings=num    Exit with error if all tests pass but the number of
                        warnings exceeds this threshold

collection:
  --collect-only, --co  Only collect tests, don't execute them
  --pyargs              Try to interpret all arguments as Python packages
  --ignore=path         Ignore path during collection (multi-allowed)
  --ignore-glob=path    Ignore path pattern during collection (multi-
                        allowed)
  --deselect=nodeid_prefix
                        Deselect item (via node id prefix) during collection
                        (multi-allowed)
  --confcutdir=dir      Only load conftest.py's relative to specified dir
  --noconftest          Don't load any conftest.py files
  --keep-duplicates     Keep duplicate tests
  --collect-in-virtualenv
                        Don't ignore tests in a local virtualenv directory
  --continue-on-collection-errors
                        Force test execution even if collection errors occur
  --import-mode={prepend,append,importlib}
                        Prepend/append to sys.path when importing test
                        modules and conftest files. Default: prepend.
  --doctest-modules     Run doctests in all .py modules
  --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                        Choose another output format for diffs on doctest
                        failure
  --doctest-glob=pat    Doctests file matching pattern, default: test*.txt
  --doctest-ignore-import-errors
                        Ignore doctest collection errors
  --doctest-continue-on-failure
                        For a given doctest, continue to run after the first
                        failure

test session debugging and configuration:
  -c, --config-file FILE
                        Load configuration from `FILE` instead of trying to
                        locate one of the implicit configuration files.
  --rootdir=ROOTDIR     Define root directory for tests. Can be relative
                        path: 'root_dir', './root_dir',
                        'root_dir/another_dir/'; absolute path:
                        '/home/user/root_dir'; path with variables:
                        '$HOME/root_dir'.
  --basetemp=dir        Base temporary directory for this test run.
                        (Warning: this directory is removed if it exists.)
  -V, --version         Display pytest version and information about
                        plugins. When given twice, also display information
                        about plugins.
  -h, --help            Show help message and configuration info
  -p name               Early-load given plugin module name or entry point
                        (multi-allowed). To avoid loading of plugins, use
                        the `no:` prefix, e.g. `no:doctest`. See also
                        --disable-plugin-autoload.
  --disable-plugin-autoload
                        Disable plugin auto-loading through entry point
                        packaging metadata. Only plugins explicitly
                        specified in -p or env var PYTEST_PLUGINS will be
                        loaded.
  --trace-config        Trace considerations of conftest.py files
  --debug=[DEBUG_FILE_NAME]
                        Store internal tracing debug information in this log
                        file. This file is opened with 'w' and truncated as
                        a result, care advised. Default: pytestdebug.log.
  -o, --override-ini OVERRIDE_INI
                        Override configuration option with "option=value"
                        style, e.g. `-o strict_xfail=True -o
                        cache_dir=cache`.
  --assert=MODE         Control assertion debugging tools.
                        'plain' performs no assertion debugging.
                        'rewrite' (the default) rewrites assert statements
                        in test modules on import to provide assert
                        expression information.
  --setup-only          Only setup fixtures, do not execute tests
  --setup-show          Show setup of fixtures while executing tests
  --setup-plan          Show what fixtures and tests would be executed but
                        don't execute anything

logging:
  --log-level=LEVEL     Level of messages to catch/display. Not set by
                        default, so it depends on the root/parent log
                        handler's effective level, where it is "WARNING" by
                        default.
  --log-format=LOG_FORMAT
                        Log format used by the logging module
  --log-date-format=LOG_DATE_FORMAT
                        Log date format used by the logging module
  --log-cli-level=LOG_CLI_LEVEL
                        CLI logging level
  --log-cli-format=LOG_CLI_FORMAT
                        Log format used by the logging module
  --log-cli-date-format=LOG_CLI_DATE_FORMAT
                        Log date format used by the logging module
  --log-file=LOG_FILE   Path to a file when logging will be written to
  --log-file-mode={w,a}
                        Log file open mode
  --log-file-level=LOG_FILE_LEVEL
                        Log file logging level
  --log-file-format=LOG_FILE_FORMAT
                        Log format used by the logging module
  --log-file-date-format=LOG_FILE_DATE_FORMAT
                        Log date format used by the logging module
  --log-auto-indent=LOG_AUTO_INDENT
                        Auto-indent multiline messages passed to the logging
                        module. Accepts true|on, false|off or an integer.
  --log-disable=LOGGER_DISABLE
                        Disable a logger by name. Can be passed multiple
                        times.

[pytest] configuration options in the first pytest.toml|pytest.ini|tox.ini|setup.cfg|pyproject.toml file found:

  markers (linelist):   Register new markers for test functions
  empty_parameter_set_mark (string):
                        Default marker for empty parametersets
  strict_config (bool): Any warnings encountered while parsing the `pytest`
                        section of the configuration file raise errors
  strict_markers (bool):
                        Markers not registered in the `markers` section of
                        the configuration file raise errors
  strict (bool):        Enables all strictness options, currently:
                        strict_config, strict_markers, strict_xfail,
                        strict_parametrization_ids
  filterwarnings (linelist):
                        Each line specifies a pattern for
                        warnings.filterwarnings. Processed after
                        -W/--pythonwarnings.
  max_warnings (string):
                        Exit with error if all tests pass but the number of
                        warnings exceeds this threshold
  norecursedirs (args): Directory patterns to avoid for recursion
  testpaths (args):     Directories to search for tests when no files or
                        directories are given on the command line
  collect_imported_tests (bool):
                        Whether to collect tests in imported modules outside
                        `testpaths`
  consider_namespace_packages (bool):
                        Consider namespace packages when resolving module
                        names during import
  usefixtures (args):   List of default fixtures to be used with this
                        project
  python_files (args):  Glob-style file patterns for Python test module
                        discovery
  python_classes (args):
                        Prefixes or glob names for Python test class
                        discovery
  python_functions (args):
                        Prefixes or glob names for Python test function and
                        method discovery
  disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool):
                        Disable string escape non-ASCII characters, might
                        cause unwanted side effects(use at your own risk)
  strict_parametrization_ids (bool):
                        Emit an error if non-unique parameter set IDs are
                        detected
  console_output_style (string):
                        Console output: "classic", or with additional
                        progress information ("progress" (percentage) |
                        "count" | "progress-even-when-capture-no" (forces
                        progress even when capture=no)
  verbosity_test_cases (string):
                        Specify a verbosity level for test case execution,
                        overriding the main level. Higher levels will
                        provide more detailed information about each test
                        case executed.
  strict_xfail (bool):  Default for the strict parameter of xfail markers
                        when not given explicitly (default: False) (alias:
                        xfail_strict)
  tmp_path_retention_count (string):
                        How many sessions should we keep the `tmp_path`
                        directories, according to
                        `tmp_path_retention_policy`.
  tmp_path_retention_policy (string):
                        Controls which directories created by the `tmp_path`
                        fixture are kept around, based on test outcome.
                        (all/failed/none)
  enable_assertion_pass_hook (bool):
                        Enables the pytest_assertion_pass hook. Make sure to
                        delete any previously generated pyc cache files.
  truncation_limit_lines (string):
                        Set threshold of LINES after which truncation will
                        take effect
  truncation_limit_chars (string):
                        Set threshold of CHARS after which truncation will
                        take effect
  assertion_text_diff_style (string):
                        Choose how pytest renders diffs for string equality
                        assertions: ndiff or block
  verbosity_assertions (string):
                        Specify a verbosity level for assertions, overriding
                        the main level. Higher levels will provide more
                        detailed explanation when an assertion fails.
  junit_suite_name (string):
                        Test suite name for JUnit report
  junit_logging (string):
                        Write captured log messages to JUnit report: one of
                        no|log|system-out|system-err|out-err|all
  junit_log_passing_tests (bool):
                        Capture log information for passing tests to JUnit
                        report:
  junit_duration_report (string):
                        Duration time to report: one of total|call
  junit_family (string):
                        Emit XML for schema: one of legacy|xunit1|xunit2
  doctest_optionflags (args):
                        Option flags for doctests
  doctest_encoding (string):
                        Encoding used for doctest files
  cache_dir (string):   Cache directory path
  log_level (string):   Default value for --log-level
  log_format (string):  Default value for --log-format
  log_date_format (string):
                        Default value for --log-date-format
  log_cli (bool):       Enable log display during test run (also known as
                        "live logging")
  log_cli_level (string):
                        Default value for --log-cli-level
  log_cli_format (string):
                        Default value for --log-cli-format
  log_cli_date_format (string):
                        Default value for --log-cli-date-format
  log_file (string):    Default value for --log-file
  log_file_mode (string):
                        Default value for --log-file-mode
  log_file_level (string):
                        Default value for --log-file-level
  log_file_format (string):
                        Default value for --log-file-format
  log_file_date_format (string):
                        Default value for --log-file-date-format
  log_auto_indent (string):
                        Default value for --log-auto-indent
  faulthandler_timeout (string):
                        Dump the traceback of all threads if a test takes
                        more than TIMEOUT seconds to finish
  faulthandler_exit_on_timeout (bool):
                        Exit the test process if a test takes more than
                        faulthandler_timeout seconds to finish
  verbosity_subtests (string):
                        Specify verbosity level for subtests. Higher levels
                        will generate output for passed subtests. Failed
                        subtests are always reported.
  addopts (args):       Extra command line options
  minversion (string):  Minimally required pytest version
  pythonpath (paths):   Add paths to sys.path
  required_plugins (args):
                        Plugins that must be present for pytest to run

Environment variables:
  CI                       When set to a non-empty value, pytest knows it is running in a CI process and does not truncate summary info
  BUILD_NUMBER             Equivalent to CI
  PYTEST_ADDOPTS           Extra command line options
  PYTEST_PLUGINS           Comma-separated plugins to load during startup
  PYTEST_DISABLE_PLUGIN_AUTOLOAD Set to disable plugin auto-loading
  PYTEST_DEBUG             Set to enable debug tracing of pytest's internals
  PYTEST_DEBUG_TEMPROOT    Override the system temporary directory
  PYTEST_THEME             The Pygments style to use for code output
  PYTEST_THEME_MODE        Set the PYTEST_THEME to be either 'dark' or 'light'

to see available markers type: pytest --markers
to see available fixtures type: pytest --fixtures
(shown according to specified file_or_dir or current dir if not specified; fixtures with leading '_' are only shown with the '-v' option
```
