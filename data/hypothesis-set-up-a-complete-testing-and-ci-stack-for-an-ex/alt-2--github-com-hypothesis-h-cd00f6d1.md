---
library: "hypothesis"
query: "Set up a complete testing and CI stack for an existing FastAPI service. Use pytest with async fixtures, httpx's ASGI transport for endpoint tests without a live server, pytest-cov with an 80 percent gate, Hypothesis for property-based tests of the validation layer, and ruff for linting. Wire it into GitHub Actions running against a Postgres service container. Use testcontainers-python for the docker container management library."
url: "https://github.com/hypothesis/h"
role: "alternate"
rank: 2
fetched_at: "2026-08-17T19:28:29.809136+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "afef40d37fb564b78e37a18b0bb47e17e8c49445dde234a796a12d449b45aeca"
---

[!](https://github.com/hypothesis/h/actions/workflows/ci.yml?query=branch%3Amain)   [!](https://camo.githubusercontent.com/3f70317f71f6f58785658284668394e517d4e4559df88301085de5a851aa7547/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e31312d73756363657373)   [!](https://github.com/hypothesis/h/blob/main/LICENSE)   [!](https://github.com/hypothesis/cookiecutters/tree/main/pyramid-app)   [!](https://black.readthedocs.io/en/stable/)

# h

h is the web app that serves most of the <https://hypothes.is/> website, including the web annotations API at <https://hypothes.is/api/> . The [Hypothesis client](https://github.com/hypothesis/client) is a browser-based annotator that is a client for h's API.

## Community

Join us on Slack ( [request an invite](https://slack.hypothes.is) or [log in once you've created an account](https://hypothesis-open.slack.com/) ).

If you'd like to contribute to the project, you should also [subscribe](mailto:dev+subscribe@list.hypothes.is) to the [development mailing list](https://groups.google.com/a/list.hypothes.is/forum/#!forum/dev) and read our [Contributor's guide](https://h.readthedocs.io/en/latest/developing/) . Then consider getting started on one of the issues that are ready for work.

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/hypothesis/.github/blob/main/CODE_OF_CONDUCT.md) . By participating in this project you agree to abide by its terms.

## Setting up Your h Development Environment

First you'll need to install:

* [Git](https://git-scm.com/) . On Ubuntu: `sudo apt install git` , on macOS: `brew install git` .
* [GNU Make](https://www.gnu.org/software/make/) . This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv) . Follow the instructions in pyenv's README to install it. The **Homebrew** method works best on macOS. The **Basic GitHub Checkout** method works best on Ubuntu. You *don't* need to set up pyenv's shell integration ("shims"), you can [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims) .
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) . On Ubuntu follow [Install on Ubuntu](https://docs.docker.com/desktop/install/ubuntu/) . On macOS follow [Install on Mac](https://docs.docker.com/desktop/install/mac-install/) .
* [Node](https://nodejs.org/) and npm. On Ubuntu: `sudo snap install --classic node` . On macOS: `brew install node` .
* [Yarn](https://yarnpkg.com/) : `sudo npm install -g yarn` .

Then to set up your development environment:

```
git clone https://github.com/hypothesis/h.git
cd h
make services
make devdata
make help
```

See the [Contributor's guide](https://h.readthedocs.io/en/latest/developing/) for further instructions on setting up a development environment and contributing to h.

## Changing the Project's Python Version

To change what version of Python the project uses:

1. Change the Python version in the [cookiecutter.json](/hypothesis/h/blob/main/.cookiecutter/cookiecutter.json) file. For example:

   ```
   "python_version"
   "3.10.4"
   ```
2. Re-run the cookiecutter template:

   ```
   make template
   ```
3. Re-compile the `requirements/*.txt` files. This is necessary because the same `requirements/*.in` file can compile to different `requirements/*.txt` files in different versions of Python:

   ```
   make requirements
   ```
4. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

### To Add a New Dependency

Add the package to the appropriate  [`requirements/*.in`](/hypothesis/h/blob/main/requirements)  file(s) and then run:

```
make requirements
```

### To Remove a Dependency

Remove the package from the appropriate  [`requirements/*.in`](/hypothesis/h/blob/main/requirements)  file(s) and then run:

```
make requirements
```

### To Upgrade or Downgrade a Dependency

We rely on [Dependabot](https://github.com/dependabot) to keep all our dependencies up to date by sending automated pull requests to all our repos. But if you need to upgrade or downgrade a package manually you can do that locally.

To upgrade a package to the latest version in all `requirements/*.txt` files:

```
make requirements --always-make args='--upgrade-package <FOO>'
```

To upgrade or downgrade a package to a specific version:

```
make requirements --always-make args='--upgrade-package <FOO>==<X.Y.Z>'
```

To upgrade **all** packages to their latest versions:

```
make requirements --always-make args=--upgrade
```
