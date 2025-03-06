from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

job_resume_association = Table(
    'job_resume_association',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id')),
    Column('resume_id', Integer, ForeignKey('resumes.id'))
)

