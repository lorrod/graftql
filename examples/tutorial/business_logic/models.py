"""Business logic tutorial models.

This example demonstrates how to extend GraftQL with:

- custom resolvers (computed fields)
- custom mutations (domain actions)
- permission classes
- context injection (a request/session object available in resolvers)

The models use :class:`~graftql.Dl` for relationships so the tutorial stays
focused on GraftQL patterns.
"""

from graftql import Dl, Field, GraftModel


class StudentCourse(GraftModel, table=True):
    student_id: int = Field(primary_key=True)
    course_id: int = Field(primary_key=True)


class Student(GraftModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str

    courses: list["StudentCourse"] = Dl(source="id", target="student_id")


class Course(GraftModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    positive_feedbacks_count: int = Field(default=0)
    negative_feedbacks_count: int = Field(default=0)

    student_courses: list["StudentCourse"] = Dl(source="id", target="course_id")
