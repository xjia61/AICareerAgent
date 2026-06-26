from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class ResumeExtractionRead(BaseModel):
    id: int
    resume_id: int
    extraction_json: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)