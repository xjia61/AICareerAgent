from typing import List


def normalize_text(text: str) -> str:
    return (text or "").lower()


def find_keywords(text: str, keywords: List[str]) -> List[str]:
    text_lower = normalize_text(text)
    return [keyword for keyword in keywords if keyword.lower() in text_lower]


def mock_match_resume_to_job(resume_profile: dict, job_description: str, job_title: str = "") -> dict:
    technical_skills = resume_profile.get("technical_skills", []) or []
    domain_skills = resume_profile.get("domain_skills", []) or []

    candidate_skills = list(set(technical_skills + domain_skills))
    job_text = normalize_text(job_title + "\n" + (job_description or ""))

    common_job_keywords = [
        "python",
        "fastapi",
        "react",
        "postgresql",
        "sql",
        "aws",
        "docker",
        "openai",
        "rag",
        "langchain",
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "javascript",
        "java",
        "c++",
        "clinical",
        "healthcare",
        "pathology",
        "ehr",
        "data",
        "backend",
        "api",
        "cloud",
        "llm",
    ]

    required_keywords = find_keywords(job_text, common_job_keywords)
    matched_skills = [
        skill for skill in candidate_skills if skill.lower() in job_text
    ]

    missing_skills = [
        keyword for keyword in required_keywords
        if keyword not in [skill.lower() for skill in matched_skills]
    ]

    if required_keywords:
        score = int((len(matched_skills) / len(required_keywords)) * 100)
    else:
        score = 50

    if "ai" in job_text or "llm" in job_text or "machine learning" in job_text:
        score += 10

    if "clinical" in job_text or "healthcare" in job_text or "pathology" in job_text:
        score += 10

    score = max(0, min(score, 100))

    if score >= 80:
        fit_level = "Strong"
    elif score >= 60:
        fit_level = "Moderate"
    elif score >= 40:
        fit_level = "Weak"
    else:
        fit_level = "Low"

    resume_bullets = [
        "Built a full-stack AI career assistant using React, FastAPI, PostgreSQL, and AI-assisted job matching workflows.",
        "Implemented backend APIs for resume ingestion, structured extraction, job tracking, and application workflow management.",
    ]

    if "aws" in job_text:
        resume_bullets.append(
            "Designed the system for AWS deployment with containerized backend services and cloud-ready database configuration."
        )

    if "clinical" in job_text or "healthcare" in job_text or "pathology" in job_text:
        resume_bullets.append(
            "Applied clinical and pathology domain knowledge to AI workflow design for healthcare-related use cases."
        )

    return {
        "match_score": score,
        "fit_level": fit_level,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_keywords_detected": required_keywords,
        "summary": (
            f"This is a {fit_level.lower()} match based on overlap between the resume profile "
            f"and the job description."
        ),
        "recommended_resume_bullets": resume_bullets,
        "application_strategy": (
            "Apply after tailoring the resume bullets to emphasize the matched skills. "
            "Address missing skills briefly in the cover letter or learning plan."
        ),
    }