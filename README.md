# AI Resume-JD Matcher

> 🚀 **Live Demo:** [resume-matcher-nurbolsultanov.streamlit.app](https://resume-matcher-nurbolsultanov.streamlit.app/)

A Streamlit web app that analyzes resume-JD fit using Claude AI and semantic search. Upload up to 3 resumes, paste a job description, and get actionable analysis across 4 tools.

---

## What It Does

### Tab 1 — Global Analysis
- **Match Score (0-100)** — how well your resume fits the JD
- **Missing Keywords** — top 5 terms in JD not found in your resume
- **Bullet Rewrites** — 3 suggested improvements tailored to the JD
- **Gap Analysis** — short summary of what's missing

### Tab 2 — Section Analysis
- Individual scores for: Professional Summary, Technical Skills, Experience, Projects, Education
- Strengths, weaknesses, and one concrete suggestion per section
- Overall verdict

### Tab 3 — Compare Resumes
- Upload 2-3 resume versions and compare them against the same JD
- Comparison table: match score, quantification score, missing keywords
- Per-resume details and final verdict: which resume to submit

### Tab 4 — Generate Documents
- **Cover Letter** — tailored to the JD, downloads as .txt
- **Resume Rewrite** — section-by-section bullet rewrites with reasoning, what to add/remove, downloads as .txt
- **Full Resume PDF** — complete resume rewritten for this JD, auto-fits to 1 page, downloads as PDF

---

## How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Streamlit   │ ──> │  pdfplumber  │ ──> │  Resume bullets  │
│      UI      │     │  PDF parser  │     │   (text chunks)  │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                    │
                            ┌───────────────────────┴────────┐
                            │                                │
                            ▼                                ▼
                   ┌────────────────────┐         ┌─────────────────┐
                   │ sentence-          │         │   JD keywords   │
                   │ transformers       │         │   extraction    │
                   │ (MiniLM-L6-v2)     │         └────────┬────────┘
                   │ embeddings + RAG   │                  │
                   └─────────┬──────────┘                  │
                             │                             │
                             └──────────────┬──────────────┘
                                            ▼
                              ┌──────────────────────────┐
                              │  Anthropic Claude API    │
                              │  (analysis + rewrites)   │
                              └─────────────┬────────────┘
                                            │
                                            ▼
                              ┌──────────────────────────┐
                              │  Match score · keywords  │
                              │  rewrites · gap analysis │
                              │  section scores · PDF    │
                              └──────────────────────────┘
```

---

## Tech Stack

- **Python 3.11+**
- **[Streamlit](https://streamlit.io)** — UI
- **[Anthropic Claude](https://anthropic.com)** — AI analysis and generation
- **[sentence-transformers](https://www.sbert.net)** — semantic retrieval (`all-MiniLM-L6-v2`)
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** — PDF parsing
- **[reportlab](https://www.reportlab.com)** — PDF generation
- **[pytest](https://pytest.org)** — testing

---

## Setup

```bash
git clone https://github.com/nurbolsultanov/resume-matcher.git
cd resume-matcher
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Create `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Run:

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Deploy on Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo, set main file: `app.py`
4. Add `ANTHROPIC_API_KEY` in **Settings → Secrets**

---

## Project Structure

```
resume-matcher/
├── app.py              # Streamlit UI (4 tabs)
├── matcher.py          # Claude API logic
├── pdf_parser.py       # PDF text extraction
├── pdf_generator.py    # Resume PDF generation (reportlab)
├── prompts.py          # Claude prompts
├── requirements.txt
├── .gitignore
├── README.md
└── tests/
    └── test_matcher.py
```

---

## Limitations

- Match score reflects language overlap, not hiring probability
- Plain single-column PDFs parse best — heavy formatting loses ordering
- English only
- Each analysis uses ~2-5K tokens (~$0.01-0.05 per run)

---

## About

Built by **Nurbol Sultanov** — Data Analyst in Los Angeles.

[LinkedIn](https://linkedin.com/in/nurbolsultanov) · [GitHub](https://github.com/nurbolsultanov) · [Tableau](https://public.tableau.com/app/profile/nurbol.sultanov)

## License

MIT
