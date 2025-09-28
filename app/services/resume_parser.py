import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Sample skill list (extendable or replace with database)
COMMON_SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "java", "c++", "excel",
    "communication", "teamwork", "problem-solving", "tableau",
]

def extract_skills(text: str):
    found_skills = []
    for skill in COMMON_SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return list(set(found_skills))

def extract_education(text: str):
    education_keywords = [
        "b.tech", "bachelor", "b.sc", "m.tech", "m.sc", "mba", "ph.d", "undergraduate", "postgraduate"
    ]
    matches = []
    for line in text.lower().split('\n'):
        for keyword in education_keywords:
            if keyword in line and line not in matches:
                matches.append(line.strip())
    return matches

def extract_experience(text: str):
    exp_lines = []
    exp_patterns = re.findall(r'(at|@)\s+[A-Za-z0-9 &]+|[A-Za-z]+(?:\s+Technologies|\s+Solutions|\s+Inc\.?)', text)
    for match in exp_patterns:
        exp_lines.append(match.strip())
    return list(set(exp_lines))

def parse_resume_text(text: str):
    doc = nlp(text)
    name = None
    email = None

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "EMAIL" and not email:
            email = ent.text

    return {
        "name": name,
        "email": email,
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }
