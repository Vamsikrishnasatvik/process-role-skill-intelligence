import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.process import Process
from app.schemas.process_analysis import (
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)
from services.ai_service import ai_service
from services.graph_persistence import graph_persistence_service


router = APIRouter(
    prefix="/api/processes",
    tags=["Process Analysis"],
)


@router.post(
    "/{process_id}/analyze",
    response_model=ProcessAnalysisResponse,
)
def analyze_process(
    process_id: uuid.UUID,
    payload: ProcessAnalysisRequest,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found",
        )

    analysis = ai_service.analyze_process(
        process_name=process.name,
        process_description=process.description,
        payload=payload,
    )

    try:
        graph_persistence_service.persist_analysis(
            db=db,
            process=process,
            analysis=analysis,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return analysis