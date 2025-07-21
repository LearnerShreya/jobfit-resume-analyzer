# Approach and Methodology

## Overview
Smart Resume Analyzer was developed to provide a practical, user-friendly solution for resume analysis and job role recommendation. The project combines machine learning, natural language processing, and a modern web interface to deliver actionable insights for both job seekers and recruiters.

## Problem Statement
Job seekers often lack feedback on how well their resumes align with specific job roles. Recruiters need efficient tools to screen and match candidates. This project addresses both needs by automating resume parsing, skill extraction, scoring, and job role recommendation.

## Data and Preprocessing
- **Resume Dataset:** Used a labeled dataset of resumes for model training. Data was cleaned and standardized.
- **Skills List:** Maintained a curated list of technical and soft skills, with support for synonyms and partial matches.
- **Text Extraction:** Supported PDF, DOCX, DOC, and TXT formats using PyPDF2 and python-docx.
- **NLP Preprocessing:** Applied tokenization, lowercasing, and stopword removal using spaCy and scikit-learn.

## Model Training
- **Vectorization:** Used TF-IDF to convert resume text into numerical features.
- **Role Classifier:** Trained a multi-class classifier to predict likely job roles.
- **Scoring Model:** Trained a regression/classification model to predict resume strength.
- **Label Encoding:** Used for job role classes.

## Application Architecture
- **Backend:** Modular Python scripts for parsing, scoring, recommending, and matching.
- **Frontend:** Streamlit for a clean, interactive user interface.
- **Model Storage:** Models serialized with joblib and stored in the model directory.
- **Configuration:** Centralized in config.py for maintainability.

## Key Features
- Upload resumes in multiple formats with validation.
- Extracts name, email, phone, skills, education, experience, projects, and achievements.
- Skill matching supports synonyms and partial matches.
- Customizable scoring with user-uploaded skill lists.
- Downloadable PDF and HTML analysis reports.
- Modern, accessible UI with progress indicators and clear error messages.

## Design Decisions
- **Modularity:** Each function (parsing, scoring, recommending, matching) is in a separate module.
- **Transparency:** The app displays matched/missing keywords and all role probabilities.
- **Extensibility:** Skill lists and models can be updated or retrained.
- **Error Handling:** Robust error handling throughout.

## Workflow
1. User uploads a resume (PDF, DOCX, DOC, or TXT).
2. The app extracts text and entities, including major sections.
3. The resume is scored against all job roles, and top matches are displayed.
4. The user can upload a custom skill list or paste a job description for further analysis.
5. The app provides actionable feedback and downloadable reports.

## Conclusion
Smart Resume Analyzer delivers a practical, extensible tool for resume analysis and job role recommendation. The modular design and clear workflow ensure maintainability and real-world applicability.
