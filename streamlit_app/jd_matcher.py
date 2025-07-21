import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_text(text):
    """
    Clean input text: lowercase, remove special characters & extra spaces.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_tfidf_similarity(resume_text, job_description):
    """
    Calculate TF-IDF cosine similarity between resume and job description.
    """
    texts = [clean_text(resume_text), clean_text(job_description)]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)  # Return percentage score


def match_resume_to_jd(resume_text, jd_text, threshold=50):
    """
    Match resume with job description and return match score with result.
    """
    score = get_tfidf_similarity(resume_text, jd_text)
    result = "✅ Good Match" if score >= threshold else "❌ Not a Strong Match"
    return {
        "similarity_score": score,
        "result": result
    }
