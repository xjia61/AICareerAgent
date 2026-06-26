from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import Job
from app.models.resume import Resume
from app.models.resume_extraction import ResumeExtraction
from app.models.job_match import JobMatch
from app.schemas.job_match import JobMatchCreate, JobMatchRead
from app.services.job_matcher import mock_match_resume_to_job

router = APIRouter(prefix="/jobs", tags=["job-matches"])


@router.post("/{job_id}/match", response_model=JobMatchRead)
def match_job_to_resume(
    job_id: int,
    request: JobMatchCreate,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    extraction = (
        db.query(ResumeExtraction)
        .filter(ResumeExtraction.resume_id == resume.id)
        .order_by(ResumeExtraction.id.desc())
        .first()
    )

    if not extraction:
        raise HTTPException(
            status_code=400,
            detail="Resume has no extracted profile. Please run resume extraction first.",
        )

    match_json = mock_match_resume_to_job(
        resume_profile=extraction.extraction_json,
        job_description=job.description or "",
        job_title=job.title or "",
    )

    job.match_score = match_json["match_score"]

    job_match = JobMatch(
        job_id=job.id,
        resume_id=resume.id,
        match_json=match_json,
    )

    db.add(job_match)
    db.commit()
    db.refresh(job_match)

    return job_match


@router.get("/{job_id}/matches", response_model=List[JobMatchRead])
def list_job_matches(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return (
        db.query(JobMatch)
        .filter(JobMatch.job_id == job_id)
        .order_by(JobMatch.id.desc())
        .all()
    )