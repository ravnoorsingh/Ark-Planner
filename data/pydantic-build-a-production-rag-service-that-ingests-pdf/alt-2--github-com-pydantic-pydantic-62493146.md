---
library: "pydantic"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, LangChain for the retrieval chain and Pydantic models for request and response validation. Include streaming responses and health checks. Use pinecone-client for the vector database."
url: "https://github.com/pydantic/pydantic"
role: "alternate"
rank: 2
fetched_at: "2026-08-18T11:02:11.752862+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "1721d40b4ee89d6ac877e412a275082c0452bc9b68ceac87747ff4030a237e6d"
---

# Pydantic Validation

[![CI](https://camo.githubusercontent.com/58ba29aa31e5066829678f11af3b5f93f22036c73837c7c34b7449080e3be1fb/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f707964616e7469632f707964616e7469632f63692e796d6c3f6272616e63683d6d61696e266c6f676f3d676974687562266c6162656c3d4349)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)   [![Coverage](https://camo.githubusercontent.com/4fe07b3b8f6c7c9021cc0f7aac90f7a04d481089522e01f8ee14cf0340267ce6/68747470733a2f2f636f7665726167652d62616467652e73616d75656c636f6c76696e2e776f726b6572732e6465762f707964616e7469632f707964616e7469632e737667)](https://coverage-badge.samuelcolvin.workers.dev/redirect/pydantic/pydantic)   [![pypi](https://camo.githubusercontent.com/f7e0c0894a9675bf3cb0ec10ddd91c732772f55d0e23282f314d4781d7b29f95/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f707964616e7469632e737667)](https://pypi.python.org/pypi/pydantic)   [![CondaForge](https://camo.githubusercontent.com/e83b7c2ad6d216bb1017afa850bdc91dca52667aa112b53e07a6773145e2f45b/68747470733a2f2f696d672e736869656c64732e696f2f636f6e64612f762f636f6e64612d666f7267652f707964616e7469632e737667)](https://anaconda.org/conda-forge/pydantic)   [![downloads](https://camo.githubusercontent.com/c7ce52ac4a4829c87f1abd67bf7c9302ac1ad00290e769b5e2d2bf23fd9b6f30/68747470733a2f2f7374617469632e706570792e746563682f62616467652f707964616e7469632f6d6f6e7468)](https://pepy.tech/project/pydantic)   [![versions](https://camo.githubusercontent.com/e9aaa764d4a85c39c1a49776a64ff35fd1843afe658dfdf04a759f51f830690c/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f707964616e7469632e737667)](https://github.com/pydantic/pydantic)   [![license](https://camo.githubusercontent.com/9c365eca3dd5fc1e28fdea8b0232b7c75218a2e15034f478ab1477ff3f46e450/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f707964616e7469632f707964616e7469632e737667)](https://github.com/pydantic/pydantic/blob/main/LICENSE)   [![Pydantic v2](https://camo.githubusercontent.com/225cfe67be4e841d9763753ec947434ef7a9469f9723474322e3818d3272e333/68747470733a2f2f696d672e736869656c64732e696f2f656e64706f696e743f75726c3d68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f707964616e7469632f707964616e7469632f6d61696e2f646f63732f62616467652f76322e6a736f6e)](https://pydantic.dev/docs/validation/latest/get-started/contributing/#badges)   [![llms.txt](https://camo.githubusercontent.com/f445bf6af9faf49d4bd91302fb37d038e5e3fe059b7808106a48c2758aefb8a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6c6d732e7478742d677265656e)](https://pydantic.dev/docs/validation/latest/llms.txt)

Data validation using Python type hints.

Fast and extensible, Pydantic plays nicely with your linters/IDE/brain. Define how data should be in pure, canonical Python 3.10+; validate it with Pydantic.

## Pydantic Logfire 🔥

We've launched Pydantic Logfire to help you monitor your applications. [Learn more](https://pydantic.dev/logfire/?utm_source=pydantic_validation)

## Pydantic V1.10 vs. V2

Pydantic V2 is a ground-up rewrite that offers many new features, performance improvements, and some breaking changes compared to Pydantic V1.

If you're using Pydantic V1 you may want to look at the [pydantic V1.10 Documentation](https://pydantic.dev/docs/validation/1.10/overview/) or,  [`1.10.X-fixes` git branch](https://github.com/pydantic/pydantic/tree/1.10.X-fixes)  . Pydantic V2 also ships with the latest version of Pydantic V1 built in so that you can incrementally upgrade your code base and projects: `from pydantic import v1 as pydantic_v1` .

## Help

See [documentation](https://pydantic.dev/docs/validation/latest/get-started/) for more details.

## Installation

Install using `pip install -U pydantic` or `conda install pydantic -c conda-forge` . For more installation options to make Pydantic even faster, see the [Install](https://pydantic.dev/docs/validation/latest/get-started/install/) section in the documentation.

## A Simple Example

```
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: list[int] =
 []
external_data =
 {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}user = User(**
external_data)print(user)#> User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)#> 123
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to Pydantic, see [Contributing to Pydantic](https://pydantic.dev/docs/validation/latest/get-started/contributing/) .

## Reporting a Security Vulnerability

See our [security policy](https://github.com/pydantic/pydantic/security/policy) .
