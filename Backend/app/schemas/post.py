from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PostModel(BaseModel):

    Img: Optional[str] = "https://placehold.co/100"
    Title: str
    Body: str
    Tags: Optional[str] = None
    Author: str = "DEV-KONO"

class PostCreate(PostModel):
    pass

class Post(PostModel):
    PostId: Optional[int] = None
    Date: Optional[datetime]

    class config:
        orm_mode = True