
jobfit-resume-analyzer/
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── approach.md               # Project methodology and approach
├── output.txt                # Sample output from the app
├── streamlit_app/
│   ├── app.py               # Main Streamlit UI
│   ├── resume_parser.py     # Extract text, skills, and sections from resumes
│   ├── recommender.py       # Recommend job roles based on content
│   ├── score_resume.py      # Score resume using trained ML model
│   ├── jd_matcher.py        # Match resume with job description
│   ├── utils.py             # Helper functions (file handling, NLP, etc.)
│   └── config.py            # Central config (file paths, model type, etc.)
├── notebooks/
│   ├── model_training.ipynb  # Jupyter notebook for model training
│   └── embedding_analysis.ipynb # Jupyter notebook for embedding analysis
├── model/
│   ├── classifier.pkl         # Resume role classifier (ML model)
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   ├── scorer_model.pkl       # Resume score predictor (ML model)
│   └── label_encoder.pkl      # Encodes/decodes job role classes
├── data/
│   ├── skills_list.txt       # Skill dictionary
│   ├── UpdatedResumeDataSet.csv # Resume dataset for training/testing
│   └── resume_embeddings.csv # Embedding and cluster data for visualization
├── assets/
│   ├── icon.png               # App icon
│   ├── demo_resume.pdf        # Demo/sample resume for testing
│   ├── image-2.png            # Screenshot images for README
│   ├── image-3.png            # Screenshot images for README     
│   ├── image-4.png            # Screenshot images for README
│   ├── image-5.png            # Screenshot images for README
│   ├── image-6.png            # Screenshot images for README
├── folder_structure.md       # This file: folder structure documentation
├── .gitignore                # Git ignore rules