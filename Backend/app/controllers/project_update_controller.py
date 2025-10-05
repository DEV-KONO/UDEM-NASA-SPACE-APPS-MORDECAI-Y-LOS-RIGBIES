from sqlalchemy.orm import Session
from app.models.project_update import ProjectUpdate


def create_update(db: Session, update_data: dict) -> ProjectUpdate:
    upd = ProjectUpdate(**update_data)
    db.add(upd)
    try:
        db.commit()
        db.refresh(upd)
        return upd
    except Exception:
        db.rollback()
        raise


def list_updates_for_project(db: Session, project_id: int):
    return db.query(ProjectUpdate).filter(ProjectUpdate.project_id == project_id).all()
