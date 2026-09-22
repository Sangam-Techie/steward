"""Remote execution target models."""

import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RemoteTarget(Base):
    """SSH or similar remote host a user can execute against.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        type: Target type identifier.
        host_or_distro: Hostname or distribution name.
        port: Optional connection port.
        username: Optional login username.
        credential_ref: Optional reference to a stored credential.
        created_at: Creation timestamp.
    """

    __tablename__ = "remote_targets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(10))
    host_or_distro: Mapped[str] = mapped_column(String(255))
    port: Mapped[int | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    credential_ref: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
