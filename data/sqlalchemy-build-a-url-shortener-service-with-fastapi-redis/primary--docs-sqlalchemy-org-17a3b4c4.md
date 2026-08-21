---
library: "sqlalchemy"
query: "Build a URL shortener service with FastAPI, Redis for the key-value store, and click analytics. Use sqlalchemy for the orm."
url: "https://docs.sqlalchemy.org/"
resolved_url: "https://docs.sqlalchemy.org/en/20/"
role: "primary"
rank: 0
fetched_at: "2026-08-21T07:37:08.225014+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "a0dc0c03d3eb4e9f3ffef22e0475093cd5bcd50d4336d47506a5fe41791fcc5b"
---

# SQLAlchemy Documentation

Getting Started

New to SQLAlchemy? Start here:

* **For Python Beginners:**  [Installation Guide](intro.html#installation)  - basic guidance on installing with pip and similar
* **For Python Veterans:**  [SQLAlchemy Overview](intro.html)  - brief architectural overview

Tutorials

New users of SQLAlchemy, as well as veterans of older SQLAlchemy release series, should start with the  [SQLAlchemy Unified Tutorial](tutorial/index.html)  , which covers everything an Alchemist needs to know when using the ORM or just Core.

* **For a quick glance:**  [ORM Quick Start](orm/quickstart.html)  - a glimpse at what working with the ORM looks like
* **For all users:**  [SQLAlchemy Unified Tutorial](tutorial/index.html)  - In depth tutorial for Core and ORM

Migration Notes

Users coming from older versions of SQLAlchemy, especially those transitioning from the 1.x style of working, will want to review this documentation.

* [Migrating to SQLAlchemy 2.0](changelog/migration_20.html)  - Complete background on migrating from 1.3 or 1.4 to 2.0
* [What’s New in SQLAlchemy 2.0?](changelog/whatsnew_20.html)  - New 2.0 features and behaviors beyond the 1.x migration
* [Changelog catalog](changelog/index.html)  - Detailed changelogs for all SQLAlchemy Versions

Reference and How To

**SQLAlchemy ORM** - Detailed guides and API reference for using the ORM

* **Mapping Classes:**  [Mapping Python Classes](orm/mapper_config.html)  |  [Relationship Configuration](orm/relationships.html)
* **Using the ORM:**  [Using the ORM Session](orm/session.html)  |  [ORM Querying Guide](orm/queryguide/index.html)  |  [Using AsyncIO](orm/extensions/asyncio.html)
* **Configuration Extensions:**  [Association Proxy](orm/extensions/associationproxy.html)  |  [Hybrid Attributes](orm/extensions/hybrid.html)  |  [Mutable Scalars](orm/extensions/mutable.html)  |  [Automap](orm/extensions/automap.html)  |  [All extensions](orm/extensions/index.html)
* **Extending the ORM:**  [ORM Events and Internals](orm/extending.html)
* **Other:**  [Introduction to Examples](orm/examples.html)

**SQLAlchemy Core** - Detailed guides and API reference for working with Core

* **Engines, Connections, Pools:**  [Engine Configuration](core/engines.html)  |  [Connections, Transactions, Results](core/connections.html)  |  [AsyncIO Support](orm/extensions/asyncio.html)  |  [Connection Pooling](core/pooling.html)
* **Schema Definition:**  [Overview](core/schema.html)  |  [Tables and Columns](core/metadata.html)  |  [Database Introspection (Reflection)](core/reflection.html)  |  [Insert/Update Defaults](core/defaults.html)  |  [Constraints and Indexes](core/constraints.html)  |  [Using Data Definition Language (DDL)](core/ddl.html)
* **SQL Statements:**  [SQL Expression Elements](core/sqlelement.html)  |  [Operator Reference](core/operators.html)  |  [SELECT and related constructs](core/selectable.html)  |  [INSERT, UPDATE, DELETE](core/dml.html)  |  [SQL Functions](core/functions.html)  |  [Table of Contents](core/expression_api.html)
* **Datatypes:**  [Overview](core/types.html)  |  [Building Custom Types](core/custom_types.html#types-custom)  |  [Type API Reference](core/type_api.html#types-api)
* **Core Basics:**  [Overview](core/api_basics.html)  |  [Runtime Inspection API](core/inspection.html)  |  [Event System](core/event.html)  |  [Core Event Interfaces](core/events.html)  |  [Creating Custom SQL Constructs](core/compiler.html)

Dialect Documentation

The **dialect** is the system SQLAlchemy uses to communicate with various types of DBAPIs and databases. This section describes notes, options, and usage patterns regarding individual dialects.

[PostgreSQL](dialects/postgresql.html)  |  [MySQL and MariaDB](dialects/mysql.html)  |  [SQLite](dialects/sqlite.html)  |  [Oracle Database](dialects/oracle.html)  |  [Microsoft SQL Server](dialects/mssql.html)

[More Dialects …](dialects/index.html)

Supplementary

* [Frequently Asked Questions](faq/index.html)  - A collection of common problems and solutions
* [Glossary](glossary.html)  - Definitions of terms used in SQLAlchemy documentation
* [Error Message Guide](errors.html)  - Explanations of many SQLAlchemy errors
* [Complete table of of contents](contents.html)  - Full list of available documentation
* [Index](genindex.html)  - Index for easy lookup of documentation topics
