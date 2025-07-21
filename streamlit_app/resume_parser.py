import re
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

# Predefined Skill List — expand as needed
SKILLS_DB = [
    'python', 'java', 'c++', 'sql', 'machine learning', 'deep learning',
    'data science', 'pandas', 'numpy', 'tensorflow', 'flask', 'django',
    'html', 'css', 'javascript', 'react', 'node.js', 'excel', 'power bi'
]

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        return f"ERROR: {e}"

def extract_entities(text):
    doc = nlp(text)

    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    email_match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w{2,4}', text)
    phone_match = re.findall(r'((?:\+\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4})', text)

    skills_found = []
    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            skills_found.append(skill)

    return {
        "name": name,
        "email": email_match[0] if email_match else "",
        "phone": phone_match[0] if phone_match else "",
        "skills": list(set(skills_found)),
        "education": [],  # Optional: Add later if needed
        "experience": "",  # Optional: Add later
        "company_names": [],
        "designations": [],
        "summary": "",  # Optional: Add NLP summary logic
        "error": "",
        "text": text
    }

def parse_resume(resume_path):
    text = extract_text_from_pdf(resume_path)
    if text.startswith("ERROR"):
        return {"error": text}
    return extract_entities(text)
