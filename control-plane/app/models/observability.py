"""Observability models for task traces and spans."""

import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Span(Base):
    """Timed span within a task trace.

    Attributes:
        id: Primary key.
        task_id: Parent task.
        trace_id: Trace identifier shared by related spans.
        span_name: Display name of the span.
        attibutes_json: Span attributes as JSON.
        started_at: Span start timestamp.
        ended_at: Optional span end timestamp.
    """

    __tablename__ = "spans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"))
    trace_id: Mapped[str] = mapped_column(String(64))
    span_name: Mapped[str] = mapped_column(String(100))
    attibutes_json: Mapped[dict] = mapped_column(JSON)
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    ended_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
