from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    status: Optional[str] = "Applied"

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    application_date: datetime

    class Config:
        orm_mode = True

