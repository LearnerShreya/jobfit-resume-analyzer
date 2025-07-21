import streamlit as st
import traceback
try:
    import os
    from resume_parser import parse_resume
    from recommender import ResumeRecommender
    from score_resume import calculate_score, SKILL_KEYWORDS
    from jd_matcher import match_resume_to_jd
    from utils import load_pickle_model, render_pdf_as_iframe, save_uploaded_resume
    import spacy
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        spacy.load("en_core_web_sm")

    st.set_page_config(
        page_title="Smart Resume Analyzer",
        page_icon=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")),
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        .matched-keyword {background-color: #d4edda; color: #155724; border-radius: 5px; padding: 2px 6px; margin: 2px; display: inline-block;}
        .missing-keyword {background-color: #f8d7da; color: #721c24; border-radius: 5px; padding: 2px 6px; margin: 2px; display: inline-block;}
        .section-divider {border-top: 2px solid #eee; margin: 30px 0 20px 0;}
    </style>
    """, unsafe_allow_html=True)

    st.title("📄 Smart Resume Analyzer")
    st.markdown("""
    Welcome to **Smart Resume Analyzer** — an AI-powered platform to help you:
    - 📤 Upload your resume
    - 📊 Analyze & score your resume
    - 🔍 Match your resume with job descriptions
    - 🧠 Get AI-based job role recommendations
    """)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Upload Resume", "Analyze Resume", "Get Recommendations"])

    if "resume_path" not in st.session_state:
        st.session_state.resume_path = None

    if page == "Upload Resume":
        st.header("Upload Your Resume")
        st.markdown("Supported formats: PDF, DOCX, DOC, TXT. Max size: 5MB.")
        uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "doc", "txt"])
        error_message = ""
        if uploaded_file:

            # File size validation (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                error_message = "File too large. Please upload a file smaller than 5MB."

            # File content validation
            elif uploaded_file.size == 0:
                error_message = "Uploaded file is empty. Please select a valid resume."
            else:

                # Save file and parse content
                save_path = save_uploaded_resume(uploaded_file)
                st.session_state.resume_path = save_path
                st.success("Resume uploaded successfully.")
                st.markdown(render_pdf_as_iframe(save_path), unsafe_allow_html=True)
        if error_message:
            st.error(error_message)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    elif page == "Analyze Resume":
        st.header("📊 Resume Analysis & JD Matching")
        if not st.session_state.resume_path:
            st.warning("⚠️ Please upload your resume first.")
        else:
            with st.spinner("Parsing your resume..."):
                data = parse_resume(st.session_state.resume_path)
            if data and data.get("error"):
                st.error(f"❌ Failed to parse resume: {data['error']}")
            elif data:
                with st.expander("📄 Extracted Resume Content"):
                    st.json(data)
                recommender = ResumeRecommender()
                predicted_roles = recommender.recommend_roles(data.get("text", ""), top_n=10)
                st.subheader("🎯 All Role Probabilities")
                for role, confidence in predicted_roles:
                    st.progress(confidence / 100, text=f"{role}: {confidence}%")
                available_fields = list(SKILL_KEYWORDS.keys())
                default_field = predicted_roles[0][0] if predicted_roles else available_fields[0]
                
                # Add a subtle horizontal bar above the label
                st.markdown('<hr style="border: none; border-top: 2px solid #e0e0e0; margin-top: 24px; margin-bottom: 0;">', unsafe_allow_html=True)
                st.markdown('<div style="font-size:1.4em; font-weight:bold; margin-top:10px; margin-bottom:6px;">Select job role/domain to score against:</div>', unsafe_allow_html=True)
                selected_field = st.selectbox(
                    " ",  # Hide default label
                    available_fields,
                    index=available_fields.index(default_field) if default_field in available_fields else 0,
                    help="Choose the job role you want your resume scored against."
                )

                # Custom skill list upload
                st.markdown("**Optional: Upload your own skill list (TXT or CSV, one skill per line/cell):**")
                custom_skill_file = st.file_uploader("Upload skill list", type=["txt", "csv"], key="custom_skill_list")
                custom_skills = None
                if custom_skill_file:
                    import pandas as pd
                    if custom_skill_file.name.endswith(".csv"):
                        df = pd.read_csv(custom_skill_file, header=None)
                        custom_skills = df[0].dropna().astype(str).tolist()
                    else:
                        custom_skills = [line.strip() for line in custom_skill_file if line.strip()]
                resume_text = data.get("text", "").lower().strip()

                # Use custom skills if provided
                skills_to_use = custom_skills if custom_skills else SKILL_KEYWORDS[selected_field]
                from score_resume import _skill_in_text
                matched_keywords = [skill for skill in skills_to_use if _skill_in_text(skill, resume_text)]
                missing_keywords = [skill for skill in skills_to_use if not _skill_in_text(skill, resume_text)]
                st.markdown(f"**Matched Keywords for {selected_field}:**")
                st.markdown(' '.join([f'<span class="matched-keyword">{kw}</span>' for kw in matched_keywords]), unsafe_allow_html=True)
                st.markdown(f"**Missing Keywords for {selected_field}:**")
                st.markdown(' '.join([f'<span class="missing-keyword">{kw}</span>' for kw in missing_keywords]), unsafe_allow_html=True)

                # Score using custom or default skills
                if custom_skills:
                    score = round(100 * len(matched_keywords) / len(skills_to_use), 2) if skills_to_use else 0.0
                else:
                    score = calculate_score(data.get("text", ""), selected_field)
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                st.subheader("💯 Resume Score")
                st.progress(score / 100, text=f"{score}/100")
                st.metric("Score", f"{score}/100")
                st.caption("Tip: Add more missing keywords to your resume for a higher score!")

                # Downloadable PDF report
                from fpdf import FPDF
                if st.button("Download Analysis Report (PDF)"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=14)
                    pdf.cell(0, 10, "Resume Analysis Report", ln=True, align="C")
                    pdf.ln(5)
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, f"Selected Role: {selected_field}", ln=True)
                    pdf.cell(0, 10, f"Score: {score}/100", ln=True)
                    pdf.ln(3)
                    pdf.set_font("Arial", style="B", size=12)
                    pdf.cell(0, 10, "Matched Keywords:", ln=True)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 8, ", ".join(matched_keywords) if matched_keywords else "None")
                    pdf.set_font("Arial", style="B", size=12)
                    pdf.cell(0, 10, "Missing Keywords:", ln=True)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 8, ", ".join(missing_keywords) if missing_keywords else "None")
                    pdf.ln(2)
                    pdf.set_font("Arial", style="B", size=12)
                    pdf.cell(0, 10, "Role Probabilities:", ln=True)
                    pdf.set_font("Arial", size=12)
                    for role, confidence in predicted_roles:
                        pdf.cell(0, 8, f"{role}: {confidence}%", ln=True)
                    pdf.ln(2)
                    pdf.set_font("Arial", style="B", size=12)
                    pdf.cell(0, 10, "Top Recommendations:", ln=True)
                    pdf.set_font("Arial", size=12)
                    for role, confidence in predicted_roles[:3]:
                        pdf.cell(0, 8, f"{role} ({confidence}%)", ln=True)
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                        pdf.output(tmpfile.name)
                        with open(tmpfile.name, "rb") as f:
                            st.download_button(
                                label="Click here to download your PDF report",
                                data=f.read(),
                                file_name="resume_analysis_report.pdf",
                                mime="application/pdf"
                            )
                # Downloadable HTML report
                if st.button("Download Analysis Report (HTML)"):
                    html_report = f"""
                    <h2>Resume Analysis Report</h2>
                    <h3>Selected Role: {selected_field}</h3>
                    <p><b>Score:</b> {score}/100</p>
                    <p><b>Matched Keywords:</b> {', '.join(matched_keywords) if matched_keywords else 'None'}</p>
                    <p><b>Missing Keywords:</b> {', '.join(missing_keywords) if missing_keywords else 'None'}</p>
                    <h4>Role Probabilities</h4>
                    <ul>
                    {''.join([f'<li>{role}: {confidence}%' for role, confidence in predicted_roles])}
                    </ul>
                    <h4>Recommendations</h4>
                    <ul>
                    {''.join([f'<li>{role} ({confidence}%)' for role, confidence in predicted_roles[:3]])}
                    </ul>
                    """
                    import base64
                    b64 = base64.b64encode(html_report.encode()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="resume_analysis_report.html">Click here to download your report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                jd_input = st.text_area(
                    "📑 Paste a Job Description (Optional)",
                    help="Paste a job description here to see how well your resume matches it."
                )
                if jd_input.strip():
                    match = match_resume_to_jd(data.get("text", ""), jd_input)
                    st.success(f"🔗 JD Match Score: {match['similarity_score']}%")
                    st.info(f"🧾 Interpretation: {match['result']}")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    elif page == "Get Recommendations":
        st.header("🧠 AI-Based Job Role Recommendation")
        if not st.session_state.resume_path:
            st.warning("⚠️ Please upload your resume first.")
        else:
            data = parse_resume(st.session_state.resume_path)
            if data and data.get("error"):
                st.error(f"❌ Failed to parse resume: {data['error']}")
            elif data:
                recommender = ResumeRecommender()
                predicted_roles = recommender.recommend_roles(data.get("text", ""), top_n=5)
                st.subheader("🎯 Suggested Roles")
                for role, confidence in predicted_roles:
                    st.success(f"🎯 {role} ({confidence}%)")
                st.caption("🧠 Based on extracted keywords, technologies, and your experience.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Startup error: {e}")
    st.text(traceback.format_exc())