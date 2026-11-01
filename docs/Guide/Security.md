# Security

GraftQL's router accepts auxiliary hooks that enable access control at multiple levels of the API.



## Table Control


In most cases this is all you need: it controls access per table.

### permission_getter

If you want the same access-control logic across your API, define a function that receives the model class (a `GraftModel` subclass), the request context, and the request type (e.g. `'query'`, `'mutation'`), and returns a boolean indicating whether the request is permitted.

``` python
{!./examples/tutorial/auth/main.py[ln:44-47]!}

{!./examples/tutorial/auth/main.py[ln:65-67]!}
```

/// note

These hooks should be passed to `GraftRouter`.

``` python
{!./examples/tutorial/auth/main.py[ln:70-78]!}
```

for more details about context:[Strawberry](https://strawberry.rocks/docs/integrations/fastapi#context_getter).

///

/// tip

You can also define `permission_getter` on a `GraftModel` subclass to make the permission logic model-specific.

If you set a generic `permission_getter` in router and also in a model, the model `permission_getter` has priority above router's `permission_getter`

///

## Rows Control

For more complex access control (e.g. row-level filtering), you can provide additional query filter hooks to `GraftRouter`.

### query_filter

Adds a filter to every top-level query. In our example:

``` python
{!./examples/tutorial/auth/main.py[ln:44-47]!}

{!./examples/tutorial/auth/main.py[ln:58-62]!}
```

/// note

This function should return a SQLAlchemy filter statement.

///

### dl_filter


Post-filters the results returned by DataLoaders (relationship fields). In our example:

``` python
{!./examples/tutorial/auth/main.py[ln:44-47]!}

{!./examples/tutorial/auth/main.py[ln:50-55]!}
```

/// note

It receives the loaded rows and the context, and returns the filtered rows.

///