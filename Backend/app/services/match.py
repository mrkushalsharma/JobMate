from sqlalchemy.orm import Session

from app.crud.job import job
from app.crud.match import match_score
from app.crud.resume import resume
from app.utils.text_processing import calculate_match_score

async def calculate_resume_job_match(db: Session, job_id: int, resume_id: int):
    """
    Calculate the match score between a resume and a job description.
    If a match score already exists, it will be updated.
    """
    # Get job and resume objects
    db_job = job.get(db=db, id=job_id)
    db_resume = resume.get(db=db, id=resume_id)
    
    if not db_job or not db_resume:
        return None
    
    # Calculate match score
    score = calculate_match_score(db_resume.content, db_job.description)
    
    # Check if a match score already exists
    existing_match = match_score.get_by_job_resume(db=db, job_id=job_id, resume_id=resume_id)
    
    if existing_match:
        # Update existing match score
        existing_match.score = score
        db.commit()
        db.refresh(existing_match)
        return existing_match
    else:
        # Create new match score
        return match_score.create_score(db=db, job_id=job_id, resume_id=resume_id, score=score)

async def get_best_resume_for_job(db: Session, job_id: int, owner_id: int):
    """
    Get the best matching resume for a job based on match scores.
    Returns both the resume object and its match score.
    """
    # Get job object
    db_job = job.get(db=db, id=job_id)
    if not db_job or db_job.owner_id != owner_id:
        return None, None
    
    # Get all match scores for this job
    scores = match_score.get_by_job(db=db, job_id=job_id)
    
    if not scores:
        return None, None
    
    # Find the highest score
    best_match = max(scores, key=lambda score: score.score)
    
    # Get the corresponding resume
    db_resume = resume.get(db=db, id=best_match.resume_id)
    
    return db_resume, best_match

async def get_top_matching_resumes(db: Session, job_id: int, owner_id: int, limit: int = 3):
    """
    Get the top N matching resumes for a job based on match scores.
    Returns a list of (resume, match_score) tuples.
    """
    # Get job object
    db_job = job.get(db=db, id=job_id)
    if not db_job or db_job.owner_id != owner_id:
        return []
    
    # Get all match scores for this job
    scores = match_score.get_by_job(db=db, job_id=job_id)
    
    if not scores:
        return []
    
    # Sort scores by score value (descending)
    sorted_scores = sorted(scores, key=lambda score: score.score, reverse=True)
    
    # Take top N scores
    top_scores = sorted_scores[:limit]
    
    # Get corresponding resumes
    results = []
    for score in top_scores:
        db_resume = resume.get(db=db, id=score.resume_id)
        if db_resume:
            results.append((db_resume, score))
    
    return results

async def calculate_all_matches_for_user(db: Session, user_id: int):
    """
    Calculate match scores for all combinations of a user's jobs and resumes.
    """
    # Get all jobs and resumes for the user
    user_jobs = job.get_multi_by_owner(db=db, owner_id=user_id)
    user_resumes = resume.get_multi_by_owner(db=db, owner_id=user_id)
    
    results = []
    
    # Calculate match scores for all combinations
    for db_job in user_jobs:
        for db_resume in user_resumes:
            match = await calculate_resume_job_match(db=db, job_id=db_job.id, resume_id=db_resume.id)
            if match:
                results.append(match)
    
    return results