
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.db.session import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(Text, nullable=False)
    parsed_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)