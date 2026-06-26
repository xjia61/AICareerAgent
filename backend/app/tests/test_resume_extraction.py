from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_missing_resume_returns_404():
    response = client.post("/resumes/999999/extract")

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"