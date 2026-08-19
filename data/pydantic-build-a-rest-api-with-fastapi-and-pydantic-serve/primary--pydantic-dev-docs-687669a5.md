---
library: "pydantic"
query: "Build a REST API with FastAPI and Pydantic, served by uvicorn, with typed request models"
url: "https://pydantic.dev/docs/"
role: "primary"
rank: 0
fetched_at: "2026-08-19T12:46:16.738729+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "7f28bd28fb2d3081591197db28229507cbf34d1996ebe7ac410557c144246496"
---

# Pydantic Docs

Pydantic is the end-to-end AI Engineering stack. Validate untrusted data and build agents you’ll actually ship to production using our Python libraries. Observe, govern, and optimize agents written in any language or framework once they’re live.

[### Pydantic Validation

Data validation from Python type hints. Parse, validate, and serialize with confidence.

```
class User(BaseModel):
    name: str

    age: int
```

 Learn about Validation →](/docs/validation/latest/get-started/) [### Pydantic AI

The batteries-included type-safe framework for building production agents.

```
model = 'openai:gpt-5.6-sol'

agent = Agent(model)
agent.run_sync('Does it snow?')
```

!

 Build production-ready Agents →](/docs/ai/overview/)  [Not just Python !  Logfire lets you monitor, secure, and optimize agents written in Python, TypeScript, Rust, Go, Java, Ruby, or any other language.

### Pydantic Logfire

Observability and governance for AI agents, LLMs, applications, services, and hosts.

```
logfire.configure();

logfire.info('app started');
```

 See the best AI Engineering platform →](/docs/logfire/get-started/) [### HTTPX2

A next-generation HTTP client. Sync and async APIs, HTTP/1.1 and HTTP/2.

```
client = httpx2.Client()
r = client.get('https://pydantic.dev')
```

 Make requests with HTTPX2 →](/docs/httpx2/get-started/)
