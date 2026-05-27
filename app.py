import streamlit as st
import pandas as pd
from pdf_parser import extract_text_from_pdf
from matcher import analyze_match, analyze_sections, compare_resumes, generate_cover_letter, generate_resume_rewrite, generate_full_resume
from pdf_generator import generate_pdf_from_text

st.set_page_config(page_title="Resume-JD Matcher", layout="wide")

if "full_resume_text" not in st.session_state:
    st.session_state.full_resume_text = ""
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

st.title("AI Resume-JD Matcher")
st.caption("Paste a job description and upload your resumes to get match scores and improvement tips.")

with st.container():
    col_jd, col_resume = st.columns(2)
    with col_jd:
        jd_text = st.text_area("Job Description", height=200,
                                placeholder="Paste the job description here...")
    with col_resume:
        uploaded_files = st.file_uploader("Upload Resumes (PDF, up to 3)",
                                           type=["pdf"],
                                           accept_multiple_files=True,
                                           key="main_upload")

selected_resume = None

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    if len(uploaded_files) > 1:
        selected_name = st.selectbox("Select resume for Global / Section / Generate:", file_names)
        selected_resume = next(f for f in uploaded_files if f.name == selected_name)
    else:
        selected_resume = uploaded_files[0]
        st.caption(f"Using: {selected_resume.name}")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Global Analysis", "Section Analysis", "Compare Resumes", "Generate Documents"])

# TAB 1
with tab1:
    analyze_btn = st.button("Analyze", type="primary", key="btn1")
    if analyze_btn:
        if not jd_text.strip():
            st.error("Paste a job description first.")
        elif selected_resume is None:
            st.error("Upload at least one resume PDF.")
        else:
            with st.spinner("Analyzing... this takes 15-30 seconds"):
                try:
                    resume_text = extract_text_from_pdf(selected_resume)
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
        st.info("Fill in the inputs above and click Analyze.")

# TAB 2
with tab2:
    section_btn = st.button("Analyze Sections", type="primary", key="btn2")
    if section_btn:
        if not jd_text.strip():
            st.error("Paste a job description first.")
        elif selected_resume is None:
            st.error("Upload at least one resume PDF.")
        else:
            with st.spinner("Analyzing sections... this takes 20-40 seconds"):
                try:
                    resume_text2 = extract_text_from_pdf(selected_resume)
                    result2 = analyze_sections(jd_text, resume_text2)
                    sections = result2.get("sections", {})
                    section_names = ["summary", "skills", "experience", "projects", "education"]
                    labels = ["Professional Summary", "Technical Skills",
                              "Experience", "Projects", "Education"]
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
        st.info("Fill in the inputs above and click Analyze Sections.")

# TAB 3
with tab3:
    st.caption("Uses all uploaded resumes. Upload at least 2 to compare.")
    compare_btn = st.button("Compare Resumes", type="primary", key="btn3")
    if compare_btn:
        if not jd_text.strip():
            st.error("Paste a job description first.")
        elif len(uploaded_files) < 2:
            st.error("Upload at least 2 resume PDFs.")
        elif len(uploaded_files) > 3:
            st.error("Maximum 3 resumes.")
        else:
            with st.spinner(f"Comparing {len(uploaded_files)} resumes... this takes 30-60 seconds"):
                try:
                    resumes = []
                    for f in uploaded_files:
                        text = extract_text_from_pdf(f)
                        resumes.append({'name': f.name, 'text': text})
                    result3 = compare_resumes(jd_text, resumes)
                    winner = result3.get("winner", "")
                    st.success(f"Winner: {winner}")
                    st.subheader("Score Comparison")
                    rows = result3.get("resumes", [])
                    if rows:
                        df = pd.DataFrame(rows)
                        df = df.rename(columns={
                            "name": "Resume",
                            "match_score": "Match Score",
                            "quantification_score": "Quantification",
                            "missing_keywords": "Missing Keywords",
                            "strengths": "Strengths",
                            "weaknesses": "Weaknesses"
                        })
                        df["Missing Keywords"] = df["Missing Keywords"].apply(lambda x: ", ".join(x))
                        st.dataframe(df[["Resume", "Match Score", "Quantification",
                                        "Missing Keywords"]], use_container_width=True)
                    st.subheader("Details")
                    for r in rows:
                        with st.expander(f"{r['name']} - {r['match_score']}/100"):
                            st.markdown(f"**Strengths:** {r.get('strengths', '')}")
                            st.markdown(f"**Weaknesses:** {r.get('weaknesses', '')}")
                            st.markdown(f"**Missing:** {', '.join(r.get('missing_keywords', []))}")
                    st.subheader("Verdict")
                    st.info(result3.get("verdict", ""))
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Upload 2-3 resumes above and click Compare Resumes.")

# TAB 4
with tab4:
    st.caption("Generate tailored documents for this JD.")
    col7, col8 = st.columns(2)

    with col7:
        cover_btn = st.button("Generate Cover Letter", type="primary", key="btn4")
        if cover_btn:
            if not jd_text.strip():
                st.error("Paste a job description first.")
            elif selected_resume is None:
                st.error("Upload at least one resume PDF.")
            else:
                with st.spinner("Writing cover letter... this takes 15-30 seconds"):
                    try:
                        resume_text4 = extract_text_from_pdf(selected_resume)
                        cover_letter = generate_cover_letter(jd_text, resume_text4)
                        st.subheader("Cover Letter")
                        st.text_area("", value=cover_letter, height=400, key="cover_output")
                        st.download_button(
                            label="Download Cover Letter (.txt)",
                            data=cover_letter,
                            file_name="cover_letter.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("Click to generate a tailored cover letter.")

    with col8:
        rewrite_btn = st.button("Rewrite Resume for this JD", type="primary", key="btn5")
        if rewrite_btn:
            if not jd_text.strip():
                st.error("Paste a job description first.")
            elif selected_resume is None:
                st.error("Upload at least one resume PDF.")
            else:
                with st.spinner("Rewriting resume... this takes 20-40 seconds"):
                    try:
                        resume_text5 = extract_text_from_pdf(selected_resume)
                        result5 = generate_resume_rewrite(jd_text, resume_text5)
                        st.subheader("Rewritten Summary")
                        st.info(result5.get("summary_rewrite", ""))
                        st.subheader("Tailored Bullets")
                        for item in result5.get("tailored_bullets", []):
                            with st.expander(f"{item.get('section', '')}: {item.get('original', '')[:60]}..."):
                                st.markdown(f"**Rewritten:** {item.get('rewritten', '')}")
                                st.markdown(f"**Why:** {item.get('reason', '')}")
                        if result5.get("sections_to_add"):
                            st.subheader("Sections to Add")
                            for item in result5.get("sections_to_add", []):
                                with st.expander(f"Add: {item.get('section', '')}"):
                                    st.markdown(f"**Why:** {item.get('reason', '')}")
                                    st.markdown(f"**Example:** {item.get('example', '')}")
                        if result5.get("sections_to_remove"):
                            st.subheader("Sections to Remove")
                            for item in result5.get("sections_to_remove", []):
                                with st.expander(f"Remove: {item.get('section', '')}"):
                                    st.markdown(f"**Why:** {item.get('reason', '')}")
                        output_lines = ["REWRITTEN PROFESSIONAL SUMMARY", "=" * 40,
                                        result5.get("summary_rewrite", ""), "", "TAILORED BULLETS", "=" * 40]
                        for item in result5.get("tailored_bullets", []):
                            output_lines += [f"[{item.get('section', '')}]",
                                             f"Original:  {item.get('original', '')}",
                                             f"Rewritten: {item.get('rewritten', '')}",
                                             f"Why: {item.get('reason', '')}", ""]
                        st.download_button(
                            label="Download Resume Rewrite (.txt)",
                            data="\n".join(output_lines),
                            file_name="resume_rewrite.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("Click to get tailored bullets and resume suggestions.")

    st.divider()
    st.subheader("Generate Full Tailored Resume")
    st.caption("Claude rewrites your entire resume tailored to this JD. Downloads as PDF.")
    full_resume_btn = st.button("Generate Full Resume", type="primary", key="btn6")

    if full_resume_btn:
        if not jd_text.strip():
            st.error("Paste a job description first.")
        elif selected_resume is None:
            st.error("Upload at least one resume PDF.")
        else:
            with st.spinner("Rewriting full resume... this takes 30-60 seconds"):
                try:
                    resume_text6 = extract_text_from_pdf(selected_resume)
                    st.session_state.full_resume_text = generate_full_resume(jd_text, resume_text6)
                    st.session_state.pdf_bytes = generate_pdf_from_text(st.session_state.full_resume_text)
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.full_resume_text:
        st.subheader("Tailored Resume Preview")
        st.text_area("", value=st.session_state.full_resume_text, height=500, key="full_resume_output")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="Download as TXT",
                data=st.session_state.full_resume_text,
                file_name="tailored_resume.txt",
                mime="text/plain",
                key="dl_txt"
            )
        with col_dl2:
            st.download_button(
                label="Download as PDF",
                data=st.session_state.pdf_bytes,
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                key="dl_pdf"
            )
    else:
        st.info("Click to generate a fully rewritten resume tailored to this JD.")