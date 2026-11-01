"""Federation tutorial (service 2).

This module defines "service 2" of a two-service Apollo Federation v2 example.
Run this app on a different port from service 1, then compose them in a federated gateway.
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

from examples.tutorial.federation.logical_operations_2 import *
from graftql import GraftModel, GraftRouter

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

GraftModel.metadata.create_all(engine)

app = FastAPI(title="GraftQL federation tutorial - service 2")
router = GraftRouter(
    engine=engine,
    enable_put_mutations=True,
    enable_delete_mutations=True,
    enable_federation_2=True,
)
app.include_router(router, prefix="/graphql")

# Expose the underlying Strawberry schema for federation composition tooling.
schema = router.schema
