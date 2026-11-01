"""Many-to-many relationship tutorial models.

This example compares:

- :class:`~graftql.Dl`: direct, single-hop relationships (1-N, N-1)
- :class:`~graftql.ManyRelation`: a convenience helper for many-to-many fields
  that traverse through a link table (``relation_class``).

Use ``ManyRelation`` when you want the GraphQL field to expose the *target*
records directly (e.g. ``Student.courses -> list[Course]``), while still
storing the relationship in a link table.
"""

from datetime import date

from graftql import Dl, Field, GraftModel, ManyRelation


class Teacher(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    courses: list["Course"] = Dl(source="id", target="teacher_id")


class Course(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    students: list["StudentCourse"] = Dl(source="id", target="course_id")

    teacher_id: int
    teacher: "Teacher" = Dl(source="teacher_id", target="id")


class StudentCourse(GraftModel, table=True):
    student_id: int = Field(primary_key=True)
    course_id: int = Field(primary_key=True)

    student: "Student" = Dl(source="student_id", target="id")
    course: "Course" = Dl(source="course_id", target="id")

    grader: list["Grade"] = Dl(
        source=["student_id", "course_id"],
        target=["student_id", "course_id"],
    )


class Student(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    birth_date: date

    # ManyRelation params:
    # - response_class: the type returned by this field (Course)
    # - relation_class: the link table model (StudentCourse)
    # - source/source_relation: how to match Student -> StudentCourse
    # - target/target_relation: how to match Course -> StudentCourse
    courses: list["Course"] = ManyRelation(
        response_class=Course,
        relation_class=StudentCourse,
        source="id",
        source_relation="student_id",
        target="id",
        target_relation="course_id",
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
