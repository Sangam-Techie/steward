"""Identity models: users, profiles, and registered devices."""

import datetime
import uuid

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """Account identity for a control-plane user.

    Attributes:
        id: Primary key.
        email: Unique login email.
        created_at: Account creation timestamp.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


class UserProfile(Base):
    """Job-search preferences and resume data for a user.

    Attributes:
        user_id: Primary key and foreign key to ``users.id``.
        resume_text: Optional resume contents as plain text.
        must_have_skills: Optional list of required skills.
        title_keywords: Optional keywords used to match job titles.
        location_preference: Optional preferred location.
        remote_ok: Whether remote work is acceptable.
        salary_floor: Optional minimum acceptable salary.
        updated_at: Last profile update timestamp.
    """

    __tablename__ = "user_profile"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    resume_text: Mapped[str | None] = mapped_column(String, nullable=True)
    must_have_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    title_keywords: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    location_preference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_ok: Mapped[bool | None] = mapped_column(nullable=True)
    salary_floor: Mapped[int | None] = mapped_column(nullable=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Device(Base):
    """Registered client device belonging to a user.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        name: Human-readable device name.
        platform: Device platform identifier.
        last_seen_at: Last heartbeat or activity timestamp.
        token_hash: Hash of the device authentication token.
    """

    __tablename__ = "devices"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    platform: Mapped[str] = mapped_column(String(20))
    last_seen_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    token_hash: Mapped[str] = mapped_column(String(64))
