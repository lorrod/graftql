"""Tests for graftql Setup configuration and registry behavior."""

from __future__ import annotations

from sqlmodel import create_engine

from graftql import GraftModel, Setup


def test_setup_accepts_single_engine_and_sets_default():
    """Setup.setup() should accept a single Engine and store it under 'default'."""
    engine = create_engine("sqlite://")
    Setup.setup(engine)
    assert isinstance(Setup.engine, dict)
    assert "default" in Setup.engine


def test_classes_registry_populated_via_bootmodel_subclass():
    """GraftModel subclass registration should populate Setup.classes."""
    Setup.classes = {}

    class User(GraftModel):
        pass

    assert "User" in Setup.classes
    assert Setup.classes["User"] is User
