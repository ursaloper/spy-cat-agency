from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_db_session
from ..schemas.cats import CatCreate, CatRead, CatUpdateSalary
from ..services.cat_service import CatService

router = APIRouter(prefix="/cats", tags=["cats"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_cat_service(session: SessionDep) -> CatService:
    """Build CatService with injected session."""
    return CatService(session)


@router.post("", response_model=CatRead, status_code=status.HTTP_201_CREATED)
async def create_cat(payload: CatCreate, service: Annotated[CatService, Depends(get_cat_service)]) -> CatRead:
    """Create a new cat."""
    return await service.create_cat(payload)


@router.get("", response_model=list[CatRead])
async def list_cats(service: Annotated[CatService, Depends(get_cat_service)]) -> list[CatRead]:
    """List all cats."""
    return await service.list_cats()


@router.get("/{cat_id}", response_model=CatRead)
async def get_cat(cat_id: UUID, service: Annotated[CatService, Depends(get_cat_service)]) -> CatRead:
    """Get a single cat by id."""
    return await service.get_cat(cat_id)


@router.patch("/{cat_id}/salary", response_model=CatRead)
async def update_cat_salary(cat_id: UUID, payload: CatUpdateSalary, service: Annotated[CatService, Depends(get_cat_service)]) -> CatRead:
    """Update salary for a cat."""
    return await service.update_salary(cat_id, payload)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: UUID, service: Annotated[CatService, Depends(get_cat_service)]) -> None:
    """Delete a cat if it is not assigned to an active mission."""
    await service.delete_cat(cat_id)
    return None
