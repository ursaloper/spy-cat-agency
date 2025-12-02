from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import get_settings


class Base(DeclarativeBase):
    """Base declarative class for ORM models."""

    pass


def _build_engine() -> AsyncEngine:
    """Create async SQLAlchemy engine from settings."""
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=False, future=True)


engine: AsyncEngine = _build_engine()
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async SQLAlchemy session dependency."""
    async with AsyncSessionFactory() as session:
        yield session
