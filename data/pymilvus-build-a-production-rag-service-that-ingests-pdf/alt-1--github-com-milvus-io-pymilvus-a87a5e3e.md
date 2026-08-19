---
library: "pymilvus"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://github.com/milvus-io/pymilvus"
role: "alternate"
rank: 1
fetched_at: "2026-08-19T12:36:05.378738+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "caf55975ac9ccab2deefd14fa2429234416f09db21438887d3866166de90d019"
---

# Milvus Python SDK

[![version](https://camo.githubusercontent.com/50e51b83c19acd2a1c2d137eb2676b78da613912ec6d250b4821837e7ce4a4ab/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f70796d696c7675732e7376673f636f6c6f723d626c7565)](https://pypi.org/project/pymilvus/)   [![Supported Python Versions](https://camo.githubusercontent.com/81f7f232bcfe976c67dc8e1d76ecb1f446005575fcce11547a093c119dd1dd6b/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f70796d696c7675733f6c6f676f3d707974686f6e266c6f676f436f6c6f723d626c7565)](https://pypi.org/project/pymilvus/)   [![Downloads](https://camo.githubusercontent.com/87c9359552a47c077e7db054433cee9e1d8c731431ae4dc2ce75a6621985ab1c/68747470733a2f2f7374617469632e706570792e746563682f62616467652f70796d696c767573)](https://pepy.tech/project/pymilvus)   [![Downloads](https://camo.githubusercontent.com/620eab7d3ddc2a0771bdcdb0dc1d6c4b47577731d45b1055935d3cf0c58868c8/68747470733a2f2f7374617469632e706570792e746563682f62616467652f70796d696c7675732f6d6f6e7468)](https://pepy.tech/project/pymilvus)   [![Downloads](https://camo.githubusercontent.com/fc37a9d0c1ca43aac25b4e6bf85f39947904b0bdd6c885ea27522ac502808a45/68747470733a2f2f7374617469632e706570792e746563682f62616467652f70796d696c7675732f7765656b)](https://pepy.tech/project/pymilvus)

[![license](https://camo.githubusercontent.com/ac780891a4128fd8bc0efa0f5644c66327cbaf4bb2d06e057ddb362df03988e7/68747470733a2f2f696d672e736869656c64732e696f2f686578706d2f6c2f706c75672e7376673f636f6c6f723d677265656e)](https://github.com/milvus-io/pymilvus/blob/master/LICENSE)   [![Static Badge](https://camo.githubusercontent.com/969b1f65dacaf068381270b5a0b2f3696228d7d0dd7cc6de43fa9d0c1937bcf4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f736c61636b2d25323370792d2d6d696c7675732d626c75653f7374796c653d736f6369616c266c6f676f3d736c61636b266c696e6b3d68747470732533412532462532466d696c767573696f2e736c61636b2e636f6d2532466172636869766573253246433032345854574d54344c)](https://camo.githubusercontent.com/969b1f65dacaf068381270b5a0b2f3696228d7d0dd7cc6de43fa9d0c1937bcf4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f736c61636b2d25323370792d2d6d696c7675732d626c75653f7374796c653d736f6369616c266c6f676f3d736c61636b266c696e6b3d68747470732533412532462532466d696c767573696f2e736c61636b2e636f6d2532466172636869766573253246433032345854574d54344c)

Python SDK for [Milvus](https://github.com/milvus-io/milvus) . To contribute code to this project, please read our [contribution guidelines](https://github.com/milvus-io/milvus/blob/master/CONTRIBUTING.md) first. If you have some ideas or encounter a problem, you can find us in the Slack channel [#py-milvus](https://milvusio.slack.com/archives/C024XTWMT4L) .

## Compatibility

The following collection shows Milvus versions and recommended PyMilvus versions:

| Milvus version | Recommended PyMilvus version |
| --- | --- |
| 1.0.\* | 1.0.1 |
| 1.1.\* | 1.1.2 |
| 2.0.\* | 2.0.2 |
| 2.1.\* | 2.1.3 |
| 2.2.\* | 2.2.15 |
| 2.3.\* | 2.3.7 |
| 2.4.\* | 2.4.X |
| 2.5.\* | 2.5.X |
| 2.6.\* | 2.6.X |
| 3.0.\* | 3.0.X |

## Installation

You can install PyMilvus via `pip` or `pip3` for Python 3.9+:

```
# for milvus-model
# for bulk_writer
```

You can install a specific version of PyMilvus by:

```
$ pip3 install pymilvus==2.4.10
```

You can upgrade PyMilvus to the latest version by:

```
$ pip3 install --upgrade pymilvus
```

## FAQ

Local development commands use [uv](https://docs.astral.sh/uv/) . Install uv before running the `make` targets below.

Q1. How to get submodules?

A1. The following command will get the protos matching to the generated files, for protos of certain version, see [milvus-proto](https://github.com/milvus-io/milvus-proto#usage) for details.

```
$ git submodule update --init
```

Q2. How to generate python files from milvus-proto?

A2.

```
$ make gen_proto
```

Q3. How to use the local PyMilvus repository for Milvus server?

A3.

```
$ make install
```

Q4. How to check and auto-fix the coding styles?

A4.

```
make lint
make format
```

Q5. How to set up pre-commit hooks to automatically check and fix the coding styles?

Once installed, the hooks will automatically run `make format` and `make lint` before each commit. If the checks fail, the commit will be aborted, and you'll need to fix the issues before committing again.

A5. Pre-commit hooks help ensure code quality by automatically running linting and formatting checks before each commit.

```
# Install pre-commit (if not already installed)
# Install the git hook scripts
```

Q7. How to run the maintained test suites?

A7

```
$ uv sync --group dev
$ make unittest
$ make integration-lite
```

Q8. `zsh: no matches found: pymilvus[model]` , how do I solve this?

A8

```
"pymilvus[model]"
```

## Documentation

Documentation is available online: <https://milvus.io/api-reference/pymilvus/v2.6.x/About.md>

## Developing package releases

The commits on the development branch of each version will be packaged and uploaded to [Test PyPI](https://test.pypi.org/) .

The package name generated by the development branch is x.y.z.rc, where is the number of commits that differ from the most recent release.

* For example, after the release of **2.3.4** , two commits were submitted on the 2.3 branch. The version number of the latest commit of 2.3 branch is **2.3.5.rc2** .
* For example, after the release of **2.3.4** , 10 commits were submitted on the master branch. The version number of the latest commit of master branch is **2.4.0.rc10** .

To install the package on Test PyPi, you need to append `--extra-index-url` after pip, for example:

```
$ python3 -m pip install --extra-index-url https://test.pypi.org/simple/ pymilvus==2.1.0.dev66
```

## License

[Apache License 2.0](/milvus-io/pymilvus/blob/master/LICENSE)
