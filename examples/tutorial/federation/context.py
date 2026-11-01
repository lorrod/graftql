from fastapi import Request
from sqlalchemy import Engine
from sqlmodel import Session


def get_session(engine: Engine) -> Session:
    return Session(engine, expire_on_commit=False)


async def get_context(request: Request, response, existing_context: dict):
    name = request.headers.get("name")
    id = request.headers.get("id")
    if id and name:
        existing_context["user"] = {"id": int(id), "name": name}

    return existing_context
