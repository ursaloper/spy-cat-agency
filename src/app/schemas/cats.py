from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


def _quantize_salary(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class CatBase(BaseModel):
    """Shared cat fields with validation and salary quantization."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(min_length=1, max_length=100)
    years_experience: int = Field(ge=0)
    breed: str = Field(min_length=1, max_length=100)
    salary: Decimal = Field(gt=Decimal("0"))

    @field_validator("salary")
    @classmethod
    def validate_salary(cls, value: Decimal) -> Decimal:
        return _quantize_salary(value)

    @field_serializer("salary")
    def serialize_salary(self, value: Decimal) -> str:
        return format(_quantize_salary(value), ".2f")


class CatCreate(CatBase):
    """Payload for creating a cat."""

    pass


class CatRead(BaseModel):
    """Cat representation for responses."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    name: str
    years_experience: int
    breed: str
    salary: Decimal

    @field_serializer("salary")
    def serialize_salary(self, value: Decimal) -> str:
        return format(_quantize_salary(value), ".2f")


class CatUpdateSalary(BaseModel):
    """Payload for updating cat salary."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    salary: Decimal = Field(gt=Decimal("0"))

    @field_validator("salary")
    @classmethod
    def validate_salary(cls, value: Decimal) -> Decimal:
        return _quantize_salary(value)

    @field_serializer("salary")
    def serialize_salary(self, value: Decimal) -> str:
        return format(_quantize_salary(value), ".2f")
