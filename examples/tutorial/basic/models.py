"""Basic tutorial models.

This is the simplest possible GraftQL example: a couple of SQLModel tables that
automatically become a typed GraphQL API when mounted via :class:`~graftql.GraftRouter`.
"""

from datetime import date

from graftql import Field, GraftModel


class Student(GraftModel, table=True):
    __filter_attributes__ = {
        "name": {"required": False, "description": "Filter by name"},
    }

    id: int | None = Field(primary_key=True, default=None)
    name: str
    birth_date: date


class Course(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
