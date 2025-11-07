"""
Resume Parser using spaCy NLP
Extracts: skills, experience, education
"""
import spacy
import re
import json
from pathlib import Path
from typing import Dict, List, Any
from app.utils.skill_normalizer import get_normalizer

class ResumeParser:
    def __init__(self):
        """Initialize spaCy model and skills taxonomy"""
        print("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")

        # Load skill normalizer
        self.skill_normalizer = get_normalizer()

        # Load skills taxonomy
        self.skills_taxonomy = self._load_skills_taxonomy()
        self.all_skills = self._flatten_skills()

        print(f"Loaded {len(self.all_skills)} skills in taxonomy")

    def _load_skills_taxonomy(self) -> Dict:
        """Load skills from JSON file"""
        taxonomy_path = Path("data/skills/skills_taxonomy.json")
        if taxonomy_path.exists():
            with open(taxonomy_path, 'r') as f:
                return json.load(f)
        return {}

    def _flatten_skills(self) -> List[str]:
        """Flatten skills taxonomy into single list (handles nested structure)"""
        all_skills = []

        def flatten_recursive(obj):
            if isinstance(obj, list):
                all_skills.extend(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    flatten_recursive(value)

        flatten_recursive(self.skills_taxonomy)
        return list(set(all_skills))  # Remove duplicates
    
    def parse_resume(self, text: str) -> Dict[str, Any]:
        """
        Main parsing function - extracts all information from resume
        
        Args:
            text: Raw resume text
            
        Returns:
            Dictionary with skills, experience, education
        """
        # Process text with spaCy
        doc = self.nlp(text.lower())
        
        # Extract each component
        skills = self._extract_skills(text)
        experience = self._extract_experience(text, doc)
        education = self._extract_education(text, doc)
        
        return {
            "skills": {
                "technical": skills
            },
            "experience": experience,
            "education": education
        }
    
    def _extract_skills(self, text: str) -> List[Dict]:
        """
        Extract technical skills and estimate proficiency

        Returns list of dicts: [{"name": "Python", "proficiency_score": 4.5, "confidence": 0.9}]
        """
        found_skills = []

        for skill in self.all_skills:
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            matches = re.findall(pattern, text.lower())

            if matches:
                # Calculate proficiency based on context
                proficiency = self._estimate_proficiency(text, skill)

                # Include all skills found (removed the 2.0 threshold)
                mentions = len(matches)
                confidence = min(0.95, 0.6 + (mentions * 0.08))

                found_skills.append({
                    "name": skill,
                    "proficiency_score": round(proficiency, 1),
                    "confidence": round(confidence, 2)
                })

        # Sort by proficiency (highest first)
        found_skills.sort(key=lambda x: (x['proficiency_score'], x['confidence']), reverse=True)

        return found_skills
    
    def _estimate_proficiency(self, text: str, skill: str) -> float:
        """
        Estimate skill proficiency from context clues
        
        Proficiency scale:
        5.0 = Expert (5+ years, expert, lead, architect)
        4.0 = Advanced (3-5 years, advanced, senior)
        3.0 = Intermediate (1-3 years, intermediate, experienced)
        2.0 = Beginner (< 1 year, beginner, familiar, basic)
        1.0 = Novice (learning, studied, coursework)
        """
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # Find context around skill mention
        pattern = rf'.{{0,50}}{re.escape(skill_lower)}.{{0,50}}'
        matches = re.findall(pattern, text_lower)
        
        if not matches:
            return 2.5  # Default
        
        context = ' '.join(matches)
        
        # Expert indicators (5.0)
        expert_keywords = [
            'expert', 'expertise', 'mastery', 'master', 'architect',
            'lead', '5+ years', '6 years', '7 years', '8 years', '10 years'
        ]
        if any(keyword in context for keyword in expert_keywords):
            return 5.0
        
        # Advanced indicators (4.0-4.5)
        advanced_keywords = [
            'advanced', 'senior', 'proficient', '3 years', '4 years', '5 years',
            'extensive', 'strong', 'deep knowledge'
        ]
        if any(keyword in context for keyword in advanced_keywords):
            return 4.2
        
        # Intermediate indicators (3.0-3.5)
        intermediate_keywords = [
            'intermediate', 'experienced', '2 years', '3 years',
            'working knowledge', 'hands-on', 'practical'
        ]
        if any(keyword in context for keyword in intermediate_keywords):
            return 3.5
        
        # Beginner indicators (2.0-2.5)
        beginner_keywords = [
            'beginner', 'basic', 'familiar', 'exposure', '1 year',
            'some experience', 'introduced'
        ]
        if any(keyword in context for keyword in beginner_keywords):
            return 2.5
        
        # Novice indicators (1.0-1.5)
        novice_keywords = [
            'learning', 'studied', 'coursework', 'academic', 'theory'
        ]
        if any(keyword in context for keyword in novice_keywords):
            return 1.5
        
        # Default to intermediate
        return 3.0
    
    def _extract_experience(self, text: str, doc) -> List[Dict]:
        """
        Extract work experience entries (handles complex formats)

        Returns: [{"position": "Data Scientist", "company": "TechCorp", "duration": "2020-2023"}]
        """
        experiences = []

        # Find the experience section - more flexible patterns
        exp_patterns = [
            r'(?:PROFESSIONAL\s+)?EXPERIENCE[:\s_]*\n(.*?)(?:\n\n[A-Z][A-Z\s]{8,}|\Z)',
            r'(?:WORK\s+)?HISTORY[:\s_]*\n(.*?)(?:\n\n[A-Z][A-Z\s]{8,}|\Z)',
            r'EMPLOYMENT[:\s_]*\n(.*?)(?:\n\n[A-Z][A-Z\s]{8,}|\Z)',
            # Try to find experience even without clear header
            r'(Engineer.*?(?:\d{2}/\d{4}\s*[-–]\s*\d{2}/\d{4}|[A-Z][a-z]+\s+\d{4}\s*[-–]\s*[A-Z][a-z]+\s+\d{4}).*?)(?:\n\n[A-Z][A-Z\s]{8,}|\Z)'
        ]

        exp_text = None
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                exp_text = match.group(1)
                break

        # If no section found, search the entire text
        if not exp_text:
            exp_text = text

        # Pattern 1: "Job Title | Company, Location Date - Date"
        # Example: "Business Systems Analyst | Florida Blue, Jacksonville, FL (Remote) October 2024 - Present"
        pattern1 = r'([A-Za-z\s&/]+(?:Engineer|Developer|Scientist|Analyst|Manager|Architect|Consultant|Specialist|Lead|Director|Coordinator|Administrator|Designer|Technician|Officer|Executive|Intern))\s*[|,]\s*([A-Z][A-Za-z\s&.,()-]+?)(?:\s*\((?:Remote|Hybrid|On-site)\))?\s+([A-Z][a-z]+\s+\d{4}\s*[-–]\s*(?:Present|[A-Z][a-z]+\s+\d{4})|\d{2}/\d{4}\s*[-–]\s*\d{2}/\d{4})'
        matches1 = re.findall(pattern1, text, re.IGNORECASE)

        for position, company, duration in matches1:
            experiences.append({
                "position": position.strip(),
                "company": company.strip().rstrip(',').strip(),
                "duration": duration.strip()
            })

        # Pattern 2: "Job Title, Company Date - Date"
        # Example: "Senior Software Engineer, Wipro | PUNE 06/2019 – 02/2022"
        pattern2 = r'([A-Za-z\s&/]+(?:Engineer|Developer|Scientist|Analyst|Manager|Architect|Consultant|Specialist|Lead|Director|Intern)),\s*([A-Z][A-Za-z\s&.]+?)(?:\s*\|)?\s+(?:[A-Z\s]+)?\s+(\d{2}/\d{4}\s*[-–]\s*\d{2}/\d{4})'
        matches2 = re.findall(pattern2, text)

        for position, company, duration in matches2:
            experiences.append({
                "position": position.strip(),
                "company": company.strip().rstrip('|').strip(),
                "duration": duration.strip()
            })

        # Pattern 3: Extract positions with parenthetical role descriptions
        # Example: "Engineer , BOSCH | HYDERABAD DevOps & CI/CD (DevOps Engineer, 03/2022 - 12/2023):"
        # This handles MM/YYYY date format
        pattern3a = r'(?:Engineer|Developer|Analyst)\s*,?\s*([A-Z][A-Z\s&]+)\s*\|.*?\(([A-Za-z\s&/]+(?:Engineer|Developer|Scientist|Analyst|Manager)),\s*(\d{2}/\d{4}\s*[-–]\s*\d{2}/\d{4})\)'
        matches3a = re.findall(pattern3a, exp_text)

        for company, position, duration in matches3a:
            experiences.append({
                "position": position.strip(),
                "company": company.strip(),
                "duration": duration.strip()
            })

        # Pattern 3b: Same but with Month Year format
        pattern3b = r'(?:Engineer|Developer|Analyst)\s*,?\s*([A-Z][A-Z\s&]+)\s*\|.*?\(([A-Za-z\s&/]+(?:Engineer|Developer|Scientist|Analyst|Manager)),\s*([A-Z][a-z]+\s+\d{4}\s*[-–]\s*[A-Z][a-z]+\s+\d{4})\)'
        matches3b = re.findall(pattern3b, exp_text)

        for company, position, duration in matches3b:
            experiences.append({
                "position": position.strip(),
                "company": company.strip(),
                "duration": duration.strip()
            })

        # Pattern 4: Simpler parenthetical format without clear company before
        # Example: "Infrastructure & Platform Management (Software Engineer, Mar 2022 - Dec 2022):"
        pattern4 = r'([A-Za-z\s&/]+)\s*\(([A-Za-z\s&/]+(?:Engineer|Developer|Scientist|Analyst|Manager)),\s*([A-Z][a-z]+\s+\d{4}\s*[-–]\s*[A-Z][a-z]+\s+\d{4})\)'
        matches4 = re.findall(pattern4, exp_text)

        for section_title, position, duration in matches4:
            # Try to find company in previous context (look back for company pattern)
            position_idx = exp_text.find(section_title)
            if position_idx > 0:
                # Look at the previous 200 characters for company name
                context_before = exp_text[max(0, position_idx-200):position_idx]

                # Try to find company pattern: "Engineer, COMPANY |" or "Company Location"
                company_patterns = [
                    r'(?:Engineer|Developer|Analyst)\s*,?\s*([A-Z][A-Z\s&]+)\s*\|',
                    r'\n([A-Z][A-Za-z\s&.]+(?:,|:))\s*[A-Z][a-z]+'
                ]

                company = None
                for comp_pattern in company_patterns:
                    comp_match = re.search(comp_pattern, context_before)
                    if comp_match:
                        company = comp_match.group(1).strip()
                        # Clean up trailing commas, colons
                        company = re.sub(r'[,:]+$', '', company).strip()
                        break

                if company and len(company) > 2:
                    experiences.append({
                        "position": position.strip(),
                        "company": company,
                        "duration": duration.strip()
                    })

        # Remove duplicates and clean up
        unique_experiences = []
        seen = set()

        for exp in experiences:
            # Clean up company name
            exp['company'] = re.sub(r'[,.\s|]+$', '', exp['company'])
            exp['company'] = re.sub(r'\s+', ' ', exp['company']).strip()

            # Clean up position
            exp['position'] = re.sub(r'\s+', ' ', exp['position']).strip()

            # Skip if company or position is too short or invalid
            if len(exp['company']) < 2 or len(exp['position']) < 5:
                continue

            # Skip if it's all caps and very short (likely location code)
            if exp['company'].isupper() and len(exp['company']) < 10:
                continue

            key = (exp['position'].lower(), exp['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_experiences.append(exp)

        return unique_experiences[:5]  # Return top 5
    
    def _extract_duration(self, text: str, position: str) -> str:
        """Extract duration for a position"""
        # Find context around position
        pattern = rf'.{{0,100}}{re.escape(position)}.{{0,100}}'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        if not matches:
            return "Unknown"
        
        context = ' '.join(matches)
        
        # Look for year patterns
        year_pattern = r'(\d+)\s*(?:years?|yrs?)'
        year_match = re.search(year_pattern, context)
        if year_match:
            return f"{year_match.group(1)} years"
        
        # Look for month patterns
        month_pattern = r'(\d+)\s*(?:months?|mos?)'
        month_match = re.search(month_pattern, context)
        if month_match:
            return f"{month_match.group(1)} months"
        
        return "Unknown"
    
    def _extract_education(self, text: str, doc) -> List[Dict]:
        """
        Extract education information (handles multiple formats)

        Returns: [{"degree": "Master of Science", "field": "Computer Science", "institution": "MIT", "year": "2020"}]
        """
        education = []

        # Simpler, more robust patterns

        # Pattern 1: Pipe-separated format with "in"
        # "Master's in computer science | Governors State University, Chicago IL | CGPA: 3.96 Dec 2025"
        pattern1 = r"(Master'?s?|Bachelor'?s?|B\.?Tech|M\.?Tech|MBA|M\.?S\.?|B\.?S\.?)\s+(?:of\s+[A-Za-z]+\s+)?in\s+([^|]+?)\s*\|\s*([^|,\n]+?(?:University|College|Institute|School|Tech))"
        matches1 = re.findall(pattern1, text, re.IGNORECASE)

        for degree, field, institution in matches1:
            # Try to extract year from nearby text
            year = "Unknown"
            inst_idx = text.find(institution)
            if inst_idx != -1:
                context = text[inst_idx:inst_idx+150]
                year_match = re.search(r'(20\d{2}|19\d{2})|([A-Z][a-z]+\s+20\d{2})', context)
                if year_match:
                    year = year_match.group(1) or year_match.group(2)

            education.append({
                "degree": degree.strip().title(),
                "field": field.strip().title(),
                "institution": institution.strip(),
                "year": year.strip()
            })

        # Pattern 2: Simple format without pipes
        # "Master's in Computer Science Governors State University Aug 2024 – Dec 2025"
        pattern2 = r"(Master'?s?|Bachelor'?s?|B\.?Tech|M\.?Tech)\s+(?:in|of)\s+([A-Za-z\s&]+?)\s+([A-Z][A-Za-z\s&.'-]+(?:University|College|Institute))\s+([A-Z][a-z]{2,}\s+\d{4})"
        matches2 = re.findall(pattern2, text)

        for degree, field, institution, year_str in matches2:
            education.append({
                "degree": degree.strip().title(),
                "field": field.strip().title(),
                "institution": institution.strip(),
                "year": year_str.strip()
            })

        # Pattern 3: Full degree name with pipe
        # "Bachelor of Technology in computer science | Jawaharlal Nehru Technological University"
        pattern3 = r"(Bachelor\s+of\s+Technology|Bachelor\s+of\s+Engineering|Bachelor\s+of\s+Science|Master\s+of\s+Science|Master\s+of\s+Engineering)\s+in\s+([^|]+?)\s*\|\s*([^|,\n]+?(?:University|College|Institute))"
        matches3 = re.findall(pattern3, text, re.IGNORECASE)

        for degree, field, institution in matches3:
            # Try to extract year
            year = "Unknown"
            inst_idx = text.find(institution)
            if inst_idx != -1:
                context = text[inst_idx:inst_idx+100]
                year_match = re.search(r'(20\d{2}|19\d{2})|([A-Z][a-z]+\s+20\d{2})', context)
                if year_match:
                    year = year_match.group(1) or year_match.group(2)

            education.append({
                "degree": degree.strip().title(),
                "field": field.strip().title(),
                "institution": institution.strip(),
                "year": year.strip()
            })

        # Pattern 4: University first format (common in some resumes)
        # "Governors State University Masters in Analytics Harrisburg, PA"
        # "CVR College of Engineering Bachelor of Technology in Computer Science"
        pattern4 = r"([A-Z][A-Za-z\s&.'-]+(?:University|College|Institute))\s+(Master'?s?|Bachelor'?s?|Bachelor\s+of\s+Technology|Master\s+of\s+Science)\s+(?:in\s+)?([A-Za-z\s&]+?)(?:\s+[A-Z][a-z]+,?\s+[A-Z]{2}|\n|$)"
        matches4 = re.findall(pattern4, text, re.IGNORECASE)

        for institution, degree, field in matches4:
            education.append({
                "degree": degree.strip().title(),
                "field": field.strip().title(),
                "institution": institution.strip(),
                "year": "Unknown"
            })

        # Remove duplicates and clean up
        unique_education = []
        seen = set()

        for edu in education:
            # Clean up
            edu['field'] = re.sub(r'\s+', ' ', edu['field']).strip()
            edu['institution'] = re.sub(r'\s+', ' ', edu['institution']).strip()
            edu['institution'] = re.sub(r'[,|]+$', '', edu['institution']).strip()

            # Skip if field is too short
            if len(edu['field']) < 3:
                continue

            # Skip common false positives in field names
            if any(word in edu['field'].lower() for word in ['hyderabad', 'india', 'chicago', 'newark', 'boston']):
                continue

            # Create unique key
            key = (edu['degree'].lower(), edu['field'].lower()[:20], edu['institution'].lower()[:30])
            if key not in seen:
                seen.add(key)
                unique_education.append(edu)

        return unique_education

if __name__ == "__main__":
    # Test the parser
    parser = ResumeParser()
    
    sample_resume = """
    John Doe
    Senior Data Scientist
    
    EXPERIENCE
    Senior Data Scientist at TechCorp (3 years)
    - Built machine learning models using Python and TensorFlow
    - Advanced proficiency in SQL and data visualization
    
    Data Analyst at StartupXYZ (2 years)
    - Worked with Python, Pandas, and Tableau
    
    EDUCATION
    Master of Science in Data Science
    University of Technology
    
    SKILLS
    Expert in Python, Machine Learning, Deep Learning
    Proficient in SQL, TensorFlow, PyTorch, AWS
    Familiar with Docker and Kubernetes
    """
    
    result = parser.parse_resume(sample_resume)
    
    print("\nParsed Result:")
    print(f"Skills found: {len(result['skills']['technical'])}")
    print(f"Experience entries: {len(result['experience'])}")
    print(f"Education entries: {len(result['education'])}")
    
    print("\nTop 5 Skills:")
    for skill in result['skills']['technical'][:5]:
        print(f"  {skill['name']}: {skill['proficiency_score']:.1f}/5.0 (confidence: {skill['confidence']:.2f})")
