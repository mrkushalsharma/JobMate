"""
Common dependencies for the application
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_active_user, get_current_user

# Re-export common dependencies for convenience
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")