from fastapi import APIRouter

from app.schemas.process_analysis import (
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)
from services.ai_service import ai_service


router = APIRouter(
    prefix="/api/processes",
    tags=["Process Analysis"],
)


@router.post(
    "/analyze",
    response_model=ProcessAnalysisResponse,
)
def analyze_process(
    payload: ProcessAnalysisRequest,
):
    return ai_service.analyze_process(payload)