---
library: "pytest-cov"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://github.com/pytest-dev/pytest-cov"
role: "alternate"
rank: 1
fetched_at: "2026-08-17T19:28:29.366224+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "ca66047cc44aa2bfdaee0aaf09606974e1ca857c4c604c68d3ac50bbdd298066"
---

# Overview

|  |  |
| --- | --- |
| docs | [Documentation Status](https://readthedocs.org/projects/pytest-cov/) |
| tests | [GitHub Actions Status](https://github.com/pytest-dev/pytest-cov/actions) |
| package | [PyPI Package latest release](https://pypi.org/project/pytest-cov)   [conda-forge](https://anaconda.org/conda-forge/pytest-cov)   [PyPI Wheel](https://pypi.org/project/pytest-cov)   [Supported versions](https://pypi.org/project/pytest-cov)   [Supported implementations](https://pypi.org/project/pytest-cov)   [Commits since latest release](https://github.com/pytest-dev/pytest-cov/compare/v7.1.0...master) |

This plugin provides coverage functionality as a pytest plugin. Compared to just using `coverage run` this plugin does some extras:

* Automatic erasing and combination of .coverage files and default reporting.
* Support for detailed coverage contexts (add `--cov-context=test` to have the full test name including parametrization as the context).
* Xdist support: you can use all of pytest-xdist's features including remote interpreters and still get coverage.
* Consistent pytest behavior. If you run `coverage run -m pytest` you will have slightly different `sys.path` (CWD will be in it, unlike when running `pytest` ).

All features offered by the coverage package should work, either through pytest-cov's command line options or through coverage's config file.

* Free software: MIT license

## Installation

Install with pip:

```
pip install pytest-cov
```

For distributed testing support install pytest-xdist:

```
pip install pytest-xdist
```

### Upgrading from pytest-cov 6.3

pytest-cov 6.3 and older were using a `.pth` file to enable coverage measurements in subprocesses. This was removed in pytest-cov 7 - use [coverage's patch options](https://coverage.readthedocs.io/en/latest/config.html#run-patch) to enable subprocess measurements.

### Uninstalling

Uninstall with pip:

```
pip uninstall pytest-cov
```

Under certain scenarios a stray `.pth` file may be left around in site-packages.

* pytest-cov 2.0 may leave a `pytest-cov.pth` if you installed without wheels ( `easy_install` , `setup.py install` etc).
* pytest-cov 1.8 or older will leave a `init_cov_core.pth` .

## Usage

```
pytest --cov=myproj tests/
```

Would produce a report like:

```
-------------------- coverage: ... ---------------------
Name                 Stmts   Miss  Cover
----------------------------------------
myproj/__init__          2      0   100%
myproj/myproj          257     13    94%
myproj/feature4286      94      7    92%
----------------------------------------
TOTAL                  353     20    94%
```

## Documentation

<https://pytest-cov.readthedocs.io/en/latest/>

## Coverage Data File

The data file is erased at the beginning of testing to ensure clean data for each test run. If you need to combine the coverage of several test runs you can use the `--cov-append` option to append this coverage data to coverage data from previous test runs.

The data file is left at the end of testing so that it is possible to use normal coverage tools to examine it.

## Limitations

For distributed testing the workers must have the pytest-cov package installed. This is needed since the plugin must be registered through setuptools for pytest to start the plugin on the worker.

## Security

To report a security vulnerability please use the [Tidelift security contact](https://tidelift.com/security) . Tidelift will coordinate the fix and disclosure.

## Acknowledgements

Whilst this plugin has been built fresh from the ground up it has been influenced by the work done on pytest-coverage (Ross Lawley, James Mills, Holger Krekel) and nose-cover (Jason Pellerin) which are other coverage plugins.

Ned Batchelder for coverage and its ability to combine the coverage results of parallel runs.

Holger Krekel for pytest with its distributed testing support.

Jason Pellerin for nose.

Michael Foord for unittest2.

No doubt others have contributed to these tools as well.
