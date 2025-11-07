"""
Resume processing endpoints - upload, parse, and retrieve
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.models.database import User, Resume, UserSkill, get_db
from app.models.schemas import ResumeUploadResponse, ResumeResponse, ParsedResumeData
from app.utils.auth import get_current_user, get_current_active_user  # Import both
from app.services.file_processor import FileProcessor
from app.services.resume_parser import ResumeParser

router = APIRouter(prefix="/resume", tags=["Resume"])

# Initialize services
file_processor = FileProcessor()
resume_parser = ResumeParser()

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user),  # Optional - anonymous OK
    db: Session = Depends(get_db)
):
    """
    Upload and process resume
    
    - **file**: Resume file (PDF, DOCX, or TXT, max 10MB)
    - Authentication is optional (works for anonymous users)
    
    Returns resume_id and processing status
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size {file_size} bytes exceeds maximum allowed size {MAX_FILE_SIZE} bytes"
        )
    
    # Determine user_id (0 for anonymous)
    user_id = current_user.id if current_user else 0
    
    # Create user directory
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = user_dir / safe_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Create resume record
    resume = Resume(
        user_id=user_id,
        file_name=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        file_type=file_ext,
        processing_status="processing"
    )
    
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # Process resume asynchronously (in real app, use background task)
    try:
        # Extract text
        raw_text = file_processor.extract_text(str(file_path), file_ext)
        resume.raw_text = raw_text
        
        # Parse with NLP
        parsed_data = resume_parser.parse_resume(raw_text)
        resume.processed_data = parsed_data
        
        # Store skills in UserSkills table (only for registered users)
        if current_user and 'skills' in parsed_data and 'technical' in parsed_data['skills']:
            for skill_obj in parsed_data['skills']['technical']:
                user_skill = UserSkill(
                    user_id=user_id,
                    skill_name=skill_obj['name'],
                    proficiency_score=skill_obj['proficiency_score'],
                    confidence_score=skill_obj['confidence'],
                    extracted_from="resume"
                )
                db.add(user_skill)
        
        resume.processing_status = "completed"
        
    except Exception as e:
        resume.processing_status = "failed"
        print(f"Error processing resume: {e}")
    
    db.commit()
    db.refresh(resume)
    
    return {
        "message": "Resume uploaded and processed successfully",
        "resume_id": resume.id,
        "processing_status": resume.processing_status
    }


@router.get("/parsed/{resume_id}", response_model=ResumeResponse)
def get_parsed_resume(
    resume_id: int,
    current_user: Optional[User] = Depends(get_current_user),  # Optional
    db: Session = Depends(get_db)
):
    """
    Get parsed resume data
    
    - **resume_id**: ID of the uploaded resume
    - Authentication optional (anonymous resumes accessible by anyone)
    
    Returns parsed skills, experience, and education
    """
    # Find resume
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check authorization (only for registered users' private resumes)
    if current_user and resume.user_id != 0 and resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume"
        )
    
    # Check if processing complete
    if resume.processing_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=f"Resume is still processing. Status: {resume.processing_status}"
        )
    
    # Format response
    response = {
        "id": resume.id,
        "file_name": resume.file_name,
        "processing_status": resume.processing_status,
        "upload_date": resume.upload_date,
        "extracted_data": resume.processed_data
    }
    
    return response


@router.get("/list", response_model=List[ResumeResponse])
def list_resumes(
    current_user: User = Depends(get_current_active_user),  # Required - must be logged in
    db: Session = Depends(get_db)
):
    """
    List all resumes for authenticated user
    
    Requires authentication
    """
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "processing_status": r.processing_status,
            "upload_date": r.upload_date,
            "extracted_data": r.processed_data if r.processing_status == "completed" else None
        }
        for r in resumes
    ]


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),  # Required
    db: Session = Depends(get_db)
):
    """
    Delete resume
    
    Requires authentication
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Delete file
    try:
        os.remove(resume.file_path)
    except:
        pass
    
    # Delete from database
    db.delete(resume)
    db.commit()
    
    return None
