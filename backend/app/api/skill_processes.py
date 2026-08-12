import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.skill import Skill


router = APIRouter(
    prefix="/api/skills",
    tags=["Skill Processes"],
)


@router.get("/{skill_id}/processes")
def list_skill_processes(
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    skill = db.get(Skill, skill_id)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    processes = {}

    for role in skill.roles:
        for activity in role.activities:
            if activity.process is None:
                continue

            process = activity.process

            processes[process.id] = {
                "id": process.id,
                "name": process.name,
                "description": process.description,
                "metadata": process.metadata_,
            }

    return list(processes.values())