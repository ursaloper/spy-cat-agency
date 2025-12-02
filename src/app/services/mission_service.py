from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Cat, Mission, Target
from ..schemas.missions import MissionAssign, MissionCreate, TargetUpdate


class MissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_mission(self, mission_id: UUID, with_targets: bool = False) -> Mission:
        stmt = select(Mission).where(Mission.id == mission_id)
        if with_targets:
            stmt = stmt.options(selectinload(Mission.targets))
        result = await self.session.execute(stmt)
        mission = result.scalars().first()
        if not mission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
        return mission

    async def list_missions(self) -> list[Mission]:
        result = await self.session.execute(select(Mission).options(selectinload(Mission.targets)))
        return list(result.scalars().all())

    async def get_mission(self, mission_id: UUID) -> Mission:
        return await self._get_mission(mission_id, with_targets=True)

    async def create_mission(self, payload: MissionCreate) -> Mission:
        targets_payload = payload.targets
        if not (1 <= len(targets_payload) <= 3):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Mission must include between 1 and 3 targets",
            )
        mission = Mission()
        self.session.add(mission)
        await self.session.flush()
        targets = [
            Target(
                mission_id=mission.id,
                name=target.name,
                country=target.country,
                notes=target.notes,
                complete=target.complete,
            )
            for target in targets_payload
        ]
        self.session.add_all(targets)
        await self.session.commit()
        await self.session.refresh(mission)
        await self.session.refresh(mission, attribute_names=["targets"])
        await self._update_mission_completion(mission)
        await self.session.refresh(mission, attribute_names=["targets"])
        return mission

    async def delete_mission(self, mission_id: UUID) -> None:
        mission = await self._get_mission(mission_id)
        if mission.assigned_cat_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Mission cannot be deleted while assigned to a cat",
            )
        await self.session.delete(mission)
        await self.session.commit()

    async def assign_cat(self, mission_id: UUID, payload: MissionAssign) -> Mission:
        mission = await self._get_mission(mission_id, with_targets=True)
        if mission.complete:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Completed mission cannot be assigned",
            )
        if mission.assigned_cat_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Mission already has an assigned cat",
            )

        cat = await self.session.get(Cat, payload.cat_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")

        busy_mission = await self.session.execute(
            select(Mission).where(and_(Mission.assigned_cat_id == payload.cat_id, Mission.complete.is_(False)))
        )
        if busy_mission.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cat is busy with another active mission")

        mission.assigned_cat_id = payload.cat_id
        await self.session.commit()
        await self.session.refresh(mission)
        await self.session.refresh(mission, attribute_names=["targets"])
        return mission

    async def update_target(self, mission_id: UUID, target_id: UUID, payload: TargetUpdate) -> Target:
        mission = await self._get_mission(mission_id, with_targets=True)
        target = next((t for t in mission.targets if t.id == target_id), None)
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")

        if mission.complete or target.complete:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot update target because it or its mission is completed",
            )

        if payload.notes is not None:
            target.notes = payload.notes
        if payload.complete is not None:
            target.complete = payload.complete

        await self.session.commit()
        await self._update_mission_completion(mission)
        await self.session.refresh(target)
        return target

    async def _update_mission_completion(self, mission: Mission) -> None:
        if all(target.complete for target in mission.targets):
            mission.complete = True
            await self.session.commit()
            await self.session.refresh(mission)
