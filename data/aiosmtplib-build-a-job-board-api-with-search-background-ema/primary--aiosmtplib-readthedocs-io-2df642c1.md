---
library: "aiosmtplib"
query: "Build a job board API with search, background email digests and a vector database for semantic matching. Use qdrant-client for the vector database. Use elasticsearch for the search. Use celery for the task queue."
url: "https://aiosmtplib.readthedocs.io/"
resolved_url: "https://aiosmtplib.readthedocs.io/en/latest/"
role: "primary"
rank: 0
fetched_at: "2026-08-20T18:31:23.698841+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "8af25c8c13d30d177e97d751c79fa12f69f061bb36195219f5a180b6168cfea8"
---

# aiosmtplib

aiosmtplib is an asynchronous SMTP client for use with  [`asyncio`](https://docs.python.org/3.10/library/asyncio.html#module-asyncio "(in Python v3.10)")  . It is an async version of the  [`smtplib`](https://docs.python.org/3.10/library/smtplib.html#module-smtplib "(in Python v3.10)")  module, with similar APIs.

## Table of Contents

* [Getting Started](quickstart.html)
  + [Requirements](quickstart.html#requirements)
  + [Quickstart](quickstart.html#quickstart)
* [The send Coroutine](usage.html)
  + [Sending Messages](usage.html#sending-messages)
  + [Multipart Messages](usage.html#multipart-messages)
  + [Sending Raw Messages](usage.html#sending-raw-messages)
  + [Connecting Over TLS/SSL](usage.html#connecting-over-tls-ssl)
  + [Authentication](usage.html#authentication)
* [The SMTP Client Class](client.html)
  + [Connecting to an SMTP Server](client.html#connecting-to-an-smtp-server)
  + [Sending Messages](client.html#sending-messages)
  + [Parallel Execution](client.html#parallel-execution)
* [TLS, SSL & STARTTLS](encryption.html)
* [OAuth2 Authentication (XOAUTH2)](oauth.html)
  + [Basic Structure](oauth.html#basic-structure)
  + [Token Expiry and Refresh](oauth.html#token-expiry-and-refresh)
  + [Gmail Example](oauth.html#gmail-example)
  + [Outlook / Microsoft 365 Example](oauth.html#outlook-microsoft-365-example)
* [Timeouts](timeouts.html)
* [Proxy Support](proxies.html)
  + [SOCKS Proxies](proxies.html#socks-proxies)
* [Trio Support](trio.html)
* [API Reference](reference.html)
  + [The send Coroutine](reference.html#the-send-coroutine)
  + [The SMTP Class](reference.html#the-smtp-class)
  + [Server Responses](reference.html#server-responses)
  + [Status Codes](reference.html#status-codes)
  + [Exceptions](reference.html#module-aiosmtplib.errors)
* [Bug Reporting](bug-reporting.html)

## Release History

* [Changelog](changelog.html)
  + [5.1.3 (unreleased)](changelog.html#unreleased)
  + [5.1.2](changelog.html#id1)
  + [5.1.1](changelog.html#id2)
  + [5.1.0](changelog.html#id3)
  + [5.0.0](changelog.html#id4)
  + [4.0.2](changelog.html#id5)
  + [4.0.1](changelog.html#id6)
  + [4.0.0](changelog.html#id7)
  + [3.0.2](changelog.html#id8)
  + [3.0.1](changelog.html#id9)
  + [3.0.0](changelog.html#id10)
  + [2.0.2](changelog.html#id11)
  + [2.0.1](changelog.html#id12)
  + [2.0.0](changelog.html#id13)
  + [1.1.7](changelog.html#id14)
  + [1.1.6](changelog.html#id15)
  + [1.1.5](changelog.html#id16)
  + [1.1.4](changelog.html#id17)
  + [1.1.3](changelog.html#id18)
  + [1.1.2](changelog.html#id19)
  + [1.1.1](changelog.html#id20)
  + [1.1.0](changelog.html#id21)
  + [1.0.6](changelog.html#id22)
  + [1.0.5](changelog.html#id23)
  + [1.0.4](changelog.html#id24)
  + [1.0.3](changelog.html#id25)
  + [1.0.2](changelog.html#id26)
  + [1.0.1](changelog.html#id27)
  + [1.0.0](changelog.html#id28)
