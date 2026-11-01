<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/lorrod/graftql/main/docs/assets/graftql-wordmark-dark.svg">
    <img alt="GraftQL" src="https://raw.githubusercontent.com/lorrod/graftql/main/docs/assets/graftql-wordmark.svg" width="380">
  </picture>
</p>

<p align="center"><strong>SQLModel in, typed GraphQL out.</strong></p>

<p align="center">
  <a href="https://github.com/lorrod/graftql/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/lorrod/graftql/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://pypi.org/project/graftql/"><img alt="PyPI" src="https://img.shields.io/pypi/v/graftql?color=1f9d66"></a>
  <a href="https://pypi.org/project/graftql/"><img alt="Python" src="https://img.shields.io/pypi/pyversions/graftql?color=1f9d66"></a>
  <a href="https://lorrod.github.io/graftql/"><img alt="Docs" src="https://img.shields.io/badge/docs-lorrod.github.io%2Fgraftql-1f9d66"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-1f9d66"></a>
</p>

GraftQL turns your SQLModel definitions into a fully-typed GraphQL API — no schema duplication, no glue code.

---

## Overview

**GraftQL** lets you define your data models once (as `GraftModel` subclasses) and get a
fully-typed GraphQL API automatically — no schema duplication, no glue code. It layers on top of
[SQLModel](https://sqlmodel.tiangolo.com/) for the ORM and [Strawberry](https://strawberry.rocks/)
for the GraphQL schema. Mount `GraftRouter` in any FastAPI app and your models are immediately
queryable and mutable over GraphQL — including paginated connections, filters, ordering, and
fine-grained permission hooks.

Async (SQLAlchemy async engines) and sync engines are both supported, and multiple database
engines can be registered under different names for multi-tenant or federated setups.

---

## Features

- **Single model class** — extend `GraftModel` instead of both `SQLModel` and a Strawberry type.
- **Auto GraphQL schema** — queries, mutations (PUT / DELETE), and paginated connections generated automatically.
- **DataLoaders** — declare relations with `Dl` and `ManyRelation`; N+1 queries solved out of the box.
- **Composable filters** — date ranges, ordering, and custom filter attributes, all typed.
- **Permission hooks** — override `permission_getter` per-model or supply a global `get_permission` function.
- **Async support** — pass an async SQLAlchemy engine and GraftQL handles the rest.
- **Multi-engine** — register multiple engines by name; each model picks its engine via `__enginename__`.
- **Federation-ready** — Strawberry federation directives can be applied through the schema DSL.

---

## Installation

```bash
pip install graftql
```

Pull requests from branches in this repository publish development releases for testing. These
releases use versions such as `2.0.5.dev123456`, so pip ignores them during normal installation.
Install a specific preview using the version shown in the pull request workflow summary:

```bash
pip install "graftql==2.0.5.dev123456"
```

---

## Quick Start

```python
from datetime import date

from fastapi import FastAPI
from sqlmodel import create_engine

from graftql import Field, GraftModel, GraftRouter

# 1. Define your models — once. No separate Pydantic/Strawberry types needed.
class Student(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    birth_date: date

# 2. Create tables and mount the router.
engine = create_engine("sqlite:///./dev.db")
GraftModel.metadata.create_all(engine)

app = FastAPI()
router = GraftRouter(
    engine=engine,
    enable_put_mutations=True,
    enable_delete_mutations=True,
)
app.include_router(router, prefix="/graphql")

# 3. Run:  uvicorn main:app --reload
#    Visit: http://localhost:8000/graphql
```

You can now run queries like:

```graphql
mutation {
  students {
    put(input: { name: "Alice", birthDate: "2000-01-01" }) { id }
  }
}

query {
  students {
    many { edges { node { id name birthDate } } }
  }
}
```

---

## Documentation

See the [documentation](https://lorrod.github.io/graftql/) for the full guide including relations, DataLoaders,
authentication, async engines, and federation.

---

## Contributing

1. Fork [lorrod/graftql](https://github.com/lorrod/graftql).
2. Create a feature branch: `git checkout -b feat/my-change`.
3. Make your changes and add tests.
4. Run the checks: `uv run --group dev ruff check . && uv run --group dev pytest`.
5. Open a pull request whose title follows Conventional Commits, for example
   `feat(api): add cursor filtering` or `fix: handle missing relationships`.

All contributions are welcome — bug reports, documentation fixes, and new features alike.

---

## License

MIT — see [LICENSE](LICENSE).
