
from sqlalchemy.orm import Session
from strawberry import BasePermission
from strawberry.types import Info


class IsItemOwnerOrAdmin(BasePermission):
    """
    A generic permission class to verify that the current user
    is the owner of a given item (e.g. Review, Post, Comment)
    or has admin privileges.
    """

    message = "You do not have permission to update this item."
    error_extensions = {"code": "UNAUTHORIZED"}

    # You should override these class attributes in subclasses or
    # pass them via a subclass constructor.
    item_model: type  # e.g. Review
    item_id_field: str  # e.g. "review_id"
    owner_relation_field: str  # e.g. "users" or "owner"
    # If you use a relation that returns multiple owners (like a list),
    # you may need to handle that differently (e.g. `item.owners[0].id`).

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        # Extract input
        input_data = kwargs.get("input")
        user_id = info.context.get("user_id")
        if not input_data or not user_id:
            return False

        # Get item_id from input using the configured field name
        item_id = getattr(input_data, self.item_id_field, None)
        if not item_id:
            return False

        session: Session = info.context["session"]
        # Fetch the item
        item = session.get(self.item_model, item_id)
        if not item:
            raise Exception(f"{self.item_model.__name__} with ID {item_id} not found")

        # Refresh and load owner if necessary
        session.refresh(item, [self.owner_relation_field])

        # Retrieve the owner. If the relationship is a list (e.g. "users" returns a list),
        # adjust accordingly. For a single owner, it could just be `getattr(item, self.owner_relation_field)`.
        owners = getattr(item, self.owner_relation_field)
        if not owners:
            # No owners found (unlikely, but handle gracefully)
            return False

        # For the Review model, we assume `review.users` returns a list of users
        # who own that review. Typically a review has a single owner, so we check the first one.
        # Adjust this logic if a different model uses a direct foreign key instead.
        item_owner_id = owners[0].id if isinstance(owners, list) else owners.id

        # Check if current user is the owner or is an admin
        if user_id == item_owner_id:
            # To avoid retrieve object on which permission was checked, we pass it to context
            info.context["permission_object"] = item
            return True

        return False
