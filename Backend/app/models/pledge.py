from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from datetime import datetime
from app.database import Base

# Pledge model for backers pledging to projects
class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reward_tier = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
