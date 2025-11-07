"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import re

# User Schemas

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: str  # Changed from EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str


# Resume Schemas

class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response"""
    message: str
    resume_id: int
    processing_status: str


class ParsedSkill(BaseModel):
    """Schema for parsed skill"""
    name: str
    proficiency_score: float
    confidence: float


class ParsedExperience(BaseModel):
    """Schema for parsed experience"""
    position: str
    company: str
    duration: str


class ParsedEducation(BaseModel):
    """Schema for parsed education"""
    degree: str
    field: str
    institution: str


class ParsedResumeData(BaseModel):
    """Schema for parsed resume data"""
    skills: Dict[str, List[ParsedSkill]]
    experience: List[ParsedExperience]
    education: List[ParsedEducation]


class ResumeResponse(BaseModel):
    """Schema for resume details response"""
    id: int
    file_name: str
    processing_status: str
    upload_date: datetime
    extracted_data: Optional[ParsedResumeData] = None
    
    class Config:
        from_attributes = True


# Job Role Schemas

class JobRoleResponse(BaseModel):
    """Schema for job role response"""
    id: int
    title: str
    category: str
    description: Optional[str]
    required_skills: Dict[str, int]
    experience_level: str
    industry: Optional[str]
    
    class Config:
        from_attributes = True


# Recommendation Schemas

class SkillGap(BaseModel):
    """Schema for skill gap"""
    skill: str
    required_level: int
    current_level: float
    gap_size: float
    priority: str


class SkillMatch(BaseModel):
    """Schema for skill match details"""
    skill: str
    user_level: float
    required_level: int
    status: str


class SkillMatchDetails(BaseModel):
    """Schema for detailed skill matching"""
    matched_skills: List[SkillMatch]
    weak_skills: List[SkillMatch]
    missing_skills: List[SkillMatch]


class RecommendationResponse(BaseModel):
    """Schema for role recommendation"""
    role: JobRoleResponse
    suitability_percentage: float
    match_explanation: str
    skill_match_details: SkillMatchDetails
    skill_gaps: List[SkillGap]


class RecommendationsResponse(BaseModel):
    """Schema for all recommendations"""
    resume_id: int
    ml_powered: bool
    recommendations: List[RecommendationResponse]
    total_roles_analyzed: int
    user_profile_summary: Dict[str, Any]
