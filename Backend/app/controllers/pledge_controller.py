from sqlalchemy.orm import Session
from app.models.pledge import Pledge
from app.models.project import Project
from datetime import datetime


def create_pledge(db: Session, pledge_data: dict) -> Pledge:
    """Create a pledge and update project's current amount and backers count."""
    pledge = Pledge(**pledge_data)
    db.add(pledge)
    try:
        # update project totals
        project = db.query(Project).filter(Project.id == pledge.project_id).first()
        if project:
            project.current_amount = (project.current_amount or 0.0) + pledge.amount
            project.backers_count = (project.backers_count or 0) + 1
        db.commit()
        db.refresh(pledge)
        return pledge
    except Exception:
        db.rollback()
        raise


def list_pledges_for_project(db: Session, project_id: int):
    return db.query(Pledge).filter(Pledge.project_id == project_id).all()
