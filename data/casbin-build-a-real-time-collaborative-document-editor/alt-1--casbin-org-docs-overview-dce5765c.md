---
library: "casbin"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://casbin.org/docs/overview"
resolved_url: "https://casbin.apache.org/docs/overview/"
role: "alternate"
rank: 1
fetched_at: "2026-08-18T14:21:14.841475+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "1794d259fdb8a737bd98cbc0fc54053dae3fabc98a4b7aa5c57fd75fa18da124"
---

Casbin is an efficient, open-source access control library that enforces authorization and supports multiple [access control models](https://en.wikipedia.org/wiki/Access_control#Access_control_models) .

Implementing rule-based access control is straightforward: define subjects, objects, and permitted actions in a  ***policy***  file in any format that fits your needs. This pattern is consistent across all Casbin implementations. The  ***model***  file gives developers and administrators full control over authorization logic—layout, execution flow, and conditions. The  ***Enforcer***  component evaluates incoming requests against your model and policy.

## Languages Supported by Casbin [​](#languages-supported-by-casbin "Direct link to Languages Supported by Casbin")

Casbin provides native support for multiple programming languages so you can integrate it into a wide range of projects and workflows:

| [golang](https://github.com/apache/casbin) | [java](https://github.com/apache/casbin-jcasbin) | [nodejs](https://github.com/apache/casbin-node-casbin) | [php](https://github.com/php-casbin/php-casbin) |
| --- | --- | --- | --- |
| [Casbin](https://github.com/apache/casbin) | [jCasbin](https://github.com/apache/casbin-jcasbin) | [node-Casbin](https://github.com/apache/casbin-node-casbin) | [PHP-Casbin](https://github.com/php-casbin/php-casbin) |
| Production-ready | Production-ready | Production-ready | Production-ready |

| [python](https://github.com/apache/casbin-pycasbin) | [dotnet](https://github.com/apache/casbin-Casbin.NET) | [c++](https://github.com/apache/casbin-cpp) | [rust](https://github.com/apache/casbin-rs) |
| --- | --- | --- | --- |
| [PyCasbin](https://github.com/apache/casbin-pycasbin) | [Casbin.NET](https://github.com/apache/casbin-Casbin.NET) | [Casbin-CPP](https://github.com/apache/casbin-cpp) | [Casbin-RS](https://github.com/apache/casbin-rs) |
| Production-ready | Production-ready | Production-ready | Production-ready |

### Feature Set by Language [​](#feature-set-by-language "Direct link to Feature Set by Language")

We aim for feature parity across all language implementations; complete uniformity is not yet achieved.

| Feature | Go | Java | Node.js | PHP | Python | C# | Delphi | Rust | C++ | Lua | Dart | Elixir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enforcement | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| RBAC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ABAC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scaling ABAC ( `eval()` ) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Adapter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Management API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| RBAC API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Batch API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Filtered Adapter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Watcher | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Role Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Multi-Threading | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 'in' of matcher | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |

note

A checkmark (✅) for Watcher or Role Manager means the interface exists in the core library; it does not guarantee that an implementation is available for that language.

## What is Casbin? [​](#what-is-casbin "Direct link to What is Casbin?")

Casbin is an authorization library for applications that need controlled access to resources. Typically, a **subject** (user or service) requests access to an **object** (resource or entity) to perform an **action** (e.g. *read* , *write* , or *delete* ). You define these actions to match your application. This is the standard `{ subject, object, action }` flow that Casbin handles most often.

Casbin also supports more complex scenarios through [roles (RBAC)](/docs/rbac) , [attributes (ABAC)](/docs/abac) , and other patterns.

### What Casbin Does [​](#what-casbin-does "Direct link to What Casbin Does")

1. **Enforces policy** in the classic `{ subject, object, action }` format or any custom format you define, including both allow and deny.
2. **Manages storage** for the access control model and policies.
3. **Handles user–role and role–role relationships** (RBAC role hierarchy).
4. **Supports built-in superusers** (e.g. `root` , `administrator` ) with unrestricted access without explicit rules.
5. **Provides built-in operators** for pattern matching (e.g. `keyMatch` matches `/foo/bar` against `/foo*` ).

### What Casbin Does Not Do [​](#what-casbin-does-not-do "Direct link to What Casbin Does Not Do")

1. **User authentication** — validating usernames and passwords at login.
2. **User or role list management** — maintaining the list of users or roles.

Most applications already manage users, roles, and credentials. Casbin focuses only on authorization and does not store or verify passwords. In RBAC mode, it does maintain user–role associations.
