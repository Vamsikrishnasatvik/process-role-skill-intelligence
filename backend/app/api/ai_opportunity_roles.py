import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_opportunity import AIOpportunity
from app.models.role import Role


router = APIRouter(
    prefix="/api/ai-opportunities",
    tags=["AI Opportunity Role Impacts"],
)


@router.post(
    "/{opportunity_id}/roles/{role_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_role_impact(
    opportunity_id: uuid.UUID,
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    opportunity = db.get(AIOpportunity, opportunity_id)
    role = db.get(Role, role_id)

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI opportunity not found",
        )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role in opportunity.impacted_roles:
        return {
            "message": "Role already impacted by AI opportunity",
            "opportunity_id": opportunity_id,
            "role_id": role_id,
        }

    opportunity.impacted_roles.append(role)

    db.commit()

    return {
        "message": "Role impact assigned",
        "opportunity_id": opportunity_id,
        "role_id": role_id,
    }


@router.get(
    "/{opportunity_id}/roles",
)
def list_impacted_roles(
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
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "metadata": role.metadata_,
        }
        for role in opportunity.impacted_roles
    ]