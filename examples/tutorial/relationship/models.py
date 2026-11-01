"""Relationship tutorial models.

Demonstrates using :class:`~graftql.Dl` to declare 1-N and N-1 relationships.
The relationship fields are resolved via DataLoader (batched DB queries), giving
N+1-safe GraphQL resolvers out of the box.
"""

from datetime import date

from graftql import Dl, Field, GraftModel
from graftql.schemas.types import DateFilter


class Teacher(GraftModel, table=True):
    __filter_attributes__ = {"id": {"required": False}}

    id: int | None = Field(primary_key=True, default=None)
    name: str

    # Dl(source=...) points to this model's key field(s), Dl(target=...) points to
    # the related model field(s) that should match.
    courses: list["Course"] = Dl(source="id", target="teacher_id")


class Course(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    students: list["StudentCourse"] = Dl(source="id", target="course_id")

    teacher_id: int
    teacher: "Teacher" = Dl(source="teacher_id", target="id")


class Student(GraftModel, table=True):
    __filter_attributes__ = {
        "name": {"required": False},
        "birth_date": {"required": False, "filter_class": DateFilter},
    }

    id: int | None = Field(primary_key=True, default=None)
    name: str
    birth_date: date

    courses: list["StudentCourse"] = Dl(source="id", target="student_id")


class StudentCourse(GraftModel, table=True):
    student_id: int = Field(primary_key=True)
    course_id: int = Field(primary_key=True)

    student: "Student" = Dl(source="student_id", target="id")
    course: "Course" = Dl(source="course_id", target="id")

    grader: list["Grade"] = Dl(
        source=["student_id", "course_id"],
        target=["student_id", "course_id"],
    )


class Grade(GraftModel, table=True):
    student_id: int = Field(primary_key=True)
    course_id: int = Field(primary_key=True)
    grade: float
    semester: int = Field(primary_key=True)

    student_course: "StudentCourse" = Dl(
        source=["student_id", "course_id"],
        target=["student_id", "course_id"],
    )
