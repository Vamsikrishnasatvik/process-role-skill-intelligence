import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillResponse


router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"],
)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
):
    skill = Skill(
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill


@router.get(
    "",
    response_model=list[SkillResponse],
)
def list_skills(
    db: Session = Depends(get_db),
):
    return db.query(Skill).order_by(Skill.created_at.desc()).all()


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def get_skill(
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    skill = db.get(Skill, skill_id)

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return skill