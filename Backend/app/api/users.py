from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.crud.user import user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.security import get_current_active_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user(
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if email:
        email_exists = user.get_by_email(db, email=email)
        if email_exists and email_exists.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = email

    if password:
        current_user.hashed_password = get_password_hash(password)

    db.commit()
    db.refresh(current_user)
    return current_user

