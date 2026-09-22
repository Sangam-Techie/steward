"""Reusable skill definitions and per-user semantic memory embeddings."""

import datetime
import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Skill(Base):
    """Reusable skill definition with parameterized steps.

    Attributes:
        id: Primary key.
        name: Skill display name.
        description: Human-readable skill description.
        steps_json: Ordered skill steps as JSON.
        parameters_json: Skill parameter schema as JSON.
        source: Origin of the skill definition.
        risk_tier: Numeric risk level of the skill.
        reviewed: Whether the skill has been reviewed.
        reviewed_by: Optional reviewer identifier.
        reviewed_at: Optional review timestamp.
        created_at: Creation timestamp.
    """

    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    steps_json: Mapped[dict] = mapped_column(JSON)
    parameters_json: Mapped[dict] = mapped_column(JSON)
    source: Mapped[str] = mapped_column(String(20))
    risk_tier: Mapped[int] = mapped_column()
    reviewed: Mapped[bool] = mapped_column(default=False)
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class SemanticMemory(Base):
    """Vector embedding linking a user to a prior task or skill outcome.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        ref_type: Type of referenced entity.
        ref_id: Identifier of the referenced entity.
        task_summary: Summary of the associated task.
        embedding: 1536-dimension embedding vector.
        outcome: Optional outcome label.
        last_used_at: Last retrieval or use timestamp.
    """

    __tablename__ = "semantic_memory"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    ref_type: Mapped[str] = mapped_column(String(10))
    ref_id: Mapped[uuid.UUID] = mapped_column()
    task_summary: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
    outcome: Mapped[str | None] = mapped_column(String(20), nullable=True)
    last_used_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )
