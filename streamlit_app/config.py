import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from config import CLASSIFIER_MODEL_PATH, VECTORIZER_PATH, SCORER_MODEL_PATH

class ResumeRecommender:
    def __init__(self):
        """
        Initialize the Resume Recommender by loading all required models:
        - Classifier for role prediction
        - TF-IDF vectorizer for text processing
        - Scoring model for resume strength evaluation
        """
        # Load classifier model
        with open(CLASSIFIER_MODEL_PATH, 'rb') as f:
            self.classifier = pickle.load(f)

        # Load TF-IDF vectorizer
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)

        # Load resume scorer model
        with open(SCORER_MODEL_PATH, 'rb') as f:
            self.resume_scorer = pickle.load(f)

        # Extract class labels if available
        self.labels = self.classifier.classes_ if hasattr(self.classifier, "classes_") else None

    def recommend_roles(self, resume_text, top_n=3):
        """
        Predict the top N job roles suited for the given resume text.

        Parameters:
        - resume_text (str): Cleaned and preprocessed resume content.
        - top_n (int): Number of top roles to return.

        Returns:
        - List of (role, probability%) tuples sorted in descending order.
        """
        if not resume_text.strip():
            return [("No content provided", 0.0)]

        # Transform text using vectorizer
        vectorized = self.vectorizer.transform([resume_text])

        # Predict role probabilities
        try:
            probs = self.classifier.predict_proba(vectorized)[0]
        except Exception as e:
            return [(f"Error during prediction: {e}", 0.0)]

        # Get top N predictions
        top_indices = np.argsort(probs)[::-1][:top_n]
        recommendations = [(self.labels[i], round(probs[i] * 100, 2)) for i in top_indices]

        return recommendations

    def score_resume(self, resume_text):
        """
        Predict the overall strength score of the resume using a trained regression/classification model.

        Parameters:
        - resume_text (str): Cleaned resume content.

        Returns:
        - Float score (0.0 - 1.0 or scaled appropriately)
        """
        if not resume_text.strip():
            return 0.0

        # Vectorize text
        vectorized = self.vectorizer.transform([resume_text])

        try:
            score = self.resume_scorer.predict(vectorized)[0]
            return round(score, 2)
        except Exception as e:
            print(f"[ERROR] Resume scoring failed: {e}")
            return 0.0