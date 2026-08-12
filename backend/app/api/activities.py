import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.activity import Activity
from app.models.process import Process
from app.schemas.activity import ActivityCreate, ActivityResponse


router = APIRouter(
    prefix="/api/activities",
    tags=["Activities"],
)


@router.post(
    "",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
):
    process = db.get(Process, payload.process_id)

    if process is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found",
        )

    activity = Activity(
        process_id=payload.process_id,
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get(
    "",
    response_model=list[ActivityResponse],
)
def list_activities(
    db: Session = Depends(get_db),
):
    return (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .all()
    )


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
)
def get_activity(
    activity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    return activity