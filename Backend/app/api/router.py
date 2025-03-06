from fastapi import APIRouter

from app.api import auth, jobs, match, resumes, users

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(resumes.router)
api_router.include_router(jobs.router)
api_router.include_router(match.router)