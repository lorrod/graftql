"""Getting-started example: turn SQLModel models into a GraphQL API with GraftQL.

Run:
    uvicorn examples.tutorial.basic.main:app --reload
Then open:
    http://127.0.0.1:8000/graphql

Sample queries:

    query {
      students {
        many {
          edges {
            node { id name birthDate }
          }
        }
      }
    }

    query {
      courses {
        many {
          edges {
            node { id name }
          }
        }
      }
    }
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool

import examples.tutorial.basic.models as _models  # noqa: F401
from examples.tutorial.basic.models import Course, Student
from graftql import GraftModel, GraftRouter

# In-memory SQLite for a self-contained tutorial.
engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

# Create the tables for our GraftModel subclasses.
GraftModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Seed some data so users can run queries immediately.

    Kept in a lifespan hook (not module import time) so importing this module
    has no side-effects — important for test environments and tooling.
    """

    with Session(engine) as session:
        has_student = session.exec(select(Student.id).limit(1)).first() is not None
        if not has_student:
            session.add_all(
                [
                    Student(name="Ada Lovelace", birth_date=date(1815, 12, 10)),
                    Student(name="Alan Turing", birth_date=date(1912, 6, 23)),
                ]
            )

        has_course = session.exec(select(Course.id).limit(1)).first() is not None
        if not has_course:
            session.add_all([Course(name="Algorithms"), Course(name="Databases")])

        session.commit()
    yield


app = FastAPI(title="GraftQL basic tutorial", lifespan=lifespan)

# GraftRouter mounts a Strawberry-powered GraphQL endpoint for all registered GraftModel classes.
router = GraftRouter(engine=engine, enable_put_mutations=True, enable_delete_mutations=True)
app.include_router(router, prefix="/graphql")
