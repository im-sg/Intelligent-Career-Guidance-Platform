"""
Process all collected resumes with NLP parser
"""
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from app.services.resume_parser import ResumeParser

def process_all_resumes():
    """Process all resumes and update metadata"""
    print("Initializing Resume Parser...")
    parser = ResumeParser()
    
    # Load metadata
    print("\nLoading resume metadata...")
    metadata_df = pd.read_csv('data/resume_metadata.csv')
    print(f"Found {len(metadata_df)} resumes to process")
    
    # Process each resume
    processed_data = []
    
    for idx, row in metadata_df.iterrows():
        if idx % 50 == 0:
            print(f"Processing resume {idx+1}/{len(metadata_df)}...")
        
        # Read resume file
        file_path = row['file_path']
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Parse resume
            parsed = parser.parse_resume(text)
            
            # Store results
            processed_data.append({
                'id': row['id'],
                'unified_role': row['unified_role'],
                'skills_count': len(parsed['skills']['technical']),
                'experience_count': len(parsed['experience']),
                'education_count': len(parsed['education']),
                'parsed_data': parsed
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    # Save processed data
    print("\nSaving processed data...")
    processed_df = pd.DataFrame(processed_data)
    processed_df.to_json('data/processed_resumes.json', orient='records', indent=2)
    
    # Statistics
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Total processed: {len(processed_df)}")
    print(f"Average skills per resume: {processed_df['skills_count'].mean():.1f}")
    print(f"Average experience entries: {processed_df['experience_count'].mean():.1f}")
    print(f"Average education entries: {processed_df['education_count'].mean():.1f}")
    
    print(f"\nSkills by role:")
    for role in processed_df['unified_role'].unique():
        role_df = processed_df[processed_df['unified_role'] == role]
        avg_skills = role_df['skills_count'].mean()
        print(f"  {role:<30} {avg_skills:.1f} avg skills")
    
    return processed_df

if __name__ == "__main__":
    df = process_all_resumes()
