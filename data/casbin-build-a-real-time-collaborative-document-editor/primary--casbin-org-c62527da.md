---
library: "casbin"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://casbin.org/"
resolved_url: "https://casbin.apache.org/"
role: "primary"
rank: 0
fetched_at: "2026-08-18T14:21:14.716334+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "e7b2eeeda0b7e9762de7859e5e9a31207d9258c8fdcbd29ca6f2ade3e46bf1b9"
---

## Use Apache Casbin with Multiple Languages

[![Golang](/img/langs/go-logo-1.svg)](https://github.com/casbin) [![Java](/img/langs/jee-3.svg)](https://github.com/apache/casbin-jcasbin) [![C/C++](/img/langs/c.svg)](https://github.com/apache/casbin-cpp) [![Node.js](/img/langs/nodejs-1.svg)](https://github.com/apache/casbin-node-casbin) [![Front-end JavaScript](/img/langs/logo-javascript.svg)](https://github.com/apache/casbin-casbin.js) [![PHP](/img/langs/PHP-logo.svg)](https://github.com/php-casbin/php-casbin) [![Laravel](/img/langs/laravel-2.svg)](https://github.com/php-casbin/laravel-authz) [![Python](/img/langs/python-5.svg)](https://github.com/apache/casbin-pycasbin) [![.NET (C#)](/img/langs/dotnet-logo.svg)](https://github.com/apache/casbin-Casbin.NET) [![Delphi](/img/langs/delphi-2.svg)](https://github.com/casbin4d/Casbin4D) [![Rust](/img/langs/rust.svg)](https://github.com/apache/casbin-rs) [![Ruby](/img/langs/ruby.svg)](https://github.com/CasbinRuby/casbin-ruby) [![Swift (Objective-C)](/img/langs/swift-15.svg)](https://github.com/apache/casbin-SwiftCasbin) [![Lua (OpenResty, Kong, APISIX)](/img/langs/lua-5.svg)](https://github.com/apache/casbin-lua-casbin) [![Dart (Flutter)](/img/langs/dart.svg)](https://github.com/apache/casbin-dart-casbin) [![Elixir](/img/langs/elixir-lang-icon.svg)](https://github.com/apache/casbin-ex) [![Cloud Native (Kubernetes, Istio, Envoy, KubeSphere)](/img/langs/kubernetes.svg)](/docs/cloud-native)

![[object Object]](/img/model.png)

### Hybrid access control models

Apache Casbin uses CONF files to define access control models based on the PERM metamodel (Policy, Effect, Request, Matchers). You can change or upgrade your authorization mechanism by modifying the configuration file.

![[object Object]](/img/storage.png)

### Flexible policy storage

Apache Casbin policies can be stored in memory, files, or databases. We support dozens of storage backends including MySQL, Postgres, Oracle, MongoDB, Redis, Cassandra, and AWS S3. See the full list of [adapters](/docs/adapters) .

![[object Object]](/img/language.png)

### Cross-languages & cross-platforms

Apache Casbin is implemented in multiple languages including Golang, Java, PHP, Node.js, Python, .NET, Rust, and more. All implementations share the same API and behavior.

## Try the Apache Casbin Online Editor

Write and test your Apache Casbin model and policy in real-time with the interactive online editor. Try different access control models and see results instantly.

![Preview of the Apache Casbin online editor interface](/img/online_editor_homepage_preview.png)

[Open Full Editor](https://editor.casbin.org/)

### Policy Persistence

Apache Casbin stores policies through adapters. To keep the library lightweight, adapter code is separated from the main library (except for the default file adapter). We support third-party adapter contributions. See the full list of [adapters](/docs/adapters) for more information.

![Policy Persistence](/img/store.png)

![Policy enforcement at scale](/img/scale.png)

### Policy Enforcement at Scale

Some adapters support filtered policy loading. This means Apache Casbin can load only a subset of policies from storage based on specified filters. This feature is useful for large-scale, multi-tenant applications where loading all policies at once would be inefficient.

### Role Manager

The role manager handles RBAC role hierarchy (user-role mappings) in Apache Casbin. It can load role data from Apache Casbin policy rules or from external sources like LDAP, Okta, Auth0, Azure AD, etc. To keep the library lightweight, role manager code is separated from the main library (except for the default one). See all available [role-managers](/docs/role-managers) .

![Role manager](/img/role.png)

# Who's using Apache Casbin?

Hundreds of projects use Apache Casbin, from Fortune 500 companies to new startups. If you want to see what can be built with Apache Casbin, [check out these apps](/users) !

[![Intel RMD](/img/users/intel.png "Intel RMD")](https://github.com/intel/rmd)   [![Vmware Harbor](/img/users/vmware.png "Vmware Harbor")](https://github.com/goharbor/harbor)   [![Docker](/img/users/docker.png "Docker")](https://docs.docker.com/engine/extend/legacy_plugins/#authorization-plugins)   [![Orange Gobis](/img/users/orange.png "Orange Gobis")](https://github.com/orange-cloudfoundry/gobis)   [![Cisco](/img/users/cisco.png "Cisco")](https://www.linkedin.com/in/openmohan/)   [![Microsoft](/img/users/microsoft.png "Microsoft")](https://github.com/microsoft/mouselog)   [![Verizon](/img/users/verizon.png "Verizon")](https://github.com/apache/casbin/pull/56)   [![Alibaba](/img/users/alibaba.png "Alibaba")](https://github.com/dragonflyoss/Dragonfly2/search?q=casbin&type=code)   [![Redhat](/img/users/redhat.png "Redhat")](https://github.com/skydive-project/skydive)   [![Tencent](/img/users/tencent.png "Tencent")](https://github.com/tkestack/tke)   [![ETH Zurich](/img/users/eth.png "ETH Zurich")](https://github.com/netsec-ethz/)   [![T-Mobile](/img/users/t-mobile.png "T-Mobile")](https://github.com/tmobile/jazz)   [![IBM](/img/users/ibm.png "IBM")](https://loopback.io/doc/en/lb4/migration-auth-access-control-example.html#using-casbin)   [![F5](/img/users/f5.png "F5")](https://github.com/apache/casbin/issues/299)   [![Bose](/img/users/bose.png "Bose")](https://github.com/apache/casbin/issues/302)   [![r/SpaceX](/img/users/rspacex.png "r/SpaceX")](https://github.com/r-spacex/SpaceX-API/commit/f8daa8f9878dcd7a281fc8081e3aeb8e5d216089)   [![Elastic](/img/users/elastic.png "Elastic")](https://www.elastic.co/guide/en/cloud-on-k8s/master/k8s-dependencies.html)   [![Honeywell](/img/users/honeywell.png "Honeywell")](https://www.linkedin.com/search/results/people/?keywords=casbin%20honeywell)   [![HPE](/img/users/hpe.png "HPE")](https://www.linkedin.com/in/raghavbabu)   [![Schneider Electric](/img/users/se.png "Schneider Electric")](https://www.linkedin.com/in/peterjotoole)   [![SIEMENS](/img/users/siemens.png "SIEMENS")](https://www.linkedin.com/in/kshitij-rastogi19)   [![Musma](/img/users/musma.png "Musma")](https://www.musma.net/)   [![Jdlt](/img/users/jdlt.png "Jdlt")](https://jdlt.co.uk/)   [![360](/img/users/360.png "360")](https://www.linkedin.com/in/andrew-weng/)   [![Bytebase](/img/users/bytebase.png "Bytebase")](https://github.com/bytebase/bytebase/blob/740afc6286cd855fecc3cc54875583c6b650a41a/server/server.go)   [![zilliz](/img/users/zilliz.png "zilliz")](https://github.com/milvus-io/milvus/blob/d7f38a803d5d23d3e061702e73770cb68aee1dc2/internal/proxy/privilege_interceptor.go)   [![Ontario Government](/img/users/ontario.png "Ontario Government")](https://www.linkedin.com/in/nihalpandit)   [![Apache Pulsar](/img/users/pulsar.png "Apache Pulsar")](https://apachecon.com/acasia2021/sessions/1049.html)
