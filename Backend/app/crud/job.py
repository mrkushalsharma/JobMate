from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

class CRUDJob(CRUDBase[Job, JobCreate, JobResponse]):
    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(Job.owner_id == owner_id).offset(skip).limit(limit).all()

    def associate_resume(self, db: Session, *, job_id: int, resume_id: int, owner_id: int):
        job = db.query(Job).filter(Job.id == job_id, Job.owner_id == owner_id).first()
        if not job:
            return None

        from app.models.resume import Resume
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.owner_id == owner_id).first()
        if not resume:
            return None

        job.resumes.append(resume)
        db.commit()
        return job

    def remove_resume(self, db: Session, *, job_id: int, resume_id: int, owner_id: int):
        job = db.query(Job).filter(Job.id == job_id, Job.owner_id == owner_id).first()
        if not job:
            return None

        from app.models.resume import Resume
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.owner_id == owner_id).first()
        if not resume:
            return None

        job.resumes.remove(resume)
        db.commit()
        return job

job = CRUDJob(Job)

