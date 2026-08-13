import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evidence import Evidence


router = APIRouter(
    prefix="/api/evidence",
    tags=["Evidence"],
)


@router.get("/{entity_type}/{entity_id}")
def list_evidence(
    entity_type: str,
    entity_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(
            Evidence.entity_type == entity_type,
            Evidence.entity_id == entity_id,
        )
        .order_by(Evidence.retrieved_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "entity_type": item.entity_type,
            "entity_id": item.entity_id,
            "source_title": item.source_title,
            "source_type": item.source_type,
            "snippet": item.snippet,
            "source_url": item.source_url,
            "retrieved_at": item.retrieved_at,
            "metadata": item.metadata_,
        }
        for item in evidence
    ]