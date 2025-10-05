from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

# User model for platform users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False, default="creator")
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
