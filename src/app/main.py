from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import cats as cats_router
from .db import Base, engine
from .deps import get_app_settings
from .settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    current_settings = settings or get_app_settings()
    application = FastAPI(
        title="Spy Cat Agency API",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.include_router(cats_router.router)

    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "env": "dev", "port": str(current_settings.app_port)}

    return application


app = create_app()
