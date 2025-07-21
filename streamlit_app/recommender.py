import pickle
import numpy as np
import os
import joblib

class ResumeRecommender:
    def __init__(
        self,
        classifier_path=None,
        vectorizer_path=None,
        label_encoder_path=None
    ):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
        classifier_path = classifier_path or os.path.join(base_dir, 'classifier.pkl')
        vectorizer_path = vectorizer_path or os.path.join(base_dir, 'vectorizer.pkl')
        label_encoder_path = label_encoder_path or os.path.join(base_dir, 'label_encoder.pkl')
        # Load the classifier
        self.classifier = joblib.load(classifier_path)
        # Load the vectorizer
        self.vectorizer = joblib.load(vectorizer_path)
        # Load the label encoder
        self.label_encoder = joblib.load(label_encoder_path)

    def recommend_roles(self, resume_text, top_n=3):
        """
        Recommend top N job roles based on the resume text.

        Parameters:
        - resume_text (str): Cleaned resume text.
        - top_n (int): Number of top roles to recommend.

        Returns:
        - List of tuples: [(role_name, probability %), ...]
        """
        if not resume_text.strip():
            return [("No content", 0.0)]

        # Vectorize input text
        X_vectorized = self.vectorizer.transform([resume_text])

        # Predict probabilities for each class
        probs = self.classifier.predict_proba(X_vectorized)[0]

        # Get indices of top N probabilities
        top_indices = np.argsort(probs)[::-1][:top_n]

        # Decode class indices into actual role names
        recommendations = []
        for idx in top_indices:
            role_name = self.label_encoder.inverse_transform([idx])[0]
            confidence = round(probs[idx] * 100, 2)
            recommendations.append((role_name, confidence))

        return recommendations
