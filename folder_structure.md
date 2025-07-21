```bash[]

smart_resume_analyzer/
├── streamlit_app/
│   ├── app.py                   # Main Streamlit UI
│   ├── resume_parser.py        # Extract text & skills from resumes
│   ├── recommender.py          # Recommend job roles based on content
│   ├── score_resume.py         # Score resume using trained ML model
│   ├── jd_matcher.py           # Match resume with JD
│   └── utils.py                # Helper functions (cleaning, embedding, etc.)
│   └── jd_matcher.py
│   └── config.py                   # Central config (file paths, model type, etc.)
├── model/
│   ├── classifier.pkl          # Resume role classifier
│   ├── vectorizer.pkl          # TF-IDF vectorizer
│   ├── scorer_model.pkl        # Resume score predictor
│   ├── label_encoder.pkl       # Encodes/decodes job role classes
├── data/
│   └── skills_list.txt         # Skill dictionary
│   └── UpdatedResumeDataSet.csv
├── assets/
│   ├── icon.png
│   └── sample_resume.pdf
├── notebooks/
│   ├── model_training.ipynb    # Training role classifier, scorer, etc.
│   └── embedding_analysis.ipynb
├── requirements.txt
├── README.md

```