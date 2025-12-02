from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .settings import Settings, get_settings


def get_app_settings() -> Settings:
    return get_settings()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session
