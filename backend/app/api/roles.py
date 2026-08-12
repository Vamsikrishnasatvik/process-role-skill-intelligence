import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse


router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
)


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
):
    role = Role(
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


@router.get(
    "",
    response_model=list[RoleResponse],
)
def list_roles(
    db: Session = Depends(get_db),
):
    return db.query(Role).order_by(Role.created_at.desc()).all()


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    role = db.get(Role, role_id)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    return role