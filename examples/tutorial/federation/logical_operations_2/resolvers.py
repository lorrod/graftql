import strawberry

from examples.tutorial.federation.models_2 import *


def id(root: "Profile") -> strawberry.ID:
    return strawberry.ID(f"app_2:{root.db_id}")


Profile.__custom_resolvers__ = [id]
