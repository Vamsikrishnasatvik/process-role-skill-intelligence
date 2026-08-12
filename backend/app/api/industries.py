import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.industry import Industry
from app.schemas.industry import IndustryCreate, IndustryResponse


router = APIRouter(
    prefix="/api/industries",
    tags=["Industries"],
)


@router.post(
    "",
    response_model=IndustryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_industry(
    payload: IndustryCreate,
    db: Session = Depends(get_db),
):
    industry = Industry(
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(industry)
    db.commit()
    db.refresh(industry)

    return industry


@router.get(
    "",
    response_model=list[IndustryResponse],
)
def list_industries(
    db: Session = Depends(get_db),
):
    return (
        db.query(Industry)
        .order_by(Industry.created_at.desc())
        .all()
    )


@router.get(
    "/{industry_id}",
    response_model=IndustryResponse,
)
def get_industry(
    industry_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    industry = db.get(Industry, industry_id)

    if industry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )

    return industry