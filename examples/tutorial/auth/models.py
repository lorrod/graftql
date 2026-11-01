"""Auth tutorial models.

This tutorial focuses on *authorization* (row-level filtering + model-level
permissions), not on relationship modeling.

The key ideas:

- ``query_filter`` can restrict which rows are visible (e.g. by category)
- ``dl_filter`` can post-filter DataLoader results
- ``permission_getter`` can block access to entire models
"""

from graftql import Dl, Field, GraftModel


class Resource(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    category: str

    owner_id: str | None
    private_id: int | None

    owner: "Owner" = Dl(source="owner_id", target="id")
    private: "Private" = Dl(source="private_id", target="id")


class Owner(GraftModel, table=True):
    id: str | None = Field(primary_key=True, default=None)
    name: str

    resources: list["Resource"] = Dl(source="id", target="owner_id")
    privates: list["Private"] = Dl(source="id", target="owner_id")

    async def permission_getter(self: dict, request_type: str) -> bool:
        return "Owner" in self["user"]["classes"]


class Private(GraftModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    description: str

    owner_id: str
    owner: "Owner" = Dl(source="owner_id", target="id")
