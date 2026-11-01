"""Shared pytest fixtures and configuration for the graftql test suite."""
import pytest
import pytest_asyncio

from graftql import Setup


@pytest.fixture(scope="module")
def clear_classes():
    from sqlmodel.main import default_registry

    from graftql import GraftModel

    Setup.classes = {}
    Setup.async_engine = False
    GraftModel.metadata.clear()
    default_registry.dispose()
    yield
    Setup.classes = {}
    Setup.async_engine = False
    GraftModel.metadata.clear()
    default_registry.dispose()


@pytest.fixture(scope="module")
def client(clear_classes):
    """Test client for basic CRUD tests.

    This is intentionally self-contained (no dependency on tutorial examples),
    because examples may change for pedagogy (seed data, simplified models) and
    should not affect CI.
    """

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlmodel import create_engine
    from sqlmodel.pool import StaticPool

    from graftql import Field, GraftModel, GraftRouter

    engine = create_engine(
        "sqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    class Student(GraftModel, table=True):
        __enable_put_mutation__ = True
        __enable_delete_mutation__ = True

        id: int | None = Field(primary_key=True, default=None)
        name: str
        birth_date: str

    class StudentCourse(GraftModel, table=True):
        __enable_put_mutation__ = True

        student_id: int = Field(primary_key=True)
        course_id: int = Field(primary_key=True)

    GraftModel.metadata.create_all(engine)

    app = FastAPI()
    router = GraftRouter(engine=engine, enable_put_mutations=True, enable_delete_mutations=True)
    app.include_router(router, prefix="/graphql")

    Setup.setup(engine)
    yield TestClient(app)


@pytest.fixture(scope="module")
def client_data(clear_classes):
    import importlib

    from fastapi.testclient import TestClient
    from sqlmodel.main import default_registry

    from examples.tutorial.relationship import main, models
    from graftql import GraftModel, Setup

    Setup.classes = {}
    GraftModel.metadata.clear()
    default_registry.dispose()

    importlib.reload(models)
    importlib.reload(main)

    return TestClient(main.app)


@pytest_asyncio.fixture(scope="module")
async def client_async(clear_classes):
    from fastapi import FastAPI
    from httpx import ASGITransport, AsyncClient
    from sqlalchemy.ext.asyncio import create_async_engine

    from graftql import Field, GraftModel, GraftRouter

    app = FastAPI()

    engine = create_async_engine(
        "sqlite+aiosqlite:///",
        connect_args={"check_same_thread": False},
    )

    class User(GraftModel, table=True):
        __enable_put_mutation__ = True
        __enable_delete_mutation__ = True
        id: int | None = Field(primary_key=True, default=None)
        name: str
        qtd: int

    async with engine.begin() as conn:
        await conn.run_sync(GraftModel.metadata.create_all)

    router = GraftRouter(engine=engine)
    app.include_router(router, prefix="/graphql")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def client_auth(clear_classes):
    import importlib

    from fastapi.testclient import TestClient
    from sqlmodel.main import default_registry

    from examples.tutorial.auth import main, models
    from graftql import GraftModel, Setup

    Setup.classes = {}
    GraftModel.metadata.clear()
    default_registry.dispose()

    importlib.reload(models)
    importlib.reload(main)

    return TestClient(main.app)
