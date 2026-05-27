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