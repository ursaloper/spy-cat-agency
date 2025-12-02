from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..clients.cat_api import validate_breed
from ..models import Cat, Mission
from ..schemas.cats import CatCreate, CatUpdateSalary


class CatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_cat(self, payload: CatCreate) -> Cat:
        is_valid = await validate_breed(payload.breed)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Breed is not valid according to TheCatAPI",
            )
        cat = Cat(
            name=payload.name,
            years_experience=payload.years_experience,
            breed=payload.breed,
            salary=payload.salary,
        )
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return cat

    async def list_cats(self) -> list[Cat]:
        result = await self.session.execute(select(Cat))
        return list(result.scalars().all())

    async def get_cat(self, cat_id: UUID) -> Cat:
        cat = await self.session.get(Cat, cat_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
        return cat

    async def update_salary(self, cat_id: UUID, payload: CatUpdateSalary) -> Cat:
        cat = await self.get_cat(cat_id)
        cat.salary = payload.salary
        await self.session.commit()
        await self.session.refresh(cat)
        return cat

    async def delete_cat(self, cat_id: UUID) -> None:
        cat = await self.get_cat(cat_id)
        active_mission = await self.session.execute(select(Mission).where(Mission.assigned_cat_id == cat_id, Mission.complete.is_(False)))
        if active_mission.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cat cannot be removed while assigned to an active mission",
            )
        await self.session.delete(cat)
        await self.session.commit()
