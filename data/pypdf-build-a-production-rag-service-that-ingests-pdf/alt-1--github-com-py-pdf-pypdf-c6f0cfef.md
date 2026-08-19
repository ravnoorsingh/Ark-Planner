---
library: "pypdf"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://github.com/py-pdf/pypdf"
role: "alternate"
rank: 1
fetched_at: "2026-08-19T12:36:05.661603+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "05c19cbcb141817cab8109e181233cfc222293165db5ef63789ae85477d9f3bb"
---

[![PyPI version](https://camo.githubusercontent.com/47f25195a169225643b45fda81652abc89bcb80bddf194eeaa8c5ac61002fce0/68747470733a2f2f62616467652e667572792e696f2f70792f70797064662e737667)](https://badge.fury.io/py/pypdf)   [![Python Support](https://camo.githubusercontent.com/2f308a54f71ef2bdcb5d6bdb0419354643908e1fd9a2f912e731a01d1c45f1c3/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f70797064662e737667)](https://pypi.org/project/pypdf/)   [!](https://pypdf.readthedocs.io/en/stable/)   [![GitHub last commit](https://camo.githubusercontent.com/b3e4465fc8ed7a4ba6ca6441a46cd32dbcead588c5ba3c301292c358753e182e/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6173742d636f6d6d69742f70792d7064662f7079706466)](https://github.com/py-pdf/pypdf)   [![codecov](https://camo.githubusercontent.com/fe172d6b40e7ad7f24eefae5f5b79cbe1508fde00822672a376f705350608634/68747470733a2f2f636f6465636f762e696f2f67682f70792d7064662f70797064662f6272616e63682f6d61696e2f67726170682f62616467652e7376673f746f6b656e3d6964343263474e5a355a)](https://codecov.io/gh/py-pdf/pypdf)

# pypdf

pypdf is a free and open-source pure-python PDF library capable of splitting, [merging](https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html) , [cropping, and transforming](https://pypdf.readthedocs.io/en/stable/user/cropping-and-transforming.html) the pages of PDF files. It can also add custom data, viewing options, and [passwords](https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html) to PDF files. pypdf can [retrieve text](https://pypdf.readthedocs.io/en/stable/user/extract-text.html) and [metadata](https://pypdf.readthedocs.io/en/stable/user/metadata.html) from PDFs as well.

See [pdfly](https://github.com/py-pdf/pdfly) for a CLI application that uses pypdf to interact with PDFs.

## Installation

Install pypdf using pip:

```
pip install pypdf
```

For using pypdf with AES encryption or decryption, install extra dependencies:

```
pip install pypdf[crypto]
```

> **NOTE** : `pypdf` 3.1.0 and above include significant improvements compared to previous versions. Please refer to [the migration guide](https://pypdf.readthedocs.io/en/latest/user/migration-1-to-2.html) for more information.

## Usage

```
from pypdf import PdfReader

reader = PdfReader("example.pdf")number_of_pages = len(reader.pages)page = reader.pages[0]text = page.extract_text()
```

pypdf can do a lot more, e.g. splitting, merging, reading and creating annotations, decrypting and encrypting. Check out the [documentation](https://pypdf.readthedocs.io/en/stable/) for additional usage examples!

For questions and answers, visit [StackOverflow](https://stackoverflow.com/questions/tagged/pypdf) (tagged with [pypdf](https://stackoverflow.com/questions/tagged/pypdf) ).

## Contributions

Maintaining pypdf is a collaborative effort. You can support the project by writing documentation, helping to narrow down issues, and submitting code. See the [CONTRIBUTING.md](https://github.com/py-pdf/pypdf/blob/main/CONTRIBUTING.md) file for more information.

### Q&A

The experience pypdf users have covers the whole range from beginner to expert. You can contribute to the pypdf community by answering questions on [StackOverflow](https://stackoverflow.com/questions/tagged/pypdf) , helping in [discussions](https://github.com/py-pdf/pypdf/discussions) , and asking users who report issues for [MCVE](https://stackoverflow.com/help/minimal-reproducible-example) 's (Code + example PDF!).

### Issues

A good bug ticket includes a MCVE - a minimal complete verifiable example. For pypdf, this means that you must upload a PDF that causes the bug to occur as well as the code you're executing with all of the output. Use `print(pypdf.__version__)` to tell us which version you're using.

### Code

All code contributions are welcome, but smaller ones have a better chance to get included in a timely manner. Adding unit tests for new features or test cases for bugs you've fixed help us to ensure that the Pull Request (PR) is fine.

pypdf includes a test suite which can be executed with `pytest` :

```
$ pytest
===================== test
 session starts =====================
platform linux -- Python 3.6.15, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/moose/GitHub/Martin/pypdf
plugins: cov-3.0.0
collected 233 items

tests/test_basic_features.py ..                         [  0%]
tests/test_constants.py .
                               [  1%]
tests/test_filters.py .................x.....           [ 11%]
tests/test_generic.py ................................. [ 25%]
.............                                           [ 30%]
tests/test_javascript.py ..                             [ 31%]
tests/test_merger.py .
                                  [ 32%]
tests/test_page.py .........................            [ 42%]
tests/test_pagerange.py ................                [ 49%]
tests/test_papersizes.py ..................             [ 57%]
tests/test_reader.py .................................. [ 72%]
...............                                         [ 78%]
tests/test_utils.py ....................                [ 87%]
tests/test_workflows.py ..........                      [ 91%]
tests/test_writer.py .................                  [ 98%]
tests/test_xmp.py ...                                   [100%]

========== 232 passed, 1 xfailed, 1 warning in
 4.52s ==========
```
