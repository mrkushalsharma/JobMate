from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base

class MatchScore(Base):
    __tablename__ = "match_scores"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="match_scores")

