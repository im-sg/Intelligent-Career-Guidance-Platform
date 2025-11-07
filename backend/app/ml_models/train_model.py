"""
Train ensemble with improved features
Expected: 86-89% accuracy
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib
from pathlib import Path
import json

class ImprovedEnsembleModel:
    def __init__(self):
        self.ensemble_model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = None
        self.model_path = Path("app/ml_models/saved_models")
    
    def load_improved_data(self):
        print("\n" + "=" * 70)
        print("LOADING IMPROVED FEATURES")
        print("=" * 70)
        
        df = pd.read_csv('training_data/feature_vectors_improved.csv')
        
        print(f"\nDataset shape: {df.shape}")
        print(f"Total features: {df.shape[1] - 2}")  # Exclude role and id
        
        # Remove small classes
        role_counts = df['unified_role'].value_counts()
        valid_roles = role_counts[role_counts >= 20].index
        df = df[df['unified_role'].isin(valid_roles)]
        
        self.feature_columns = [col for col in df.columns 
                               if col not in ['unified_role', 'resume_id']]
        
        print(f"Feature count: {len(self.feature_columns)}")
        
        return df[self.feature_columns], df['unified_role']
    
    def train_improved_ensemble(self, X, y):
        print("\n" + "=" * 70)
        print("TRAINING WITH IMPROVED FEATURES")
        print("=" * 70)
        
        y_encoded = self.label_encoder.fit_transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        print(f"\nData split: {len(X_train)} train, {len(X_test)} test")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("\nApplying SMOTE...")
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
        
        print(f"Training ensemble with {X_train_balanced.shape[1]} features...")
        
        rf_model = RandomForestClassifier(
            n_estimators=500,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=4,
            class_weight='balanced',
            verbose=0
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=300,
            max_depth=10,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
            verbose=0
        )
        
        self.ensemble_model = VotingClassifier(
            estimators=[('rf', rf_model), ('gb', gb_model)],
            voting='soft',
            weights=[0.6, 0.4],
            n_jobs=4
        )
        
        self.ensemble_model.fit(X_train_balanced, y_train_balanced)
        
        # Evaluate
        test_score = self.ensemble_model.score(X_test_scaled, y_test)
        
        print("\n" + "-" * 70)
        print("RESULTS WITH IMPROVED FEATURES")
        print("-" * 70)
        print(f"\nTest Accuracy: {test_score:.4f} ({test_score*100:.2f}%)")
        
        y_pred = self.ensemble_model.predict(X_test_scaled)
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_,
            digits=3
        ))
        
        return test_score
    
    def save_model(self, accuracy):
        print("\n" + "=" * 70)
        print("SAVING IMPROVED MODEL")
        print("=" * 70)
        
        joblib.dump(self.ensemble_model, self.model_path / "role_matcher.joblib")
        joblib.dump(self.scaler, self.model_path / "scaler.joblib")
        joblib.dump(self.label_encoder, self.model_path / "label_encoder.joblib")
        
        metadata = {
            'feature_columns': self.feature_columns,
            'n_features': len(self.feature_columns),
            'classes': self.label_encoder.classes_.tolist(),
            'model_type': 'VotingEnsemble_ImprovedFeatures',
            'base_models': ['RandomForestClassifier', 'GradientBoostingClassifier'],
            'accuracy': f"{accuracy*100:.2f}%",
            'improvements': [
                'Role-specific indicators',
                'Skill aggregations',
                'Domain expertise scores',
                'Experience combinations'
            ]
        }
        
        with open(self.model_path / "model_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("\n✓ Model saved successfully")

if __name__ == "__main__":
    trainer = ImprovedEnsembleModel()
    X, y = trainer.load_improved_data()
    accuracy = trainer.train_improved_ensemble(X, y)
    trainer.save_model(accuracy)
    
    print(f"\n{'='*70}")
    print(f"FINAL ACCURACY: {accuracy*100:.2f}%")
    print(f"{'='*70}\n")
    
    if accuracy >= 0.86:
        print("✓✓ EXCELLENT! Accuracy improved to 86%+")
    elif accuracy > 0.8475:
        print(f"✓ IMPROVED! Gained {(accuracy - 0.8475)*100:.2f}% from feature engineering")
    else:
        print("No significant improvement - may need more data")
