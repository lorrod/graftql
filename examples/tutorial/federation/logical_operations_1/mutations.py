import strawberry

import graftql
from examples.tutorial.federation.models_1 import Course


@strawberry.input
class CreateCourse:
    name: str


def create(
    input: CreateCourse,
    info: strawberry.Info,
) -> strawberry.LazyType["CourseSchema", "graftql.core.router"]:  # type: ignore
    if not info.context.get("user"):
        raise Exception("User must be logged in")
    session = info.context["session"]
    course = Course(
        name=input.name,
        teacher_id=info.context["user"]["id"],
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


Course.__custom_mutations__ = [create]
