import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.activity import Activity
from app.models.role import Role


router = APIRouter(
    prefix="/api/activities",
    tags=["Activity Roles"],
)


@router.post(
    "/{activity_id}/roles/{role_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_role_to_activity(
    activity_id: uuid.UUID,
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)
    role = db.get(Role, role_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role in activity.roles:
        return {
            "message": "Role already assigned to activity",
            "activity_id": activity_id,
            "role_id": role_id,
        }

    activity.roles.append(role)

    db.commit()

    return {
        "message": "Role assigned to activity",
        "activity_id": activity_id,
        "role_id": role_id,
    }


@router.get(
    "/{activity_id}/roles",
)
def list_activity_roles(
    activity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "metadata": role.metadata_,
        }
        for role in activity.roles
    ]


@router.delete(
    "/{activity_id}/roles/{role_id}",
)
def remove_role_from_activity(
    activity_id: uuid.UUID,
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    activity = db.get(Activity, activity_id)
    role = db.get(Role, role_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role not in activity.roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role is not assigned to this activity",
        )

    activity.roles.remove(role)

    db.commit()

    return {
        "message": "Role removed from activity",
        "activity_id": activity_id,
        "role_id": role_id,
    }