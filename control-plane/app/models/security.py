"""Security models: credentials, device policies, approvals, and audit logs."""

import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Credential(Base):
    """Encrypted secret stored for a user.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        name: Display name for the credential.
        encrypted_secret: Encrypted secret bytes.
        auth_type: Authentication type identifier.
        created_at: Creation timestamp.
    """

    __tablename__ = "credentials"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    encrypted_secret: Mapped[bytes] = mapped_column()
    auth_type: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class Policy(Base):
    """Device policy version containing JSON-encoded rules.

    Attributes:
        id: Primary key.
        device_id: Device this policy applies to.
        version: Monotonic policy version number.
        rules_json: Policy rules as JSON.
        updated_at: Last update timestamp.
    """

    __tablename__ = "policies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devices.id"))
    version: Mapped[int] = mapped_column()
    rules_json: Mapped[dict] = mapped_column(JSON)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class Approval(Base):
    """Human approval request for a risky task step.

    Attributes:
        id: Primary key.
        task_id: Task this approval belongs to.
        step_index: Index of the step awaiting approval.
        action_fingerprint: Hash identifying the proposed action.
        risk_tier: Numeric risk level of the action.
        human_readable_summary: Summary shown to the approver.
        target_identity_json: Target identity details as JSON.
        status: Approval status (defaults to ``pending``).
        consumed: Whether the approval has been used.
        requested_at: When approval was requested.
        responded_at: When a response was recorded.
        expires_at: Expiration timestamp.
    """

    __tablename__ = "approvals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"))
    step_index: Mapped[int] = mapped_column()
    action_fingerprint: Mapped[str] = mapped_column(String(64))
    risk_tier: Mapped[int] = mapped_column()
    human_readable_summary: Mapped[str] = mapped_column(String)
    target_identity_json: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    consumed: Mapped[bool] = mapped_column(default=False)
    requested_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    responded_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class AuditLog(Base):
    """Append-only security or operational event for a device.

    Attributes:
        id: Primary key.
        device_id: Device that produced the event.
        task_id: Optional related task.
        event_type: Event type identifier.
        detail_json: Event payload as JSON.
        ts: Event timestamp.
    """

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devices.id"))
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(20))
    detail_json: Mapped[dict] = mapped_column(JSON)
    ts: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
