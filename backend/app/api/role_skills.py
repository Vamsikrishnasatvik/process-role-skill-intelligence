import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role
from app.models.skill import Skill


router = APIRouter(
    prefix="/api/roles",
    tags=["Role Skills"],
)


@router.post(
    "/{role_id}/skills/{skill_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_skill_to_role(
    role_id: uuid.UUID,
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)
    skill = db.get(Skill, skill_id)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    if skill in role.skills:
        return {
            "message": "Skill already assigned to role",
            "role_id": role_id,
            "skill_id": skill_id,
        }

    role.skills.append(skill)

    db.commit()

    return {
        "message": "Skill assigned to role",
        "role_id": role_id,
        "skill_id": skill_id,
    }


@router.get(
    "/{role_id}/skills",
)
def list_role_skills(
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    return [
        {
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "metadata": skill.metadata_,
        }
        for skill in role.skills
    ]


@router.delete(
    "/{role_id}/skills/{skill_id}",
)
def remove_skill_from_role(
    role_id: uuid.UUID,
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)
    skill = db.get(Skill, skill_id)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    if skill not in role.skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill is not assigned to this role",
        )

    role.skills.remove(skill)

    db.commit()

    return {
        "message": "Skill removed from role",
        "role_id": role_id,
        "skill_id": skill_id,
    }