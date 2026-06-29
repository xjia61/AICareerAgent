from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.application import Application
from app.models.job import Job
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationRead,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationRead)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == application.job_id).first()
    existing_application = (
        db.query(Application)
        .filter(Application.job_id == application.job_id)
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Application already exists for this job",
        )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db_application = Application(
        job_id=application.job_id,
        status=application.status,
        next_action=application.next_action,
        notes=application.notes,
        reminder_date=application.reminder_date,
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@router.get("/", response_model=List[ApplicationRead])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.id.desc()).all()


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    update: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application