from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.process import Process
from app.models.role import Role
from app.models.skill import Skill
from app.models.ai_opportunity import AIOpportunity


client = TestClient(app)


ACTIVITY_ID = "3a076ae8-e6c8-43d4-a81b-9235fa576ecd"
AI_OPPORTUNITY_ID = "d9a89ac2-4206-4db4-b847-30865b55e7e2"
ROLE_ID = "b9c0dbe7-437a-41b7-b5a4-83e3e542e022"
SKILL_ID = "64b6ebec-75ea-4a63-8b67-d58c0a67f5b8"
PROCESS_ID = "f025eb56-24a9-4e9b-abc5-10735564d006"
CATEGORY_ANALYSIS_ACTIVITY_ID = "4c315b4f-e0ee-4a98-8488-dc3570dba8aa"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_activity_impact():
    response = client.get(
        f"/api/impact/activity/{ACTIVITY_ID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["activity"]["id"] == ACTIVITY_ID
    assert data["process"]["name"] == "Assortment Planning"
    assert len(data["ai_opportunities"]) >= 1
    assert len(data["impacted_roles"]) >= 1
    assert len(data["impacted_skills"]) >= 1

    assert data["impact"]["type"] == "augmentation"
    assert "human_in_the_loop" in data["impact"]["automation_levels"]
    assert "recommendation" in data["impact"]["ai_patterns"]


def test_activity_evidence():
    response = client.get(
        f"/api/evidence/activity/{ACTIVITY_ID}"
    )

    assert response.status_code == 200

    evidence = response.json()

    assert len(evidence) == 2
    assert all(item["entity_type"] == "activity" for item in evidence)
    assert all(item["entity_id"] == ACTIVITY_ID for item in evidence)


def test_search():
    response = client.get(
        "/api/search",
        params={"q": "Merchandising Analyst"},
    )

    assert response.status_code == 200

    results = response.json()

    assert isinstance(results, list)
    assert any(
        item["id"] == ROLE_ID
        for item in results
    )


def test_search_forecasting():
    response = client.get(
        "/api/search",
        params={"q": "Forecasting"},
    )

    assert response.status_code == 200

    results = response.json()

    assert any(
        item["id"] == SKILL_ID
        for item in results
    )


def test_ai_opportunity():
    response = client.get(
        f"/api/ai-opportunities/{AI_OPPORTUNITY_ID}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == AI_OPPORTUNITY_ID
    assert data["name"] == "AI-Assisted Assortment Optimization"


def test_process_analysis_endpoint():
    response = client.post(
        f"/api/processes/{PROCESS_ID}/analyze",
        json={},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["process_name"] == "Assortment Planning"
    assert data["process_description"] is not None

    assert len(data["activities"]) >= 4

    activity = data["activities"][0]

    assert activity["name"] == "Analyze Category Performance"

    assert len(activity["roles"]) >= 1
    assert len(activity["skills"]) >= 1
    assert len(activity["ai_opportunities"]) >= 1

    assert activity["roles"][0]["name"] == "Merchandising Analyst"
    assert activity["skills"][0]["name"] == "Category Analytics"
    assert (
        activity["ai_opportunities"][0]["name"]
        == "AI-Assisted Category Analytics"
    )

def test_process_analysis_persists_graph():
    response = client.post(
        f"/api/processes/{PROCESS_ID}/analyze",
        json={},
    )

    assert response.status_code == 200

    data = response.json()

    db = SessionLocal()

    try:
        process = db.get(Process, PROCESS_ID)

        assert process is not None

        activity = next(
            (
                item
                for item in process.activities
                if item.name == "Analyze Category Performance"
            ),
            None,
        )

        assert activity is not None

        role = next(
            (
                item
                for item in activity.roles
                if item.name == "Merchandising Analyst"
            ),
            None,
        )

        assert role is not None

        skill = next(
            (
                item
                for item in role.skills
                if item.name == "Category Analytics"
            ),
            None,
        )

        assert skill is not None

        opportunity = next(
            (
                item
                for item in activity.ai_opportunities
                if item.name == "AI-Assisted Category Analytics"
            ),
            None,
        )

        assert opportunity is not None

        assert role in opportunity.impacted_roles
        assert skill in opportunity.impacted_skills

    finally:
        db.close()


def test_process_analysis_is_idempotent():
    first = client.post(
        f"/api/processes/{PROCESS_ID}/analyze",
        json={},
    )

    second = client.post(
        f"/api/processes/{PROCESS_ID}/analyze",
        json={},
    )

    assert first.status_code == 200
    assert second.status_code == 200

    db = SessionLocal()

    try:
        process = db.get(Process, PROCESS_ID)

        matching_activities = [
            activity
            for activity in process.activities
            if activity.name == "Analyze Category Performance"
        ]

        assert len(matching_activities) == 1

        activity = matching_activities[0]

        matching_roles = [
            role
            for role in activity.roles
            if role.name == "Merchandising Analyst"
        ]

        assert len(matching_roles) == 1

        role = matching_roles[0]

        matching_skills = [
            skill
            for skill in role.skills
            if skill.name == "Category Analytics"
        ]

        assert len(matching_skills) == 1

        skill = matching_skills[0]

        matching_opportunities = [
            opportunity
            for opportunity in activity.ai_opportunities
            if opportunity.name == "AI-Assisted Category Analytics"
        ]

        assert len(matching_opportunities) == 1

        opportunity = matching_opportunities[0]

        assert opportunity.impacted_roles.count(role) == 1
        assert opportunity.impacted_skills.count(
            skill
        ) == 1

    finally:
        db.close()

def test_activity_evidence_for_category_analysis():
    response = client.get(
        f"/api/evidence/activity/{CATEGORY_ANALYSIS_ACTIVITY_ID}"
    )

    assert response.status_code == 200

    evidence = response.json()

    assert len(evidence) == 2
    assert all(
        item["entity_type"] == "activity"
        for item in evidence
    )
    assert all(
        item["entity_id"] == CATEGORY_ANALYSIS_ACTIVITY_ID
        for item in evidence
    )

    assert any(
        item["source_title"]
        == "Assortment Planning Category Analysis"
        for item in evidence
    )


def test_process_analysis_not_found():
    response = client.post(
        "/api/processes/00000000-0000-0000-0000-000000000000/analyze",
        json={},
    )

    assert response.status_code == 404


def test_process_analysis_response_contains_ai_opportunities():
    response = client.post(
        f"/api/processes/{PROCESS_ID}/analyze",
        json={},
    )

    assert response.status_code == 200

    data = response.json()

    opportunities = [
        opportunity["name"]
        for activity in data["activities"]
        for opportunity in activity["ai_opportunities"]
    ]

    assert len(opportunities) >= 4

    assert "AI-Assisted Category Analytics" in opportunities
    assert "AI-Assisted Assortment Optimization" in opportunities
    assert "AI Demand Forecasting" in opportunities
    assert "AI-Assisted Assortment Recommendation" in opportunities