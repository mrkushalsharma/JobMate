# Job Application Tracker

A FastAPI application for tracking job applications and matching resumes with job descriptions.

## Features

- User authentication with JWT
- Upload and manage resumes (PDF, DOCX, TXT)
- Track job applications and their status
- Match resumes with job descriptions using NLP
- Calculate and store match scores

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Download NLTK data (one-time setup):
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```
6. Initialize the database:
   ```
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```
7. Run the application:
   ```
   uvicorn main:app --reload
   ```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc