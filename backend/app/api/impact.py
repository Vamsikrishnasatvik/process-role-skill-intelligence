import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.activity import Activity


router = APIRouter(
    prefix="/api/impact",
    tags=["Impact"],
)


def build_impact_result(activity: Activity) -> dict:
    """
    Deterministic impact propagation.

    Chain:
        Activity
            ↓
        Process
            ↓
        AI Opportunity
            ↓
        Impacted Roles
            ↓
        Impacted Skills
            ↓
        Automation / Augmentation
            ↓
        Future Change
    """

    opportunities = activity.ai_opportunities

    # No AI opportunity means there is no downstream impact to propagate.
    if not opportunities:
        return {
            "activity": {
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
            },
            "process": (
                {
                    "id": activity.process.id,
                    "name": activity.process.name,
                    "description": activity.process.description,
                }
                if activity.process
                else None
            ),
            "ai_opportunities": [],
            "impacted_roles": [],
            "impacted_skills": [],
            "impact": {
                "type": "none",
                "role_change": "No AI opportunity is currently mapped to this activity.",
                "skill_change": "No AI-driven skill impact has been identified.",
                "future_change": "No projected change is available.",
            },
        }

    impacted_roles = {}
    impacted_skills = {}

    for opportunity in opportunities:
        for role in opportunity.impacted_roles:
            impacted_roles[role.id] = role

        for skill in opportunity.impacted_skills:
            impacted_skills[skill.id] = skill

    # Determine the overall automation / augmentation characteristics
    # from the existing opportunity metadata.
    automation_levels = []
    ai_patterns = []

    for opportunity in opportunities:
        metadata = opportunity.metadata_ or {}

        automation_level = metadata.get("automation_level")
        ai_pattern = metadata.get("ai_pattern")

        if automation_level:
            automation_levels.append(str(automation_level))

        if ai_pattern:
            ai_patterns.append(str(ai_pattern))

    # Deterministic business rule.
    #
    # Current seed data uses "human_in_the_loop", which means the
    # opportunity supports the worker rather than completely replacing
    # the decision.
    if any(level == "human_in_the_loop" for level in automation_levels):
        impact_type = "augmentation"
        role_change = (
            "Role responsibilities shift from manual analysis or execution "
            "toward reviewing, validating, and acting on AI-supported recommendations."
        )
        skill_change = (
            "Analytical and decision-making skills become more important, "
            "with increased emphasis on interpreting AI outputs and validating recommendations."
        )
        future_change = (
            "The activity becomes AI-assisted while the human remains responsible "
            "for review, judgment, and final decisions."
        )
    elif automation_levels:
        impact_type = "automation"
        role_change = (
            "Parts of the activity may become automated, reducing manual execution "
            "and shifting the role toward exception handling and oversight."
        )
        skill_change = (
            "Routine execution skills decrease in importance while monitoring, "
            "exception handling, and AI oversight become more important."
        )
        future_change = (
            "The activity is expected to require less manual execution "
            "and more human oversight."
        )
    else:
        impact_type = "augmentation"
        role_change = (
            "The role is expected to be supported by AI recommendations and analysis."
        )
        skill_change = (
            "Existing analytical and decision-making capabilities remain important."
        )
        future_change = (
            "The activity becomes more data-driven and AI-assisted."
        )

    return {
        "activity": {
            "id": activity.id,
            "name": activity.name,
            "description": activity.description,
            "metadata": activity.metadata_,
        },
        "process": (
            {
                "id": activity.process.id,
                "name": activity.process.name,
                "description": activity.process.description,
                "metadata": activity.process.metadata_,
            }
            if activity.process
            else None
        ),
        "ai_opportunities": [
            {
                "id": opportunity.id,
                "name": opportunity.name,
                "description": opportunity.description,
                "metadata": opportunity.metadata_,
            }
            for opportunity in opportunities
        ],
        "impacted_roles": [
            {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "metadata": role.metadata_,
            }
            for role in impacted_roles.values()
        ],
        "impacted_skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "metadata": skill.metadata_,
            }
            for skill in impacted_skills.values()
        ],
        "impact": {
            "type": impact_type,
            "automation_levels": automation_levels,
            "ai_patterns": ai_patterns,
            "role_change": role_change,
            "skill_change": skill_change,
            "future_change": future_change,
        },
    }


@router.get("/activity/{activity_id}")
def get_activity_impact(
    activity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = (
        db.query(Activity)
        .options(
            selectinload(Activity.process),
            selectinload(Activity.ai_opportunities),
        )
        .filter(Activity.id == activity_id)
        .first()
    )

    if activity is None:
        raise HTTPException(
            status_code=404,
            detail="Activity not found",
        )

    # Explicitly load nested opportunity relationships.
    for opportunity in activity.ai_opportunities:
        # Access relationships so SQLAlchemy loads them before response creation.
        _ = opportunity.impacted_roles
        _ = opportunity.impacted_skills

    return build_impact_result(activity)