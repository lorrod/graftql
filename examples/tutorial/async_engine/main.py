"""Async engine example for GraftQL.

Demonstrates using an async SQLAlchemy engine (aiosqlite) with GraftRouter.
GraftQL detects the async engine automatically and uses async sessions throughout.

Run:
    uvicorn examples.tutorial.async_engine.main:app --reload
Then open:
    http://127.0.0.1:8000/graphql
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

import examples.tutorial.async_engine.models as _models  # noqa: F401
from graftql import GraftModel, GraftRouter

DATABASE_URL = "sqlite+aiosqlite:///./async_dev.db"
engine = create_async_engine(DATABASE_URL, echo=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(GraftModel.metadata.create_all)


app = FastAPI(title="GraftQL async engine tutorial")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


# Pass the async engine — GraftQL detects it and uses async sessions automatically.
router = GraftRouter(engine=engine, enable_put_mutations=True, enable_delete_mutations=True)
app.include_router(router, prefix="/graphql")

# Sample queries:
# mutation { items { put(input: { name: "Widget", quantity: 10 }) { id name quantity } } }
# query    { items { many { edges { node { id name quantity } } } } }
