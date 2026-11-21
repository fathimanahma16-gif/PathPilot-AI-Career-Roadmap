
import json
import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: radial-gradient(ellipse at top left,#202b58,#0b1020 55%,#080d19);
    color:#eef2ff;
}
html,body,[class*="css"] {font-family:'DM Sans',sans-serif;}
.block-container {max-width:1300px;padding-top:2rem;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif;}
[data-testid="stSidebar"] {background:#0b1224;}
.hero {
    padding:35px;
    border-radius:22px;
    border:1px solid #35436c;
    background:linear-gradient(120deg,#26356a,#172344,#142e40);
    margin-bottom:25px;
}
.hero small {color:#a9bcff;letter-spacing:3px;font-weight:bold;}
.hero h1 {font-size:43px;color:white;margin:12px 0;}
.hero p {color:#c2cee8;font-size:17px;}
.card {
    background:#141f39;
    border:1px solid #344267;
    padding:22px;
    border-radius:18px;
    min-height:145px;
    margin-bottom:12px;
}
.card h3 {color:#aebdff;}
.card p {color:#b8c5df;}
.metric {
    background:#172442;
    border:1px solid #344267;
    padding:20px;
    border-radius:16px;
}
.metric strong {font-size:27px;color:white;}
.metric p {color:#aebbd7;}
div[data-testid="stForm"] {
    background:#131f39;
    border:1px solid #344267;
    padding:22px;
    border-radius:18px;
}
.stButton button,.stFormSubmitButton button {
    border-radius:12px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)


def get_api_key():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        return st.secrets.get("GEMINI_API_KEY", "").strip()
    except Exception:
        return ""


def clean_json(text):
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def create_roadmap(api_key, model, skills, role, hours):
    client = genai.Client(api_key=api_key)

    prompt = f"""
Create a beginner-friendly career roadmap.
Current skills: {skills}
Target role: {role}
Study hours per week: {hours}

Return only valid JSON:
{{
"career_overview":"Explanation",
"readiness_estimate":35,
"matched_skills":[{{"skill":"Python","level":"Basic","reason":"Relevant"}}],
"skills_to_learn":[{{"skill":"Machine Learning","priority":"High","reason":"Important"}}],
"roadmap":[
{{"week":1,"focus":"Topic","tasks":["Task 1","Task 2"],"deliverable":"Outcome"}}
],
"projects":[
{{"title":"Project","description":"Description","skills":["Python"],"difficulty":"Beginner"}}
],
"next_step":"Start learning today"
}}

Return exactly 8 roadmap weeks and 3 projects.
Do not invent existing skills.
Make the plan realistic for the available study hours.
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.45,
            max_output_tokens=6000
        )
    )
    return clean_json(response.text)


# SIDEBAR
with st.sidebar:
    st.markdown("## 🚀 CareerPath AI")
    st.caption("Your personal AI career planner")
    st.divider()

    st.markdown("### ⚙️ AI Settings")
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        help="Your key is not displayed."
    )

    model = st.text_input(
        "Gemini Model",
        value=os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    )

    st.divider()
    st.markdown("### 📌 About")
    st.caption("AI-powered personalized career planning.")
    st.caption("Python • Streamlit • Gemini • Pandas")


# HEADER
st.markdown("""
<div class="hero">
<small>YOUR FUTURE STARTS HERE</small>
<h1>Build your next move. 🚀</h1>
<p>Discover your strengths, identify skill gaps and create
a personalized learning roadmap powered by Generative AI.</p>
</div>
""", unsafe_allow_html=True)


# DASHBOARD METRICS
a, b, c = st.columns(3)

for col, number, label in [
    (a, "01", "Personalized Career Planning"),
    (b, "08", "Weeks of Structured Learning"),
    (c, "03", "Portfolio Project Ideas")
]:
    with col:
        st.markdown(
            f'<div class="metric"><strong>{number}</strong><p>{label}</p></div>',
            unsafe_allow_html=True
        )

st.write("")

# MAIN INPUT
left, right = st.columns([1.3, 0.7], gap="large")

with left:
    st.markdown("## 🎯 Create Your Career Plan")

    with st.form("career_form"):
        skills_text = st.text_area(
            "Your current skills",
            value="Python basics, C++, HTML, CSS, JavaScript",
            height=100
        )

        role = st.text_input(
            "Target career role",
            value="AI / Machine Learning Engineer"
        )

        hours = st.slider(
            "Weekly study hours",
            min_value=2,
            max_value=30,
            value=30
        )

        submitted = st.form_submit_button(
            "✨ Generate My AI Roadmap",
            type="primary",
            width="stretch"
        )

with right:
    st.markdown("## ✦ How it works")

    st.markdown("""
    <div class="card">
    <h3>01 · Discover</h3>
    <p>Understand your current skills and career interests.</p>
    </div>
    <div class="card">
    <h3>02 · Analyze</h3>
    <p>Identify missing skills and learning priorities.</p>
    </div>
    <div class="card">
    <h3>03 · Plan</h3>
    <p>Generate a personalized 8-week learning journey.</p>
    </div>
    <div class="card">
    <h3>04 · Build</h3>
    <p>Get practical portfolio project recommendations.</p>
    </div>
    """, unsafe_allow_html=True)


# GENERATE
if submitted:
    skills = [s.strip() for s in skills_text.split(",") if s.strip()]
    key = api_key_input.strip() or get_api_key()

    if not skills:
        st.error("Enter at least one skill.")
    elif not role.strip():
        st.error("Enter your target role.")
    elif not key:
        st.error("Please enter your Gemini API key in the sidebar.")
    else:
        try:
            with st.spinner("AI is preparing your career roadmap..."):
                result = create_roadmap(
                    key, model.strip(),
                    ", ".join(skills),
                    role.strip(), hours
                )

            if len(result.get("roadmap", [])) != 8:
                raise ValueError("The AI response must contain 8 roadmap weeks.")
            if len(result.get("projects", [])) != 3:
                raise ValueError("The AI response must contain 3 projects.")

            st.session_state["career_result"] = result
            st.session_state["career_role"] = role
            st.success("Your career roadmap is ready!")

        except Exception as exc:
            st.error(f"Roadmap generation failed: {exc}")
            st.info(
                "Your dashboard is still available. "
                "Check Gemini model availability and API access."
            )


# RESULTS
if "career_result" in st.session_state:
    data = st.session_state["career_result"]

    st.divider()
    st.markdown(f"# ✨ Your Career Roadmap")
    st.markdown(f"### Target: {st.session_state['career_role']}")
    st.write(data.get("career_overview", ""))

    x, y, z = st.columns(3)

    with x:
        st.metric(
            "Learning Readiness",
            f"{data.get('readiness_estimate', 0)}%"
        )
    with y:
        st.metric("Learning Duration", "8 Weeks")
    with z:
        st.metric("Portfolio Projects", len(data.get("projects", [])))

    tab1, tab2, tab3 = st.tabs([
        "🧩 Skill Gap Analysis",
        "🗓️ Learning Roadmap",
        "💡 Projects"
    ])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Your existing skills")
            st.dataframe(
                pd.DataFrame(data.get("matched_skills", [])),
                hide_index=True,
                width="stretch"
            )
        with col2:
            st.markdown("### Skills to develop")
            st.dataframe(
                pd.DataFrame(data.get("skills_to_learn", [])),
                hide_index=True,
                width="stretch"
            )

    with tab2:
        for week in data.get("roadmap", []):
            with st.expander(
                f"Week {week.get('week')}: {week.get('focus')}",
                expanded=True
            ):
                for task in week.get("tasks", []):
                    st.write("✓", task)
                st.success(
                    f"Deliverable: {week.get('deliverable')}"
                )

    with tab3:
        cols = st.columns(3)
        for i, project in enumerate(data.get("projects", [])):
            with cols[i % 3]:
                st.markdown(f"### {project.get('title')}")
                st.write(project.get("description"))
                st.caption(
                    "Skills: " + ", ".join(project.get("skills", []))
                )
                st.caption(
                    "Difficulty: " + project.get("difficulty", "")
                )

    st.markdown("### 🚀 Your next step")
    st.info(data.get("next_step", ""))

    st.download_button(
        "⬇️ Download Career Roadmap",
        data=json.dumps(data, indent=2),
        file_name="careerpath_roadmap.json",
        mime="application/json"
    )


st.divider()
st.caption(
    "CareerPath AI | Powered by Generative AI | "
    "Educational planning tool"
)
