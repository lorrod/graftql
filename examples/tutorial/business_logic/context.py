from fastapi import Request
from sqlalchemy import Engine
from sqlmodel import Session


def get_session(engine: Engine) -> Session:
    return Session(engine, expire_on_commit=False)


async def get_context(request: Request, response, existing_context: dict):
    user_id = request.headers.get("userId")
    if user_id:
        existing_context["user_id"] = int(user_id)

    return existing_context
