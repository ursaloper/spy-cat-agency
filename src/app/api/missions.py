from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_db_session
from ..schemas.missions import MissionAssign, MissionCreate, MissionRead, TargetRead, TargetUpdate
from ..services.mission_service import MissionService

router = APIRouter(prefix="/missions", tags=["missions"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_mission_service(session: SessionDep) -> MissionService:
    """Build MissionService with injected session."""
    return MissionService(session)


@router.post("", response_model=MissionRead, status_code=status.HTTP_201_CREATED)
async def create_mission(payload: MissionCreate, service: Annotated[MissionService, Depends(get_mission_service)]) -> MissionRead:
    """Create a mission with 1–3 targets."""
    return await service.create_mission(payload)


@router.get("", response_model=list[MissionRead])
async def list_missions(service: Annotated[MissionService, Depends(get_mission_service)]) -> list[MissionRead]:
    """List all missions with targets."""
    return await service.list_missions()


@router.get("/{mission_id}", response_model=MissionRead)
async def get_mission(mission_id: UUID, service: Annotated[MissionService, Depends(get_mission_service)]) -> MissionRead:
    """Get mission details with targets."""
    return await service.get_mission(mission_id)


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission(mission_id: UUID, service: Annotated[MissionService, Depends(get_mission_service)]) -> None:
    """Delete mission if it has no assigned cat."""
    await service.delete_mission(mission_id)
    return None


@router.post("/{mission_id}/assign", response_model=MissionRead)
async def assign_cat(
    mission_id: UUID, payload: MissionAssign, service: Annotated[MissionService, Depends(get_mission_service)]
) -> MissionRead:
    """Assign cat to mission with busy checks."""
    return await service.assign_cat(mission_id, payload)


@router.patch("/{mission_id}/targets/{target_id}", response_model=TargetRead)
async def update_target(
    mission_id: UUID,
    target_id: UUID,
    payload: TargetUpdate,
    service: Annotated[MissionService, Depends(get_mission_service)],
) -> TargetRead:
    """Update target notes or completion status."""
    return await service.update_target(mission_id, target_id, payload)
