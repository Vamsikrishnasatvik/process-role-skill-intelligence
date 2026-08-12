import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.industry import Industry
from app.models.value_chain_stage import ValueChainStage
from app.schemas.value_chain_stage import (
    ValueChainStageCreate,
    ValueChainStageResponse,
)


router = APIRouter(
    prefix="/api/value-chain-stages",
    tags=["Value Chain Stages"],
)


@router.post(
    "",
    response_model=ValueChainStageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_stage(
    payload: ValueChainStageCreate,
    db: Session = Depends(get_db),
):
    industry = db.get(Industry, payload.industry_id)

    if industry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )

    stage = ValueChainStage(
        industry_id=payload.industry_id,
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(stage)
    db.commit()
    db.refresh(stage)

    return stage


@router.get(
    "",
    response_model=list[ValueChainStageResponse],
)
def list_stages(
    db: Session = Depends(get_db),
):
    return (
        db.query(ValueChainStage)
        .order_by(ValueChainStage.created_at.desc())
        .all()
    )


@router.get(
    "/{stage_id}",
    response_model=ValueChainStageResponse,
)
def get_stage(
    stage_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    stage = db.get(ValueChainStage, stage_id)

    if stage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Value chain stage not found",
        )

    return stage