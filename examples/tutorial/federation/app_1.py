"""Federation tutorial (service 1).

This module defines "service 1" of a two-service Apollo Federation v2 example.
Run this app on one port, and :mod:`examples.tutorial.federation.app_2` on
another, then compose them in a federated gateway.
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

from examples.tutorial.federation.context import get_context, get_session
from examples.tutorial.federation.logical_operations_1 import *
from graftql import GraftModel, GraftRouter

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

GraftModel.metadata.create_all(engine)

app = FastAPI(title="GraftQL federation tutorial - service 1")
router = GraftRouter(
    engine=engine,
    context_session=get_session,
    context_getter=get_context,
    enable_put_mutations=True,
    enable_delete_mutations=True,
    enable_federation_2=True,
)
app.include_router(router, prefix="/graphql")

# Expose the underlying Strawberry schema for federation composition tooling.
schema = router.schema
