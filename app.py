import streamlit as st
from pdf_parser import extract_text_from_pdf
from matcher import analyze_match, analyze_sections

st.set_page_config(page_title="Resume-JD Matcher", layout="wide")
st.title("AI Resume-JD Matcher")
st.caption("Paste a job description and upload your resume to get a match score and improvement tips.")

tab1, tab2 = st.tabs(["Global Analysis", "Section Analysis"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input")
        jd_text = st.text_area("Job Description", height=300, placeholder="Paste the job description here...")
        uploaded_file = st.file_uploader("Resume (PDF)", type=["pdf"])
        analyze_btn = st.button("Analyze", type="primary")

    with col2:
        st.subheader("Results")

        if analyze_btn:
            if not jd_text.strip():
                st.error("Paste a job description first.")
            elif uploaded_file is None:
                st.error("Upload your resume PDF first.")
            else:
                with st.spinner("Analyzing... this takes 15-30 seconds"):
                    try:
                        resume_text = extract_text_from_pdf(uploaded_file)
                        result = analyze_match(jd_text, resume_text)

                        score = result.get("match_score", 0)
                        if score >= 70:
                            st.success(f"Match Score: {score}/100")
                        elif score >= 50:
                            st.warning(f"Match Score: {score}/100")
                        else:
                            st.error(f"Match Score: {score}/100")

                        st.subheader("Missing Keywords")
                        for kw in result.get("missing_keywords", []):
                            st.markdown(f"- `{kw}`")

                        st.subheader("Suggested Bullet Rewrites")
                        for item in result.get("bullet_rewrites", []):
                            with st.expander(f"Original: {item.get('original', '')[:80]}..."):
                                st.markdown(f"**Rewritten:** {item.get('rewritten', '')}")

                        st.subheader("Gap Analysis")
                        st.info(result.get("gap_analysis", ""))

                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("Fill in the inputs on the left and click Analyze.")

with tab2:
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Input")
        jd_text2 = st.text_area("Job Description", height=300,
                                  placeholder="Paste the job description here...",
                                  key="jd2")
        uploaded_file2 = st.file_uploader("Resume (PDF)", type=["pdf"], key="upload2")
        section_btn = st.button("Analyze Sections", type="primary", key="section_btn")

    with col4:
        st.subheader("Section Scores")

        if section_btn:
            if not jd_text2.strip():
                st.error("Paste a job description first.")
            elif uploaded_file2 is None:
                st.error("Upload your resume PDF first.")
            else:
                with st.spinner("Analyzing sections... this takes 20-40 seconds"):
                    try:
                        resume_text2 = extract_text_from_pdf(uploaded_file2)
                        result2 = analyze_sections(jd_text2, resume_text2)

                        sections = result2.get("sections", {})
                        section_names = ["summary", "skills", "experience", "projects", "education"]
                        labels = ["Professional Summary", "Technical Skills", "Experience", "Projects", "Education"]

                        for key, label in zip(section_names, labels):
                            sec = sections.get(key, {})
                            score = sec.get("score", 0)

                            with st.expander(f"{label}: {score}/100", expanded=True):
                                if score >= 70:
                                    st.success(f"Score: {score}/100")
                                elif score >= 50:
                                    st.warning(f"Score: {score}/100")
                                else:
                                    st.error(f"Score: {score}/100")

                                st.markdown(f"**Strengths:** {sec.get('strengths', '')}")
                                st.markdown(f"**Weaknesses:** {sec.get('weaknesses', '')}")
                                st.markdown(f"**Suggestion:** {sec.get('suggestion', '')}")

                        st.subheader("Overall Verdict")
                        st.info(result2.get("overall_verdict", ""))

                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("Fill in the inputs on the left and click Analyze Sections.")