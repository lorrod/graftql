"""Auth (authorization) tutorial for GraftQL.

Demonstrates:
- ``permission_getter``: block or allow access to an entire model.
- ``query_filter``: filter rows returned by top-level queries based on context.
- ``dl_filter``: post-filter DataLoader (relationship) results.

The simulated user has access only to category "A" and "B" resources and to
the Owner / Resource models.  Requests for category "C" or the Private model
will be rejected.

Run:
    uvicorn examples.tutorial.auth.main:app --reload
Then open:
    http://127.0.0.1:8000/graphql
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from graftql import GraftModel, GraftRouter

from .models import Owner, Private, Resource

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
GraftModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Owner(id="1", name="Center 1"))
    session.add(Resource(id=1, name="Base 1", category="A", owner_id="1", private_id=1))
    session.add(Resource(id=2, name="Base 2", category="B", owner_id="1", private_id=1))
    session.add(Resource(id=3, name="Base 3", category="C", owner_id="2", private_id=None))
    session.add(Private(id=1, description="Extra 1", owner_id="1"))
    session.commit()


async def get_context(request, response):
    # In a real app you would derive the user from a JWT or session cookie.
    user = {"categories": ["A", "B"], "classes": ["Resource", "Owner"]}
    return {"user": user}


def dl_filter(data, context):
    """Post-filter DataLoader results so relationship fields respect category access."""
    user = context["user"]
    if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], Resource):
        return [d for d in data if d.category in user["categories"]]
    return data


def query_filter(model, context):
    """Add a WHERE clause to top-level queries based on the requesting user's allowed categories."""
    if model.__name__ == "Resource":
        return model.category.in_(context["user"]["categories"])
    return True


async def permission_getter(module_class, context, request_type):
    """Allow access only to models listed in the user's `classes`."""
    return module_class.__name__ in context["user"]["classes"]


app = FastAPI(title="GraftQL auth tutorial")
router = GraftRouter(
    engine=engine,
    dl_filter=dl_filter,
    query_filter=query_filter,
    permission_getter=permission_getter,
    context_getter=get_context,
)
app.include_router(router, prefix="/graphql")
