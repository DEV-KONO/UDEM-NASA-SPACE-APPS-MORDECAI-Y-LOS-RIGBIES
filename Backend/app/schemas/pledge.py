from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PledgeCreate(BaseModel):
    project_id: int
    user_id: int
    amount: float
    reward_tier: Optional[str] = None


class PledgeOut(PledgeCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
