"""
resume_parser.py

Extracts text and key entities from resumes (PDFs, DOCX, TXT) using spaCy and regex.
"""
import re
import spacy
from PyPDF2 import PdfReader
import os

try:
    import docx
except ImportError:
    docx = None

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    'python', 'java', 'c++', 'sql', 'machine learning', 'deep learning',
    'data science', 'pandas', 'numpy', 'tensorflow', 'flask', 'django',
    'html', 'css', 'javascript', 'react', 'node.js', 'excel', 'power bi'
]

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                return "".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"ERROR: {e}"
    elif ext == ".docx" and docx:
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"ERROR: {e}"
    elif ext == ".txt":
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return "ERROR: Unsupported file format. Please upload PDF, DOCX, or TXT."

def extract_sections(text: str) -> dict:
    """Extracts major sections (education, experience, projects, achievements) from resume text using line-by-line parsing."""
    import re
    section_headers = {
        'education': [r'education', r'academic background', r'qualifications'],
        'experience': [r'experience', r'work experience', r'professional experience', r'employment'],
        'projects': [r'projects?', r'project experience', r'personal projects'],
        'achievements': [r'achievements', r'accomplishments', r'awards', r'honors']
    }
    lines = text.splitlines()
    current_section = None
    sections = {k: [] for k in section_headers}
    for line in lines:
        line_clean = line.strip().lower().replace(':', '').replace('-', '').replace('•', '').replace('>', '')
        for key, headers in section_headers.items():
            if any(re.fullmatch(h, line_clean) or h in line_clean for h in headers):
                current_section = key
                break
        else:
            if current_section and line.strip():
                sections[current_section].append(line.strip())
    # Join lines for each section
    return {k: '\n'.join(v).strip() for k, v in sections.items()}

def extract_entities(text: str) -> dict:
    """Extracts name, email, phone, skills, and major sections from resume text."""
    doc = nlp(text)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "")
    email_match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w{2,4}', text)
    phone_match = re.findall(r'((?:\+\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4})', text)
    skills_found = [skill for skill in SKILLS_DB if skill.lower() in text.lower()]
    sections = extract_sections(text)
    return {
        "name": name,
        "email": email_match[0] if email_match else "",
        "phone": phone_match[0] if phone_match else "",
        "skills": list(set(skills_found)),
        "education": sections['education'],
        "experience": sections['experience'],
        "projects": sections['projects'],
        "achievements": sections['achievements'],
        "company_names": [],
        "designations": [],
        "summary": "",
        "error": "",
        "text": text
    }

def parse_resume(resume_path: str) -> dict:
    """Parse a resume file and extract structured information."""
    text = extract_text_from_file(resume_path)
    if text.startswith("ERROR"):
        return {"error": text}
    return extract_entities(text)
