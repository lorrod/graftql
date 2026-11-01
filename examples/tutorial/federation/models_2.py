"""Federation tutorial models (service 2)."""

from graftql import Field, GraftModel


class Profile(GraftModel, table=True):
    db_id: int = Field(primary_key=True)
    name: str
