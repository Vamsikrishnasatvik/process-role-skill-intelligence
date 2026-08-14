import uuid

from app.db.session import SessionLocal
from app.models.evidence import Evidence


ACTIVITY_ID = uuid.UUID(
    "3a076ae8-e6c8-43d4-a81b-9235fa576ecd"
)

AI_OPPORTUNITY_ID = uuid.UUID(
    "d9a89ac2-4206-4db4-b847-30865b55e7e2"
)

CATEGORY_ANALYSIS_ACTIVITY_ID = uuid.UUID(
    "4c315b4f-e0ee-4a98-8488-dc3570dba8aa"
)

EVIDENCE = [
    {
        "entity_type": "activity",
        "entity_id": ACTIVITY_ID,
        "source_title": "Retail AI Assortment Optimization Analysis",
        "source_type": "industry_research",
        "snippet": (
            "AI-assisted analysis can evaluate historical sales, "
            "demand patterns, seasonal trends, and store characteristics "
            "to support assortment planning decisions."
        ),
        "source_url": "https://example.com/retail-assortment-ai",
        "metadata_": {
            "topic": "assortment_optimization",
            "evidence_level": "supporting",
        },
    },
    {
        "entity_type": "activity",
        "entity_id": ACTIVITY_ID,
        "source_title": "AI in Retail Merchandising",
        "source_type": "research_report",
        "snippet": (
            "Retail merchandising teams can use predictive analytics "
            "and recommendation systems to identify product demand "
            "patterns and improve assortment decisions."
        ),
        "source_url": "https://example.com/ai-retail-merchandising",
        "metadata_": {
            "topic": "merchandising",
            "evidence_level": "supporting",
        },
    },
    {
        "entity_type": "ai_opportunity",
        "entity_id": AI_OPPORTUNITY_ID,
        "source_title": "AI-Powered Retail Decision Support",
        "source_type": "industry_research",
        "snippet": (
            "Recommendation-based AI systems can augment merchandising "
            "professionals by providing data-driven recommendations "
            "while retaining human review and decision authority."
        ),
        "source_url": "https://example.com/ai-retail-decision-support",
        "metadata_": {
            "topic": "human_in_the_loop",
            "evidence_level": "supporting",
        },
    },
    {
        "entity_type": "activity",
        "entity_id": CATEGORY_ANALYSIS_ACTIVITY_ID,
        "source_title": "Assortment Planning Category Analysis",
        "source_type": "internal_analysis",
        "snippet": (
            "Historical sales, category performance, customer demand, "
            "and channel-level trends provide supporting information "
            "for assortment planning decisions."
        ),
        "source_url": None,
        "metadata_": {
            "topic": "category_performance",
            "evidence_level": "supporting",
        },
    },
    {
        "entity_type": "activity",
        "entity_id": CATEGORY_ANALYSIS_ACTIVITY_ID,
        "source_title": "Retail Demand and Category Performance Analysis",
        "source_type": "business_analysis",
        "snippet": (
            "Category and demand analysis can help merchandising teams "
            "identify trends, anomalies, and product demand patterns "
            "when evaluating assortment decisions."
        ),
        "source_url": None,
        "metadata_": {
            "topic": "demand_analysis",
            "evidence_level": "supporting",
        },
    },
    
]


def seed():
    db = SessionLocal()

    try:
        inserted = 0

        for item in EVIDENCE:
            exists = (
                db.query(Evidence)
                .filter(
                    Evidence.entity_type == item["entity_type"],
                    Evidence.entity_id == item["entity_id"],
                    Evidence.source_title == item["source_title"],
                )
                .first()
            )

            if exists:
                continue

            db.add(Evidence(**item))
            inserted += 1

        db.commit()

        print(f"Inserted {inserted} evidence records.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()