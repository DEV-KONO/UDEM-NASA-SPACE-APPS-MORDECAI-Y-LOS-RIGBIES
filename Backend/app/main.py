from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List

from app.api.api_router import api_router
from app.database import Base, engine, get_db
from app.controllers.projects_controller import list_projects
from sqlalchemy.orm import Session

origins = [
    "https://devjourney.software"
]

app = FastAPI()


# Include existing API router under /api
app.include_router(api_router, prefix="/api")

# Serve uploaded files from uploads/ directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables when the app starts."""
    Base.metadata.create_all(bind=engine)


@app.get("/projects/", response_model=list)
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of projects."""
    try:
        projects = list_projects(db, skip=skip, limit=limit)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))