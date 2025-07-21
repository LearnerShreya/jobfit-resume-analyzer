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
        from utils import save_uploaded_resume
        save_path = save_uploaded_resume(uploaded_file)
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

        if data and data.get("error"):
            st.error(f"❌ Failed to parse resume: {data['error']}")
        elif data:
            with st.expander("📄 Extracted Resume Content"):
                st.json(data)

            # Resume Recommender
            recommender = ResumeRecommender()
            predicted_roles = recommender.recommend_roles(data.get("text", ""), top_n=10)
            st.subheader("🎯 All Role Probabilities")
            for role, confidence in predicted_roles:
                st.write(f"**{role}**: {confidence}%")

            # Manual field selection for scoring
            from score_resume import SKILL_KEYWORDS, calculate_score
            available_fields = list(SKILL_KEYWORDS.keys())
            default_field = predicted_roles[0][0] if predicted_roles else available_fields[0]
            selected_field = st.selectbox("Select job role/domain to score against:", available_fields, index=available_fields.index(default_field) if default_field in available_fields else 0)

            # Show matched keywords
            resume_text = data.get("text", "").lower().strip()
            matched_keywords = [skill for skill in SKILL_KEYWORDS[selected_field] if skill in resume_text]
            st.write(f"**Matched Keywords for {selected_field}:** {', '.join(matched_keywords) if matched_keywords else 'None'}")

            # Resume Scoring
            score = calculate_score(data.get("text", ""), selected_field)
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

        if data and data.get("error"):
            st.error(f"❌ Failed to parse resume: {data['error']}")
        elif data:
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