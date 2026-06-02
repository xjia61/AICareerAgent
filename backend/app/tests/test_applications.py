from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_application_without_job_returns_404():
    response = client.post(
        "/applications/",
        json={
            "job_id": 999999,
            "status": "interested",
            "next_action": "Apply later",
            "notes": "Test application",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"