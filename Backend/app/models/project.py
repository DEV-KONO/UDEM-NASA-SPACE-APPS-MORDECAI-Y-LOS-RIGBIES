from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from app.database import Base

# Project model representing a LEO Kickstarter project
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    goal_amount = Column(Float, nullable=False, default=0.0)
    current_amount = Column(Float, nullable=False, default=0.0)
    category = Column(String(128), nullable=True)
    location = Column(String(64), nullable=False, default="LEO")
    orbit_altitude_km = Column(Float, nullable=True)
    status = Column(String(64), nullable=False, default="draft")
    image_url = Column(String(512), nullable=True)
    video_url = Column(String(512), nullable=True)
    tech_summary = Column(Text, nullable=True)
    estimated_timeline = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # store list of strings as JSON
    backers_count = Column(Integer, nullable=False, default=0)
    launch_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
