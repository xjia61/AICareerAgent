from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobRead)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(
        company=job.company,
        title=job.title,
        location=job.location,
        job_url=job.job_url,
        description=job.description,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=List[JobRead])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.id.desc()).all()


@router.post("/{job_id}/analyze")
def analyze_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    # Temporary rule-based score.
    # Later we replace this with OpenAI + RAG.
    description = (job.description or "").lower()
    score = 50

    keywords = ["python", "react", "fastapi", "aws", "sql", "ai", "machine learning", "rag"]
    for keyword in keywords:
        if keyword in description:
            score += 5

    score = min(score, 100)
    job.match_score = score
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "match_score": score,
        "summary": "Temporary keyword-based analysis. OpenAI RAG analysis will be added later."
    }