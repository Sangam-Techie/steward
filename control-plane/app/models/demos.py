"""Job-application tracking models for demo workflows."""

import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class JobApplication(Base):
    """Tracked job posting application for a user.

    Attributes:
        id: Primary key.
        user_id: Owning user.
        posting_url: Canonical URL of the job posting.
        company: Company name.
        role: Role or job title.
        status: Application status.
        skip_reason: Optional reason the posting was skipped.
        content_hash: Optional hash of posting content.
        applied_at: Optional application timestamp.
        followed_up_at: Optional follow-up timestamp.
    """

    __tablename__ = "job_applications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    posting_url: Mapped[str] = mapped_column(String)
    company: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20))
    skip_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    applied_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    followed_up_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "posting_url", name="uq_job_applications_user_posting"
        ),
    )
