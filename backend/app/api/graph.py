import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.industry import Industry
from app.models.value_chain_stage import ValueChainStage
from app.models.process import Process
from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity


router = APIRouter(
    prefix="/api/industries",
    tags=["Graph"],
)


@router.get("/{industry_id}/graph")
def get_industry_graph(
    industry_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    industry = (
        db.query(Industry)
        .options(
            # Industry
            selectinload(Industry.value_chain_stages)
            # Value Chain Stage
            .selectinload(ValueChainStage.processes)
            # Process
            .selectinload(Process.activities)
            # Activity
            .selectinload(Activity.ai_opportunities)
            # AI Opportunity -> Roles
            .selectinload(AIOpportunity.impacted_roles),

            # Same path -> AI Opportunity -> Skills
            selectinload(Industry.value_chain_stages)
            .selectinload(ValueChainStage.processes)
            .selectinload(Process.activities)
            .selectinload(Activity.ai_opportunities)
            .selectinload(AIOpportunity.impacted_skills),
        )
        .filter(Industry.id == industry_id)
        .first()
    )

    if industry is None:
        raise HTTPException(
            status_code=404,
            detail="Industry not found",
        )

    return {
        "id": industry.id,
        "name": industry.name,
        "description": industry.description,
        "metadata": industry.metadata_,
        "value_chain_stages": [
            {
                "id": stage.id,
                "name": stage.name,
                "description": stage.description,
                "metadata": stage.metadata_,
                "processes": [
                    {
                        "id": process.id,
                        "name": process.name,
                        "description": process.description,
                        "metadata": process.metadata_,
                        "activities": [
                            {
                                "id": activity.id,
                                "name": activity.name,
                                "description": activity.description,
                                "metadata": activity.metadata_,
                                "ai_opportunities": [
                                    {
                                        "id": opportunity.id,
                                        "name": opportunity.name,
                                        "description": opportunity.description,
                                        "metadata": opportunity.metadata_,
                                        "impacted_roles": [
                                            {
                                                "id": role.id,
                                                "name": role.name,
                                            }
                                            for role in opportunity.impacted_roles
                                        ],
                                        "impacted_skills": [
                                            {
                                                "id": skill.id,
                                                "name": skill.name,
                                            }
                                            for skill in opportunity.impacted_skills
                                        ],
                                    }
                                    for opportunity in activity.ai_opportunities
                                ],
                            }
                            for activity in process.activities
                        ],
                    }
                    for process in stage.processes
                ],
            }
            for stage in industry.value_chain_stages
        ],
    }