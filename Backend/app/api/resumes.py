from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.crud.resume import resume
from app.database import get_db
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeResponse
from app.security import get_current_active_user
from app.utils.file_processing import extract_text_from_resume, save_resume_file

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("/", response_model=ResumeResponse)
async def create_resume(
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Extract text content first (to validate the file)
    content = extract_text_from_resume(file)

    # Reset file pointer
    file.file.seek(0)

    # Save the file
    file_path = await save_resume_file(file, current_user.id)

    # Create resume in database
    resume_in = ResumeCreate(title=title)
    db_resume = resume.create_with_file(
        db=db,
        obj_in=resume_in,
        file_path=file_path,
        content=content,
        owner_id=current_user.id
    )

    return db_resume

@router.get("/", response_model=List[ResumeResponse])
async def read_resumes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return resume.get_multi_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{resume_id}", response_model=ResumeResponse)
async def read_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_resume = resume.get(db=db, id=resume_id)
    if db_resume is None or db_resume.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_resume = resume.get(db=db, id=resume_id)
    if db_resume is None or db_resume.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")

    import os
    # Delete file if it exists
    if db_resume.file_path and os.path.exists(db_resume.file_path):
        os.remove(db_resume.file_path)

    resume.remove(db=db, id=resume_id)
    return None

