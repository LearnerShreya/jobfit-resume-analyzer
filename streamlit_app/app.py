import streamlit as st
import os

from resume_parser import parse_resume
from recommender import ResumeRecommender
from score_resume import calculate_score
from jd_matcher import match_resume_to_jd
from utils import load_pickle_model, render_pdf_as_iframe

# ======================================
# ⚙️ Page Configuration
# ======================================
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="../assets/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# 📄 App Header
# ======================================
st.title("📄 Smart Resume Analyzer")
st.markdown("""
Welcome to **Smart Resume Analyzer** — an AI-powered platform to help you:

- 📤 Upload your resume  
- 📊 Analyze & score your resume  
- 🔍 Match your resume with job descriptions  
- 🧠 Get AI-based job role recommendations
""")

# ======================================
# 🔍 Load Models
# ======================================
with st.spinner("🔄 Loading models..."):
    try:
        scorer_model = load_pickle_model("scorer_model.pkl")
    except Exception as e:
        st.error("❌ Failed to load one or more models.")
        st.exception(e)
        st.stop()

# ======================================
# 📂 Sidebar Navigation
# ======================================
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Select a page", ["Upload Resume", "Analyze Resume", "Get Recommendations"])

# ======================================
# 🧠 Session State Setup
# ======================================
if "resume_path" not in st.session_state:
    st.session_state.resume_path = None

# ======================================
# 📤 Page 1: Upload Resume
# ======================================
if page == "Upload Resume":
    st.header("📤 Upload Your Resume")
    st.markdown("Only PDF files are supported.")

    uploaded_file = st.file_uploader("Choose your resume file", type=["pdf"])

    if uploaded_file:
        uploads_dir = os.path.join("..", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        save_path = os.path.join(uploads_dir, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.resume_path = save_path
        st.success("✅ Resume uploaded successfully.")

        # Show PDF in iframe
        st.markdown(render_pdf_as_iframe(save_path), unsafe_allow_html=True)

# ======================================
# 📊 Page 2: Analyze Resume
# ======================================
elif page == "Analyze Resume":
    st.header("📊 Resume Analysis & JD Matching")

    if not st.session_state.resume_path:
        st.warning("⚠️ Please upload your resume first.")
    else:
        data = parse_resume(st.session_state.resume_path)

        if data:
            with st.expander("📄 Extracted Resume Content"):
                st.json(data)

            # Resume Scoring
            score = calculate_score(data.get("text", ""), scorer_model)
            st.metric("💯 Resume Score", f"{score}/100")

            # JD Matcher (Optional)
            jd_input = st.text_area("📑 Paste a Job Description (Optional)")
            if jd_input.strip():
                match = match_resume_to_jd(data.get("text", ""), jd_input)
                st.success(f"🔗 JD Match Score: {match['similarity_score']}%")
                st.info(f"🧾 Interpretation: {match['result']}")

# ======================================
# 🧠 Page 3: Get Recommendations
# ======================================
elif page == "Get Recommendations":
    st.header("🧠 AI-Based Job Role Recommendation")

    if not st.session_state.resume_path:
        st.warning("⚠️ Please upload your resume first.")
    else:
        data = parse_resume(st.session_state.resume_path)

        if data:
            # Corrected: Initialize using default or path-based constructor
            recommender = ResumeRecommender()

            # Get top N predicted roles
            predicted_roles = recommender.recommend_roles(data.get("text", ""), top_n=3)

            if predicted_roles:
                for role, confidence in predicted_roles:
                    st.success(f"🎯 Suggested Role: **{role}** ({confidence}%)")
            else:
                st.info("⚠️ Not enough information to make a recommendation.")

            st.caption("🧠 Based on extracted keywords, technologies, and your experience.")