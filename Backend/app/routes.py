from fastapi import APIRouter

from .utils import init_db
from .controllers.projects import projects_controller

router = APIRouter()

@router.get("/projects")
def get_projects():
    return projects_controller.get_projects()

@router.get("/init_db")
def initialize_database():
    return init_db()