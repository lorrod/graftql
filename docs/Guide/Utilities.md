# Utilities

## Computed fields

Add computed GraphQL fields by assigning plain resolver functions to `__custom_resolvers__`. Each function receives the model instance as `root`, and its name becomes the field name.

```python
{!./examples/tutorial/business_logic/logical_operations/resolvers.py[ln:3-11]!}
```

Resolvers can return scalars or Strawberry types.

/// note

For more details about Strawberry fields: [Strawberry](https://strawberry.rocks/docs/general/schema-basics).

///


## Auto Foreign Keys

GraftQL can create foreign keys based on DataLoader declarations. For to-one relations, the source field can be referenced to the target field.

```python
router = GraftRouter(engine=engine, auto_foreign_keys=True)
```

For example:

```python hl_lines="8"
{!./examples/tutorial/relationship/models.py[ln:25-32]!}
```

Here `course.teacher_id` gets a foreign key to `teacher.id`. `students` is a to-many relationship, so no foreign key is created for it.

/// note

If you want behavior different from the router default for a specific `Dl`, set `foreign_key` explicitly (e.g. `teacher: 'Teacher' = Dl(source='teacher_id', target='id', foreign_key=False)`).

///