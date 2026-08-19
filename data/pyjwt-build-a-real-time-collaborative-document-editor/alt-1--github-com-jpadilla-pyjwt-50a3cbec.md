---
library: "pyjwt"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://github.com/jpadilla/pyjwt"
role: "alternate"
rank: 1
fetched_at: "2026-08-18T14:21:14.600136+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "061f360c5f91b80198dab394d451ee7323390f0d657a829a0be42080d6b22aa9"
---

# PyJWT

 [!](https://github.com/jpadilla/pyjwt/actions?query=workflow%3ACI)   [!](https://pypi.python.org/pypi/pyjwt)   [!](https://codecov.io/gh/jpadilla/pyjwt)   [![https://readthedocs.org/projects/pyjwt/badge/?version=stable](https://camo.githubusercontent.com/7a299e81eceb79f8efda574a89829acdba0f43b37581251d92d7f1db309586ed/68747470733a2f2f72656164746865646f63732e6f72672f70726f6a656374732f70796a77742f62616467652f3f76657273696f6e3d737461626c65)](https://pyjwt.readthedocs.io/en/stable/)

A Python implementation of [RFC 7519](https://tools.ietf.org/html/rfc7519) . Original implementation was written by [@progrium](https://github.com/progrium) .

## Sponsor

|  |  |  |
| --- | --- | --- |
| [auth0-logo](https://private-user-images.githubusercontent.com/83319/381137879-ee98379e-ee76-4bcb-943a-e25c4ea6d174.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODcwNjMwODQsIm5iZiI6MTc4NzA2Mjc4NCwicGF0aCI6Ii84MzMxOS8zODExMzc4NzktZWU5ODM3OWUtZWU3Ni00YmNiLTk0M2EtZTI1YzRlYTZkMTc0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA4MTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwODE4VDE0MTk0NFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTcxNmU3MjUyYzVjZTQ4ZTY2ZDA5MjVlYzliYTJkNzRlZTY5ZWE5M2VhNDE5Y2U3MGVmZGU4N2ZkMTdiYWJkNjYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.KwdwaXSae0WtNN_zlG3SSCv76DZKrDXNCFe6KoufEjU) | If you want to quickly add secure token-based authentication to Python projects, feel free to check Auth0's Python SDK and free plan at [auth0.com/signup](https://auth0.com/signup?utm_source=external_sites&utm_medium=pyjwt&utm_campaign=devn_signup) . | |

## Installing

Install with **pip** :

```
$ pip install PyJWT
```

## Usage

```
>>> import
 jwt
>>> encoded =
 jwt.encode({
"some"
:
"payload"
},
"secret"
, algorithm
=

"HS256"
)
>>> print(encoded)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
>>> jwt.decode(encoded,
"secret"
, algorithms
=[
"HS256"
])
{'some': 'payload'}
```

## Documentation

View the full docs online at <https://pyjwt.readthedocs.io/en/stable/>

## Tests

You can run tests from the project root after cloning with:

```
$ tox
```
