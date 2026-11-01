import re
from typing import Any, Callable

from pydantic import ConfigDict
from sqlmodel import SQLModel
from strawberry.types.base import StrawberryType

from ..loaders.dataloader import Dl, ManyRelation
from ..schemas.generators import OrderBy, get_dl_function, get_many_relation_function
from .setup import Setup


class GraftModel(SQLModel):
    """
    An extension of SQLModel that integrates Strawberry GraphQL functionalities,
    enabling the dynamic generation of GraphQL schemas directly from SQLModel definitions.
    This class supports configuring GraphQL operations such as queries and mutations,
    and facilitates the management of permissions for these operations.

    Attributes:
        __strawberry_schema__ (StrawberryType): Holds the GraphQL schema associated with
            this model, allowing for integration with the Strawberry GraphQL library.
        __enable_put_mutation__ (bool | None): Controls whether PUT mutations (update
            operations) are enabled for this model in the GraphQL API. Set to `True` to
            enable, `False` to disable, or `None` to use default settings.
        __enable_delete_mutation__ (bool | None): Determines whether DELETE mutations
            (delete operations) are enabled for this model in the GraphQL API. Set to
            `True` to enable, `False` to disable, or `None` to use default settings.
        __enable_query__ (bool | None): Specifies whether the model can be queried via
            the GraphQL API. Set to `True` to enable queries, `False` to disable, or
            `None` to leave it unset.
        __queryname__ (str): Provides a custom name for GraphQL queries related to this
            model. Defaults to the model's table name plus 's' (e.g., 'users' for a User
            model) if not explicitly set.
        __enginename__ (str): Identifier for the database engine used by this model,
            useful for applications that connect to multiple databases or require
            specific database configurations.
        __filter_attributes__ (Optional[dict[str, dict[str, Any]]]): Definition of filters allowed by the model,
            useful for filter attribute declarations. Defaults to `None`. Example
            { "id": {"required": True, "description": "Filter by ID", default: None} }
        __custom_resolvers__ (Optional[list[Callable]]): Definition of custom resolvers allowed by the model,
            useful to make custom attributes. Defaults to `None`. Example
            { full_name: Callable }. Can return basic types and strawberry types
        __directives__ (List[Any]): Maps
            Custom directives applied to model [Key(fields="id", resolvable=True)]
        __mutation_permission_classes__ (Dict[str, List[Type[BasePermission]]]): Maps
            specific mutation names to their respective permission classes. This allows
            for fine-grained control over which permissions apply to each mutation. If a
            mutation is not listed, it defaults to having no specific permissions.
        __default_order_by__ (dict[str, OrderBy] | str): Order by for database queries. Can be a string for
            backward compatibility or a dictionary with attribute as key and OrderBy as value.
            Example: {"id": OrderBy.ASC}
        __sql_preset_order_by__ (Optional[str]): Raw SQL string for setting a hidden ordering rule
        __sql_preset_filter__ (Optional[str]): Raw SQL string for setting a hidden filter condition
            for this model's queries.
    Classes:
        GraftModel: An extended SQLModel that incorporates GraphQL functionalities by using
        Strawberry GraphQL. This class allows defining GraphQL schemas, query names,
        engine names, and supports dynamic field resolution using dependency injection.

        Strawberry: An inner class used to encapsulate GraphQL-specific configurations
        and properties for the GraftModel class.
    Methods:
        __init_subclass__: Automatically called when a subclass of GraftModel is defined.
            Sets up the necessary GraphQL configurations and registers the subclass in a
            setup registry for further reference.
        permission_getter: Async static method intended to be overridden to provide
            custom logic for determining user permissions for executing GraphQL queries.
            Should return `True` if the query is permitted, `False` otherwise.
    """

    __strawberry_schema__: StrawberryType = None
    __enable_put_mutation__: bool | None = None
    __enable_delete_mutation__: bool | None = None
    __enable_query__: bool | None = None
    __queryname__: str = ""
    __enginename__: str = "default"
    __default_order_by__: dict[str, OrderBy] = {"id": OrderBy.ASC}
    __sql_preset_order_by__: str | None = None
    __sql_preset_filter__: str | None = None
    __filter_attributes__: dict[str, dict[str, Any]] | None = None
    __custom_resolvers__: list[Callable] | None = None
    __custom_mutations__: list[Callable] | None = None
    __directives__: list | None = None
    __mutation_permission_classes__ = {}
    model_config = ConfigDict(arbitrary_types_allowed=True)

    class Strawberry:
        pass

    def __init_subclass__(cls):
        if not cls.__tablename__:
            cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        cls.__queryname__ = cls.__queryname__ if cls.__queryname__ else cls.__tablename__ + "s"
        Setup.classes[cls.__name__] = cls
        to_remove = []
        for attr_name, attr_type in cls.__annotations__.items():
            if hasattr(cls, attr_name):
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, Dl):
                    to_remove.append(attr_name)
                    dl_field = get_dl_function(attr_name, attr_type, attr_value)
                    setattr(cls, attr_name, dl_field)
                elif isinstance(attr_value, ManyRelation):
                    to_remove.append(attr_name)
                    dl_field = get_many_relation_function(
                        attr_name, attr_type, attr_value, source_model=cls
                    )
                    setattr(cls, attr_name, dl_field)
        for attr in to_remove:
            del cls.__annotations__[attr]

    async def permission_getter(self: dict, request_type: str) -> bool:
        pass
