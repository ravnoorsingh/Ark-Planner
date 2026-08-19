---
library: "pydantic"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, python-multipart for uploads, and Pydantic models for validation. Use weaviate-client for the vector database. Use sentence-transformers for the embedding library."
url: "https://pydantic.dev/docs/validation/latest/get-started/"
role: "primary"
rank: 0
fetched_at: "2026-08-19T19:23:45.239938+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "9668c668f58a508c3211c4a53c5d0c76a0d7c7eb52790f50310ead369cc77e43"
---

# Pydantic Validation

[![CI](https://img.shields.io/github/actions/workflow/status/pydantic/pydantic/ci.yml?branch=main&logo=github&label=CI)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)   [![Coverage](https://coverage-badge.samuelcolvin.workers.dev/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
  [![pypi](https://img.shields.io/pypi/v/pydantic.svg)](https://pypi.python.org/pypi/pydantic)   [![CondaForge](https://img.shields.io/conda/v/conda-forge/pydantic.svg)](https://anaconda.org/conda-forge/pydantic)   [![downloads](https://static.pepy.tech/badge/pydantic/month)](https://pepy.tech/project/pydantic)
  [![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)   [![llms.txt](https://img.shields.io/badge/llms.txt-green)](https://docs.pydantic.dev/latest/llms.txt)

Documentation for version: v2.13.4.

Pydantic is the most widely used data validation library for Python.

Fast and extensible, Pydantic plays nicely with your linters/IDE/brain. Define how data should be in pure, canonical Python 3.9+; validate it with Pydantic.

**Sign up for our newsletter, *The Pydantic Stack* , with updates & tutorials on Pydantic, Logfire, and Pydantic AI:**

## Why use Pydantic?

* **Powered by type hints** — with Pydantic, schema validation and serialization are controlled by type annotations; less to learn, less code to write, and integration with your IDE and static analysis tools. [Learn more…](/docs/validation/latest/get-started/why/#type-hints)
* **Speed** — Pydantic’s core validation logic is written in Rust. As a result, Pydantic is among the fastest data validation libraries for Python. [Learn more…](/docs/validation/latest/get-started/why/#performance)
* **JSON Schema** — Pydantic models can emit JSON Schema, allowing for easy integration with other tools. [Learn more…](/docs/validation/latest/get-started/why/#json-schema)
* **Strict** and **Lax** mode — Pydantic can run in either strict mode (where data is not converted) or lax mode where Pydantic tries to coerce data to the correct type where appropriate. [Learn more…](/docs/validation/latest/get-started/why/#strict-lax)
* **Dataclasses** , **TypedDicts** and more — Pydantic supports validation of many standard library types including `dataclass` and `TypedDict` . [Learn more…](/docs/validation/latest/get-started/why/#dataclasses-typeddict-more)
* **Customisation** — Pydantic allows custom validators and serializers to alter how data is processed in many powerful ways. [Learn more…](/docs/validation/latest/get-started/why/#customisation)
* **Ecosystem** — around 8,000 packages on PyPI use Pydantic, including massively popular libraries like *FastAPI* , *huggingface* , *Django Ninja* , *SQLModel* , & *LangChain* . [Learn more…](/docs/validation/latest/get-started/why/#ecosystem)
* **Battle tested** — Pydantic is downloaded over 550M times/month and is used by all FAANG companies and 20 of the 25 largest companies on NASDAQ. If you’re trying to do something with Pydantic, someone else has probably already done it. [Learn more…](/docs/validation/latest/get-started/why/#using-pydantic)

[Installing Pydantic](/docs/validation/latest/get-started/install/) is as simple as: `pip install pydantic`

## Pydantic examples

To see Pydantic at work, let’s start with a simple example, creating a custom class that inherits from `BaseModel` :

Validation Successful

```
from datetime import datetime

from pydantic import BaseModel, PositiveInt

class User(BaseModel):
  id: int
  name: str = 'John Doe'
  signup_ts: datetime | None
  tastes: dict[str, PositiveInt]

external_data = {
  'id': 123,
  'signup_ts': '2019-06-01 12:22',
  'tastes': {
      'wine': 9,
      b'cheese': 7,
      'cabbage': '1',
  },
}

user = User(**external_data)

print(user.id)
#> 123
print(user.model_dump())
"""
{
  'id': 123,
  'name': 'John Doe',
  'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
  'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
"""
```

`id` is of type `int` ; the annotation-only declaration tells Pydantic that this field is required. Strings, bytes, or floats will be coerced to integers if possible; otherwise an exception will be raised.

`name` is a string; because it has a default, it is not required.

`signup_ts` is a  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)  field that is required, but the value `None` may be provided; Pydantic will process either a [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) integer (e.g. `1496498400` ) or a string representing the date and time.

`tastes` is a dictionary with string keys and positive integer values. The `PositiveInt` type is shorthand for `Annotated[int, annotated_types.Gt(0)]` .

The input here is an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted datetime, but Pydantic will convert it to a  [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)  object.

The key here is `bytes` , but Pydantic will take care of coercing it to a string.

Similarly, Pydantic will coerce the string `'1'` to the integer `1` .

We create instance of `User` by passing our external data to `User` as keyword arguments.

We can access fields as attributes of the model.

We can convert the model to a dictionary with  [`model_dump()`](/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump)  .

If validation fails, Pydantic will raise an error with a breakdown of what was wrong:

Validation Error

```
# continuing the above example...

from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError

class User(BaseModel):
  id: int
  name: str = 'John Doe'
  signup_ts: datetime | None
  tastes: dict[str, PositiveInt]

external_data = {'id': 'not an int', 'tastes': {}}

try:
  User(**external_data)
except ValidationError as e:
  print(e.errors())
  """
  [
      {
          'type': 'int_parsing',
          'loc': ('id',),
          'msg': 'Input should be a valid integer, unable to parse string as an integer',
          'input': 'not an int',
          'url': 'https://errors.pydantic.dev/2/v/int_parsing',
      },
      {
          'type': 'missing',
          'loc': ('signup_ts',),
          'msg': 'Field required',
          'input': {'id': 'not an int', 'tastes': {}},
          'url': 'https://errors.pydantic.dev/2/v/missing',
      },
  ]
  """
```

The input data is wrong here — `id` is not a valid integer, and `signup_ts` is missing.

Trying to instantiate `User` will raise a  [`ValidationError`](/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError)  with a list of errors.

## Who is using Pydantic?

Hundreds of organisations and packages are using Pydantic. Some of the prominent companies and organizations around the world who are using Pydantic include:

[![Adobe](/docs/validation/logos/adobe_logo.png)](why/#org-adobe "Adobe")

[![Amazon and AWS](/docs/validation/logos/amazon_logo.png)](why/#org-amazon "Amazon and AWS")

[![Anthropic](/docs/validation/logos/anthropic_logo.png)](why/#org-anthropic "Anthropic")

[![Apple](/docs/validation/logos/apple_logo.png)](why/#org-apple "Apple")

[![ASML](/docs/validation/logos/asml_logo.png)](why/#org-asml "ASML")

[![AstraZeneca](/docs/validation/logos/astrazeneca_logo.png)](why/#org-astrazeneca "AstraZeneca")

[![Cisco Systems](/docs/validation/logos/cisco_logo.png)](why/#org-cisco "Cisco Systems")

[![Capital One](/docs/validation/logos/capital_one_logo.png)](why/#org-capital_one "Capital One")

[![Comcast](/docs/validation/logos/comcast_logo.png)](why/#org-comcast "Comcast")

[![Datadog](/docs/validation/logos/datadog_logo.png)](why/#org-datadog "Datadog")

[![Facebook](/docs/validation/logos/facebook_logo.png)](why/#org-facebook "Facebook")

[![GitHub](/docs/validation/logos/github_logo.png)](why/#org-github "GitHub")

[![Google](/docs/validation/logos/google_logo.png)](why/#org-google "Google")

[![HSBC](/docs/validation/logos/hsbc_logo.png)](why/#org-hsbc "HSBC")

[![IBM](/docs/validation/logos/ibm_logo.png)](why/#org-ibm "IBM")

[![Intel](/docs/validation/logos/intel_logo.png)](why/#org-intel "Intel")

[![Intuit](/docs/validation/logos/intuit_logo.png)](why/#org-intuit "Intuit")

[![Intergovernmental Panel on Climate Change](/docs/validation/logos/ipcc_logo.png)](why/#org-ipcc "Intergovernmental Panel on Climate Change")

[![JPMorgan](/docs/validation/logos/jpmorgan_logo.png)](why/#org-jpmorgan "JPMorgan")

[![Jupyter](/docs/validation/logos/jupyter_logo.png)](why/#org-jupyter "Jupyter")

[![Microsoft](/docs/validation/logos/microsoft_logo.png)](why/#org-microsoft "Microsoft")

[![Molecular Science Software Institute](/docs/validation/logos/molssi_logo.png)](why/#org-molssi "Molecular Science Software Institute")

[![NASA](/docs/validation/logos/nasa_logo.png)](why/#org-nasa "NASA")

[![Netflix](/docs/validation/logos/netflix_logo.png)](why/#org-netflix "Netflix")

[![NSA](/docs/validation/logos/nsa_logo.png)](why/#org-nsa "NSA")

[![NVIDIA](/docs/validation/logos/nvidia_logo.png)](why/#org-nvidia "NVIDIA")

[![OpenAI](/docs/validation/logos/openai_logo.png)](why/#org-openai "OpenAI")

[![Oracle](/docs/validation/logos/oracle_logo.png)](why/#org-oracle "Oracle")

[![Palantir](/docs/validation/logos/palantir_logo.png)](why/#org-palantir "Palantir")

[![Qualcomm](/docs/validation/logos/qualcomm_logo.png)](why/#org-qualcomm "Qualcomm")

[![Red Hat](/docs/validation/logos/redhat_logo.png)](why/#org-redhat "Red Hat")

[![Revolut](/docs/validation/logos/revolut_logo.png)](why/#org-revolut "Revolut")

[![Robusta](/docs/validation/logos/robusta_logo.png)](why/#org-robusta "Robusta")

[![Salesforce](/docs/validation/logos/salesforce_logo.png)](why/#org-salesforce "Salesforce")

[![Starbucks](/docs/validation/logos/starbucks_logo.png)](why/#org-starbucks "Starbucks")

[![Texas Instruments](/docs/validation/logos/ti_logo.png)](why/#org-ti "Texas Instruments")

[![Twilio](/docs/validation/logos/twilio_logo.png)](why/#org-twilio "Twilio")

[![Twitter](/docs/validation/logos/twitter_logo.png)](why/#org-twitter "Twitter")

[![UK Home Office](/docs/validation/logos/ukhomeoffice_logo.png)](why/#org-ukhomeoffice "UK Home Office")

For a more comprehensive list of open-source projects using Pydantic see the [list of dependents on github](https://github.com/pydantic/pydantic/network/dependents) , or you can find some awesome projects using Pydantic in [awesome-pydantic](https://github.com/Kludex/awesome-pydantic) .

Was this page helpful?Thanks for your feedback!
