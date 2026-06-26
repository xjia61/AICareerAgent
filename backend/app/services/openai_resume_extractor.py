from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field

from app.db.session import settings


class EducationItem(BaseModel):
    school: str = Field(description="School or university name")
    degree: str = Field(description="Degree or program")
    field: str = Field(description="Field of study")
    years: str = Field(description="Date range or graduation year")


class ExperienceItem(BaseModel):
    title: str
    organization: str
    years: str
    description: str
    skills: List[str]


class ProjectItem(BaseModel):
    name: str
    description: str
    tech_stack: List[str]
    resume_bullets: List[str]


class ResumeProfile(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    target_roles: List[str]
    technical_skills: List[str]
    domain_skills: List[str]
    education: List[EducationItem]
    work_experience: List[ExperienceItem]
    projects: List[ProjectItem]
    strengths: List[str]
    missing_information: List[str]


def extract_resume_profile(parsed_text: str) -> dict:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please set it in backend/.env")

    client = OpenAI(api_key=settings.openai_api_key)

    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert career assistant. "
                    "Extract structured career profile information from resume text. "
                    "Do not invent facts. If information is missing, use an empty string or add it to missing_information."
                ),
            },
            {
                "role": "user",
                "content": parsed_text,
            },
        ],
        response_format=ResumeProfile,
    )

    profile = completion.choices[0].message.parsed
    return profile.model_dump()