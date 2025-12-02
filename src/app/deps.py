from collections.abc import Generator

from .settings import Settings, get_settings


def get_app_settings() -> Settings:
    return get_settings()


def get_dummy_session() -> Generator[None, None, None]:
    # Placeholder for database session dependency.
    yield None
