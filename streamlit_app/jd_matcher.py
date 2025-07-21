"""
jd_matcher.py

Provides functions to match a resume to a job description using TF-IDF cosine similarity.
"""
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text: str) -> str:
    """Lowercase, remove special characters, and extra spaces from text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_tfidf_similarity(resume_text: str, job_description: str) -> float:
    """Calculate TF-IDF cosine similarity between resume and job description (as a percentage)."""
    texts = [clean_text(resume_text), clean_text(job_description)]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def match_resume_to_jd(resume_text: str, jd_text: str, threshold: float = 50) -> dict:
    """Return similarity score and match result for resume vs. job description."""
    score = get_tfidf_similarity(resume_text, jd_text)
    result = "✅ Good Match" if score >= threshold else "❌ Not a Strong Match"
    return {
        "similarity_score": score,
        "result": result
    }
