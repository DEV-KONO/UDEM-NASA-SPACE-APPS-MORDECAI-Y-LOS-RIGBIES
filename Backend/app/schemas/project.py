from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    goal_amount: float = 0.0
    category: Optional[str] = None
    location: Optional[str] = "LEO"
    orbit_altitude_km: Optional[float] = None
    status: Optional[str] = "draft"
    image_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
    tech_summary: Optional[str] = None
    estimated_timeline: Optional[str] = None
    risks: Optional[str] = None
    tags: Optional[List[str]] = None
    launch_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    creator_id: int


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    current_amount: float
    backers_count: int
    created_at: datetime
    updated_at: datetime
    creator_id: int

    class Config:
        orm_mode = True
