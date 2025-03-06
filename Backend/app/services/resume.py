import io
import os
import uuid
from typing import List, Tuple

import PyPDF2
import docx
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.crud.resume import resume
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeCreate

async def process_resume_upload(
    file: UploadFile,
    title: str,
    user: User,
    db: Session
) -> Resume:
    """
    Process a resume upload:
    1. Extract text content from the file
    2. Save the file to the user's directory
    3. Create a resume record in the database
    
    Returns: The created Resume object
    """
    try:
        # Extract text from resume
        content = extract_text_from_resume(file)
        
        # Reset file pointer for saving
        file.file.seek(0)
        
        # Save file
        file_path = await save_resume_file(file, user.id)
        
        # Create resume in database
        resume_in = ResumeCreate(title=title)
        db_resume = resume.create_with_file(
            db=db,
            obj_in=resume_in,
            file_path=file_path,
            content=content,
            owner_id=user.id
        )
        
        return db_resume
    
    except Exception as e:
        # Clean up file if already saved
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )

def extract_text_from_resume(file: UploadFile) -> str:
    """Extract text content from a resume file"""
    content = ""
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    try:
        if file_extension == '.pdf':
            # Read PDF
            file_content = io.BytesIO(file.file.read())
            pdf_reader = PyPDF2.PdfReader(file_content)
            for page in pdf_reader.pages:
                content += page.extract_text()
        elif file_extension == '.docx':
            # Read DOCX
            file_content = io.BytesIO(file.file.read())
            doc = docx.Document(file_content)
            for para in doc.paragraphs:
                content += para.text + "\n"
        elif file_extension == '.txt':
            # Read TXT
            file_content = file.file.read().decode("utf-8")
            content = file_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
        
    # Reset file pointer
    file.file.seek(0)
    
    return content

async def save_resume_file(file: UploadFile, user_id: int) -> str:
    """Save a resume file to the user's directory"""
    # Create directory for user files if it doesn't exist
    user_dir = f"{settings.UPLOAD_DIR}/resumes/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"{user_dir}/{unique_filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return file_path

def extract_keywords_from_resume(resume_text: str) -> List[str]:
    """Extract important keywords from a resume"""
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    
    # Ensure NLTK data is downloaded
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
    
    # Tokenize text
    tokens = word_tokenize(resume_text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    # Return unique keywords
    from collections import Counter
    keyword_freq = Counter(keywords)
    
    # Return the most common keywords (top 50)
    return [word for word, count in keyword_freq.most_common(50)]

def get_user_resumes_with_content(db: Session, user_id: int) -> List[Tuple[Resume, str]]:
    """Get all resumes for a user with their content for analysis"""
    user_resumes = resume.get_multi_by_owner(db=db, owner_id=user_id)
    return [(res, res.content) for res in user_resumes]