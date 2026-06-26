from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from app.db.session import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    match_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)