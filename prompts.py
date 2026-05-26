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