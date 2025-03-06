import io
import os
import uuid

import PyPDF2
import docx
from fastapi import HTTPException, UploadFile

from app.config import settings

def extract_text_from_resume(file: UploadFile):
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

    return content

async def save_resume_file(file: UploadFile, user_id: int):
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

