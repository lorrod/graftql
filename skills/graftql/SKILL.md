---
name: graftql
description: Build or modify FastAPI GraphQL APIs with GraftQL and SQLModel, including models, routers, relationships, permissions, async engines, and tests. Use when a project imports graftql or explicitly asks to adopt GraftQL; do not use for generic Strawberry or SQLModel projects that do not use GraftQL.
---

# GraftQL

Use the project's installed GraftQL version and existing conventions. Inspect current models, engine
setup, router construction, and tests before changing them.

## Build the integration

1. Add `graftql` to the project's Python dependencies.
2. Define database models as `GraftModel` subclasses with `table=True`. Import `Field` from
   `graftql` or `sqlmodel`.
3. Import every model module before constructing `GraftRouter`; subclasses register when Python
   defines them.
4. Create the database tables through `GraftModel.metadata`. For an async engine, call
   `await connection.run_sync(GraftModel.metadata.create_all)` inside `engine.begin()`.
5. Construct `GraftRouter(engine=engine)` and include it in the FastAPI application. PUT and DELETE
   mutations are disabled unless enabled on the router or model.

Use this minimal synchronous shape when the project has no established layout:

```python
from fastapi import FastAPI
from sqlmodel import create_engine

from graftql import Field, GraftModel, GraftRouter


class Item(GraftModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


engine = create_engine("sqlite:///app.db")
GraftModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(GraftRouter(engine=engine), prefix="/graphql")
```

## Extend deliberately

- Declare relationships with `Dl`; use `list[Target]` for to-many relationships. Use
  `ManyRelation` when GraphQL should expose a many-to-many target directly.
- Put application-wide access control in `GraftRouter` hooks: `permission_getter`, `query_filter`,
  and `dl_filter`. Model-specific permission logic takes precedence over the router hook.
- Add computed GraphQL fields through the project's supported custom-resolver pattern rather than
  duplicating the generated schema manually.
- Pass a mapping of engines and set `__enginename__` on models only when the application genuinely
  uses multiple databases.

## Verify the result

- Exercise the `/graphql` endpoint with a real query, not only an import test.
- Test reads and every mutation explicitly enabled by the change.
- Test relationship batching or permission behavior when either is touched.
- Preserve both sync and async behavior when editing shared library code.

Use the canonical guides for details: [models](https://lorrod.github.io/graftql/Guide/Models/),
[relationships](https://lorrod.github.io/graftql/Guide/Relationships/), and
[security](https://lorrod.github.io/graftql/Guide/Security/).
