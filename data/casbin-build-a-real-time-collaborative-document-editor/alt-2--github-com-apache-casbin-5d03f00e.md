---
library: "casbin"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://github.com/apache/casbin"
role: "alternate"
rank: 2
fetched_at: "2026-08-18T14:21:15.130213+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "184e2928c6c79fbd0e898c9fe0f4c8e776ce624574d25f4e58f5e3fcb8446b65"
---

# Apache Casbin

[![Lint](https://github.com/apache/casbin/actions/workflows/golangci-lint.yml/badge.svg)](https://github.com/apache/casbin/actions/workflows/golangci-lint.yml)   [![Build](https://github.com/apache/casbin/actions/workflows/default.yml/badge.svg)](https://github.com/apache/casbin/actions/workflows/default.yml)   [![Coverage Status](https://camo.githubusercontent.com/d51680aba0333f5569bf9b34f27ba0fcf58c99b73c19d23983a662687da59fc0/68747470733a2f2f636f766572616c6c732e696f2f7265706f732f6769746875622f6170616368652f63617362696e2f62616467652e7376673f6272616e63683d6d6173746572)](https://coveralls.io/github/apache/casbin?branch=master)   [![Godoc](https://camo.githubusercontent.com/4ef4f4f53ebe79827b5bfabd782999c3a0012f51df266220cc88b9f2fd6e2a4c/68747470733a2f2f676f646f632e6f72672f6769746875622e636f6d2f6170616368652f63617362696e3f7374617475732e737667)](https://pkg.go.dev/github.com/casbin/casbin/v2)   [![Release](https://camo.githubusercontent.com/dc5de2b7252d6bf3cfba68291823ddb906ff6534802a161bd30c7eb6601f088c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f72656c656173652f6170616368652f63617362696e2e737667)](https://github.com/apache/casbin/releases/latest)   [![Discord](https://camo.githubusercontent.com/c8fdee241686554f3107d969c18164026ea4f0e42940af4c2ea3a7ce91e6a147/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313032323734383330363039363533373636303f6c6f676f3d646973636f7264266c6162656c3d646973636f726426636f6c6f723d353836354632)](https://discord.gg/S5UjpzGZjN)   [![Sourcegraph](https://camo.githubusercontent.com/0c2f12a63244d450152dcb44bf047ac5425a61294e620003201da5977211e5cb/68747470733a2f2f736f7572636567726170682e636f6d2f6769746875622e636f6d2f6170616368652f63617362696e2f2d2f62616467652e737667)](https://sourcegraph.com/github.com/apache/casbin?badge)

**News** : still worry about how to write the correct Apache Casbin policy? `Apache Casbin online editor` is coming to help! Try it at: <https://casbin.apache.org/editor/>

[![casbin Logo](/apache/casbin/raw/master/casbin-logo.png)](/apache/casbin/blob/master/casbin-logo.png)

Apache Casbin is a powerful and efficient open-source access control library for Golang projects. It provides support for enforcing authorization based on various [access control models](https://en.wikipedia.org/wiki/Computer_security_model) .

## All the languages supported by Apache Casbin:

| [golang](https://github.com/apache/casbin) | [java](https://github.com/casbin/jcasbin) | [nodejs](https://github.com/casbin/node-casbin) | [php](https://github.com/php-casbin/php-casbin) |
| --- | --- | --- | --- |
| [Casbin](https://github.com/apache/casbin) | [jCasbin](https://github.com/casbin/jcasbin) | [node-Casbin](https://github.com/casbin/node-casbin) | [PHP-Casbin](https://github.com/php-casbin/php-casbin) |
| production-ready | production-ready | production-ready | production-ready |

| [python](https://github.com/casbin/pycasbin) | [dotnet](https://github.com/casbin-net/Casbin.NET) | [c++](https://github.com/casbin/casbin-cpp) | [rust](https://github.com/casbin/casbin-rs) |
| --- | --- | --- | --- |
| [PyCasbin](https://github.com/casbin/pycasbin) | [Casbin.NET](https://github.com/casbin-net/Casbin.NET) | [Casbin-CPP](https://github.com/casbin/casbin-cpp) | [Casbin-RS](https://github.com/casbin/casbin-rs) |
| production-ready | production-ready | production-ready | production-ready |

## Table of contents

* [Supported models](#supported-models)
* [How it works?](#how-it-works)
* [Features](#features)
* [Installation](#installation)
* [Documentation](#documentation)
* [Online editor](#online-editor)
* [Tutorials](#tutorials)
* [Get started](#get-started)
* [Policy management](#policy-management)
* [Policy persistence](#policy-persistence)
* [Policy consistence between multiple nodes](#policy-consistence-between-multiple-nodes)
* [Role manager](#role-manager)
* [Benchmarks](#benchmarks)
* [Examples](#examples)
* [Middlewares](#middlewares)
* [Our adopters](#our-adopters)

## Supported models

1. [**ACL (Access Control List)**](https://en.wikipedia.org/wiki/Access_control_list)
2. **ACL with [superuser](https://en.wikipedia.org/wiki/Superuser)**
3. **ACL without users** : especially useful for systems that don't have authentication or user log-ins.
4. **ACL without resources** : some scenarios may target for a type of resources instead of an individual resource by using permissions like `write-article` , `read-log` . It doesn't control the access to a specific article or log.
5. **[RBAC (Role-Based Access Control)](https://en.wikipedia.org/wiki/Role-based_access_control)**
6. **RBAC with resource roles** : both users and resources can have roles (or groups) at the same time.
7. **RBAC with domains/tenants** : users can have different role sets for different domains/tenants.
8. **[ABAC (Attribute-Based Access Control)](https://en.wikipedia.org/wiki/Attribute-Based_Access_Control)**  : syntax sugar like `resource.Owner` can be used to get the attribute for a resource.
9. **[RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer)**  : supports paths like `/res/*` , `/res/:id` and HTTP methods like `GET` , `POST` , `PUT` , `DELETE` .
10. **Deny-override** : both allow and deny authorizations are supported, deny overrides the allow.
11. **Priority** : the policy rules can be prioritized like firewall rules.

## How it works?

In Casbin, an access control model is abstracted into a CONF file based on the **PERM metamodel (Policy, Effect, Request, Matchers)** . So switching or upgrading the authorization mechanism for a project is just as simple as modifying a configuration. You can customize your own access control model by combining the available models. For example, you can get RBAC roles and ABAC attributes together inside one model and share one set of policy rules.

The most basic and simplest model in Casbin is ACL. ACL's model CONF is:

```
#
 Request definition
[request_definition]
r
 = sub, obj, act

#
 Policy definition
[policy_definition]
p
 = sub, obj, act

#
 Policy effect
[policy_effect]
e
 = some(where (p.eft
 == allow))

#
 Matchers
[matchers]
m
 = r.sub
 == p.sub && r.obj
 == p.obj && r.act
 == p.act
```

An example policy for ACL model is like:

```
p, alice, data1, read
p, bob, data2, write
```

It means:

* alice can read data1
* bob can write data2

We also support multi-line mode by appending '\' in the end:

```
#
 Matchers
[matchers]
m
 = r.sub
 == p.sub && r.obj
 == p.obj \
  && r.act
 == p.act
```

Further more, if you are using ABAC, you can try operator `in` like following in Casbin **golang** edition (jCasbin and Node-Casbin are not supported yet):

```
#
 Matchers
[matchers]
m
 = r.obj
 == p.obj && r.act
 == p.act || r.obj in (
'data2'
,
'data3'
)
```

But you **SHOULD** make sure that the length of the array is **MORE** than **1** , otherwise there will cause it to panic.

For more operators, you may take a look at [govaluate](https://github.com/casbin/govaluate)

## Features

What Apache Casbin does:

1. enforce the policy in the classic `{subject, object, action}` form or a customized form as you defined, both allow and deny authorizations are supported.
2. handle the storage of the access control model and its policy.
3. manage the role-user mappings and role-role mappings (aka role hierarchy in RBAC).
4. support built-in superuser like `root` or `administrator` . A superuser can do anything without explicit permissions.
5. multiple built-in operators to support the rule matching. For example, `keyMatch` can map a resource key `/foo/bar` to the pattern `/foo*` .

What Apache Casbin does NOT do:

1. authentication (aka verify `username` and `password` when a user logs in)
2. manage the list of users or roles. I believe it's more convenient for the project itself to manage these entities. Users usually have their passwords, and Apache Casbin is not designed as a password container. However, Apache Casbin stores the user-role mapping for the RBAC scenario.

## Installation

```
go get github.com/casbin/casbin/v3
```

## Documentation

<https://casbin.apache.org/docs/overview>

## Online editor

You can also use the online editor ( <https://casbin.apache.org/editor/> ) to write your Casbin model and policy in your web browser. It provides functionality such as `syntax highlighting` and `code completion` , just like an IDE for a programming language.

## Tutorials

<https://casbin.apache.org/docs/tutorials>

## Get started

1. New a Casbin enforcer with a model file and a policy file:

   ```
   e, _ := casbin.NewEnforcer("path/to/model.conf", "path/to/policy.csv")
   ```

Note: you can also initialize an enforcer with policy in DB instead of file, see [Policy-persistence](#policy-persistence) section for details.

2. Add an enforcement hook into your code right before the access happens:

   ```
   sub := "alice" // the user that wants to access a resource.
   obj := "data1" // the resource that is going to be accessed.
   act := "read" // the operation that the user performs on the resource.

   if res, _ := e.Enforce(sub, obj, act); res
    {
       // permit alice to read data1

   } else
    {
       // deny the request, show an error

   }
   ```
3. Besides the static policy file, Apache Casbin also provides API for permission management at run-time. For example, You can get all the roles assigned to a user as below:

   ```
   roles, _ := e.GetImplicitRolesForUser(sub)
   ```

See [Policy management APIs](#policy-management) for more usage.

## Policy management

Apache Casbin provides two sets of APIs to manage permissions:

* [Management API](https://casbin.apache.org/docs/management-api) : the primitive API that provides full support for Apache Casbin policy management.
* [RBAC API](https://casbin.apache.org/docs/rbac-api) : a more friendly API for RBAC. This API is a subset of Management API. The RBAC users could use this API to simplify the code.

We also provide a [web-based UI](https://casbin.apache.org/docs/admin-portal) for model management and policy management:

[![model editor](https://camo.githubusercontent.com/7ff76257a6df015b000ac15d4a5e7079504de9c09cd57411f25ab7ac7956d0d2/68747470733a2f2f68736c756f797a2e6769746875622e696f2f63617362696e2f75695f6d6f64656c5f656469746f722e706e67)](https://camo.githubusercontent.com/7ff76257a6df015b000ac15d4a5e7079504de9c09cd57411f25ab7ac7956d0d2/68747470733a2f2f68736c756f797a2e6769746875622e696f2f63617362696e2f75695f6d6f64656c5f656469746f722e706e67)

[![policy editor](https://camo.githubusercontent.com/44a14c514322f377d198a15570b2f6791ea1098f422a6afeee1e49b339db4361/68747470733a2f2f68736c756f797a2e6769746875622e696f2f63617362696e2f75695f706f6c6963795f656469746f722e706e67)](https://camo.githubusercontent.com/44a14c514322f377d198a15570b2f6791ea1098f422a6afeee1e49b339db4361/68747470733a2f2f68736c756f797a2e6769746875622e696f2f63617362696e2f75695f706f6c6963795f656469746f722e706e67)

## Policy persistence

<https://casbin.apache.org/docs/adapters>

## Policy consistence between multiple nodes

<https://casbin.apache.org/docs/watchers>

## Role manager

<https://casbin.apache.org/docs/role-managers>

## Benchmarks

<https://casbin.apache.org/docs/benchmark>

## Examples

| Model | Model file | Policy file |
| --- | --- | --- |
| ACL | [basic\_model.conf](https://github.com/apache/casbin/blob/master/examples/basic_model.conf) | [basic\_policy.csv](https://github.com/apache/casbin/blob/master/examples/basic_policy.csv) |
| ACL with superuser | [basic\_model\_with\_root.conf](https://github.com/apache/casbin/blob/master/examples/basic_with_root_model.conf) | [basic\_policy.csv](https://github.com/apache/casbin/blob/master/examples/basic_policy.csv) |
| ACL without users | [basic\_model\_without\_users.conf](https://github.com/apache/casbin/blob/master/examples/basic_without_users_model.conf) | [basic\_policy\_without\_users.csv](https://github.com/apache/casbin/blob/master/examples/basic_without_users_policy.csv) |
| ACL without resources | [basic\_model\_without\_resources.conf](https://github.com/apache/casbin/blob/master/examples/basic_without_resources_model.conf) | [basic\_policy\_without\_resources.csv](https://github.com/apache/casbin/blob/master/examples/basic_without_resources_policy.csv) |
| RBAC | [rbac\_model.conf](https://github.com/apache/casbin/blob/master/examples/rbac_model.conf) | [rbac\_policy.csv](https://github.com/apache/casbin/blob/master/examples/rbac_policy.csv) |
| RBAC with resource roles | [rbac\_model\_with\_resource\_roles.conf](https://github.com/apache/casbin/blob/master/examples/rbac_with_resource_roles_model.conf) | [rbac\_policy\_with\_resource\_roles.csv](https://github.com/apache/casbin/blob/master/examples/rbac_with_resource_roles_policy.csv) |
| RBAC with domains/tenants | [rbac\_model\_with\_domains.conf](https://github.com/apache/casbin/blob/master/examples/rbac_with_domains_model.conf) | [rbac\_policy\_with\_domains.csv](https://github.com/apache/casbin/blob/master/examples/rbac_with_domains_policy.csv) |
| ABAC | [abac\_model.conf](https://github.com/apache/casbin/blob/master/examples/abac_model.conf) | N/A |
| RESTful | [keymatch\_model.conf](https://github.com/apache/casbin/blob/master/examples/keymatch_model.conf) | [keymatch\_policy.csv](https://github.com/apache/casbin/blob/master/examples/keymatch_policy.csv) |
| Deny-override | [rbac\_model\_with\_deny.conf](https://github.com/apache/casbin/blob/master/examples/rbac_with_deny_model.conf) | [rbac\_policy\_with\_deny.csv](https://github.com/apache/casbin/blob/master/examples/rbac_with_deny_policy.csv) |
| Priority | [priority\_model.conf](https://github.com/apache/casbin/blob/master/examples/priority_model.conf) | [priority\_policy.csv](https://github.com/apache/casbin/blob/master/examples/priority_policy.csv) |

## Middlewares

Authz middlewares for web frameworks: <https://casbin.apache.org/docs/middlewares>

## Our adopters

<https://casbin.apache.org/docs/adopters>

## How to Contribute

Please read the [contributing guide](/apache/casbin/blob/master/CONTRIBUTING.md) .

## Contributors

This project exists thanks to all the people who contribute.  [!](https://github.com/apache/casbin/graphs/contributors)

## Star History

[![Star History Chart](https://camo.githubusercontent.com/f75b62cef7782b0b64fde6e2a473f6bfa1e496539a16673eb17029e93bcb0603/68747470733a2f2f737461722d686973746f72792e646572612e706167652f7376673f7265706f733d6170616368652f63617362696e26747970653d44617465)](https://star-history.dera.page/#apache/casbin&Date)

## License

This project is licensed under the [Apache 2.0 license](/apache/casbin/blob/master/LICENSE) .

## Contact

If you have any issues or feature requests, please contact us. PR is welcomed.

* <https://github.com/apache/casbin/issues>
* <https://discord.gg/S5UjpzGZjN>
