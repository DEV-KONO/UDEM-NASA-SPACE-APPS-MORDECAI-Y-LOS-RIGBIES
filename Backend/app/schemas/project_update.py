from pydantic import BaseModel
from datetime import datetime


class ProjectUpdateCreate(BaseModel):
    project_id: int
    title: str
    content: str


class ProjectUpdateOut(ProjectUpdateCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
