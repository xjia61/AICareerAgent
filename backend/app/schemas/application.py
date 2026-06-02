from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    job_id: int
    status: str = "saved"
    next_action: Optional[str] = None
    notes: Optional[str] = None
    reminder_date: Optional[datetime] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    next_action: Optional[str] = None
    notes: Optional[str] = None
    reminder_date: Optional[datetime] = None


class ApplicationRead(BaseModel):
    id: int
    job_id: int
    status: str
    next_action: Optional[str] = None
    notes: Optional[str] = None
    reminder_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

    #class Config:
    #    from_attributes = True

