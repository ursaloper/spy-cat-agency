from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/spy_cat_agency",
        alias="DATABASE_URL",
    )
    app_port: int = Field(default=8000, alias="APP_PORT")
    cat_api_base_url: HttpUrl | None = Field(default="https://api.thecatapi.com/v1", alias="CAT_API_BASE_URL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
