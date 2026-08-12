import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_opportunity import AIOpportunity
from app.schemas.ai_opportunity import (
    AIOpportunityCreate,
    AIOpportunityResponse,
)


router = APIRouter(
    prefix="/api/ai-opportunities",
    tags=["AI Opportunities"],
)


def to_response(opportunity: AIOpportunity) -> dict:
    return {
        "id": opportunity.id,
        "name": opportunity.name,
        "description": opportunity.description,
        "metadata": opportunity.metadata_,
        "created_at": opportunity.created_at,
        "updated_at": opportunity.updated_at,
    }


@router.post(
    "",
    response_model=AIOpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ai_opportunity(
    payload: AIOpportunityCreate,
    db: Session = Depends(get_db),
):
    opportunity = AIOpportunity(
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    return to_response(opportunity)


@router.get(
    "",
    response_model=list[AIOpportunityResponse],
)
def list_ai_opportunities(
    db: Session = Depends(get_db),
):
    opportunities = (
        db.query(AIOpportunity)
        .order_by(AIOpportunity.created_at.desc())
        .all()
    )

    return [to_response(opportunity) for opportunity in opportunities]


@router.get(
    "/{opportunity_id}",
    response_model=AIOpportunityResponse,
)
def get_ai_opportunity(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    opportunity = db.get(AIOpportunity, opportunity_id)

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI opportunity not found",
        )

    return to_response(opportunity)