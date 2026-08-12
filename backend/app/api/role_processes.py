import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role


router = APIRouter(
    prefix="/api/roles",
    tags=["Role Processes"],
)


@router.get("/{role_id}/processes")
def list_role_processes(
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    processes = {}

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