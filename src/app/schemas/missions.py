from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TargetCreate(BaseModel):
    """Payload for creating a mission target."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(min_length=1, max_length=150)
    country: str = Field(min_length=1, max_length=80)
    notes: str = Field(default="", max_length=2000)
    complete: bool = Field(default=False)


class TargetUpdate(BaseModel):
    """Payload for updating target notes or completion."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    notes: str | None = Field(default=None, max_length=2000)
    complete: bool | None = None


class TargetRead(BaseModel):
    """Target representation for responses."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    name: str
    country: str
    notes: str
    complete: bool


class MissionCreate(BaseModel):
    """Payload for creating a mission with targets."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    targets: list[TargetCreate]

    @field_validator("targets")
    @classmethod
    def validate_targets_count(cls, value: list[TargetCreate]) -> list[TargetCreate]:
        if not (1 <= len(value) <= 3):
            raise ValueError("Mission must include between 1 and 3 targets")
        return value


class MissionAssign(BaseModel):
    """Payload for assigning a cat to a mission."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    cat_id: UUID


class MissionRead(BaseModel):
    """Mission representation with nested targets."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    assigned_cat_id: UUID | None
    complete: bool
    created_at: datetime
    targets: list[TargetRead]
