"""
Clean and categorize locally downloaded resume dataset
Works with JSONL, JSON, or CSV files
"""
import json
import pandas as pd
from pathlib import Path
import re
import hashlib
from collections import Counter

# Define unified role mappings
ROLE_MAPPINGS = {
    'AI Engineer': [
        'AI Engineer', 'Deep Learning Engineer', 'NLP Engineer', 
        'Computer Vision Engineer', 'Language Model Engineer',
        'Nlp Engineer'
    ],
    'Machine Learning Engineer': [
        'Machine Learning Engineer', 'MLOps Engineer', 'ML Engineer Intern',
        'Research Engineer (ML)', 'Applied Scientist (ML)', 'Mlops Engineer',
        'Machine Learning Engineer Intern'
    ],
    'Data Scientist': [
        'Data Scientist', 'Data Science Consultant', 'Data Science Intern',
        'Adjunct Faculty & Data Scientist'
    ],
    'Data Engineer': [
        'Data Engineer', 'ETL Developer', 'Big Data Engineer',
        'Data Pipeline Engineer', 'Database Engineer'
    ],
    'DevOps/Cloud Engineer': [
        'DevOps Engineer', 'Devops Engineer', 'Cloud Engineer',
        'Cloud Operations Architect', 'Site Reliability Engineer',
        'Infrastructure Engineer', 'Platform Engineer', 'SRE',
        'Cloud Operations Architect (DevOps)'
    ],
    'Cybersecurity Engineer': [
        'Cybersecurity Engineer', 'Information Security Analyst',
        'Penetration Tester', 'Security Engineer',
        'Network Security Engineer', 'Network and Security Engineer'
    ],
    'Backend Developer': [
        'Backend Developer', 'Node.Js Developer', 'Node.js Developer',
        'Java Web Developer', 'Python RESTful API Developer',
        'Python API Developer', 'Java Backend Developer',
        'Python RESTful API developer'
    ],
    'Full Stack Developer': [
        'Full Stack Developer', 'M3 Java Developer & Stream Serve Developer',
        'Web Application Developer'
    ],
    'Frontend Developer': [
        'Frontend Developer', 'Web Developer', 'React Developer',
        'Angular Developer', 'Vue Developer', 'Javascript Developer',
        'JavaScript Developer', 'React Native Developer'
    ],
    'Python Developer': [
        'Python Developer', 'Python Developer/analyst', 
        'Python Developer/Analyst'
    ]
}

class LocalDatasetCleaner:
    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.output_dir = Path("data/collected_resumes")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total_loaded': 0,
            'mapped_to_roles': 0,
            'unmapped': 0,
            'duplicates_removed': 0,
            'invalid_removed': 0,
            'final_count': 0,
            'by_role': {}
        }
    
    def load_dataset(self):
        """Load dataset from local file (supports JSONL, JSON, CSV)"""
        print("="*70)
        print("STEP 1: LOADING LOCAL DATASET")
        print("="*70)
        print(f"\n📁 Loading from: {self.input_file}")
        
        try:
            file_ext = self.input_file.suffix.lower()
            
            if file_ext == '.jsonl':
                # Load JSONL (one JSON object per line)
                data = []
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data.append(json.loads(line))
                df = pd.DataFrame(data)
            
            elif file_ext == '.json':
                # Load regular JSON
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            
            elif file_ext == '.csv':
                # Load CSV
                df = pd.read_csv(self.input_file)
            
            else:
                print(f"❌ Unsupported file format: {file_ext}")
                print("   Supported: .jsonl, .json, .csv")
                return None
            
            self.stats['total_loaded'] = len(df)
            
            print(f"✅ Successfully loaded {len(df)} resumes")
            print(f"📋 Columns found: {list(df.columns)}")
            
            # Show first row sample
            print(f"\n📊 Sample data (first row):")
            for col in df.columns[:5]:  # Show first 5 columns
                value = str(df[col].iloc[0])[:100]
                print(f"   {col}: {value}...")
            
            return df
        
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return None
    
    def identify_columns(self, df):
        """Auto-detect role and text columns"""
        print("\n" + "="*70)
        print("STEP 2: IDENTIFYING DATA COLUMNS")
        print("="*70)
        
        # Find role column
        role_column = None
        possible_role_names = ['Category', 'category', 'Role', 'role', 'Job Title', 
                              'job_title', 'job_role', 'position', 'Position']
        
        for col in possible_role_names:
            if col in df.columns:
                role_column = col
                print(f"\n✅ Role column found: '{role_column}'")
                break
        
        if not role_column:
            print("\n⚠️  No role column auto-detected.")
            print(f"   Available columns: {df.columns.tolist()}")
            role_column = input("   Please enter the role column name: ").strip()
            
            if role_column not in df.columns:
                print(f"❌ Column '{role_column}' not found!")
                return None, None
        
        # Find resume text column
        text_column = None
        possible_text_names = ['Resume', 'resume', 'Resume_str', 'resume_str', 
                              'text', 'Text', 'content', 'Content', 'resume_text']
        
        for col in possible_text_names:
            if col in df.columns:
                text_column = col
                print(f"✅ Text column found: '{text_column}'")
                break
        
        if not text_column:
            print("\n⚠️  No text column auto-detected.")
            print(f"   Available columns: {df.columns.tolist()}")
            text_column = input("   Please enter the resume text column name: ").strip()
            
            if text_column not in df.columns:
                print(f"❌ Column '{text_column}' not found!")
                return None, None
        
        # Show sample
        print(f"\n📊 Sample Data:")
        print(f"   Role: {df[role_column].iloc[0]}")
        print(f"   Text preview: {str(df[text_column].iloc[0])[:100]}...")
        
        return role_column, text_column
    
    def map_to_unified_role(self, original_role):
        """Map original role to unified category"""
        if pd.isna(original_role):
            return None
        
        original_role = str(original_role).strip()
        
        for unified_role, variants in ROLE_MAPPINGS.items():
            for variant in variants:
                if variant.lower() == original_role.lower() or \
                   variant.lower() in original_role.lower():
                    return unified_role
        
        return None
    
    def clean_text(self, text):
        """Clean resume text"""
        if pd.isna(text) or not text:
            return None
        
        text = str(text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove null bytes and special characters
        text = text.replace('\x00', '').replace('\ufffd', '')
        text = text.strip()
        
        # Minimum length check (100 chars)
        if len(text) < 100:
            return None
        
        return text
    
    def get_text_hash(self, text):
        """Generate hash for duplicate detection"""
        if not text:
            return None
        normalized = re.sub(r'\s+', '', text.lower())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def process_dataset(self, df, role_column, text_column):
        """Main processing pipeline"""
        print("\n" + "="*70)
        print("STEP 3: PROCESSING DATASET")
        print("="*70)
        
        # 3.1: Map to unified roles
        print("\n⏳ Mapping to unified roles...")
        df['unified_role'] = df[role_column].apply(self.map_to_unified_role)
        
        # 3.2: Clean text
        print("⏳ Cleaning resume text...")
        df['cleaned_text'] = df[text_column].apply(self.clean_text)
        
        # 3.3: Create hash
        print("⏳ Detecting duplicates...")
        df['text_hash'] = df['cleaned_text'].apply(self.get_text_hash)
        
        # 3.4: Filter valid resumes
        valid_df = df[
            (df['unified_role'].notna()) & 
            (df['cleaned_text'].notna())
        ].copy()
        
        self.stats['mapped_to_roles'] = len(valid_df)
        self.stats['unmapped'] = len(df) - len(valid_df)
        
        print(f"\n✅ Mapped to roles: {len(valid_df)}")
        print(f"❌ Unmapped/invalid: {len(df) - len(valid_df)}")
        
        # Show distribution
        print(f"\n📊 Role Distribution:")
        for role, count in valid_df['unified_role'].value_counts().items():
            print(f"   {role:<30} {count:>5}")
        
        # 3.5: Remove duplicates
        print(f"\n⏳ Removing duplicates...")
        initial = len(valid_df)
        valid_df = valid_df.drop_duplicates(subset=['text_hash'], keep='first')
        self.stats['duplicates_removed'] = initial - len(valid_df)
        
        print(f"✅ Removed {self.stats['duplicates_removed']} duplicates")
        
        # 3.6: Quality check (min 50 words)
        print(f"\n⏳ Validating quality...")
        valid_df['word_count'] = valid_df['cleaned_text'].str.split().str.len()
        initial = len(valid_df)
        valid_df = valid_df[valid_df['word_count'] >= 50]
        self.stats['invalid_removed'] = initial - len(valid_df)
        
        print(f"✅ Removed {self.stats['invalid_removed']} low-quality resumes")
        print(f"📊 Final count: {len(valid_df)}")
        
        return valid_df
    
    def save_organized_data(self, df, role_column):
        """Save cleaned data in organized structure"""
        print("\n" + "="*70)
        print("STEP 4: SAVING ORGANIZED DATA")
        print("="*70)
        
        metadata = []
        
        print("\n⏳ Creating organized files...")
        
        for idx, row in df.iterrows():
            if idx % 100 == 0 and idx > 0:
                print(f"   Progress: {idx}/{len(df)}...")
            
            unified_role = row['unified_role']
            original_role = row[role_column]
            cleaned_text = row['cleaned_text']
            
            # Create role folder
            role_folder = unified_role.lower().replace('/', '_').replace(' ', '_')
            role_dir = self.output_dir / role_folder
            role_dir.mkdir(exist_ok=True)
            
            # Save file
            filename = f"resume_{idx:04d}.txt"
            file_path = role_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            # Track metadata
            metadata.append({
                'id': f"clean_{idx:04d}",
                'filename': filename,
                'unified_role': unified_role,
                'original_role': original_role,
                'category_folder': role_folder,
                'source': 'local_cleaned',
                'file_path': str(file_path),
                'word_count': row['word_count'],
                'status': 'cleaned',
                'labeled': True
            })
        
        # Save metadata
        metadata_df = pd.DataFrame(metadata)
        metadata_df.to_csv('data/resume_metadata.csv', index=False)
        
        # Save JSON
        df[['unified_role', role_column, 'cleaned_text', 'word_count']].to_json(
            'data/collected_resumes/cleaned_resumes.json',
            orient='records',
            indent=2
        )
        
        # Update stats
        self.stats['final_count'] = len(df)
        for role in ROLE_MAPPINGS.keys():
            count = len(metadata_df[metadata_df['unified_role'] == role])
            self.stats['by_role'][role] = count
        
        print(f"\n✅ Saved {len(df)} organized resumes")
        print(f"📄 Metadata: data/resume_metadata.csv")
        print(f"📁 JSON: data/collected_resumes/cleaned_resumes.json")
        
        return metadata_df
    
    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*70)
        print("CLEANING COMPLETE - SUMMARY")
        print("="*70)
        
        print(f"\n📊 Statistics:")
        print(f"   Loaded:              {self.stats['total_loaded']:>6}")
        print(f"   Mapped to roles:     {self.stats['mapped_to_roles']:>6}")
        print(f"   Unmapped:            {self.stats['unmapped']:>6}")
        print(f"   Duplicates removed:  {self.stats['duplicates_removed']:>6}")
        print(f"   Low quality removed: {self.stats['invalid_removed']:>6}")
        print(f"   " + "-"*40)
        print(f"   Final clean dataset: {self.stats['final_count']:>6} ✅")
        
        print(f"\n📂 By Role:")
        for role in sorted(ROLE_MAPPINGS.keys()):
            count = self.stats['by_role'].get(role, 0)
            if count > 0:
                pct = (count / self.stats['final_count']) * 100
                print(f"   {role:<30} {count:>5} ({pct:>5.1f}%)")
        
        print("\n" + "="*70)
        print("✅ READY FOR PHASE 2: NLP FEATURE ENGINEERING")
        print("="*70)
    
    def run(self):
        """Execute full pipeline"""
        # Load
        df = self.load_dataset()
        if df is None:
            return None
        
        # Identify columns
        role_col, text_col = self.identify_columns(df)
        if not role_col or not text_col:
            return None
        
        # Process
        cleaned_df = self.process_dataset(df, role_col, text_col)
        
        # Save
        metadata = self.save_organized_data(cleaned_df, role_col)
        
        # Summary
        self.print_summary()
        
        return cleaned_df, metadata

def main():
    import sys
    
    print("\n" + "="*70)
    print("  INTELLIGENT CAREER PLATFORM - Data Cleaning")
    print("="*70)
    
    # Get input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("\nEnter the path to your downloaded dataset file:")
        print("(Supports .jsonl, .json, .csv)")
        input_file = input("File path: ").strip()
    
    if not Path(input_file).exists():
        print(f"\n❌ File not found: {input_file}")
        return
    
    # Run cleaner
    cleaner = LocalDatasetCleaner(input_file)
    df, metadata = cleaner.run()

if __name__ == "__main__":
    main()
