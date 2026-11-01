"""Business-logic tutorial for GraftQL.

Demonstrates custom resolvers, custom mutations, permission classes, and
context injection.  See ``logical_operations/`` for implementation details.

Run:
    uvicorn examples.tutorial.business_logic.main:app --reload
Then open:
    http://127.0.0.1:8000/graphql
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from examples.tutorial.business_logic.context import get_context, get_session
from examples.tutorial.business_logic.logical_operations import *
from graftql import GraftModel, GraftRouter

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

GraftModel.metadata.create_all(engine)

# Import model names exposed via the wildcard import above.
from examples.tutorial.business_logic.models import Course, Student, StudentCourse

with Session(engine) as session:
    session.add(Course(name="Mathematics"))
    session.add(Course(name="Physics"))
    session.add(Student(first_name="Some", last_name="Name"))
    session.add(Student(first_name="Other", last_name="Name"))
    session.add(Student(first_name="Another", last_name="Name"))
    session.add(StudentCourse(student_id=1, course_id=1))
    session.add(StudentCourse(student_id=2, course_id=1))
    session.add(StudentCourse(student_id=2, course_id=2))
    session.add(StudentCourse(student_id=3, course_id=1))
    session.commit()

app = FastAPI(title="GraftQL business-logic tutorial")
router = GraftRouter(
    engine=engine,
    context_session=get_session,
    context_getter=get_context,
    enable_put_mutations=True,
)
app.include_router(router, prefix="/graphql")
