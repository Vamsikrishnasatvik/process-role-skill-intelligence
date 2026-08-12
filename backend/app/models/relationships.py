from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


process_activities = Table(
    "process_activities",
    Base.metadata,
    Column(
        "process_id",
        UUID(as_uuid=True),
        ForeignKey("processes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


activity_roles = Table(
    "activity_roles",
    Base.metadata,
    Column(
        "activity_id",
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


role_skills = Table(
    "role_skills",
    Base.metadata,
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


activity_ai_opportunities = Table(
    "activity_ai_opportunities",
    Base.metadata,
    Column(
        "activity_id",
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "ai_opportunity_id",
        UUID(as_uuid=True),
        ForeignKey("ai_opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


ai_opportunity_role_impacts = Table(
    "ai_opportunity_role_impacts",
    Base.metadata,
    Column(
        "ai_opportunity_id",
        UUID(as_uuid=True),
        ForeignKey("ai_opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


ai_opportunity_skill_impacts = Table(
    "ai_opportunity_skill_impacts",
    Base.metadata,
    Column(
        "ai_opportunity_id",
        UUID(as_uuid=True),
        ForeignKey("ai_opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)