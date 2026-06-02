from pydantic import BaseModel, ConfigDict
from typing import Optional


class JobCreate(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    description: Optional[str] = None


class JobRead(BaseModel):
    id: int
    company: str
    title: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    description: Optional[str] = None
    status: str
    match_score: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

    #class Config:
    #    from_attributes = True