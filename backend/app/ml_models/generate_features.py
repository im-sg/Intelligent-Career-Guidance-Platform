"""
Improved feature generation with derived features
Expected improvement: +2-4% accuracy
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path

class ImprovedFeatureGenerator:
    def __init__(self):
        """Initialize with skills taxonomy"""
        self.load_skills_taxonomy()
        self.feature_columns = None
        
    def load_skills_taxonomy(self):
        """Load skills from taxonomy file"""
        with open('data/skills/skills_taxonomy.json', 'r') as f:
            taxonomy = json.load(f)
        
        # Flatten all skills into single list
        self.all_skills = []
        for category, skills in taxonomy.items():
            self.all_skills.extend(skills)
        
        print(f"Loaded {len(self.all_skills)} skills from taxonomy")
    
    def generate_training_data(self):
        """Generate training dataset with improved features"""
        print("\n" + "=" * 70)
        print("GENERATING IMPROVED TRAINING FEATURES")
        print("=" * 70)
        
        # Load processed resumes
        print("\nLoading processed resumes...")
        with open('data/processed_resumes.json', 'r') as f:
            processed_data = json.load(f)
        
        print(f"Loaded {len(processed_data)} processed resumes")
        
        # Generate features for each resume
        training_samples = []
        
        for idx, resume in enumerate(processed_data):
            if idx % 100 == 0 and idx > 0:
                print(f"  Generating features: {idx}/{len(processed_data)}...")
            
            # Extract base features (original method)
            features = self._extract_base_features(resume)
            
            # Add derived features (NEW!)
            derived = self._extract_derived_features(features)
            features.update(derived)
            
            # Add role label
            features['unified_role'] = resume['unified_role']
            features['resume_id'] = resume['id']
            
            training_samples.append(features)
        
        # Convert to DataFrame
        df = pd.DataFrame(training_samples)
        
        # Save training data
        output_path = 'training_data/feature_vectors_improved.csv'
        df.to_csv(output_path, index=False)
        
        print(f"\n✓ Saved improved training data to: {output_path}")
        print(f"  Shape: {df.shape}")
        print(f"  Base features: {len(self.all_skills) + 3}")
        print(f"  Derived features: {df.shape[1] - len(self.all_skills) - 5}")  # -5 for skills, exp, edu, role, id
        print(f"  Total features: {df.shape[1] - 2}")  # -2 for role and id
        
        # Show statistics
        self._show_statistics(df)
        
        return df
    
    def _extract_base_features(self, resume):
        """Extract base feature vector (original method)"""
        features = {}
        parsed_data = resume['parsed_data']
        
        # Initialize all skill features to 0
        for skill in self.all_skills:
            feature_name = f"skill_{skill.lower().replace(' ', '_').replace('.', '').replace('/', '_')}"
            features[feature_name] = 0.0
        
        # Fill in skill values from parsed data
        if 'skills' in parsed_data and 'technical' in parsed_data['skills']:
            for skill_obj in parsed_data['skills']['technical']:
                skill_name = skill_obj['name']
                proficiency = skill_obj['proficiency_score']
                
                feature_name = f"skill_{skill_name.lower().replace(' ', '_').replace('.', '').replace('/', '_')}"
                if feature_name in features:
                    features[feature_name] = proficiency
        
        # Experience level
        experience_count = len(parsed_data.get('experience', []))
        if experience_count >= 5:
            features['experience_level'] = 2  # Advanced
        elif experience_count >= 2:
            features['experience_level'] = 1  # Intermediate
        else:
            features['experience_level'] = 0  # Entry
        
        features['num_positions'] = experience_count
        
        # Education level
        education_count = len(parsed_data.get('education', []))
        if education_count > 0:
            has_masters = False
            has_phd = False
            for edu in parsed_data['education']:
                degree = edu.get('degree', '').lower()
                if 'master' in degree or 'm.s' in degree or 'm.tech' in degree:
                    has_masters = True
                if 'phd' in degree or 'ph.d' in degree or 'doctorate' in degree:
                    has_phd = True
            
            if has_phd:
                features['education_level'] = 3
            elif has_masters:
                features['education_level'] = 2
            else:
                features['education_level'] = 1
        else:
            features['education_level'] = 0
        
        return features
    
    def _extract_derived_features(self, base_features):
        """
        Extract derived features that capture skill combinations
        This is the NEW feature engineering!
        """
        derived = {}
        
        # === ROLE-SPECIFIC INDICATORS ===
        
        # Backend Developer indicator
        derived['is_backend_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_sql', 0) > 2 and
            (base_features.get('skill_django', 0) > 2 or 
             base_features.get('skill_flask', 0) > 2 or
             base_features.get('skill_nodejs', 0) > 2)
        )
        
        # Frontend Developer indicator
        derived['is_frontend_profile'] = int(
            base_features.get('skill_javascript', 0) > 3 and
            (base_features.get('skill_react', 0) > 2 or
             base_features.get('skill_angular', 0) > 2 or
             base_features.get('skill_vue', 0) > 2) and
            base_features.get('skill_html', 0) > 2
        )
        
        # Full Stack indicator
        derived['is_fullstack_profile'] = int(
            derived['is_backend_profile'] == 1 and
            derived['is_frontend_profile'] == 1
        )
        
        # Data Science indicator
        derived['is_data_science_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_machine_learning', 0) > 3 and
            (base_features.get('skill_statistics', 0) > 2 or
             base_features.get('skill_data_analysis', 0) > 2)
        )
        
        # Machine Learning Engineer indicator
        derived['is_ml_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_machine_learning', 0) > 3 and
            (base_features.get('skill_tensorflow', 0) > 2 or
             base_features.get('skill_pytorch', 0) > 2)
        )
        
        # AI Engineer indicator
        derived['is_ai_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_deep_learning', 0) > 3 and
            base_features.get('skill_tensorflow', 0) > 2
        )
        
        # DevOps/Cloud Engineer indicator
        derived['is_devops_profile'] = int(
            base_features.get('skill_docker', 0) > 2 and
            base_features.get('skill_kubernetes', 0) > 2 and
            (base_features.get('skill_aws', 0) > 2 or
             base_features.get('skill_azure', 0) > 2 or
             base_features.get('skill_gcp', 0) > 2)
        )
        
        # Data Engineer indicator
        derived['is_data_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_sql', 0) > 3 and
            (base_features.get('skill_aws', 0) > 2 or
             base_features.get('skill_azure', 0) > 2)
        )
        
        # Cybersecurity indicator
        derived['is_security_profile'] = int(
            base_features.get('skill_linux', 0) > 2 and
            base_features.get('experience_level', 0) >= 1
        )
        
        # === SKILL AGGREGATIONS ===
        
        # Count of programming languages
        prog_langs = ['skill_python', 'skill_java', 'skill_javascript', 
                     'skill_c++', 'skill_go', 'skill_ruby', 'skill_php']
        derived['num_programming_languages'] = sum(
            1 for lang in prog_langs if base_features.get(lang, 0) > 2
        )
        
        # Count of web technologies
        web_tech = ['skill_react', 'skill_angular', 'skill_vue', 'skill_django',
                   'skill_flask', 'skill_nodejs', 'skill_express']
        derived['num_web_technologies'] = sum(
            1 for tech in web_tech if base_features.get(tech, 0) > 2
        )
        
        # Count of ML/AI tools
        ml_tools = ['skill_tensorflow', 'skill_pytorch', 'skill_keras',
                   'skill_scikit-learn', 'skill_pandas', 'skill_numpy']
        derived['num_ml_tools'] = sum(
            1 for tool in ml_tools if base_features.get(tool, 0) > 2
        )
        
        # Count of cloud platforms
        cloud = ['skill_aws', 'skill_azure', 'skill_gcp']
        derived['num_cloud_platforms'] = sum(
            1 for platform in cloud if base_features.get(platform, 0) > 2
        )
        
        # Count of databases
        databases = ['skill_sql', 'skill_mysql', 'skill_postgresql',
                    'skill_mongodb', 'skill_redis']
        derived['num_databases'] = sum(
            1 for db in databases if base_features.get(db, 0) > 2
        )
        
        # === SKILL DIVERSITY & QUALITY ===
        
        # Total number of skills (any proficiency > 0)
        skill_cols = [k for k in base_features.keys() if k.startswith('skill_')]
        derived['total_skills_count'] = sum(
            1 for col in skill_cols if base_features.get(col, 0) > 0
        )
        
        # Number of expert-level skills (proficiency > 4)
        derived['expert_skills_count'] = sum(
            1 for col in skill_cols if base_features.get(col, 0) > 4
        )
        
        # Number of advanced skills (proficiency 3-4)
        derived['advanced_skills_count'] = sum(
            1 for col in skill_cols if 3 < base_features.get(col, 0) <= 4
        )
        
        # Average skill proficiency (excluding zeros)
        skill_values = [base_features.get(col, 0) for col in skill_cols]
        non_zero_skills = [s for s in skill_values if s > 0]
        derived['avg_skill_proficiency'] = (
            np.mean(non_zero_skills) if non_zero_skills else 0
        )
        
        # Max skill proficiency
        derived['max_skill_proficiency'] = max(skill_values) if skill_values else 0
        
        # Skill breadth vs depth ratio
        if derived['expert_skills_count'] > 0:
            derived['breadth_vs_depth'] = (
                derived['total_skills_count'] / derived['expert_skills_count']
            )
        else:
            derived['breadth_vs_depth'] = derived['total_skills_count']
        
        # === EXPERIENCE COMBINATIONS ===
        
        # Experience + Education score
        derived['experience_education_score'] = (
            base_features.get('experience_level', 0) * 2 +
            base_features.get('education_level', 0)
        )
        
        # Senior profile indicator (high exp + high edu)
        derived['is_senior_profile'] = int(
            base_features.get('experience_level', 0) >= 2 and
            base_features.get('education_level', 0) >= 2
        )
        
        # Entry level indicator
        derived['is_entry_level'] = int(
            base_features.get('experience_level', 0) == 0 and
            base_features.get('num_positions', 0) <= 1
        )
        
        # === DOMAIN EXPERTISE ===
        
        # Web development score
        derived['web_dev_score'] = (
            base_features.get('skill_html', 0) * 0.2 +
            base_features.get('skill_css', 0) * 0.2 +
            base_features.get('skill_javascript', 0) * 0.3 +
            (base_features.get('skill_react', 0) or 
             base_features.get('skill_angular', 0) or 
             base_features.get('skill_vue', 0)) * 0.3
        )
        
        # Data science score
        derived['data_science_score'] = (
            base_features.get('skill_python', 0) * 0.3 +
            base_features.get('skill_machine_learning', 0) * 0.3 +
            base_features.get('skill_statistics', 0) * 0.2 +
            base_features.get('skill_data_visualization', 0) * 0.2
        )
        
        # DevOps score
        derived['devops_score'] = (
            base_features.get('skill_docker', 0) * 0.3 +
            base_features.get('skill_kubernetes', 0) * 0.3 +
            (base_features.get('skill_aws', 0) or 
             base_features.get('skill_azure', 0) or 
             base_features.get('skill_gcp', 0)) * 0.4
        )
        
        return derived
    
    def _show_statistics(self, df):
        """Show training data statistics"""
        print("\n" + "-" * 70)
        print("TRAINING DATA STATISTICS")
        print("-" * 70)
        
        print(f"\nSamples by Role:")
        role_counts = df['unified_role'].value_counts()
        for role, count in role_counts.items():
            print(f"  {role:<30} {count:>5} samples")
        
        # Show new derived features
        derived_features = [col for col in df.columns if col not in 
                           [f"skill_{s.lower().replace(' ', '_').replace('.', '').replace('/', '_')}" 
                            for s in self.all_skills] and 
                           col not in ['experience_level', 'num_positions', 'education_level', 
                                      'unified_role', 'resume_id']]
        
        print(f"\nDerived Features Created: {len(derived_features)}")
        print("Sample derived features:")
        for feat in derived_features[:10]:
            print(f"  - {feat}")

if __name__ == "__main__":
    generator = ImprovedFeatureGenerator()
    df = generator.generate_training_data()
    
    print("\n Improved feature generation complete!")
