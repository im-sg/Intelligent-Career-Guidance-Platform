"""
Clean and categorize resume dataset
Works with structured Hugging Face resume data
"""
import json
import pandas as pd
from pathlib import Path
import re
import hashlib

# Role mappings (10 unified categories)
ROLE_MAPPINGS = {
    'AI Engineer': [
        'AI Engineer', 'Deep Learning Engineer', 'NLP Engineer', 
        'Computer Vision Engineer', 'Language Model Engineer',
        'Nlp Engineer', 'Artificial Intelligence'
    ],
    'Machine Learning Engineer': [
        'Machine Learning Engineer', 'MLOps Engineer', 'ML Engineer',
        'Research Engineer', 'Applied Scientist', 'Mlops Engineer',
        'Machine Learning'
    ],
    'Data Scientist': [
        'Data Scientist', 'Data Science', 'Senior Data Scientist',
        'Lead Data Scientist', 'Principal Data Scientist'
    ],
    'Data Engineer': [
        'Data Engineer', 'ETL Developer', 'Big Data Engineer',
        'Data Pipeline Engineer', 'Database Engineer'
    ],
    'DevOps/Cloud Engineer': [
        'DevOps Engineer', 'Devops Engineer', 'Cloud Engineer',
        'Cloud Architect', 'Site Reliability Engineer', 'SRE',
        'Infrastructure Engineer', 'Platform Engineer'
    ],
    'Cybersecurity Engineer': [
        'Cybersecurity', 'Security Engineer', 'Information Security',
        'Penetration Tester', 'Security Analyst', 'Network Security'
    ],
    'Backend Developer': [
        'Backend Developer', 'Backend Engineer', 'Server Side Developer',
        'API Developer', 'Node.js Developer', 'Java Developer',
        'Python Developer'
    ],
    'Full Stack Developer': [
        'Full Stack Developer', 'Full Stack Engineer',
        'Full-Stack Developer', 'Fullstack Developer'
    ],
    'Frontend Developer': [
        'Frontend Developer', 'Frontend Engineer', 'UI Developer',
        'React Developer', 'Angular Developer', 'Vue Developer',
        'Web Developer', 'JavaScript Developer'
    ],
    'Data Analyst': [
        'Data Analyst', 'Business Analyst', 'Analytics',
        'Business Intelligence Analyst', 'BI Analyst'
    ]
}

def extract_job_titles_from_experience(experience_data):
    """Extract job titles from experience field"""
    # Handle None or NaN
    if experience_data is None:
        return []
    
    # Check if pandas NaN
    try:
        if pd.isna(experience_data):
            return []
    except (ValueError, TypeError):
        # If it's an array, pd.isna will fail, so it's valid data
        pass
    
    job_titles = []
    
    # Handle different data types
    if isinstance(experience_data, str):
        # Empty string check
        if not experience_data.strip():
            return []
        
        # Try to parse as JSON
        try:
            experience_data = json.loads(experience_data)
        except:
            # If not JSON, extract titles using patterns
            patterns = [
                r'(?:Position|Role|Title):\s*([^\n]+)',
                r'(?:as|as a|as an)\s+([A-Z][a-zA-Z\s]+(?:Engineer|Developer|Scientist|Analyst))',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, experience_data, re.IGNORECASE)
                job_titles.extend(matches)
            return job_titles
    
    # Handle list
    if isinstance(experience_data, list):
        # Empty list check
        if len(experience_data) == 0:
            return []
        
        for exp in experience_data:
            if isinstance(exp, dict):
                # Look for common keys
                for key in ['position', 'title', 'role', 'job_title', 'designation', 'Position', 'Title', 'Role']:
                    if key in exp and exp[key]:
                        job_titles.append(str(exp[key]))
            elif isinstance(exp, str):
                job_titles.append(exp)
    
    # Handle dict
    elif isinstance(experience_data, dict):
        for key in ['position', 'title', 'role', 'job_title', 'designation', 'Position', 'Title', 'Role']:
            if key in experience_data and experience_data[key]:
                if isinstance(experience_data[key], list):
                    job_titles.extend([str(x) for x in experience_data[key]])
                else:
                    job_titles.append(str(experience_data[key]))
    
    return job_titles

def map_to_unified_role(job_titles):
    """Map job titles to unified role category"""
    if not job_titles:
        return None
    
    # Try each job title
    for title in job_titles:
        if not title:
            continue
        
        # Handle if title is not a string
        title = str(title).strip()
        
        if not title:
            continue
        
        # Check against each unified role
        for unified_role, variants in ROLE_MAPPINGS.items():
            for variant in variants:
                if variant.lower() in title.lower():
                    return unified_role
    
    return None

def reconstruct_resume_text(row):
    """Reconstruct full resume text from structured fields"""
    text_parts = []
    
    # Helper function to convert any data to string
    def to_string(data):
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        if isinstance(data, (list, dict)):
            return json.dumps(data, indent=2)
        return str(data)
    
    # Personal info
    if 'personal_info' in row and row['personal_info'] is not None:
        try:
            if not pd.isna(row['personal_info']):
                text_parts.append(to_string(row['personal_info']))
        except (ValueError, TypeError):
            text_parts.append(to_string(row['personal_info']))
    
    # Experience
    if 'experience' in row and row['experience'] is not None:
        try:
            if not pd.isna(row['experience']):
                text_parts.append("\nEXPERIENCE\n")
                text_parts.append(to_string(row['experience']))
        except (ValueError, TypeError):
            text_parts.append("\nEXPERIENCE\n")
            text_parts.append(to_string(row['experience']))
    
    # Education
    if 'education' in row and row['education'] is not None:
        try:
            if not pd.isna(row['education']):
                text_parts.append("\nEDUCATION\n")
                text_parts.append(to_string(row['education']))
        except (ValueError, TypeError):
            text_parts.append("\nEDUCATION\n")
            text_parts.append(to_string(row['education']))
    
    # Skills
    if 'skills' in row and row['skills'] is not None:
        try:
            if not pd.isna(row['skills']):
                text_parts.append("\nSKILLS\n")
                skills = row['skills']
                if isinstance(skills, list):
                    text_parts.append(", ".join(str(s) for s in skills))
                else:
                    text_parts.append(to_string(skills))
        except (ValueError, TypeError):
            text_parts.append("\nSKILLS\n")
            skills = row['skills']
            if isinstance(skills, list):
                text_parts.append(", ".join(str(s) for s in skills))
            else:
                text_parts.append(to_string(skills))
    
    # Projects
    if 'projects' in row and row['projects'] is not None:
        try:
            if not pd.isna(row['projects']):
                text_parts.append("\nPROJECTS\n")
                text_parts.append(to_string(row['projects']))
        except (ValueError, TypeError):
            text_parts.append("\nPROJECTS\n")
            text_parts.append(to_string(row['projects']))
    
    # Certifications
    if 'certifications' in row and row['certifications'] is not None:
        try:
            if not pd.isna(row['certifications']):
                text_parts.append("\nCERTIFICATIONS\n")
                text_parts.append(to_string(row['certifications']))
        except (ValueError, TypeError):
            text_parts.append("\nCERTIFICATIONS\n")
            text_parts.append(to_string(row['certifications']))
    
    # Achievements
    if 'achievements' in row and row['achievements'] is not None:
        try:
            if not pd.isna(row['achievements']):
                text_parts.append("\nACHIEVEMENTS\n")
                text_parts.append(to_string(row['achievements']))
        except (ValueError, TypeError):
            text_parts.append("\nACHIEVEMENTS\n")
            text_parts.append(to_string(row['achievements']))
    
    return "\n".join(text_parts)

def clean_resume_text(text):
    """Clean resume text"""
    if text is None:
        return None
    
    try:
        if pd.isna(text):
            return None
    except (ValueError, TypeError):
        pass
    
    if not text:
        return None
    
    text = str(text)
    text = text.replace('\x00', '').replace('\ufffd', '')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    if len(text) < 100:
        return None
    
    return text

def compute_text_hash(text):
    """Generate hash for duplicate detection"""
    if not text:
        return None
    normalized = re.sub(r'\s+', '', text.lower())
    return hashlib.md5(normalized.encode()).hexdigest()

def clean_and_categorize_dataset():
    """Main cleaning pipeline"""
    print("=" * 70)
    print("DATA CLEANING AND CATEGORIZATION")
    print("=" * 70)
    
    # Load dataset
    print("\nLoading dataset...")
    df = pd.read_json("data/raw/master_resumes.jsonl", lines=True)
    print(f"Loaded {len(df)} resumes")
    print(f"Dataset columns: {list(df.columns)}")
    
    # Extract job titles from experience field
    print("\n" + "-" * 70)
    print("STEP 1: Extracting job titles from experience")
    print("-" * 70)
    
    print("\nExtracting job titles...")
    df['job_titles'] = df['experience'].apply(extract_job_titles_from_experience)
    
    # Show sample
    print("\nSample job titles extracted:")
    for idx in range(min(5, len(df))):
        titles = df['job_titles'].iloc[idx]
        print(f"  Resume {idx}: {titles[:3] if len(titles) > 3 else titles}")
    
    # Map to unified roles
    print("\nMapping to unified roles...")
    df['unified_role'] = df['job_titles'].apply(map_to_unified_role)
    
    mapped_count = df['unified_role'].notna().sum()
    unmapped_count = df['unified_role'].isna().sum()
    
    print(f"\nResults:")
    print(f"  Mapped to unified roles: {mapped_count}")
    print(f"  Unmapped: {unmapped_count}")
    
    # Show distribution
    if mapped_count > 0:
        print(f"\nRole distribution:")
        role_counts = df['unified_role'].value_counts()
        for role, count in role_counts.items():
            print(f"  {role:<30} {count:>5} resumes")
    else:
        print("\nWARNING: No resumes were mapped to roles!")
        print("Sample unmapped job titles:")
        unmapped_df = df[df['unified_role'].isna()]
        for idx in range(min(10, len(unmapped_df))):
            titles = unmapped_df['job_titles'].iloc[idx]
            print(f"  {titles}")
    
    # Reconstruct resume text
    print("\n" + "-" * 70)
    print("STEP 2: Reconstructing resume text from structured fields")
    print("-" * 70)
    
    print("\nReconstructing text...")
    df['resume_text'] = df.apply(reconstruct_resume_text, axis=1)
    
    # Clean text
    print("\nCleaning resume text...")
    df['cleaned_text'] = df['resume_text'].apply(clean_resume_text)
    
    valid_text_count = df['cleaned_text'].notna().sum()
    invalid_text_count = df['cleaned_text'].isna().sum()
    
    print(f"\nResults:")
    print(f"  Valid resume text: {valid_text_count}")
    print(f"  Invalid: {invalid_text_count}")
    
    # Filter valid resumes
    print("\n" + "-" * 70)
    print("STEP 3: Filtering valid resumes")
    print("-" * 70)
    
    valid_df = df[
        (df['unified_role'].notna()) &
        (df['cleaned_text'].notna())
    ].copy()
    
    print(f"\nValid resumes: {len(valid_df)} out of {len(df)}")
    
    if len(valid_df) == 0:
        print("\nERROR: No valid resumes found!")
        return None
    
    # Remove duplicates
    print("\n" + "-" * 70)
    print("STEP 4: Removing duplicates")
    print("-" * 70)
    
    valid_df['text_hash'] = valid_df['cleaned_text'].apply(compute_text_hash)
    before_dedup = len(valid_df)
    valid_df = valid_df.drop_duplicates(subset=['text_hash'], keep='first')
    after_dedup = len(valid_df)
    
    print(f"\nDuplicates removed: {before_dedup - after_dedup}")
    print(f"Unique resumes: {after_dedup}")
    
    # Quality validation
    print("\n" + "-" * 70)
    print("STEP 5: Quality validation")
    print("-" * 70)
    
    valid_df['word_count'] = valid_df['cleaned_text'].str.split().str.len()
    before_quality = len(valid_df)
    valid_df = valid_df[valid_df['word_count'] >= 50]
    after_quality = len(valid_df)
    
    print(f"\nResumes with < 50 words removed: {before_quality - after_quality}")
    print(f"Quality-validated: {after_quality}")
    
    if after_quality == 0:
        print("\nERROR: No resumes passed quality validation!")
        return None
    
    # Save organized data
    print("\n" + "-" * 70)
    print("STEP 6: Saving organized data")
    print("-" * 70)
    
    save_organized_resumes(valid_df)
    
    # Final summary
    print("\n" + "=" * 70)
    print("CLEANING COMPLETE")
    print("=" * 70)
    print(f"\nFinal statistics:")
    print(f"  Total processed: {len(df)}")
    print(f"  Final clean dataset: {len(valid_df)}")
    
    return valid_df

def save_organized_resumes(df):
    """Save resumes in organized structure"""
    output_dir = Path("data/collected_resumes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    metadata = []
    
    print("\nCreating organized files...")
    
    for idx, row in df.iterrows():
        if len(metadata) % 100 == 0 and len(metadata) > 0:
            print(f"  Processed {len(metadata)}/{len(df)}...")
        
        unified_role = row['unified_role']
        job_titles = row['job_titles']
        cleaned_text = row['cleaned_text']
        word_count = row['word_count']
        
        # Create role folder
        role_folder = unified_role.lower().replace('/', '_').replace(' ', '_')
        role_dir = output_dir / role_folder
        role_dir.mkdir(exist_ok=True)
        
        # Save file
        filename = f"resume_{len(metadata):04d}.txt"
        file_path = role_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        # Track metadata
        metadata.append({
            'id': f"clean_{len(metadata):04d}",
            'filename': filename,
            'unified_role': unified_role,
            'original_titles': ', '.join(str(t) for t in job_titles) if job_titles else '',
            'category_folder': role_folder,
            'file_path': str(file_path),
            'word_count': word_count,
            'source': 'huggingface',
            'status': 'cleaned',
            'labeled': True
        })
    
    # Save metadata
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv('data/resume_metadata.csv', index=False)
    
    print(f"\nSaved:")
    print(f"  Files: data/collected_resumes/<role_folder>/")
    print(f"  Metadata: data/resume_metadata.csv")
    
    # Save JSON backup
    df[['unified_role', 'job_titles', 'cleaned_text', 'word_count']].to_json(
        'data/collected_resumes/cleaned_resumes.json',
        orient='records',
        indent=2
    )
    
    print(f"  JSON: data/collected_resumes/cleaned_resumes.json")
    
    # Final distribution
    print(f"\nFinal role distribution:")
    for role, count in metadata_df['unified_role'].value_counts().items():
        percentage = (count / len(metadata_df)) * 100
        print(f"  {role:<30} {count:>5} ({percentage:>5.1f}%)")

if __name__ == "__main__":
    df = clean_and_categorize_dataset()
    
    if df is not None:
        print(f"\nReady for Phase 2: NLP Feature Engineering")
