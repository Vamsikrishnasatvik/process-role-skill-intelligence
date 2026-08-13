from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


ACTIVITY_ID = "3a076ae8-e6c8-43d4-a81b-9235fa576ecd"
AI_OPPORTUNITY_ID = "d9a89ac2-4206-4db4-b847-30865b55e7e2"
ROLE_ID = "b9c0dbe7-437a-41b7-b5a4-83e3e542e022"
SKILL_ID = "64b6ebec-75ea-4a63-8b67-d58c0a67f5b8"


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
        "/api/processes/analyze",
        json={
            "name": "Assortment Planning",
            "description": "Planning the product assortment across retail channels.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["process_name"] == "Assortment Planning"
    assert data["process_description"] == (
        "Planning the product assortment across retail channels."
    )

    assert len(data["activities"]) == 1

    activity = data["activities"][0]

    assert activity["name"] == "Analyze Assortment Planning"
    assert len(activity["roles"]) >= 1
    assert len(activity["skills"]) >= 1