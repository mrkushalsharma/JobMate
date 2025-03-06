from datetime import datetime
from pydantic import BaseModel

class MatchScoreResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    score: float
    created_at: datetime

    class Config:
        orm_mode = True

