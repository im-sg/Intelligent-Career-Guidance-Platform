"""
SQLAlchemy database models
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL
DATABASE_URL = "sqlite:///./career_ai.db"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

# Models

class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """Resume upload model"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(10), nullable=False)
    raw_text = Column(Text)
    processed_data = Column(JSON)  # Stores parsed resume data
    processing_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    recommendations = relationship("Recommendation", back_populates="resume", cascade="all, delete-orphan")


class JobRole(Base):
    """Job role definitions"""
    __tablename__ = "job_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    required_skills = Column(JSON, nullable=False)  # {"Python": 4, "SQL": 3, ...}
    experience_level = Column(String(20))  # entry, intermediate, advanced
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="role")


class UserSkill(Base):
    """User skills extracted from resume"""
    __tablename__ = "user_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency_score = Column(Float, nullable=False)  # 0.0 - 5.0
    confidence_score = Column(Float)  # 0.0 - 1.0
    extracted_from = Column(String(20), default="resume")  # resume, manual_input, assessment
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="skills")


class Recommendation(Base):
    """ML-generated role recommendations"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("job_roles.id"), nullable=False)
    suitability_score = Column(Float, nullable=False)  # 0.0 - 100.0
    match_explanation = Column(Text)
    skill_gaps = Column(JSON)  # [{"skill": "TensorFlow", "required": 4, "current": 0, ...}]
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    resume = relationship("Resume", back_populates="recommendations")
    role = relationship("JobRole", back_populates="recommendations")


# Create all tables
def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


# Dependency for getting DB session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
