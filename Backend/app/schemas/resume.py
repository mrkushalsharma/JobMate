from datetime import datetime
from pydantic import BaseModel

class ResumeBase(BaseModel):
    title: str

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

