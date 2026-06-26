from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class JobMatchCreate(BaseModel):
    resume_id: int


class JobMatchRead(BaseModel):
    id: int
    job_id: int
    resume_id: int
    match_json: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)