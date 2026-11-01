# GraftQL contributor guide

GraftQL turns `GraftModel` subclasses into a Strawberry GraphQL schema mounted through FastAPI.
Keep changes compatible with both synchronous and asynchronous SQLAlchemy engines.

## Repository map

- `graftql/core/` contains model registration, setup, and the FastAPI router.
- `graftql/schemas/` generates Strawberry types, filters, queries, and mutations.
- `graftql/loaders/` implements relationship DataLoaders.
- `tests/` is the authoritative behavior suite; `examples/tutorial/` is runnable documentation.
- `docs/` is the MkDocs source.

## Setup and verification

```bash
uv sync --all-groups --all-extras
uv run --group dev ruff check .
uv run --group dev --with pytest-cov pytest --cov=graftql --cov-report=term-missing
uv run --extra doc mkdocs build --strict
uv build
```

Run the test suite on Python 3.12 and 3.13 when changing generated schemas, dependencies, or
runtime behavior.

## Working agreements

- Treat imports from `graftql/__init__.py` as the public API.
- Ensure model modules are imported before constructing `GraftRouter`; model discovery happens when
  `GraftModel` subclasses are defined.
- Keep PUT and DELETE mutations opt-in through the router or model flags.
- Add focused regression tests for schema-generation, permissions, filtering, or relationship changes.
- Update `uv.lock` with `uv lock` when dependency constraints change.
- Prefer supported SQLModel, Strawberry, FastAPI, and GraphQL-core APIs over their internals.
