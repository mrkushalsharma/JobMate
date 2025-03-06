from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.job import job
from app.crud.match import match_score
from app.crud.resume import resume
from app.database import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse
from app.schemas.resume import ResumeResponse
from app.security import get_current_active_user
from app.services.match import calculate_resume_job_match

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
async def create_job(
    job_in: JobCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return job.create(db=db, obj_in=job_in, owner_id=current_user.id)

@router.get("/", response_model=List[JobResponse])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return job.get_multi_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{job_id}", response_model=JobResponse)
async def read_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_in: JobCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.update(db=db, db_obj=db_job, obj_in=job_in)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    job.remove(db=db, id=job_id)
    return None

@router.post("/{job_id}/resumes/{resume_id}", response_model=JobResponse)
async def associate_resume_with_job(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check job exists and belongs to user
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check resume exists and belongs to user
    db_resume = resume.get(db=db, id=resume_id)
    if db_resume is None or db_resume.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Associate resume with job
    result = job.associate_resume(db=db, job_id=job_id, resume_id=resume_id, owner_id=current_user.id)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to associate resume with job")
    
    # Calculate match score
    await calculate_resume_job_match(db=db, job_id=job_id, resume_id=resume_id)
    
    return result

@router.delete("/{job_id}/resumes/{resume_id}", response_model=JobResponse)
async def remove_resume_from_job(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    result = job.remove_resume(db=db, job_id=job_id, resume_id=resume_id, owner_id=current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job or resume not found")
    return result

@router.get("/{job_id}/resumes", response_model=List[ResumeResponse])
async def read_job_resumes(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job.resumes