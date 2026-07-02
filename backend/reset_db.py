from app.db.session import SessionLocal
from app.models.job_match import JobMatch
from app.models.resume_extraction import ResumeExtraction
from app.models.application import Application
from app.models.resume import Resume
from app.models.job import Job

db = SessionLocal()

try:
    for model in [JobMatch, ResumeExtraction, Application, Resume, Job]:
        db.query(model).delete()
    db.commit()
    print("Database data cleared successfully.")
finally:
    db.close()