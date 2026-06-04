
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResumeRead(BaseModel):
    id: int
    filename: str
    file_path: str
    parsed_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)