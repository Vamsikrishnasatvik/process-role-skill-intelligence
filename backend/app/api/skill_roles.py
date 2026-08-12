import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.skill import Skill


router = APIRouter(
    prefix="/api/skills",
    tags=["Skill Roles"],
)


@router.get("/{skill_id}/roles")
def list_skill_roles(
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    skill = db.get(Skill, skill_id)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "metadata": role.metadata_,
        }
        for role in skill.roles
    ]