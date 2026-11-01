---
hide:
  - navigation
---

# GraftQL { .graftql-sr }

![GraftQL](assets/graftql-wordmark.svg#only-light){ .graftql-hero width="420" }
![GraftQL](assets/graftql-wordmark-dark.svg#only-dark){ .graftql-hero width="420" }

**SQLModel in, typed GraphQL out.**

GraftQL turns your SQLModel definitions into a fully-typed GraphQL API — no schema duplication, no glue code.

[![CI](https://github.com/lorrod/graftql/actions/workflows/ci.yml/badge.svg)](https://github.com/lorrod/graftql/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/graftql?color=1f9d66)](https://pypi.org/project/graftql/)
[![Python](https://img.shields.io/pypi/pyversions/graftql?color=1f9d66)](https://pypi.org/project/graftql/)
[![License](https://img.shields.io/badge/license-MIT-1f9d66)](https://github.com/lorrod/graftql/blob/main/LICENSE)

## Overview

GraftQL grafts a GraphQL API onto your SQL models. It builds on [SQLModel](https://sqlmodel.tiangolo.com/), [Strawberry GraphQL](https://strawberry.rocks/) and [FastAPI](https://fastapi.tiangolo.com/): define each model once as a `GraftModel`, mount a `GraftRouter`, and get queries, mutations, filters, pagination and N+1-safe relationships.

| You write | GraftQL gives you |
|---|---|
| `class Student(GraftModel, table=True)` | A table, a GraphQL type, a filter input and a paginated connection |
| `teacher: "Teacher" = Dl(source="teacher_id", target="id")` | A batched DataLoader-backed relationship field |
| `GraftRouter(engine=engine)` | A FastAPI router serving the whole schema |

{% include "templates/instalation.md" %}

Then follow [Getting started](Guide/Models.md) to define your first models.
