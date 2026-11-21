# PathPilot AI — Career Roadmap & Skill Gap Finder

**Problem statement:** Task 2, Problem 4 — AI Career Roadmap & Skill Gap Finder (from the NIAT Generative AI task sheet).

A futuristic Streamlit web application powered by Google Gemini. It compares a student's current skills with a target job role and generates:
- Skills the student already has vs. skills to learn
- An 8-week, week-by-week learning roadmap
- 3 mini portfolio project ideas
- A downloadable text report

## 1. Requirements
- Python 3.10+
- A Gemini API key from Google AI Studio
- Internet connection

## 2. Setup in VS Code

Open this project folder in VS Code, then open the terminal.

### Create and activate a virtual environment (recommended)

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install packages
```bash
pip install -r requirements.txt
```

### Add your API key securely
1. Copy `.env.example` and rename the copy to `.env`.
2. Paste your Gemini key after `GEMINI_API_KEY=`.
3. Do not share `.env` or upload it to GitHub / your submission ZIP.

The app also supports Streamlit secrets. Create `.streamlit/secrets.toml` with:
```toml
GEMINI_API_KEY = "your_key_here"
```
Do not submit that file with your API key.

### Run
```bash
streamlit run app.py
```
Your browser should open the local application.

## 3. How it works
1. The user enters current skills, selects a target role and chooses weekly study hours.
2. The app builds a prompt with those inputs.
3. The Google Gemini model generates structured JSON containing the skill comparison, 8-week roadmap and three projects.
4. Streamlit displays the result and provides a text download.

## 4. Project files
- `app.py` — Streamlit interface and Gemini integration
- `requirements.txt` — Python dependencies
- `.env.example` — safe API-key template (contains no real key)
- `.gitignore` — prevents secrets and local environment files from being committed

## 5. Important
- Never hard-code your API key in `app.py`.
- Never include `.env` or `.streamlit/secrets.toml` with a real key in your submission.
- AI recommendations are suggestions. Check the skills required by real job descriptions and adapt the roadmap.
- Be prepared to explain the input → Gemini API → output flow and how the prompt requests JSON.
