from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_match_missing_job_returns_404():
    response = client.post(
        "/jobs/999999/match",
        json={"resume_id": 1},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"