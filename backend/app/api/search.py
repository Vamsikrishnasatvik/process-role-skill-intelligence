from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.activity import Activity
from app.models.process import Process
from app.models.role import Role
from app.models.skill import Skill
from app.models.ai_opportunity import AIOpportunity


router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


@router.get("")
def search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    query = f"%{q.strip()}%"

    results = []

    activities = (
        db.query(Activity)
        .filter(
            (Activity.name.ilike(query))
            | (Activity.description.ilike(query))
        )
        .limit(20)
        .all()
    )

    for item in activities:
        results.append(
            {
                "id": item.id,
                "type": "activity",
                "name": item.name,
                "description": item.description,
            }
        )

    processes = (
        db.query(Process)
        .filter(
            (Process.name.ilike(query))
            | (Process.description.ilike(query))
        )
        .limit(20)
        .all()
    )

    for item in processes:
        results.append(
            {
                "id": item.id,
                "type": "process",
                "name": item.name,
                "description": item.description,
            }
        )

    roles = (
        db.query(Role)
        .filter(
            (Role.name.ilike(query))
            | (Role.description.ilike(query))
        )
        .limit(20)
        .all()
    )

    for item in roles:
        results.append(
            {
                "id": item.id,
                "type": "role",
                "name": item.name,
                "description": item.description,
            }
        )

    skills = (
        db.query(Skill)
        .filter(
            (Skill.name.ilike(query))
            | (Skill.description.ilike(query))
        )
        .limit(20)
        .all()
    )

    for item in skills:
        results.append(
            {
                "id": item.id,
                "type": "skill",
                "name": item.name,
                "description": item.description,
            }
        )

    opportunities = (
        db.query(AIOpportunity)
        .filter(
            (AIOpportunity.name.ilike(query))
            | (AIOpportunity.description.ilike(query))
        )
        .limit(20)
        .all()
    )

    for item in opportunities:
        results.append(
            {
                "id": item.id,
                "type": "ai_opportunity",
                "name": item.name,
                "description": item.description,
            }
        )

    return results[:50]