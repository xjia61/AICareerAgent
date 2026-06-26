from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from app.db.session import Base


class ResumeExtraction(Base):
    __tablename__ = "resume_extractions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    extraction_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)