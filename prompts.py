def build_matching_prompt(job_description: str, resume_text: str) -> str:
    return f"""You are an expert ATS (Applicant Tracking System) and resume coach.

Analyze this resume against the job description and return ONLY a JSON object with this exact structure:
{{
    "match_score": <integer 0-100>,
    "missing_keywords": [<5 strings>],
    "bullet_rewrites": [
        {{"original": "<original bullet>", "rewritten": "<improved bullet>"}},
        {{"original": "<original bullet>", "rewritten": "<improved bullet>"}},
        {{"original": "<original bullet>", "rewritten": "<improved bullet>"}}
    ],
    "gap_analysis": "<2-3 sentence summary of what is missing>"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY the JSON. No explanation. No markdown. No backticks."""

def build_section_analysis_prompt(job_description: str, resume_text: str) -> str:
    return f"""You are an expert resume coach and ATS specialist.

Analyze this resume section by section against the job description.
Return ONLY a JSON object with this exact structure:
{{
    "sections": {{
        "summary": {{
            "score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>",
            "suggestion": "<one concrete improvement>"
        }},
        "skills": {{
            "score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>",
            "suggestion": "<one concrete improvement>"
        }},
        "experience": {{
            "score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>",
            "suggestion": "<one concrete improvement>"
        }},
        "projects": {{
            "score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>",
            "suggestion": "<one concrete improvement>"
        }},
        "education": {{
            "score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>",
            "suggestion": "<one concrete improvement>"
        }}
    }},
    "overall_verdict": "<2 sentence summary of strongest and weakest sections>"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY the JSON. No explanation. No markdown. No backticks."""

def build_comparison_prompt(job_description: str, resumes: list[dict]) -> str:
    resumes_text = ""
    for i, r in enumerate(resumes, 1):
        resumes_text += f"\nRESUME {i} ({r['name']}):\n{r['text']}\n"

    return f"""You are an expert ATS specialist and resume coach.

Compare these {len(resumes)} resumes against the job description.
Return ONLY a JSON object with this exact structure:
{{
    "resumes": [
        {{
            "name": "<resume filename>",
            "match_score": <integer 0-100>,
            "missing_keywords": [<3 strings>],
            "quantification_score": <integer 0-100>,
            "strengths": "<one sentence>",
            "weaknesses": "<one sentence>"
        }}
    ],
    "verdict": "<which resume to use and why - 2 sentences>",
    "winner": "<exact filename of best resume>"
}}

JOB DESCRIPTION:
{job_description}
{resumes_text}
Return ONLY the JSON. No explanation. No markdown. No backticks."""

def build_cover_letter_prompt(job_description: str, resume_text: str) -> str:
    return f"""You are an expert career coach and professional writer.

Write a tailored cover letter based on this resume and job description.
The cover letter should:
- Be 3-4 paragraphs, professional but not robotic
- Opening: specific hook tied to the company/role, not generic
- Middle: 2-3 concrete achievements from the resume that directly match JD requirements
- Closing: clear call to action
- Tone: confident, human, not AI-sounding
- Length: 250-350 words

Return ONLY the cover letter text. No subject line. No date. No address. Start directly with "Dear Hiring Manager," or the specific name if mentioned in JD.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}"""


def build_resume_rewrite_prompt(job_description: str, resume_text: str) -> str:
    return f"""You are an expert ATS specialist and resume coach.

Analyze this resume against the job description and return ONLY a JSON object with this exact structure:
{{
    "tailored_bullets": [
        {{
            "section": "<Experience/Projects/Summary>",
            "original": "<original bullet or sentence>",
            "rewritten": "<improved version tailored to JD>",
            "reason": "<one sentence why this change helps>"
        }}
    ],
    "sections_to_add": [
        {{
            "section": "<section name>",
            "reason": "<why this section would help>",
            "example": "<brief example of what to include>"
        }}
    ],
    "sections_to_remove": [
        {{
            "section": "<section name>",
            "reason": "<why this section hurts or is irrelevant>"
        }}
    ],
    "summary_rewrite": "<rewritten professional summary tailored to this JD>"
}}

Provide at least 5 tailored bullets. Be specific and use numbers/metrics where possible.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY the JSON. No explanation. No markdown. No backticks."""

def build_full_resume_prompt(job_description: str, resume_text: str) -> str:
    return f"""You are a resume writer. Your ONLY job is to rewrite the resume below.

CRITICAL RULES - VIOLATION IS NOT ACCEPTABLE:
- Use ONLY the name, contact info, companies, dates, and experience from the resume below
- Do NOT invent any person, company, date, skill, or achievement
- Do NOT use placeholder names like "Michael Chen" or fake emails
- If information is not in the resume, do not add it
- Keep all real dates, company names, job titles exactly as they appear

WHAT TO IMPROVE:
- Rewrite bullets using keywords and language from the job description
- Strengthen the professional summary to match this specific role
- Reorder/rename sections for maximum impact
- Add metrics where clearly implied by existing bullets

RESUME TO REWRITE (use ONLY this person's real information):
{resume_text}

JOB DESCRIPTION (use for keyword alignment only):
{job_description}

Return the rewritten resume as clean plain text with this format:

[FULL NAME from resume]
[Contact info from resume]

PROFESSIONAL SUMMARY
<rewritten>

TECHNICAL SKILLS
<rewritten>

EXPERIENCE
[Job Title] | [Company] | [Dates]
- <bullet>

PROJECTS
[Project Name]
- <bullet>

EDUCATION
[Degree] | [Institution] | [Year]

Return ONLY the resume text. No commentary. No backticks."""