from sqlalchemy import Boolean, Integer, Text, Column
from app.core.database import base

class Users(base):
    __tablename__ = "User_table"

    userid = Column(Integer, primary_key=True, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)