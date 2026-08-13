import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.process import Process


router = APIRouter(
    prefix="/api/processes",
    tags=["Process Activities"],
)


@router.get("/{process_id}/activities")
def list_process_activities(
    process_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found",
        )

    return [
        {
            "id": activity.id,
            "process_id": activity.process_id,
            "name": activity.name,
            "description": activity.description,
            "metadata": activity.metadata_,
            "created_at": activity.created_at,
            "updated_at": activity.updated_at,
        }
        for activity in process.activities
    ]