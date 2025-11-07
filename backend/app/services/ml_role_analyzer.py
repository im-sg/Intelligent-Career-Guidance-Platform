"""
ML Role Analyzer - Hybrid approach using rule-based logic with ML-style interface
"""
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json


class MLRoleAnalyzer:
    def __init__(self):
        """Load role requirements and initialize analyzer"""
        self.model_path = Path("app/ml_models/saved_models")

        # Load roles dataset for rule-based matching
        self.roles = self._load_roles()

        # Load metadata for compatibility
        try:
            with open(self.model_path / "model_metadata.json", 'r') as f:
                self.metadata = json.load(f)
            self.classes = self.metadata['classes']
        except:
            self.classes = [
                "AI Engineer", "Backend Developer", "Cybersecurity Engineer",
                "Data Engineer", "Data Scientist", "DevOps/Cloud Engineer",
                "Frontend Developer", "Full Stack Developer", "Machine Learning Engineer"
            ]

        print(f"✓ ML Model loaded: {len(self.classes)} classes (hybrid rule-based approach)")

    def _load_roles(self) -> List[Dict]:
        """Load roles from dataset"""
        roles_path = Path("data/job_roles/roles_dataset.json")
        with open(roles_path, 'r') as f:
            data = json.load(f)
        return data['job_roles']
    
    def predict_roles(self, parsed_resume: Dict) -> List[Dict]:
        """
        Predict suitable job roles using hybrid rule-based + ML approach

        Args:
            parsed_resume: Parsed resume data with skills, experience, education

        Returns:
            List of role predictions with scores
        """
        # Extract user skills with proficiency scores
        user_skills = {}
        if 'skills' in parsed_resume and 'technical' in parsed_resume['skills']:
            for skill_obj in parsed_resume['skills']['technical']:
                user_skills[skill_obj['name']] = skill_obj['proficiency_score']

        # Score each role using rule-based logic
        predictions = []
        for role in self.roles:
            score, details = self._calculate_role_score(user_skills, role['required_skills'], role)

            predictions.append({
                "role": role['title'],
                "probability": score / 100.0,
                "percentage": score,
                "matched": details['matched'],
                "weak": details['weak'],
                "missing": details['missing']
            })

        # Sort by percentage (descending)
        predictions.sort(key=lambda x: x['percentage'], reverse=True)

        return predictions

    def _calculate_role_score(self, user_skills: Dict[str, float], required_skills: Dict[str, int], role: Dict) -> Tuple[float, Dict]:
        """
        Calculate match score for a role using intelligent scoring

        Scoring algorithm:
        - Full match (user >= required): 100% credit + bonus
        - Partial match (user < required): Proportional credit
        - Missing skill: 0% credit
        """
        matched = []
        weak = []
        missing = []

        total_score = 0
        max_possible_score = 0

        for skill_name, required_level in required_skills.items():
            max_possible_score += required_level

            # Check for skill match (case-insensitive)
            user_level = self._find_skill_match(skill_name, user_skills)

            if user_level is None:
                # Skill missing
                missing.append({"skill": skill_name, "required_level": required_level, "user_level": 0})
            elif user_level >= required_level:
                # Strong match
                matched.append({"skill": skill_name, "required_level": required_level, "user_level": user_level})
                # Full credit + bonus for exceeding
                skill_score = required_level + min(1, user_level - required_level) * 0.3
                total_score += skill_score
            else:
                # Weak match
                weak.append({"skill": skill_name, "required_level": required_level, "user_level": user_level})
                # Proportional credit
                skill_score = (user_level / required_level) * required_level
                total_score += skill_score

        # Calculate percentage
        if max_possible_score > 0:
            percentage = (total_score / max_possible_score) * 100
        else:
            percentage = 0

        # Apply bonuses and penalties
        percentage = self._apply_adjustments(percentage, len(matched), len(weak), len(missing), len(required_skills))

        # Cap at 100%
        percentage = min(100, max(0, percentage))

        details = {"matched": matched, "weak": weak, "missing": missing}

        return percentage, details

    def _find_skill_match(self, required_skill: str, user_skills: Dict[str, float]) -> float:
        """Find skill in user skills (case-insensitive, handle variations)"""
        required_lower = required_skill.lower()

        # Direct match
        for user_skill, level in user_skills.items():
            if user_skill.lower() == required_lower:
                return level

        # Partial match
        for user_skill, level in user_skills.items():
            user_lower = user_skill.lower()
            if required_lower in user_lower or user_lower in required_lower:
                if self._are_skills_equivalent(required_lower, user_lower):
                    return level

        return None

    def _are_skills_equivalent(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are equivalent"""
        equivalences = [
            ("ci/cd", "cicd", "ci cd", "continuous integration"),
            ("node.js", "nodejs", "node"),
            ("html/css", "html", "css"),
            ("rest api", "rest", "restful api", "api"),
            ("kubernetes", "k8s"),
            ("machine learning", "ml"),
            ("deep learning", "dl"),
            ("natural language processing", "nlp"),
        ]

        for equiv_group in equivalences:
            if skill1 in equiv_group and skill2 in equiv_group:
                return True

        return False

    def _apply_adjustments(self, base_percentage: float, matched_count: int, weak_count: int, missing_count: int, total_required: int) -> float:
        """Apply bonuses and penalties"""
        adjusted = base_percentage

        # Bonus for having all required skills
        if missing_count == 0:
            adjusted += 8  # +8% bonus

        # Bonus for strong skill coverage
        if matched_count >= total_required * 0.8:
            adjusted += 5  # +5% bonus

        # Penalty for many missing skills
        if missing_count > total_required * 0.4:
            adjusted -= 10  # -10% penalty

        return adjusted
    
    def _extract_features(self, parsed_resume: Dict) -> Dict:
        """Extract features from parsed resume"""
        features = {}
        
        # Extract skills
        if 'skills' in parsed_resume and 'technical' in parsed_resume['skills']:
            for skill_obj in parsed_resume['skills']['technical']:
                skill_name = skill_obj['name'].lower().replace(' ', '_').replace('.', '').replace('/', '_')
                feature_name = f"skill_{skill_name}"
                features[feature_name] = skill_obj['proficiency_score']
        
        # Extract experience
        experience_count = len(parsed_resume.get('experience', []))
        if experience_count >= 5:
            features['experience_level'] = 2
        elif experience_count >= 2:
            features['experience_level'] = 1
        else:
            features['experience_level'] = 0
        
        features['num_positions'] = experience_count
        
        # Extract education
        education_count = len(parsed_resume.get('education', []))
        if education_count > 0:
            has_masters = False
            has_phd = False
            for edu in parsed_resume['education']:
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
        
        # Add derived features (matching training)
        derived = self._extract_derived_features(features)
        features.update(derived)
        
        return features
    
    def _extract_derived_features(self, base_features: Dict) -> Dict:
        """Extract derived features (same as training)"""
        derived = {}

        # Role indicators - Backend
        derived['is_backend_profile'] = int(
            (base_features.get('skill_python', 0) > 3 or base_features.get('skill_nodejs', 0) > 3 or
             base_features.get('skill_node_js', 0) > 3 or base_features.get('skill_java', 0) > 3) and
            (base_features.get('skill_sql', 0) > 2 or base_features.get('skill_rest_api', 0) > 3)
        )

        # Frontend
        derived['is_frontend_profile'] = int(
            base_features.get('skill_javascript', 0) > 3 and
            (base_features.get('skill_react', 0) > 2 or base_features.get('skill_angular', 0) > 2 or
             base_features.get('skill_vue', 0) > 2) and
            (base_features.get('skill_html', 0) > 2 or base_features.get('skill_css', 0) > 2)
        )

        # Data Science
        derived['is_data_science_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_machine_learning', 0) > 3 and
            (base_features.get('skill_pandas', 0) > 3 or base_features.get('skill_statistics', 0) > 3)
        )

        # ML Engineer
        derived['is_ml_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_machine_learning', 0) > 3 and
            (base_features.get('skill_tensorflow', 0) > 2 or base_features.get('skill_pytorch', 0) > 2) and
            (base_features.get('skill_docker', 0) > 1 or base_features.get('skill_aws', 0) > 1)
        )

        # AI Engineer
        derived['is_ai_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_deep_learning', 0) > 3 and
            (base_features.get('skill_nlp', 0) > 2 or base_features.get('skill_computer_vision', 0) > 2 or
             base_features.get('skill_neural_networks', 0) > 2)
        )

        # DevOps/Cloud Engineer
        derived['is_devops_profile'] = int(
            (base_features.get('skill_docker', 0) > 2 or base_features.get('skill_kubernetes', 0) > 2 or
             base_features.get('skill_jenkins', 0) > 2 or base_features.get('skill_cicd', 0) > 3 or
             base_features.get('skill_ci_cd', 0) > 3) and
            (base_features.get('skill_aws', 0) > 2 or base_features.get('skill_azure', 0) > 2 or
             base_features.get('skill_gcp', 0) > 2) and
            base_features.get('skill_linux', 0) > 2
        )

        # Data Engineer
        derived['is_data_engineer_profile'] = int(
            base_features.get('skill_python', 0) > 3 and
            base_features.get('skill_sql', 0) > 3 and
            (base_features.get('skill_etl', 0) > 3 or base_features.get('skill_apache_spark', 0) > 2 or
             base_features.get('skill_airflow', 0) > 2 or base_features.get('skill_kafka', 0) > 2)
        )

        # Full Stack
        derived['is_fullstack_profile'] = int(
            base_features.get('skill_javascript', 0) > 3 and
            (base_features.get('skill_react', 0) > 2 or base_features.get('skill_angular', 0) > 2) and
            (base_features.get('skill_nodejs', 0) > 2 or base_features.get('skill_node_js', 0) > 2 or
             base_features.get('skill_python', 0) > 2) and
            base_features.get('skill_sql', 0) > 2
        )

        # Cybersecurity
        derived['is_security_profile'] = int(
            (base_features.get('skill_network_security', 0) > 3 or
             base_features.get('skill_penetration_testing', 0) > 3 or
             base_features.get('skill_cybersecurity', 0) > 3) and
            base_features.get('skill_linux', 0) > 2
        )
        
        # Skill counts
        prog_langs = ['skill_python', 'skill_java', 'skill_javascript', 'skill_c++', 'skill_c#',
                      'skill_go', 'skill_ruby', 'skill_php', 'skill_typescript', 'skill_scala']
        derived['num_programming_languages'] = sum(
            1 for lang in prog_langs if base_features.get(lang, 0) > 2
        )

        # Web technologies count
        web_tech = ['skill_html', 'skill_css', 'skill_react', 'skill_angular', 'skill_vue',
                    'skill_nodejs', 'skill_django', 'skill_flask', 'skill_fastapi', 'skill_express']
        derived['num_web_technologies'] = sum(
            1 for tech in web_tech if base_features.get(tech, 0) > 2
        )

        # ML tools count
        ml_tools = ['skill_tensorflow', 'skill_pytorch', 'skill_scikit-learn', 'skill_keras',
                    'skill_pandas', 'skill_numpy']
        derived['num_ml_tools'] = sum(
            1 for tool in ml_tools if base_features.get(tool, 0) > 2
        )

        # Cloud platforms count
        cloud_platforms = ['skill_aws', 'skill_azure', 'skill_gcp']
        derived['num_cloud_platforms'] = sum(
            1 for platform in cloud_platforms if base_features.get(platform, 0) > 2
        )

        # Databases count
        databases = ['skill_sql', 'skill_mysql', 'skill_postgresql', 'skill_mongodb',
                     'skill_redis', 'skill_cassandra', 'skill_oracle', 'skill_elasticsearch']
        derived['num_databases'] = sum(
            1 for db in databases if base_features.get(db, 0) > 2
        )

        # Total skills
        skill_cols = [k for k in base_features.keys() if k.startswith('skill_')]
        derived['total_skills_count'] = sum(
            1 for col in skill_cols if base_features.get(col, 0) > 0
        )

        # Expert skills (proficiency > 4)
        derived['expert_skills_count'] = sum(
            1 for col in skill_cols if base_features.get(col, 0) > 4
        )

        # Advanced skills (proficiency 3-4)
        derived['advanced_skills_count'] = sum(
            1 for col in skill_cols if 3 < base_features.get(col, 0) <= 4
        )

        # Average proficiency
        skill_values = [base_features.get(col, 0) for col in skill_cols]
        non_zero = [s for s in skill_values if s > 0]
        derived['avg_skill_proficiency'] = np.mean(non_zero) if non_zero else 0

        # Max proficiency
        derived['max_skill_proficiency'] = max(skill_values) if skill_values else 0

        # Breadth vs depth (ratio of total skills to expert skills)
        if derived['expert_skills_count'] > 0:
            derived['breadth_vs_depth'] = derived['total_skills_count'] / derived['expert_skills_count']
        else:
            derived['breadth_vs_depth'] = derived['total_skills_count']

        # Experience + Education score
        exp_level = base_features.get('experience_level', 0)
        edu_level = base_features.get('education_level', 0)
        derived['experience_education_score'] = (exp_level * 2) + edu_level

        # Senior profile indicator
        derived['is_senior_profile'] = int(
            exp_level >= 2 or
            derived['expert_skills_count'] > 5 or
            derived['avg_skill_proficiency'] > 4.0
        )

        # Entry level indicator
        derived['is_entry_level'] = int(
            exp_level == 0 and
            derived['expert_skills_count'] < 2 and
            derived['avg_skill_proficiency'] < 3.0
        )

        # Domain-specific scores
        # Web dev score
        derived['web_dev_score'] = (
            base_features.get('skill_javascript', 0) +
            base_features.get('skill_react', 0) +
            base_features.get('skill_nodejs', 0) +
            base_features.get('skill_html', 0) +
            base_features.get('skill_css', 0)
        ) / 5.0

        # Data science score
        derived['data_science_score'] = (
            base_features.get('skill_python', 0) +
            base_features.get('skill_machine_learning', 0) +
            base_features.get('skill_pandas', 0) +
            base_features.get('skill_statistics', 0)
        ) / 4.0

        # DevOps score
        derived['devops_score'] = (
            base_features.get('skill_docker', 0) +
            base_features.get('skill_kubernetes', 0) +
            base_features.get('skill_jenkins', 0) +
            base_features.get('skill_terraform', 0) +
            base_features.get('skill_ci_cd', 0) +
            base_features.get('skill_aws', 0)
        ) / 6.0

        return derived
    
    def _create_feature_vector(self, features: Dict) -> List[float]:
        """Create feature vector in correct order"""
        vector = []
        
        for feature_name in self.feature_columns:
            value = features.get(feature_name, 0.0)
            vector.append(float(value))
        
        return vector


if __name__ == "__main__":
    # Test ML analyzer
    analyzer = MLRoleAnalyzer()
    
    # Sample resume
    sample_resume = {
        "skills": {
            "technical": [
                {"name": "Python", "proficiency_score": 4.5, "confidence": 0.9},
                {"name": "Machine Learning", "proficiency_score": 4.2, "confidence": 0.85},
                {"name": "SQL", "proficiency_score": 3.5, "confidence": 0.8}
            ]
        },
        "experience": [
            {"position": "Data Scientist", "company": "TechCorp", "duration": "3 years"}
        ],
        "education": [
            {"degree": "Master of Science", "field": "Data Science", "institution": "Tech Uni"}
        ]
    }
    
    predictions = analyzer.predict_roles(sample_resume)
    
    print("\nTop 5 Predictions:")
    for pred in predictions[:5]:
        print(f"  {pred['role']:<30} {pred['percentage']:>6.2f}%")
