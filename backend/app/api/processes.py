import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.process import Process
from app.models.value_chain_stage import ValueChainStage
from app.schemas.process import ProcessCreate, ProcessResponse


router = APIRouter(
    prefix="/api/processes",
    tags=["Processes"],
)


@router.post(
    "",
    response_model=ProcessResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_process(
    payload: ProcessCreate,
    db: Session = Depends(get_db),
):
    stage = db.get(ValueChainStage, payload.value_chain_stage_id)

    if stage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Value chain stage not found",
        )

    process = Process(
        value_chain_stage_id=payload.value_chain_stage_id,
        name=payload.name,
        description=payload.description,
        metadata_=payload.metadata,
    )

    db.add(process)
    db.commit()
    db.refresh(process)

    return process


@router.get(
    "",
    response_model=list[ProcessResponse],
)
def list_processes(
    db: Session = Depends(get_db),
):
    return (
        db.query(Process)
        .order_by(Process.created_at.desc())
        .all()
    )


@router.get(
    "/{process_id}",
    response_model=ProcessResponse,
)
def get_process(
    process_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found",
        )

    return process