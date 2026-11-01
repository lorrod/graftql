"""Async engine example — same models as basic, but served via an async SQLAlchemy engine."""

from graftql import Field, GraftModel


class Item(GraftModel, table=True):
    __filter_attributes__ = {"name": {"required": False, "description": "Filter by item name"}}

    id: int | None = Field(primary_key=True, default=None)
    name: str
    quantity: int = 0
