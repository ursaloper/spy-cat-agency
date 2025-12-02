from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Cat(Base):
    __tablename__ = "cats"
    """Spy cat entity with salary and breed information."""

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    years_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    missions: Mapped[list["Mission"]] = relationship("Mission", back_populates="assigned_cat")


class Mission(Base):
    __tablename__ = "missions"
    """Mission entity containing targets and optional assigned cat."""

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    assigned_cat_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("cats.id", ondelete="SET NULL"), nullable=True, index=True
    )
    complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assigned_cat: Mapped[Cat | None] = relationship("Cat", back_populates="missions")
    targets: Mapped[list["Target"]] = relationship("Target", back_populates="mission", cascade="all, delete-orphan", passive_deletes=True)


class Target(Base):
    __tablename__ = "targets"
    """Target entity belonging to a mission."""

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    mission_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(80), nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False, default="")
    complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    mission: Mapped[Mission] = relationship("Mission", back_populates="targets")
