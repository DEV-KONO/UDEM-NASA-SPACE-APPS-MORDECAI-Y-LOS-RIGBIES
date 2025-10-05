from sqlalchemy import Column, DateTime, Integer, String, Text
from app.core.database import base

class Post(base):
    __tablename__ = "Posts_Table"

    PostId = Column(Integer, primary_key=True, nullable=False)
    Img = Column(String, nullable=True, default="https://placehold.co/100")
    Title = Column(String, nullable=False)
    Body = Column(Text, nullable=False)
    Tags = Column(String, nullable=True)
    Author = Column(String, nullable=False, default="Samuel Kono Peralta")
    Date = Column(DateTime, nullable=False)