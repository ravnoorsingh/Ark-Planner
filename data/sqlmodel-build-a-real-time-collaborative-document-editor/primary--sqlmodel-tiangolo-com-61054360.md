---
library: "sqlmodel"
query: "Build a real-time collaborative document editor backend. FastAPI serves WebSocket connections, Redis pub/sub broadcasts operational-transform patches between clients, SQLModel persists document snapshots to a Database, and Alembic manages migrations. Include JWT authentication, per-document access control, and graceful reconnection with missed-update replay. Use PyJWT for the jwt authentication. Use casbin for the access control. Use text-ot for the operational transform."
url: "https://sqlmodel.tiangolo.com/"
role: "primary"
rank: 0
fetched_at: "2026-08-18T14:21:13.815541+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "01189e865712f8fcc7a1fa4be04edefb362d20308b5ce3cc12fb5294d8256348"
---

#

[![SQLModel](https://sqlmodel.tiangolo.com/img/logo-margin/logo-margin-vector.svg#only-light)](https://sqlmodel.tiangolo.com)    [![SQLModel](https://sqlmodel.tiangolo.com/img/logo-margin/logo-margin-white-vector.svg#only-dark)](https://sqlmodel.tiangolo.com)

*SQLModel, SQL databases in Python, designed for simplicity, compatibility, and robustness.*

[![Test](https://github.com/fastapi/sqlmodel/actions/workflows/test.yml/badge.svg?event=push&branch=main)](https://github.com/fastapi/sqlmodel/actions?query=workflow%3ATest+event%3Apush+branch%3Amain)   [![Coverage](https://coverage-badge.samuelcolvin.workers.dev/fastapi/sqlmodel.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/sqlmodel)   [![Package version](https://img.shields.io/pypi/v/sqlmodel?color=%2334D058&label=pypi%20package)](https://pypi.org/project/sqlmodel)

---

**Documentation** : <https://sqlmodel.tiangolo.com>

**Source Code** : <https://github.com/fastapi/sqlmodel>

---

SQLModel is a library for interacting with SQL databases from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust.

**SQLModel** is based on Python type annotations, and powered by  [Pydantic](https://pydantic-docs.helpmanual.io/)  and  [SQLAlchemy](https://sqlalchemy.org/)  .

The key features are:

* **Intuitive to write** : Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
* **Easy to use** : It has sensible defaults and does a lot of work underneath to simplify the code you write.
* **Compatible** : It is designed to be compatible with **FastAPI** , Pydantic, and SQLAlchemy.
* **Extensible** : You have all the power of SQLAlchemy and Pydantic underneath.
* **Short** : Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in SQLAlchemy and Pydantic.

## Sponsors

[!](https://www.govcert.lu "This project is being supported by GOVCERT.LU")

## SQL Databases in FastAPI

[!](https://fastapi.tiangolo.com)

**SQLModel** is designed to simplify interacting with SQL databases in  [FastAPI](https://fastapi.tiangolo.com)  applications, it was created by the same  [author](https://tiangolo.com/)  . 😁

It combines SQLAlchemy and Pydantic and tries to simplify the code you write as much as possible, allowing you to reduce the **code duplication to a minimum** , but while getting the **best developer experience** possible.

**SQLModel** is, in fact, a thin layer on top of **Pydantic** and **SQLAlchemy** , carefully designed to be compatible with both.

## Requirements

A recent and currently supported  [version of Python](https://www.python.org/downloads/)  .

As **SQLModel** is based on **Pydantic** and **SQLAlchemy** , it requires them. They will be automatically installed when you install SQLModel.

## Installation

First,  [install `uv`](https://docs.astral.sh/uv/getting-started/installation/)  , and then add SQLModel to your project:

```
uv add sqlmodel

uv add sqlmodel
```

If you prefer to use `pip` , install `sqlmodel` inside a virtual environment. See the  [installation guide](https://sqlmodel.tiangolo.com/install/)  for the alternative steps.

## Example

For an introduction to databases, SQL, and everything else, see the  [SQLModel documentation](https://sqlmodel.tiangolo.com/databases/)  .

Here's a quick example. ✨

### A SQL Table

Imagine you have a SQL table called `hero` with:

* `id`
* `name`
* `secret_name`
* `age`

And you want it to have this data:

| id | name | secret\_name | age |
| --- | --- | --- | --- |
| 1 | Deadpond | Dive Wilson | null |
| 2 | Spider-Boy | Pedro Parqueador | null |
| 3 | Rusty-Man | Tommy Sharp | 48 |

### Create a SQLModel Model

Then you could create a **SQLModel** model like this:

```
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```

That class `Hero` is a **SQLModel** model, the equivalent of a SQL table in Python code.

And each of those class attributes is equivalent to each **table column** .

### Create Rows

Then you could **create each row** of the table as an **instance** of the model:

```
hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
```

This way, you can use conventional Python code with **classes** and **instances** that represent **tables** and **rows** , and that way communicate with the **SQL database** .

### Editor Support

Everything is designed for you to get the best developer experience possible, with the best editor support.

Including **autocompletion** :

!

And **inline errors** :

!

### Write to the Database

You can learn a lot more about **SQLModel** by quickly following the **tutorial** , but if you need a taste right now of how to put all that together and save to the database, you can do this:

```
from sqlmodel import Field, Session, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
```

That will save a **SQLite** database with the 3 heroes.

### Select from the Database

Then you could write queries to select from that same database, for example with:

```
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

engine = create_engine("sqlite:///database.db")

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)
```

### Editor Support Everywhere

**SQLModel** was carefully designed to give you the best developer experience and editor support, **even after selecting data** from the database:

!

## SQLAlchemy and Pydantic

That class `Hero` is a **SQLModel** model.

But at the same time, ✨ it is a **SQLAlchemy** model ✨. So, you can combine it and use it with other SQLAlchemy models, or you could easily migrate applications with SQLAlchemy to **SQLModel** .

And at the same time, ✨ it is also a **Pydantic** model ✨. You can use inheritance with it to define all your **data models** while avoiding code duplication. That makes it very easy to use with **FastAPI** .

## License

This project is licensed under the terms of the  [MIT license](https://github.com/fastapi/sqlmodel/blob/main/LICENSE)  .
