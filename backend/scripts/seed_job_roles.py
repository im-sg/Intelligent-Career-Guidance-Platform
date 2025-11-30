"""
Seed job roles into database
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.database import SessionLocal, JobRole

# 9 job roles with required skills
JOB_ROLES = [
    {
        "title": "AI Engineer",
        "category": "AI & ML",
        "description": "Design and implement AI systems using deep learning",
        "required_skills": {
            "Python": 4,
            "Deep Learning": 4,
            "TensorFlow": 4,
            "PyTorch": 3,
            "Machine Learning": 4
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Machine Learning Engineer",
        "category": "AI & ML",
        "description": "Build and deploy machine learning models",
        "required_skills": {
            "Python": 4,
            "Machine Learning": 4,
            "TensorFlow": 3,
            "Scikit-learn": 4,
            "Data Analysis": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Analyze complex data and build predictive models",
        "required_skills": {
            "Python": 4,
            "Machine Learning": 4,
            "Statistics": 4,
            "Data Visualization": 3,
            "SQL": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Data Engineer",
        "category": "Data & Analytics",
        "description": "Build and maintain data pipelines and infrastructure",
        "required_skills": {
            "Python": 4,
            "SQL": 4,
            "AWS": 3,
            "Pandas": 3,
            "Data Visualization": 2
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "DevOps/Cloud Engineer",
        "category": "Infrastructure",
        "description": "Manage cloud infrastructure and deployment pipelines",
        "required_skills": {
            "Docker": 4,
            "Kubernetes": 4,
            "AWS": 3,
            "Linux": 4,
            "CI/CD": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Backend Developer",
        "category": "Software Development",
        "description": "Develop server-side applications and APIs",
        "required_skills": {
            "Python": 4,
            "SQL": 3,
            "Django": 3,
            "REST API": 4,
            "Microservices": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Frontend Developer",
        "category": "Software Development",
        "description": "Build user interfaces and client-side applications",
        "required_skills": {
            "JavaScript": 4,
            "React": 4,
            "HTML": 4,
            "CSS": 4,
            "TypeScript": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Full Stack Developer",
        "category": "Software Development",
        "description": "Develop both frontend and backend applications",
        "required_skills": {
            "JavaScript": 4,
            "React": 3,
            "Python": 3,
            "SQL": 3,
            "REST API": 4
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    },
    {
        "title": "Cybersecurity Engineer",
        "category": "Security",
        "description": "Protect systems and networks from security threats",
        "required_skills": {
            "Linux": 4,
            "Python": 3,
            "Agile": 2,
            "Testing": 3
        },
        "experience_level": "intermediate",
        "industry": "Technology"
    }
]


def seed_job_roles():
    """Seed job roles into database"""
    db = SessionLocal()
    
    print("\n" + "=" * 70)
    print("SEEDING JOB ROLES")
    print("=" * 70)
    
    # Check if roles already exist
    existing_count = db.query(JobRole).count()
    
    if existing_count > 0:
        print(f"\n⚠ Database already has {existing_count} job roles")
        response = input("Do you want to clear and re-seed? (yes/no): ")
        
        if response.lower() == 'yes':
            db.query(JobRole).delete()
            db.commit()
            print("✓ Cleared existing roles")
        else:
            print("Skipping seed")
            return
    
    # Add roles
    for role_data in JOB_ROLES:
        role = JobRole(**role_data)
        db.add(role)
    
    db.commit()
    
    print(f"\n✓ Seeded {len(JOB_ROLES)} job roles successfully!")
    
    # Display seeded roles
    print("\nSeeded Roles:")
    for role_data in JOB_ROLES:
        print(f"  • {role_data['title']} ({role_data['category']})")
    
    db.close()


if __name__ == "__main__":
    seed_job_roles()
