import os
import json
import re
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="PathPilot AI | Career Roadmap",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- FUTURISTIC UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#080b16; --panel:#11182b; --line:rgba(157,176,226,.16); --muted:#929db7; --violet:#a99aff; --blue:#70baff; }
.stApp { background: radial-gradient(ellipse at 12% 4%,rgba(101,75,255,.16),transparent 34%), radial-gradient(ellipse at 90% 30%,rgba(31,146,205,.12),transparent 34%), #080b16; color:#f4f6ff; font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1180px; padding-top:1.5rem; padding-bottom:4rem; }
h1,h2,h3,.brand,.eyebrow { font-family:'Space Grotesk',sans-serif !important; }
.brand { font-size:1.25rem; font-weight:700; letter-spacing:-.7px; color:#fff; }
.brand-mark { display:inline-grid; place-items:center; width:30px;height:30px;border-radius:9px; margin-right:9px; background:linear-gradient(135deg,#8274ff,#4dbce9); box-shadow:0 0 25px #7568ff55; }
.brand span:last-child { color:#9d94ff; }
.navline { border-bottom:1px solid var(--line); padding:0 0 18px; display:flex; justify-content:space-between; align-items:center; }
.eyebrow { color:#9d9abe; font-size:.68rem; letter-spacing:2px; font-weight:700; text-transform:uppercase; }
.hero { padding:3.2rem 0 2.2rem; }
.hero h1 { font-size:clamp(2.8rem,6vw,5rem); line-height:1.02; letter-spacing:-3px; margin:.9rem 0 1rem; }
.gradient { background:linear-gradient(100deg,#b5a5ff,#70baff 60%,#68dfd0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sub { color:#a2adc5; font-size:1rem; line-height:1.8; max-width:690px; }
.pill { display:inline-block; border:1px solid #8175ff55; color:#b9afff; background:#8175ff12; border-radius:30px; padding:7px 12px; font-size:.68rem; letter-spacing:1px; font-weight:700; }
.panel { background:linear-gradient(145deg,rgba(22,31,55,.94),rgba(12,18,33,.96)); border:1px solid var(--line); border-radius:17px; padding:1.4rem; box-shadow:0 20px 60px #0002; }
.panel-title { font-family:'Space Grotesk'; font-size:1.2rem; font-weight:700; margin-bottom:.2rem; }
.muted { color:var(--muted); font-size:.85rem; line-height:1.65; }
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] div[data-baseweb="select"], div[data-testid="stNumberInput"] input { background:#0b1223 !important; color:#f4f6ff !important; border-color:#3a4667 !important; border-radius:9px !important; }
label, .stMarkdown p { color:#dce3f5; }
.stButton>button, .stFormSubmitButton>button { background:linear-gradient(105deg,#8174ff,#438fdc); color:white; border:0; border-radius:9px; padding:.72rem 1.2rem; font-weight:700; box-shadow:0 8px 28px #625cff35; }
.stButton>button:hover, .stFormSubmitButton>button:hover { border:0; color:white; transform:translateY(-1px); }
div[data-testid="stMetric"] { background:#111a2e; border:1px solid var(--line); border-radius:12px; padding:15px; }
div[data-testid="stMetricLabel"] { color:#929db7; }
div[data-testid="stMetricValue"] { color:#b5a5ff; font-family:'Space Grotesk'; }
.skill-chip { display:inline-block; padding:7px 10px; margin:4px 5px 4px 0; background:#1b2540; border:1px solid #58678b66; border-radius:7px; color:#dce5ff; font-size:.78rem; }
.gap-chip { display:inline-block; padding:7px 10px; margin:4px 5px 4px 0; background:#2a203d; border:1px solid #a68aff55; border-radius:7px; color:#d8caff; font-size:.78rem; }
.week { border-left:2px solid #8d80ff; padding:0 0 1.15rem 1rem; margin-left:.4rem; }
.week-label { color:#a99aff; font-size:.7rem; font-weight:700; letter-spacing:1px; }
.week h4 { margin:.25rem 0; font-family:'Space Grotesk'; }
.week p { color:#a2adc5; font-size:.85rem; line-height:1.65; margin:0; }
.project-card { background:#101a30; border:1px solid var(--line); border-radius:12px; padding:1rem; height:100%; }
.project-card b { color:#f4f6ff; font-family:'Space Grotesk'; }
hr { border-color:var(--line); }
footer { color:#697692; font-size:.7rem; letter-spacing:1px; border-top:1px solid var(--line); padding-top:1.2rem; margin-top:3rem; }
.stAlert { border-radius:10px; }
@media(max-width:700px){.hero{padding:2rem 0 1rem}.hero h1{letter-spacing:-2px}.panel{padding:1rem}}
</style>
""", unsafe_allow_html=True)

# ---------- HELPERS ----------
def get_api_key():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            key = st.secrets.get("GEMINI_API_KEY", "").strip()
        except Exception:
            key = ""
    return key

def clean_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

def create_prompt(current_skills, target_role, hours):
    return f"""
You are an expert career learning-path advisor. Create a practical, realistic learning plan.
The student currently knows these skills: {current_skills}
Their target job role is: {target_role}
They can study {hours} hours per week.

Return ONLY valid JSON with this exact structure:
{{
  "summary": "2-3 sentence personalized overview",
  "skills_have": ["skill 1", "skill 2"],
  "skills_to_learn": [
    {{"skill":"skill name","why":"short reason","priority":"High"}}
  ],
  "roadmap": [
    {{"week":"Week 1","focus":"topic","tasks":["task 1","task 2"],"outcome":"measurable outcome"}}
  ],
  "projects": [
    {{"title":"project title","description":"what to build","skills":["skill 1","skill 2"],"level":"Beginner"}}
  ]
}}

Requirements:
- Include exactly 8 roadmap entries, one for each week.
- Include exactly 3 mini portfolio project ideas.
- Compare the student's current skills with the target role's typical entry-level skills.
- Put skills already known in skills_have. Do not claim the student knows skills they did not list.
- Put missing or next skills in skills_to_learn, with priority High, Medium or Low.
- Order the roadmap from foundations to practical application.
- Scale the workload to {hours} hours per week.
- Keep the language student-friendly, specific and actionable.
- Do not promise employment or invent certifications.
"""

# ---------- HEADER + HERO ----------
st.markdown("""
<div class="navline">
  <div class="brand"><span class="brand-mark">✦</span>pathpilot<span>.ai</span></div>
  <div class="pill">AI CAREER INTELLIGENCE · PROTOTYPE</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">✦ &nbsp; YOUR SKILLS. YOUR NEXT MOVE.</div>
  <h1>Build a career path<br><span class="gradient">with direction.</span></h1>
  <p class="sub">Tell us what you know, choose the role you're aiming for, and let AI map the skills you need next — with an eight-week learning plan designed around your time.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, .85], gap="large")
with left:
    st.markdown('<div class="panel"><div class="panel-title">01 / Your starting point</div><div class="muted">Add the skills you already have. Be honest — this helps make your roadmap useful.</div>', unsafe_allow_html=True)
    with st.form("career_form"):
        current_skills = st.text_area(
            "Your current skills",
            placeholder="Example: C, basic Python, HTML, CSS, communication",
            height=115,
            help="Separate skills with commas."
        )
        target_role = st.selectbox(
            "Your target job role",
            ["AI / Machine Learning Engineer", "Data Scientist", "Data Analyst",
             "Python Developer", "Web Developer", "Cybersecurity Analyst",
             "UI / UX Designer", "Cloud Engineer", "Product Manager",
             "Business Analyst", "Custom / Other"]
        )
        custom_role = ""
        if target_role == "Custom / Other":
            custom_role = st.text_input("Enter your target role", placeholder="e.g. Robotics Engineer")
        hours = st.slider("Hours available to study per week", min_value=2, max_value=30, value=8, step=1)
        submitted = st.form_submit_button("Generate my AI roadmap  ✦", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="panel" style="height:100%">
      <div class="eyebrow">HOW IT WORKS</div>
      <h3 style="font-family:Space Grotesk;margin-top:15px">From where you are<br>to where you want to be.</h3>
      <div style="margin-top:25px">
        <div style="display:flex;gap:14px;margin:20px 0"><span class="pill">01</span><div><b>Skill snapshot</b><div class="muted">Map your current knowledge.</div></div></div>
        <div style="display:flex;gap:14px;margin:20px 0"><span class="pill">02</span><div><b>Gap analysis</b><div class="muted">Find the skills your target role expects.</div></div></div>
        <div style="display:flex;gap:14px;margin:20px 0"><span class="pill">03</span><div><b>8-week roadmap</b><div class="muted">Learn in a clear, achievable order.</div></div></div>
        <div style="display:flex;gap:14px;margin:20px 0"><span class="pill">04</span><div><b>Portfolio projects</b><div class="muted">Turn learning into proof of skill.</div></div></div>
      </div>
      <hr>
      <div class="muted">Powered by Google Gemini. Your inputs are sent to the AI model only when you generate a roadmap.</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- GENERATION ----------
if submitted:
    role = custom_role.strip() if target_role == "Custom / Other" else target_role
    if not current_skills.strip():
        st.error("Please enter at least one current skill before generating your roadmap.")
    elif not role:
        st.error("Please enter a target job role.")
    else:
        api_key = get_api_key()
        if not api_key:
            st.error("Gemini API key not found. Add GEMINI_API_KEY to your .env file or Streamlit secrets, then restart the app.")
            st.info("See the README for setup instructions. Never paste your API key into the source code.")
        else:
            with st.spinner("Gemini is mapping your skills and building your roadmap..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=create_prompt(current_skills.strip(), role, hours),
                        config=types.GenerateContentConfig(
                            temperature=0.35,
                            response_mime_type="application/json"
                        )
                    )
                    data = clean_json(response.text)
                    st.session_state["career_result"] = data
                    st.session_state["career_role"] = role
                    st.session_state["career_hours"] = hours
                except Exception as e:
                    st.error("We couldn't generate the roadmap. Check your API key, internet connection and model access, then try again.")
                    with st.expander("Technical details"):
                        st.code(str(e))

# ---------- RESULTS ----------
if "career_result" in st.session_state:
    data = st.session_state["career_result"]
    role = st.session_state["career_role"]
    hours = st.session_state["career_hours"]
    st.markdown("---")
    st.markdown('<div class="eyebrow">02 / YOUR PERSONALIZED REPORT</div>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-family:Space Grotesk;font-size:2.3rem;letter-spacing:-1px">Your roadmap to <span class="gradient">{role}</span></h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="muted">{data.get("summary","")}</p>', unsafe_allow_html=True)

    m1,m2,m3 = st.columns(3)
    m1.metric("Target role", role)
    m2.metric("Learning runway", "8 weeks")
    m3.metric("Study commitment", f"{hours} hrs / week")

    c1,c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="panel"><div class="panel-title">✓ Skills you already have</div><div class="muted">Your current foundation</div>', unsafe_allow_html=True)
        skills_have = data.get("skills_have", [])
        if skills_have:
            st.markdown("".join(f'<span class="skill-chip">{s}</span>' for s in skills_have), unsafe_allow_html=True)
        else:
            st.write("No current skills were identified.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><div class="panel-title">✧ Skills to develop</div><div class="muted">Your next learning priorities</div>', unsafe_allow_html=True)
        for item in data.get("skills_to_learn", []):
            if isinstance(item, dict):
                priority = item.get("priority", "Medium")
                st.markdown(f'**{item.get("skill","Skill")}**  ·  `{priority}`')
                st.caption(item.get("why", ""))
            else:
                st.markdown(f'<span class="gap-chip">{item}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">03 / Your 8-week learning roadmap</div><div class="muted">A progressive plan based on your target role and weekly study time.</div><br>', unsafe_allow_html=True)
    roadmap = data.get("roadmap", [])
    for week in roadmap:
        tasks = week.get("tasks", [])
        task_html = "".join(f"<li>{t}</li>" for t in tasks)
        st.markdown(f"""
        <div class="week">
          <div class="week-label">{week.get('week','WEEK')}</div>
          <h4>{week.get('focus','Learning focus')}</h4>
          <ul style="color:#a2adc5;font-size:.84rem;line-height:1.8">{task_html}</ul>
          <p><b style="color:#b8adff">Outcome:</b> {week.get('outcome','')}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">04 / BUILD YOUR PORTFOLIO</div><h3 style="font-family:Space Grotesk">Three projects to make your skills visible.</h3>', unsafe_allow_html=True)
    projects = data.get("projects", [])
    cols = st.columns(3)
    for i, project in enumerate(projects[:3]):
        with cols[i]:
            skills = ", ".join(project.get("skills", []))
            st.markdown(f"""
            <div class="project-card">
              <div class="eyebrow">PROJECT 0{i+1} · {project.get('level','PRACTICE')}</div>
              <br><b>{project.get('title','Portfolio project')}</b>
              <p class="muted">{project.get('description','')}</p>
              <hr><div class="muted"><b>Skills:</b> {skills}</div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("AI-generated guidance is a starting point, not a guarantee of employment. Verify role requirements and adapt the plan to your learning needs.")
    report_text = f"PATHPILOT AI — CAREER ROADMAP\nTarget role: {role}\nStudy hours/week: {hours}\n\nSUMMARY\n{data.get('summary','')}\n\nSKILLS YOU HAVE\n" + "\n".join(f"- {s}" for s in data.get("skills_have", [])) + "\n\nSKILLS TO LEARN\n" + "\n".join(f"- {x.get('skill')} ({x.get('priority')}): {x.get('why')}" if isinstance(x,dict) else f"- {x}" for x in data.get("skills_to_learn", [])) + "\n\n8-WEEK ROADMAP\n" + "\n".join(f"{w.get('week')}: {w.get('focus')}\n" + "\n".join(f"  - {t}" for t in w.get("tasks", [])) + f"\n  Outcome: {w.get('outcome')}" for w in data.get("roadmap", [])) + "\n\nPORTFOLIO PROJECTS\n" + "\n".join(f"- {p.get('title')}: {p.get('description')}" for p in projects)
    st.download_button("↓ Download my career roadmap (.txt)", report_text, file_name="PathPilot_Career_Roadmap.txt", mime="text/plain")

st.markdown('<footer>PATHPILOT.AI &nbsp; · &nbsp; CAREER INTELLIGENCE, BUILT AROUND YOU. <span style="float:right">GENERATIVE AI PROTOTYPE · 2026</span></footer>', unsafe_allow_html=True)
