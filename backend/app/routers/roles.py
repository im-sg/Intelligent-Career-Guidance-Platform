"""
Job role recommendation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.database import Resume, JobRole, Recommendation, User, get_db
from app.models.schemas import (
    JobRoleResponse,
    RecommendationsResponse,
    RecommendationResponse,
    SkillGap,
    SkillMatch,
    SkillMatchDetails
)
from app.utils.auth import get_current_user, get_current_active_user  # Import both
from app.services.ml_role_analyzer import MLRoleAnalyzer

router = APIRouter(prefix="/roles", tags=["Job Roles"])

# Initialize ML analyzer
ml_analyzer = MLRoleAnalyzer()


@router.get("/available", response_model=List[JobRoleResponse])
def get_available_roles(db: Session = Depends(get_db)):
    """
    Get all available job roles
    
    Returns list of all job roles in the system
    """
    roles = db.query(JobRole).all()
    return roles


@router.get("/recommendations/{resume_id}", response_model=RecommendationsResponse)
def get_role_recommendations(
    resume_id: int,
    limit: int = 5,
    current_user: Optional[User] = Depends(get_current_user),  # Optional - anonymous OK
    db: Session = Depends(get_db)
):
    """
    Get ML-powered role recommendations for a resume
    
    - **resume_id**: ID of the processed resume
    - **limit**: Number of top recommendations to return (default: 5)
    - Authentication optional
    
    Returns top matching roles with suitability scores and skill gaps
    """
    # Find resume
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check if processing complete
    if resume.processing_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resume processing not complete. Status: {resume.processing_status}"
        )
    
    # Check authorization (for registered users)
    if current_user and resume.user_id != 0 and resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume"
        )
    
    # Get predictions using PURE ML approach
    parsed_data = resume.processed_data

    # Get ML predictions
    ml_predictions = ml_analyzer.predict_roles(parsed_data)

    # Get all job roles from database
    all_roles = {role.title: role for role in db.query(JobRole).all()}

    # Create recommendations
    recommendations = []

    for pred in ml_predictions[:limit]:
        role_name = pred['role']
        suitability_percentage = pred['percentage']

        # Get role details
        role = all_roles.get(role_name)

        if not role:
            continue
        
        # Generate match explanation
        match_explanation = _generate_match_explanation(suitability_percentage)
        
        # Analyze skill matches and gaps
        skill_match_details, skill_gaps = _analyze_skills(
            parsed_data,
            role.required_skills
        )
        
        # Create recommendation response
        recommendation = RecommendationResponse(
            role=JobRoleResponse(
                id=role.id,
                title=role.title,
                category=role.category,
                description=role.description,
                required_skills=role.required_skills,
                experience_level=role.experience_level,
                industry=role.industry
            ),
            suitability_percentage=suitability_percentage,
            match_explanation=match_explanation,
            skill_match_details=skill_match_details,
            skill_gaps=skill_gaps
        )
        
        recommendations.append(recommendation)
        
        # Save to database (for registered users)
        if current_user and resume.user_id != 0:
            db_recommendation = Recommendation(
                user_id=resume.user_id,
                resume_id=resume.id,
                role_id=role.id,
                suitability_score=suitability_percentage,
                match_explanation=match_explanation,
                skill_gaps=[gap.dict() for gap in skill_gaps]
            )
            db.add(db_recommendation)
    
    if current_user and resume.user_id != 0:
        db.commit()
    
    # Create user profile summary
    user_profile_summary = {
        "skills_count": len(parsed_data.get('skills', {}).get('technical', [])),
        "experience_count": len(parsed_data.get('experience', [])),
        "education_count": len(parsed_data.get('education', []))
    }
    
    return RecommendationsResponse(
        resume_id=resume_id,
        ml_powered=True,
        recommendations=recommendations,
        total_roles_analyzed=len(ml_predictions),
        user_profile_summary=user_profile_summary
    )


def _generate_match_explanation(percentage: float) -> str:
    """Generate human-readable match explanation"""
    if percentage >= 80:
        return "Excellent match! ML model predicts strong alignment with requirements."
    elif percentage >= 60:
        return "Good match! You have most of the required skills for this role."
    elif percentage >= 40:
        return "Moderate match. Some skill development recommended to qualify for this role."
    else:
        return "Limited match. Significant skill gaps exist for this role."


def _analyze_skills(parsed_data: dict, required_skills: dict):
    """
    Analyze skill matches and gaps
    
    Returns: (skill_match_details, skill_gaps)
    """
    # Extract user skills
    user_skills = {}
    if 'skills' in parsed_data and 'technical' in parsed_data['skills']:
        for skill_obj in parsed_data['skills']['technical']:
            user_skills[skill_obj['name']] = skill_obj['proficiency_score']
    
    matched_skills = []
    weak_skills = []
    missing_skills = []
    skill_gaps = []
    
    # Analyze each required skill
    for skill_name, required_level in required_skills.items():
        user_level = user_skills.get(skill_name, 0)
        
        if user_level >= required_level:
            # Strong match
            matched_skills.append(SkillMatch(
                skill=skill_name,
                user_level=user_level,
                required_level=required_level,
                status="strong"
            ))
        elif user_level > 0:
            # Weak match (has skill but below required level)
            weak_skills.append(SkillMatch(
                skill=skill_name,
                user_level=user_level,
                required_level=required_level,
                status="weak"
            ))
            
            gap_size = required_level - user_level
            skill_gaps.append(SkillGap(
                skill=skill_name,
                required_level=required_level,
                current_level=user_level,
                gap_size=gap_size,
                priority="medium"
            ))
        else:
            # Missing skill
            missing_skills.append(SkillMatch(
                skill=skill_name,
                user_level=0,
                required_level=required_level,
                status="missing"
            ))
            
            skill_gaps.append(SkillGap(
                skill=skill_name,
                required_level=required_level,
                current_level=0,
                gap_size=required_level,
                priority="high" if required_level >= 4 else "medium"
            ))
    
    skill_match_details = SkillMatchDetails(
        matched_skills=matched_skills,
        weak_skills=weak_skills,
        missing_skills=missing_skills
    )
    
    # Sort gaps by priority
    skill_gaps.sort(key=lambda x: (x.priority == "high", x.gap_size), reverse=True)
    
    return skill_match_details, skill_gaps


@router.get("/history", response_model=List[RecommendationsResponse])
def get_recommendation_history(
    current_user: User = Depends(get_current_active_user),  # Required
    db: Session = Depends(get_db)
):
    """
    Get recommendation history for authenticated user
    
    Requires authentication
    """
    # Get all recommendations for user
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).all()
    
    # Group by resume_id
    history = {}
    for rec in recommendations:
        if rec.resume_id not in history:
            history[rec.resume_id] = []
        history[rec.resume_id].append(rec)
    
    # Format response (simplified)
    return []  # TODO: Format properly if needed
