from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
from app.models.job import Job
from app.models.application import Application
from app.models.resume import Resume
from app.routers import jobs, applications, resumes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Career Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(resumes.router)


@app.get("/")
def root():
    return {"message": "AI Career Agent API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}