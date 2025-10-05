from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.projects_controller import list_projects, get_project, create_project, update_project, delete_project
from app.controllers.pledge_controller import create_pledge, list_pledges_for_project
from app.controllers.project_update_controller import create_update, list_updates_for_project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate as ProjectUpdateSchema
from app.schemas.pledge import PledgeCreate, PledgeOut
from app.schemas.project_update import ProjectUpdateCreate, ProjectUpdateOut

router = APIRouter()


@router.get("/", response_model=List[ProjectOut])
def api_list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_projects(db, skip=skip, limit=limit)


@router.post("/", response_model=ProjectOut)
def api_create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    data = payload.dict()
    try:
        project = create_project(db, project_data=data)
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}", response_model=ProjectOut)
def api_get_project(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def api_update_project(project_id: int, payload: ProjectUpdateSchema, db: Session = Depends(get_db)):
    project = update_project(db, project_id, updates=payload.dict(exclude_unset=True))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def api_delete_project(project_id: int, db: Session = Depends(get_db)):
    ok = delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"deleted": True}


@router.post("/{project_id}/pledges", response_model=PledgeOut)
def api_create_pledge(project_id: int, payload: PledgeCreate, db: Session = Depends(get_db)):
    data = payload.dict()
    # ensure path project_id matches body
    if data.get('project_id') != project_id:
        raise HTTPException(status_code=400, detail="project_id mismatch")
    try:
        pledge = create_pledge(db, pledge_data=data)
        return pledge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}/pledges", response_model=List[PledgeOut])
def api_list_pledges(project_id: int, db: Session = Depends(get_db)):
    return list_pledges_for_project(db, project_id)


@router.post("/{project_id}/updates", response_model=ProjectUpdateOut)
def api_create_update(project_id: int, payload: ProjectUpdateCreate, db: Session = Depends(get_db)):
    data = payload.dict()
    if data.get('project_id') != project_id:
        raise HTTPException(status_code=400, detail="project_id mismatch")
    try:
        upd = create_update(db, update_data=data)
        return upd
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}/updates", response_model=List[ProjectUpdateOut])
def api_list_updates(project_id: int, db: Session = Depends(get_db)):
    return list_updates_for_project(db, project_id)
