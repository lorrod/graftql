"""Federation tutorial models (service 1)."""

from graftql import Field, GraftModel


class Course(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    teacher_id: int = Field(default=None)
