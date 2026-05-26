# AI Resume-JD Matcher

A Streamlit web app that analyzes how well your resume matches a job description using Claude AI and semantic search.

## What it does

- **Match Score** (0-100) - how well your resume fits the JD
- **Missing Keywords** - top 5 terms in JD not found in your resume
- **Bullet Rewrites** - 3 suggested improvements tailored to the JD
- **Gap Analysis** - short summary of what's missing

## Tech Stack

- Python 3.11+
- [Streamlit](https://streamlit.io) - UI
- [Anthropic Claude](https://anthropic.com) - AI analysis
- [sentence-transformers](https://www.sbert.net) - semantic retrieval (all-MiniLM-L6-v2)
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF parsing

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/nurbolsultanov/resume-matcher.git
cd resume-matcher
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file:
ANTHROPIC_API_KEY=sk-ant-...

### 5. Run

```bash
streamlit run app.py
```

Open http://localhost:8501

## Run Tests

```bash
pytest tests/ -v
```

## Deploy on Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo, set main file as `app.py`
4. Add `ANTHROPIC_API_KEY` in Secrets settings

## Project Structure
resume-matcher/
├── app.py              # Streamlit UI
├── matcher.py          # Core matching logic
├── pdf_parser.py       # PDF text extraction
├── prompts.py          # Claude prompts
├── requirements.txt
├── .env                # API key (gitignored)
├── .gitignore
├── README.md
└── tests/
└── test_matcher.py