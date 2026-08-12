import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AIOpportunity(Base):
    __tablename__ = "ai_opportunities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    metadata_: Mapped[dict] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    activities: Mapped[list["Activity"]] = relationship(
        secondary="activity_ai_opportunities",
        back_populates="ai_opportunities",
    )

    impacted_roles: Mapped[list["Role"]] = relationship(
        secondary="ai_opportunity_role_impacts",
        back_populates="ai_opportunities",
    )

    impacted_skills: Mapped[list["Skill"]] = relationship(
        secondary="ai_opportunity_skill_impacts",
        back_populates="ai_opportunities",
    )
