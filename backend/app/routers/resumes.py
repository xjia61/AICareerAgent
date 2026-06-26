from pathlib import Path
from uuid import uuid4
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.resume import Resume
from app.schemas.resume import ResumeRead
from app.services.resume_parser import extract_resume_text

from app.models.resume_extraction import ResumeExtraction
from app.schemas.resume_extraction import ResumeExtractionRead
from app.services.openai_resume_extractor import extract_resume_profile

router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=ResumeRead)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    lower_name = file.filename.lower()

    if not lower_name.endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported right now",
        )

    safe_filename = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / safe_filename

    content = await file.read()
    file_path.write_bytes(content)

    try:
        parsed_text = extract_resume_text(str(file_path), file.filename)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse resume: {str(exc)}",
        )

    resume = Resume(
        filename=file.filename,
        file_path=str(file_path),
        parsed_text=parsed_text,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


@router.get("/", response_model=List[ResumeRead])
def list_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).order_by(Resume.id.desc()).all()


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return resume


@router.post("/{resume_id}/extract", response_model=ResumeExtractionRead)
def extract_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if not resume.parsed_text:
        raise HTTPException(status_code=400, detail="Resume has no parsed text")

    try:
        extraction_json = extract_resume_profile(resume.parsed_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI extraction failed: {str(exc)}",
        )

    extraction = ResumeExtraction(
        resume_id=resume.id,
        extraction_json=extraction_json,
    )

    db.add(extraction)
    db.commit()
    db.refresh(extraction)

    return extraction


@router.get("/{resume_id}/extractions", response_model=list[ResumeExtractionRead])
def list_resume_extractions(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return (
        db.query(ResumeExtraction)
        .filter(ResumeExtraction.resume_id == resume_id)
        .order_by(ResumeExtraction.id.desc())
        .all()
    )