from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.associations import job_resume_association

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="Applied")
    application_date = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="jobs")
    resumes = relationship("Resume", secondary=job_resume_association, back_populates="jobs")
    match_scores = relationship("MatchScore", back_populates="job")

