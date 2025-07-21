"""
recommender.py

Provides ResumeRecommender for predicting top job roles based on resume text using pre-trained models.
"""
import os
import numpy as np
import joblib

class ResumeRecommender:
    def __init__(self, classifier_path=None, vectorizer_path=None, label_encoder_path=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
        self.classifier = joblib.load(classifier_path or os.path.join(base_dir, 'classifier.pkl'))
        self.vectorizer = joblib.load(vectorizer_path or os.path.join(base_dir, 'vectorizer.pkl'))
        self.label_encoder = joblib.load(label_encoder_path or os.path.join(base_dir, 'label_encoder.pkl'))

    def recommend_roles(self, resume_text: str, top_n: int = 3):
        """
        Recommend top N job roles based on the resume text.

        Args:
            resume_text (str): Cleaned resume text.
            top_n (int): Number of top roles to recommend.
        Returns:
            List[Tuple[str, float]]: [(role_name, probability %), ...]
        """
        if not resume_text or not resume_text.strip():
            return [("No content", 0.0)]
        X_vectorized = self.vectorizer.transform([resume_text])
        probs = self.classifier.predict_proba(X_vectorized)[0]
        top_indices = np.argsort(probs)[::-1][:top_n]
        return [
            (self.label_encoder.inverse_transform([idx])[0], round(probs[idx] * 100, 2))
            for idx in top_indices
        ]
