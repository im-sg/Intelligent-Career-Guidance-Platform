"""
Skill Normalizer - Handles skill synonyms and normalization
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class SkillNormalizer:
    """Normalize skill names using synonym mapping"""

    def __init__(self):
        """Load skill synonyms"""
        synonyms_path = Path("data/skills/skill_synonyms.json")

        with open(synonyms_path, 'r') as f:
            data = json.load(f)
            self.synonyms = data['skill_synonyms']

        # Create reverse mapping (synonym -> canonical name)
        self.reverse_map = {}
        for canonical, synonyms_list in self.synonyms.items():
            # Add canonical name to itself
            self.reverse_map[canonical.lower()] = canonical
            # Add all synonyms
            for synonym in synonyms_list:
                self.reverse_map[synonym.lower()] = canonical

        print(f"✓ Skill Normalizer loaded: {len(self.synonyms)} canonical skills")

    def normalize(self, skill_name: str) -> str:
        """
        Normalize a skill name to its canonical form

        Args:
            skill_name: Raw skill name from resume

        Returns:
            Canonical skill name
        """
        # Clean the skill name
        cleaned = skill_name.strip()

        # Try exact match (case-insensitive)
        canonical = self.reverse_map.get(cleaned.lower())

        if canonical:
            return canonical

        # Try partial matches for common patterns
        cleaned_lower = cleaned.lower()

        # Special cases
        if 'node' in cleaned_lower and 'js' in cleaned_lower:
            return 'Node.js'
        if 'react' in cleaned_lower:
            return 'React'
        if 'ci' in cleaned_lower and 'cd' in cleaned_lower:
            return 'CI/CD'
        if 'html' in cleaned_lower and 'css' in cleaned_lower:
            return 'HTML/CSS'
        if 'machine' in cleaned_lower and 'learning' in cleaned_lower:
            return 'Machine Learning'
        if 'deep' in cleaned_lower and 'learning' in cleaned_lower:
            return 'Deep Learning'
        if 'natural' in cleaned_lower and 'language' in cleaned_lower:
            return 'Natural Language Processing'
        if 'rest' in cleaned_lower and 'api' in cleaned_lower:
            return 'REST API'

        # Return original if no match found (capitalized)
        return cleaned.title()

    def normalize_batch(self, skill_names: List[str]) -> List[str]:
        """Normalize a batch of skill names"""
        return [self.normalize(skill) for skill in skill_names]

    def get_canonical_name(self, skill_name: str) -> Optional[str]:
        """Get canonical name if it exists, None otherwise"""
        return self.reverse_map.get(skill_name.lower())


# Singleton instance
_normalizer_instance = None


def get_normalizer() -> SkillNormalizer:
    """Get or create singleton normalizer instance"""
    global _normalizer_instance
    if _normalizer_instance is None:
        _normalizer_instance = SkillNormalizer()
    return _normalizer_instance


if __name__ == "__main__":
    # Test normalizer
    normalizer = SkillNormalizer()

    test_skills = [
        "python", "Python", "PYTHON",
        "nodejs", "node.js", "Node", "NodeJS",
        "kubernetes", "k8s", "K8s",
        "aws", "AWS", "Amazon Web Services",
        "ci/cd", "CI CD", "cicd",
        "machine learning", "ML", "ml",
        "reactjs", "react", "React.js"
    ]

    print("\nSkill Normalization Tests:")
    print("-" * 60)
    for skill in test_skills:
        normalized = normalizer.normalize(skill)
        print(f"{skill:30} → {normalized}")