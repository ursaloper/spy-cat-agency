from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .settings import Settings, get_settings


def get_app_settings() -> Settings:
    """Dependency wrapper for application settings."""
    return get_settings()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency wrapper for database session."""
    async for session in get_session():
        yield session
