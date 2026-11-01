"""Tests for graftql loader helper classes (Dl and ManyRelation)."""

import pytest

from graftql import Dl, GraftModel, ManyRelation


def test_dl_target_type_mismatch_raises_value_error():
    """Dl should reject mismatched source/target type (str vs list[str])."""
    with pytest.raises(ValueError):
        Dl(source="id", target=["id"])  # type: ignore[arg-type]


def test_manyrelation_source_length_mismatch_raises_value_error():
    """ManyRelation should require same-length composite key lists."""

    class Target(GraftModel):
        pass

    class Relation(GraftModel):
        pass

    with pytest.raises(ValueError):
        ManyRelation(
            response_class=Target,
            relation_class=Relation,
            source=["a", "b"],
            source_relation=["a"],
            target=["c"],
            target_relation=["c"],
        )


def test_happy_path_dl_and_manyrelation_construct():
    """Smoke-test that Dl and ManyRelation can be constructed with valid inputs."""

    class Target(GraftModel):
        pass

    class Relation(GraftModel):
        pass

    dl = Dl(source="id", target="id")
    mr = ManyRelation(
        response_class=Target,
        relation_class=Relation,
        source="id",
        source_relation="source_id",
        target="id",
        target_relation="target_id",
    )

    assert dl.source == "id"
    assert dl.target == "id"
    assert mr.source == "id"
    assert mr.target == "id"
