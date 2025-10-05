from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User
from app.database import SessionLocal
from datetime import datetime


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """Return a list of projects with pagination."""
    return db.query(Project).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Retrieve a single project by id."""
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, *, project_data: dict) -> Project:
    """Create a new project from a dict of fields."""
    project = Project(**project_data)
    db.add(project)
    try:
        db.commit()
        db.refresh(project)
        return project
    except Exception:
        db.rollback()
        raise


def update_project(db: Session, project_id: int, updates: dict) -> Optional[Project]:
    """Apply updates to a project and return it."""
    project = get_project(db, project_id)
    if not project:
        return None
    for key, value in updates.items():
        if hasattr(project, key):
            setattr(project, key, value)
    project.updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(project)
        return project
    except Exception:
        db.rollback()
        raise


def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project by id. Returns True if deleted."""
    project = get_project(db, project_id)
    if not project:
        return False
    try:
        db.delete(project)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
