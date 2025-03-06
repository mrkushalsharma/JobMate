import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Job Application Tracker"
    PROJECT_VERSION = "1.0.0"
    PROJECT_DESCRIPTION = "API for tracking job applications and matching resumes with job descriptions"

    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/job_tracker")

    # JWT Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "0d25c27b9a38f33e6a1aef3d5d5518691c456e4ce3ee1dcfa9f9f12ccc5ddaba")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Upload settings
    UPLOAD_DIR = "uploads"
    ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

    # CORS settings
    CORS_ORIGINS = ["*"]  # Modify in production

settings = Settings()

