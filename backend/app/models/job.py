from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    location = Column(String, nullable=True)
    job_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="saved")
    match_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)