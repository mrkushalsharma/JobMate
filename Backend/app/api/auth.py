from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import settings
from app.crud.user import user
from app.database import get_db
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    authenticated_user = user.authenticate(db, username=form_data.username, password=form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = user.get_by_username(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    return user.create(db, obj_in=user_in)

