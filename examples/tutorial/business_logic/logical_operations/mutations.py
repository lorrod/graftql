"""Custom mutations for the business-logic tutorial."""

from enum import StrEnum

import strawberry

import graftql
from examples.tutorial.business_logic.logical_operations.permissions import IsStudentCourse
from examples.tutorial.business_logic.models import Course


@strawberry.enum
class FeedbackType(StrEnum):
    POSITIVE: str = "POSITIVE"
    NEGATIVE: str = "NEGATIVE"


@strawberry.input
class CourseFeedback:
    course_id: int
    type: FeedbackType


def leave_feedback(
    input: CourseFeedback,
    info: strawberry.Info,
) -> strawberry.LazyType["CourseSchema", "graftql.core.router"]:  # type: ignore
    # Increment the appropriate counter and persist via the injected session.
    session = info.context["session"]
    permission_object = info.context["permission_object"]
    if input.type == FeedbackType.POSITIVE:
        permission_object.positive_feedbacks_count += 1
    elif input.type == FeedbackType.NEGATIVE:
        permission_object.negative_feedbacks_count += 1
    else:
        raise Exception(f"Invalid feedback type: {input.type}")
    session.commit()
    session.refresh(permission_object)
    return permission_object


Course.__custom_mutations__ = [leave_feedback]
Course.__mutation_permission_classes__ = {leave_feedback.__name__: [IsStudentCourse]}
