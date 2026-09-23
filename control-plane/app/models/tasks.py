"""Task execution records and per-step event history."""

import datetime
import uuid

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Task(Base):
    """Work item assigned to a user and device.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        device_id: Device executing the task.
        goal_text: Natural-language goal for the task.
        execution_mode: How the task should be executed.
        status: Task status (defaults to ``pending``).
        created_at: Creation timestamp.
        completed_at: Optional completion timestamp.
    """

    __tablename__ = "tasks"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devices.id"))
    goal_text: Mapped[str] = mapped_column(String)
    execution_mode: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    completed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)


class TaskEvent(Base):
    """Immutable log of a single step taken during task execution.

    Attributes:
        id: Primary key.
        task_id: Parent task.
        step_index: Index of the executed step.
        node: Graph or pipeline node name.
        adapter: Optional adapter that performed the action.
        action_json: Action payload as JSON.
        verification: Optional verification result.
        ladder_rung: Optional autonomy ladder rung.
        latency_ms: Optional step latency in milliseconds.
        ts: Event timestamp.
    """

    __tablename__ = "task_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"))
    step_index: Mapped[int] = mapped_column()
    node: Mapped[str] = mapped_column(String(50))
    adapter: Mapped[str | None] = mapped_column(String(50), nullable=True)
    action_json: Mapped[dict] = mapped_column(JSON)
    verification: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ladder_rung: Mapped[str | None] = mapped_column(String(30), nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    ts: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
