import json
import os
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv
from prompts import build_matching_prompt, build_section_analysis_prompt, build_comparison_prompt, build_cover_letter_prompt, build_resume_rewrite_prompt, build_full_resume_prompt

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_relevant_resume_chunks(resume_text: str, job_description: str, top_k: int = 10) -> str:
    chunks = [c.strip() for c in resume_text.split("\n") if len(c.strip()) > 30]
    if not chunks:
        return resume_text

    jd_embedding = model.encode([job_description])
    chunk_embeddings = model.encode(chunks)

    scores = cosine_similarity(jd_embedding, chunk_embeddings)[0]
    top_indices = [i for i in np.argsort(scores)[::-1] if i < len(chunks)][:top_k]
    top_chunks = [chunks[i] for i in sorted(top_indices)]

    return "\n".join(top_chunks)


def analyze_match(job_description: str, resume_text: str) -> dict:
    relevant_resume = get_relevant_resume_chunks(resume_text, job_description)
    prompt = build_matching_prompt(job_description, relevant_resume)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    result = json.loads(raw)
    return result

def analyze_sections(job_description: str, resume_text: str) -> dict:
    relevant_resume = get_relevant_resume_chunks(resume_text, job_description)
    prompt = build_section_analysis_prompt(job_description, relevant_resume)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    result = json.loads(raw)
    return result

def compare_resumes(job_description: str, resumes: list[dict]) -> dict:
    processed = []
    for r in resumes:
        relevant_text = get_relevant_resume_chunks(r['text'], job_description)
        processed.append({'name': r['name'], 'text': relevant_text})

    prompt = build_comparison_prompt(job_description, processed)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    result = json.loads(raw)
    return result

def generate_cover_letter(job_description: str, resume_text: str) -> str:
    relevant_resume = get_relevant_resume_chunks(resume_text, job_description)
    prompt = build_cover_letter_prompt(job_description, relevant_resume)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text.strip()


def generate_resume_rewrite(job_description: str, resume_text: str) -> dict:
    relevant_resume = get_relevant_resume_chunks(resume_text, job_description)
    prompt = build_resume_rewrite_prompt(job_description, relevant_resume)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    
    # Strip markdown backticks if Claude added them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    
    if not raw:
        raise ValueError("Claude returned empty response. Try again.")
    
    result = json.loads(raw)
    return result

def generate_full_resume(job_description: str, resume_text: str) -> str:
    prompt = build_full_resume_prompt(job_description, resume_text)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text.strip()