"""Custom resolvers for the business-logic tutorial."""

from examples.tutorial.business_logic.models import Student


def full_name(root: "Student") -> str:
    # A simple computed field that is exposed via GraphQL.
    return " ".join([root.first_name, root.last_name])


Student.__custom_resolvers__ = [full_name]
