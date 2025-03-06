from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.job import job
from app.crud.match import match_score
from app.crud.resume import resume
from app.database import get_db
from app.models.user import User
from app.schemas.match import MatchScoreResponse
from app.security import get_current_active_user
from app.services.match import calculate_resume_job_match

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/jobs/{job_id}", response_model=List[MatchScoreResponse])
async def get_job_match_scores(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify job belongs to user
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get match scores for job
    return match_score.get_by_job(db=db, job_id=job_id)

@router.get("/jobs/{job_id}/resumes/{resume_id}", response_model=MatchScoreResponse)
async def get_specific_match_score(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify job belongs to user
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify resume belongs to user
    db_resume = resume.get(db=db, id=resume_id)
    if db_resume is None or db_resume.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get match score
    db_match = match_score.get_by_job_resume(db=db, job_id=job_id, resume_id=resume_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match score not found")
    
    return db_match

@router.post("/calculate/jobs/{job_id}/resumes/{resume_id}", response_model=MatchScoreResponse)
async def calculate_match(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify job belongs to user
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify resume belongs to user
    db_resume = resume.get(db=db, id=resume_id)
    if db_resume is None or db_resume.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Calculate match score
    return await calculate_resume_job_match(db=db, job_id=job_id, resume_id=resume_id)

@router.post("/calculate-all/jobs/{job_id}", response_model=List[MatchScoreResponse])
async def calculate_all_matches_for_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify job belongs to user
    db_job = job.get(db=db, id=job_id)
    if db_job is None or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get all user's resumes
    resumes = resume.get_multi_by_owner(db=db, owner_id=current_user.id)
    
    # Calculate match scores for all resumes
    results = []
    for res in resumes:
        match = await calculate_resume_job_match(db=db, job_id=job_id, resume_id=res.id)
        results.append(match)
    
    return results