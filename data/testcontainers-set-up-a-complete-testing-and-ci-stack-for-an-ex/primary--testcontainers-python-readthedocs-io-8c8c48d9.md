---
library: "testcontainers"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://testcontainers-python.readthedocs.io"
resolved_url: "https://testcontainers-python.readthedocs.io/en/latest/"
role: "primary"
rank: 0
fetched_at: "2026-08-17T19:28:30.412046+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "72b57f586cfdc80e5557dda9700fc99bfb7a5244c45430b89454db519096ce3e"
---

# testcontainers-python

 [![https://github.com/testcontainers/testcontainers-python/actions/workflows/ci-core.yml/badge.svg](https://github.com/testcontainers/testcontainers-python/actions/workflows/ci-core.yml/badge.svg)](https://github.com/testcontainers/testcontainers-python/actions/workflows/ci-core.yml)   [![https://img.shields.io/pypi/v/testcontainers.svg](https://img.shields.io/pypi/v/testcontainers.svg)](https://pypi.python.org/pypi/testcontainers)   [![https://readthedocs.org/projects/testcontainers-python/badge/?version=latest](https://readthedocs.org/projects/testcontainers-python/badge/?version=latest)](http://testcontainers-python.readthedocs.io/en/latest/?badge=latest)   [![https://github.com/codespaces/badge.svg](https://github.com/codespaces/badge.svg)](https://codespaces.new/testcontainers/testcontainers-python)

testcontainers-python facilitates the use of Docker containers for functional and integration testing. The collection of packages currently supports the following features.

## Getting Started

```
>>> from testcontainers.postgres import PostgresContainer>>> import sqlalchemy

>>> with PostgresContainer("postgres:16") as postgres:...     psql_url = postgres.get_connection_url()...     engine = sqlalchemy.create_engine(psql_url)...     with engine.begin() as connection:...         version, = connection.execute(sqlalchemy.text("SELECT version()")).fetchone()>>> version'PostgreSQL 16...'
```

The snippet above will spin up the current latest version of a postgres database in a container. The `get_connection_url()` convenience method returns a `sqlalchemy` compatible url (using the `psycopg2` driver per default) to connect to the database and retrieve the database version.

```
>>> from testcontainers.postgres import PostgresContainer>>> import psycopg

>>> with PostgresContainer("postgres:16", driver=None) as postgres:...     psql_url = postgres.get_connection_url()...     with psycopg.connect(psql_url) as connection:...         with connection.cursor() as cursor:...             version, = cursor.execute("SELECT version()").fetchone()>>> version'PostgreSQL 16...'
```

This snippet does the same, however using a specific version and the driver is set to None, to influence the `get_connection_url()` convenience method to not include a driver in the URL (e.g. for compatibility with `psycopg` v3).

Note, that the `sqlalchemy` and `psycopg` packages are no longer a dependency of `testcontainers[postgres]` and not needed to launch the Postgres container. Your project therefore needs to declare a dependency on the used driver and db access methods you use in your code.

By default, Testcontainers will search for the container via the gateway IP. You can manually specify your own IP with the environment variable TESTCONTAINERS\_HOST\_OVERRIDE .

## Installation

The suite of testcontainers packages is available on [PyPI](https://pypi.org/project/testcontainers/) , the package can be installed using `pip` .

Version 4.0.0 onwards we do not support the testcontainers-\* packages as it is unsustainable to maintain ownership.

Instead packages can be installed by specifying [extras](https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies) , e.g., `pip install testcontainers[postgres]` .

Please note, that community modules are supported on a best-effort basis and breaking changes DO NOT create major versions in the package. Therefore, only the package core is strictly following SemVer. If your workflow is broken by a minor update, please look at the changelogs for guidance.

## Custom Containers

Crafting containers that are based on custom images is supported by the core module. Please check the [core documentation](core/README.html) for more information.

This allows you to create containers from images that are not part of the modules provided by testcontainers-python.

For common use cases, you can also use the generic containers provided by the testcontainers-generic module. Please check the [generic documentation](modules/generic/README.html) for more information. (example: ServerContainer for running a FastAPI server)

## Docker in Docker (DinD)

When trying to launch Testcontainers from within a Docker container, e.g., in continuous integration testing, two things have to be provided:

1. The container has to provide a docker client installation. Either use an image that has docker pre-installed (e.g. the [official docker images](https://hub.docker.com/_/docker) ) or install the client from within the Dockerfile specification.
2. The container has to have access to the docker daemon which can be achieved by mounting /var/run/docker.sock or setting the DOCKER\_HOST environment variable as part of your docker run command.

## Private Docker registry

Using a private docker registry requires the DOCKER\_AUTH\_CONFIG environment variable to be set. [official documentation](https://docs.docker.com/engine/reference/commandline/login/#credential-helpers)

The value of this variable should be a JSON string containing the authentication information for the registry.

Example:

```
DOCKER_AUTH_CONFIG='{"auths": {"https://myregistry.com": {"auth": "dXNlcm5hbWU6cGFzc3dvcmQ="}}}'
```

In order to generate the JSON string, you can use the following command:

```
echo -n '{"auths": {"<url>": {"auth": "'$(echo -n "<username>:<password>" | base64 -w 0)'"}}}'
```

Fetching passwords from cloud providers:

```
ECR_PASSWORD = $(aws ecr get-login-password --region eu-west-1)GCP_PASSWORD = $(gcloud auth print-access-token)AZURE_PASSWORD = $(az acr login --name  --expose-token --output tsv)
```

## Configuration

| Env Variable | Example | Description |
| --- | --- | --- |
| `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` | `/var/run/docker.sock` | Path to Docker’s socket used by ryuk |
| `TESTCONTAINERS_RYUK_PRIVILEGED` | `false` | Run ryuk as a privileged container |
| `TESTCONTAINERS_RYUK_DISABLED` | `false` | Disable ryuk |
| `RYUK_CONTAINER_IMAGE` | `testcontainers/ryuk:0.8.1` | Custom image for ryuk |
| `DOCKER_AUTH_CONFIG` | `{"auths": {"<url>": {"auth": "<encoded>"}}}` | Custom registry auth config |

## Development and Contributing

We recommend you use a [Poetry](https://python-poetry.org/docs/) for development. After having installed poetry , you can run the following snippet to set up your local dev environment.

```
make install
```

### Package Structure

Testcontainers is a collection of [implicit namespace packages](https://peps.python.org/pep-0420/) to decouple the development of different extensions, e.g., `testcontainers[mysql]` and `testcontainers[postgres]` for MySQL and PostgreSQL database containers, respectively.

The folder structure is as follows:

```
modules# One folder per feature.[feature name]    # Folder without __init__.py for implicit namespace packages.    testcontainers        # Implementation as namespace package with __init__.py.        [feature name]            __init__.py            # Other files for this            ...    # Tests for the feature.    tests        test_[some_aspect_for_the_feature].py        ...    # README for this feature.    README.rst
```

### Contributing a New Feature

You want to contribute a new feature or container? Great! - We recommend you first [open an issue](https://github.com/testcontainers/testcontainers-python/issues/new/choose) - Then follow the suggestions from the team - We also have a Pull Request [template](https://github.com/testcontainers/testcontainers-python/blob/main/.github/PULL_REQUEST_TEMPLATE/new_container.md) for new containers!
