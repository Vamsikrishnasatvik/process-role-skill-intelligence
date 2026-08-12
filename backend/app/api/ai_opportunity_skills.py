import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_opportunity import AIOpportunity
from app.models.skill import Skill


router = APIRouter(
    prefix="/api/ai-opportunities",
    tags=["AI Opportunity Skill Impacts"],
)


@router.post(
    "/{opportunity_id}/skills/{skill_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_skill_impact(
    opportunity_id: uuid.UUID,
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    opportunity = db.get(AIOpportunity, opportunity_id)
    skill = db.get(Skill, skill_id)

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI opportunity not found",
        )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    if skill in opportunity.impacted_skills:
        return {
            "message": "Skill already impacted by AI opportunity",
            "opportunity_id": opportunity_id,
            "skill_id": skill_id,
        }

    opportunity.impacted_skills.append(skill)

    db.commit()

    return {
        "message": "Skill impact assigned",
        "opportunity_id": opportunity_id,
        "skill_id": skill_id,
    }


@router.get(
    "/{opportunity_id}/skills",
)
def list_impacted_skills(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    opportunity = db.get(AIOpportunity, opportunity_id)

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI opportunity not found",
        )

    return [
        {
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "metadata": skill.metadata_,
        }
        for skill in opportunity.impacted_skills
    ]