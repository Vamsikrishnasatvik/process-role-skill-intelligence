import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity


router = APIRouter(
    prefix="/api/activities",
    tags=["Activity AI Opportunities"],
)


@router.post(
    "/{activity_id}/ai-opportunities/{opportunity_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_ai_opportunity_to_activity(
    activity_id: uuid.UUID,
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)
    opportunity = db.get(AIOpportunity, opportunity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI opportunity not found",
        )

    if opportunity in activity.ai_opportunities:
        return {
            "message": "AI opportunity already assigned to activity",
            "activity_id": activity_id,
            "opportunity_id": opportunity_id,
        }

    activity.ai_opportunities.append(opportunity)

    db.commit()

    return {
        "message": "AI opportunity assigned to activity",
        "activity_id": activity_id,
        "opportunity_id": opportunity_id,
    }


@router.get(
    "/{activity_id}/ai-opportunities",
)
def list_activity_ai_opportunities(
    activity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    return [
        {
            "id": opportunity.id,
            "name": opportunity.name,
            "description": opportunity.description,
            "metadata": opportunity.metadata_,
        }
        for opportunity in activity.ai_opportunities
    ]