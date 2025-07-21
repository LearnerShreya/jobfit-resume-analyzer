import pickle
import numpy as np

class ResumeRecommender:
    def __init__(
        self,
        classifier_path='model/classifier.pkl',
        vectorizer_path='model/vectorizer.pkl',
        label_encoder_path='model/label_encoder.pkl'
    ):
        # Load the classifier
        with open(classifier_path, 'rb') as f:
            self.classifier = pickle.load(f)

        # Load the vectorizer
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)

        # Load the label encoder
        with open(label_encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)

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
