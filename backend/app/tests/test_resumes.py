from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_txt_resume():
    response = client.post(
        "/resumes/upload",
        files={
            "file": (
                "test_resume.txt",
                b"Python FastAPI React PostgreSQL OpenAI RAG AWS",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["filename"] == "test_resume.txt"
    assert "Python" in data["parsed_text"]
    assert "FastAPI" in data["parsed_text"]


def test_upload_unsupported_file_type():
    response = client.post(
        "/resumes/upload",
        files={
            "file": (
                "test_resume.docx",
                b"fake content",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 400
    assert data_detail(response) == "Only PDF and TXT files are supported right now"


def data_detail(response):
    return response.json()["detail"]