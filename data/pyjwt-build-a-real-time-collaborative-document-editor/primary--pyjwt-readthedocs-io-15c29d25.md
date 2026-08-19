---
library: "pyjwt"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://pyjwt.readthedocs.io/"
resolved_url: "https://pyjwt.readthedocs.io/en/stable/"
role: "primary"
rank: 0
fetched_at: "2026-08-18T14:21:14.505045+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "aaee8ecb1caf590dc9ce4824dc9eea66f3fca1d8d4465e7a91050c744f512100"
---

# Welcome to `PyJWT`

`PyJWT` is a Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard ( [RFC 7519](https://tools.ietf.org/html/rfc7519) ) for representing claims securely between two parties.

## Sponsor

|  |  |  |
| --- | --- | --- |
| [auth0-logo](https://github.com/user-attachments/assets/ee98379e-ee76-4bcb-943a-e25c4ea6d174) | If you want to quickly add secure token-based authentication to Python projects, feel free to check Auth0’s Python SDK and free plan at [auth0.com/signup](https://auth0.com/signup?utm_source=external_sites&utm_medium=pyjwt&utm_campaign=devn_signup) . | |

## Installation

You can install `pyjwt` with `pip` :

```
$ pip install pyjwt
```

See  [Installation](installation.html)  for more information.

## Example Usage

```
>>> import jwt>>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")>>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]){'some': 'payload'}
```

See  [Usage Examples](usage.html)  for more examples.

## Index

* [Installation](installation.html)
  + [Cryptographic Dependencies (Optional)](installation.html#cryptographic-dependencies-optional)
* [Usage Examples](usage.html)
  + [Encoding & Decoding Tokens with HS256](usage.html#encoding-decoding-tokens-with-hs256)
  + [Encoding & Decoding Tokens with RS256 (RSA)](usage.html#encoding-decoding-tokens-with-rs256-rsa)
  + [Encoding & Decoding Tokens with PS256 (RSA)](usage.html#encoding-decoding-tokens-with-ps256-rsa)
  + [Encoding & Decoding Tokens with EdDSA (Ed25519)](usage.html#encoding-decoding-tokens-with-eddsa-ed25519)
  + [Encoding & Decoding Tokens with ES256 (ECDSA)](usage.html#encoding-decoding-tokens-with-es256-ecdsa)
  + [Specifying Additional Headers](usage.html#specifying-additional-headers)
  + [Reading the Claimset without Validation](usage.html#reading-the-claimset-without-validation)
  + [Reading Headers without Validation](usage.html#reading-headers-without-validation)
  + [Registered Claim Names](usage.html#registered-claim-names)
  + [Key Length Validation](usage.html#key-length-validation)
  + [Requiring Presence of Claims](usage.html#requiring-presence-of-claims)
  + [Retrieve RSA signing keys from a JWKS endpoint](usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint)
  + [OIDC Login Flow](usage.html#oidc-login-flow)
* [Frequently Asked Questions](faq.html)
  + [How can I extract a public / private key from a x509 certificate?](faq.html#how-can-i-extract-a-public-private-key-from-a-x509-certificate)
* [Digital Signature Algorithms](algorithms.html)
  + [Minimum Key Length Requirements](algorithms.html#minimum-key-length-requirements)
  + [Asymmetric (Public-key) Algorithms](algorithms.html#asymmetric-public-key-algorithms)
  + [Specifying an Algorithm](algorithms.html#specifying-an-algorithm)
* [API Reference](api.html)
  + [`encode()`](api.html#jwt.encode)
  + [`decode()`](api.html#jwt.decode)
  + [`decode_complete()`](api.html#jwt.decode_complete)
  + [`PyJWT`](api.html#jwt.PyJWT)
  + [`PyJWK`](api.html#jwt.PyJWK)
  + [`PyJWKSet`](api.html#jwt.PyJWKSet)
  + [`PyJWKClient`](api.html#jwt.PyJWKClient)
  + [`PyJWS`](api.html#jwt.api_jws.PyJWS)
  + [Algorithms](api.html#module-jwt.algorithms)
  + [Types](api.html#module-jwt.types)
  + [Warnings](api.html#module-jwt.warnings)
  + [Exceptions](api.html#module-jwt.exceptions)
* [Changelog](changelog.html)
  + [Unreleased](changelog.html#unreleased)
  + [v2.13.0](changelog.html#v2-13-0)
  + [v2.12.1](changelog.html#v2-12-1)
  + [v2.12.0](changelog.html#v2-12-0)
  + [v2.11.0](changelog.html#v2-11-0)
  + [v2.10.1](changelog.html#v2-10-1)
  + [v2.10.0](changelog.html#v2-10-0)
  + [v2.9.0](changelog.html#v2-9-0)
  + [v2.8.0](changelog.html#v2-8-0)
  + [v2.7.0](changelog.html#v2-7-0)
  + [v2.6.0](changelog.html#v2-6-0)
  + [v2.5.0](changelog.html#v2-5-0)
  + [v2.4.0](changelog.html#v2-4-0)
  + [v2.3.0](changelog.html#v2-3-0)
  + [v2.2.0](changelog.html#v2-2-0)
  + [v2.1.0](changelog.html#v2-1-0)
  + [v2.0.1](changelog.html#v2-0-1)
  + [v2.0.0](changelog.html#v2-0-0)
  + [v1.7.1](changelog.html#v1-7-1)
  + [v1.7.0](changelog.html#v1-7-0)
  + [v1.6.4](changelog.html#v1-6-4)
  + [v1.6.3](changelog.html#v1-6-3)
  + [v1.6.1](changelog.html#v1-6-1)
  + [v1.6.0](changelog.html#v1-6-0)
  + [v1.5.3](changelog.html#v1-5-3)
  + [v1.5.2](changelog.html#v1-5-2)
  + [v1.5.1](changelog.html#v1-5-1)
  + [v1.5.0](changelog.html#v1-5-0)
  + [v1.4.2](changelog.html#v1-4-2)
  + [v1.4.1](changelog.html#v1-4-1)
  + [v1.4](changelog.html#v1-4)
  + [v1.3](changelog.html#v1-3)
  + [v1.2.0](changelog.html#v1-2-0)
  + [v1.1.0](changelog.html#v1-1-0)
  + [v1.0.1](changelog.html#v1-0-1)
  + [v1.0.0](changelog.html#v1-0-0)
