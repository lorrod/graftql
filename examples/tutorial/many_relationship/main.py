"""Many-to-many relationship tutorial for GraftQL.

Demonstrates ManyRelation for direct many-to-many traversal in GraphQL,
plus Dl for standard 1-N and N-1 relationships.

Run:
    uvicorn examples.tutorial.many_relationship.main:app --reload
Then open:
    http://127.0.0.1:8000/graphql

Sample queries:

    query {
      students {
        many {
          edges {
            node {
              id
              name
              # ManyRelation exposes Course directly (no link-table hop):
              courses { id name }
            }
          }
        }
      }
    }

    query {
      courses {
        many {
          edges {
            node {
              id
              name
              teacher { id name }
              students { student { id name } }
            }
          }
        }
      }
    }
"""

from __future__ import annotations

from datetime import date

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from examples.tutorial.many_relationship.models import (
    Course,
    Grade,
    Student,
    StudentCourse,
    Teacher,
)
from graftql import GraftModel, GraftRouter

engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
GraftModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Teacher(name="Some Teacher"))
    session.add(Course(name="Mathematics", teacher_id=1))
    session.add(Course(name="Physics", teacher_id=1))
    session.add(Student(name="Some Name", birth_date=date(1999, 9, 16)))
    session.add(Student(name="Other Name", birth_date=date(1999, 7, 24)))
    session.add(Student(name="Another Name", birth_date=date(1998, 5, 12)))
    session.add(StudentCourse(student_id=1, course_id=1))
    session.add(StudentCourse(student_id=1, course_id=2))
    session.add(StudentCourse(student_id=2, course_id=1))
    session.add(StudentCourse(student_id=2, course_id=2))
    session.add(StudentCourse(student_id=3, course_id=1))
    session.add(Grade(student_id=1, course_id=1, grade=10.0, semester=1))
    session.add(Grade(student_id=1, course_id=2, grade=9.0, semester=1))
    session.add(Grade(student_id=2, course_id=1, grade=8.0, semester=1))
    session.commit()

app = FastAPI(title="GraftQL many-to-many relationship tutorial")
router = GraftRouter(engine=engine, enable_put_mutations=True, enable_delete_mutations=True)
app.include_router(router, prefix="/graphql")
