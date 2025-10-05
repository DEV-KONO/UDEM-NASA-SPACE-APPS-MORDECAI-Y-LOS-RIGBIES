from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    role = Column(String(20), default="backer")  # backer, creator, admin
    bio = Column(Text)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="creator")
    pledges = relationship("Pledge", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    goal_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    category = Column(String(50))
    location = Column(String(50), default="LEO")
    orbit_altitude_km = Column(Float)
    status = Column(String(20), default="draft")  # draft, active, funded, canceled, in orbit
    image_url = Column(String)
    video_url = Column(String)
    tech_summary = Column(Text)
    estimated_timeline = Column(Text)
    risks = Column(Text)
    tags = Column(JSON)
    backers_count = Column(Integer, default=0)
    launch_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="projects")

    pledges = relationship("Pledge", back_populates="project", cascade="all, delete-orphan")
    updates = relationship("ProjectUpdate", back_populates="project", cascade="all, delete-orphan")


class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reward_tier = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="pledges")
    user = relationship("User", back_populates="pledges")


class ProjectUpdate(Base):
    __tablename__ = "project_updates"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="updates")