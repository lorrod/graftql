import strawberry

from examples.tutorial.federation.models_1 import *


@strawberry.federation.type(keys=["id"])
@strawberry.type
class Profile:
    id: strawberry.ID


def teacher(root: "Course") -> Profile:
    return Profile(id=f"app_2:{root.teacher_id}")


Course.__custom_resolvers__ = [teacher]
