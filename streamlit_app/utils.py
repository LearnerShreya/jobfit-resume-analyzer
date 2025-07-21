import os
import base64
import joblib
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ======================================
# 📁 File System Utilities
# ======================================

def ensure_directory_exists(directory_path: str) -> None:
    """Ensure a directory exists. If not, create it."""
    os.makedirs(directory_path, exist_ok=True)

def generate_unique_resume_path(uploaded_file) -> str:
    """
    Generate a unique file path using timestamp for an uploaded resume.
    Example: uploaded_resumes/20250721_153015_resume.pdf
    """
    upload_dir = "uploaded_resumes"
    ensure_directory_exists(upload_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    return os.path.join(upload_dir, filename)

def save_uploaded_resume(uploaded_file) -> str:
    """
    Save an uploaded file (e.g., resume) to disk and return the file path.
    """
    path = generate_unique_resume_path(uploaded_file)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def generate_download_link(file_path: str, label: str = "Download File") -> str:
    """
    Generate a download link for Streamlit to allow downloading a file.
    Returns HTML anchor tag as string.
    """
    with open(file_path, "rb") as f:
        file_data = f.read()
    encoded_data = base64.b64encode(file_data).decode()
    filename = os.path.basename(file_path)

    return f'<a href="data:application/octet-stream;base64,{encoded_data}" download="{filename}">{label}</a>'


# ======================================
# 📦 Model Utilities
# ======================================

def load_pickle_model(model_filename: str):
    """
    Load a .pkl model saved using joblib from the /model directory.
    Example: load_pickle_model("classifier.pkl")
    """
    current_dir = os.path.dirname(__file__)
    model_dir = os.path.abspath(os.path.join(current_dir, "..", "model"))
    model_path = os.path.join(model_dir, model_filename)

    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"❌ Model not found: {model_path}")

    return joblib.load(model_path)


# ======================================
# 🧠 NLP Utilities
# ======================================

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Compute the cosine similarity between two texts using TF-IDF.
    Returns similarity as a percentage rounded to 2 decimal places.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity_score * 100, 2)


# ======================================
# 📊 Data Utilities
# ======================================

def load_data_file(file_path: str) -> pd.DataFrame:
    """
    Load dataset from a CSV or Excel file and return as a DataFrame.
    Supported formats: .csv, .xls, .xlsx
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        return pd.read_csv(file_path)
    elif extension in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"❌ Unsupported file format: {extension}")


# ======================================
# 📄 PDF Viewer (Streamlit)
# ======================================

def render_pdf_as_iframe(pdf_path: str) -> str:
    """
    Generate an HTML iframe to display a PDF inside Streamlit.
    Returns an iframe HTML string.
    """
    with open(pdf_path, "rb") as f:
        encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

    return f"""
    <iframe src="data:application/pdf;base64,{encoded_pdf}"
            width="700" height="1000" type="application/pdf"></iframe>
    """