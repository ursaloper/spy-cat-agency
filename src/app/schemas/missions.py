from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TargetCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(min_length=1, max_length=150)
    country: str = Field(min_length=1, max_length=80)
    notes: str = Field(default="", max_length=2000)
    complete: bool = Field(default=False)


class TargetUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    notes: str | None = Field(default=None, max_length=2000)
    complete: bool | None = None


class TargetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    name: str
    country: str
    notes: str
    complete: bool


class MissionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    targets: list[TargetCreate]

    @field_validator("targets")
    @classmethod
    def validate_targets_count(cls, value: list[TargetCreate]) -> list[TargetCreate]:
        if not (1 <= len(value) <= 3):
            raise ValueError("Mission must include between 1 and 3 targets")
        return value


class MissionAssign(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    cat_id: UUID


class MissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    assigned_cat_id: UUID | None
    complete: bool
    created_at: datetime
    targets: list[TargetRead]
