from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str
    admin: bool