---
library: "pytest-cov"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://pytest-cov.readthedocs.io"
resolved_url: "https://pytest-cov.readthedocs.io/en/latest/"
role: "primary"
rank: 0
fetched_at: "2026-08-17T19:28:29.263429+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "78750b833cffe44c180bb8fe4a3b8294c4b3ca26710057c5f90a6b5cbb4605c4"
---

# Welcome to pytest-cov’s documentation!

Contents:

* [Overview](readme.html)
  + [Installation](readme.html#installation)
  + [Usage](readme.html#usage)
  + [Documentation](readme.html#documentation)
  + [Coverage Data File](readme.html#coverage-data-file)
  + [Limitations](readme.html#limitations)
  + [Security](readme.html#security)
  + [Acknowledgements](readme.html#acknowledgements)
* [Configuration](config.html)
  + [Caveats](config.html#caveats)
* [Reporting](reporting.html)
* [Debuggers and PyCharm](debuggers.html)
* [Distributed testing (xdist)](xdist.html)
  + [“load” mode](xdist.html#load-mode)
  + [“each” mode](xdist.html#each-mode)
* [Subprocess support](subprocess-support.html)
* [Contexts](contexts.html)
* [Tox](tox.html)
* [Plugin coverage](plugins.html)
* [Markers and fixtures](markers-fixtures.html)
  + [Markers](markers-fixtures.html#markers)
  + [Fixtures](markers-fixtures.html#fixtures)
* [Changelog](changelog.html)
  + [7.1.0 (2026-03-21)](changelog.html#id1)
  + [7.0.0 (2025-09-09)](changelog.html#id7)
  + [6.3.0 (2025-09-06)](changelog.html#id11)
  + [6.2.1 (2025-06-12)](changelog.html#id15)
  + [6.2.0 (2025-06-11)](changelog.html#id16)
  + [6.1.1 (2025-04-05)](changelog.html#id17)
  + [6.1.0 (2025-04-01)](changelog.html#id18)
  + [6.0.0 (2024-10-29)](changelog.html#id21)
  + [5.0.0 (2024-03-24)](changelog.html#id22)
  + [4.1.0 (2023-05-24)](changelog.html#id30)
  + [4.0.0 (2022-09-28)](changelog.html#id36)
  + [3.0.0 (2021-10-04)](changelog.html#id45)
  + [2.12.1 (2021-06-01)](changelog.html#id54)
  + [2.12.0 (2021-05-14)](changelog.html#id57)
  + [2.11.1 (2021-01-20)](changelog.html#id61)
  + [2.11.0 (2021-01-18)](changelog.html#id63)
  + [2.10.1 (2020-08-14)](changelog.html#id69)
  + [2.10.0 (2020-06-12)](changelog.html#id71)
  + [2.9.0 (2020-05-22)](changelog.html#id72)
  + [2.8.1 (2019-10-05)](changelog.html#id81)
  + [2.8.0 (2019-10-04)](changelog.html#id83)
  + [2.7.1 (2019-05-03)](changelog.html#id102)
  + [2.7.0 (2019-05-03)](changelog.html#id103)
  + [2.6.1 (2019-01-07)](changelog.html#id113)
  + [2.6.0 (2018-09-03)](changelog.html#id120)
  + [2.5.1 (2017-05-11)](changelog.html#id129)
  + [2.5.0 (2017-05-09)](changelog.html#id133)
  + [2.4.0 (2016-10-10)](changelog.html#id137)
  + [2.3.1 (2016-08-07)](changelog.html#id139)
  + [2.3.0 (2016-07-05)](changelog.html#id141)
  + [2.2.1 (2016-01-30)](changelog.html#id142)
  + [2.2.0 (2015-10-04)](changelog.html#id143)
  + [2.1.0 (2015-08-23)](changelog.html#id144)
  + [2.0.0 (2015-07-28)](changelog.html#id145)
  + [1.8.2 (2014-11-06)](changelog.html#id146)
* [Authors](authors.html)
* [Releasing](releasing.html)
* [Contributing](contributing.html)
  + [Bug reports](contributing.html#bug-reports)
  + [Documentation improvements](contributing.html#documentation-improvements)
  + [Feature requests and feedback](contributing.html#feature-requests-and-feedback)
  + [Development](contributing.html#development)

# Indices and tables

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)
