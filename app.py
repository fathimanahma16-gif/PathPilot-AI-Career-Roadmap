import streamlit as st
from google import genai

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="PathPilot AI | Career Companion",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 5% 5%, rgba(91, 31, 150, .26), transparent 32%),
            radial-gradient(circle at 95% 8%, rgba(0, 117, 130, .22), transparent 30%),
            #080910;
        color: #f5f6ff;
    }
    [data-testid="stSidebar"] {
        background: #0d0d19;
        border-right: 1px solid rgba(255,255,255,.12);
    }
    [data-testid="stSidebar"] * { color: #f2f2fa; }
    .brand-title { font-size: 1.45rem; font-weight: 800; margin-bottom: .2rem; }
    .brand-sub { color: #a3a3b7; font-size: .82rem; letter-spacing: .04em; }
    .hero {
        padding: 30px 34px;
        border-radius: 22px;
        border: 1px solid rgba(150,150,255,.18);
        background: linear-gradient(120deg, rgba(83,24,130,.34), rgba(0,95,112,.27));
        margin-bottom: 25px;
    }
    .hero h1 { margin: 8px 0 12px 0; font-size: 2.1rem; }
    .hero p { color: #c3c6dc; font-size: 1rem; margin-bottom: 0; }
    .hero-kicker { letter-spacing: .22em; text-transform: uppercase; color: #aab5ff; font-size: .75rem; font-weight: 700; }
    .feature-card {
        background: rgba(20,22,40,.9);
        border: 1px solid rgba(140,140,190,.2);
        border-radius: 18px;
        padding: 22px 23px;
        min-height: 170px;
        margin-bottom: 12px;
    }
    .feature-icon { font-size: 1.9rem; margin-bottom: 8px; }
    .feature-card h3 { font-size: 1.15rem; margin: 5px 0 10px 0; }
    .feature-card p { color: #aeb2ce; line-height: 1.55; font-size: .92rem; }
    .section-title { font-size: 1.75rem; font-weight: 750; margin: 12px 0 8px; }
    .section-sub { color: #b9bbd0; margin-bottom: 18px; }
    .panel {
        border: 1px solid rgba(150,150,190,.23);
        background: rgba(15,16,28,.72);
        border-radius: 16px;
        padding: 20px;
    }
    .mini-card {
        border: 1px solid rgba(130,140,190,.2);
        background: #14182c;
        border-radius: 15px;
        padding: 20px;
        min-height: 115px;
    }
    .mini-number { font-size: 1.6rem; font-weight: 800; }
    .mini-label { color: #b6bddb; margin-top: 4px; }
    div.stButton > button[kind="primary"] {
        border: 0;
        border-radius: 12px;
        background: linear-gradient(90deg,#9633e8,#315ef2);
        color: white;
        font-weight: 700;
        padding: .72rem 1rem;
    }
    div.stButton > button[kind="primary"]:hover { border: 0; filter: brightness(1.12); }
    div.stButton > button { border-radius: 10px; }
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div,
    div[data-testid="stTextArea"] textarea {
        border-radius: 10px;
    }
    hr { border-color: rgba(255,255,255,.14); }
    .small-muted { color: #8f92aa; font-size: .83rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
defaults = {
    "career_plan": "",
    "skill_analysis": "",
    "learning_roadmap": "",
    "portfolio_projects": "",
    "profile": {},
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown('<div class="brand-title">🚀 PathPilot AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">YOUR PERSONAL AI CAREER COMPANION</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Career Planner", "Skill Gap Analysis", "Learning Roadmap", "Portfolio Projects"],
        index=0,
        label_visibility="visible",
    )

    st.markdown("---")
    st.subheader("⚙️ AI Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Paste your Gemini API key here. It is used for this session only.",
    )
    model = st.selectbox(
        "Gemini Model",
        ["gemini-2.5-flash", "gemini-2.0-flash"],
        index=0,
        help="If a model is unavailable for your API key, try the other option.",
    )
    st.markdown("---")
    st.subheader("📌 About PathPilot")
    st.write("An AI-powered career guidance platform that helps students discover their potential, identify skill gaps and plan their future.")
    st.markdown("---")
    st.markdown('<div class="small-muted">Powered by Google Gemini AI · Streamlit</div>', unsafe_allow_html=True)

# Prefer a configured secret if the user has set it in Streamlit secrets.
try:
    secret_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    secret_key = ""
effective_key = api_key.strip() or secret_key

# -------------------- AI HELPER --------------------
def ask_gemini(prompt: str) -> str:
    if not effective_key:
        raise ValueError("Please enter your Gemini API key in the sidebar AI Settings.")
    client = genai.Client(api_key=effective_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    answer = getattr(response, "text", None)
    if not answer:
        return "The AI returned an empty response. Please try again."
    return answer

def show_result(title: str, content: str):
    st.markdown(f"### {title}")
    st.markdown(content)

# -------------------- CAREER PLANNER --------------------
if page == "Career Planner":
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Your personal career companion</div>
        <h1>🚀 Your Career Journey Starts Here</h1>
        <p>Discover your strengths, identify skill gaps and create a personalized learning roadmap powered by AI.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><div class="feature-icon">🎯</div><h3>Skill Gap Analysis</h3><p>Identify the skills you need to achieve your dream career.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🗓️</div><h3>Learning Roadmap</h3><p>Follow a structured learning plan designed around your goals.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><div class="feature-icon">💡</div><h3>Portfolio Projects</h3><p>Build practical projects that demonstrate your technical abilities.</p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-title">🎓 Build Your Career Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Tell us about yourself. PathPilot AI will create a personalised career development plan.</div>', unsafe_allow_html=True)

    with st.form("career_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            education = st.selectbox(
                "Education Level",
                ["High School Student", "First Year Bachelor's Student", "Second Year Bachelor's Student",
                 "Third Year Bachelor's Student", "Final Year Bachelor's Student", "Graduate", "Other"],
                index=1,
            )
            career = st.selectbox(
                "Target Career",
                ["Artificial Intelligence Engineer", "Data Scientist", "Software Developer",
                 "Web Developer", "Cybersecurity Analyst", "Cloud Engineer", "UI/UX Designer",
                 "Mobile App Developer", "Other"],
            )
        with col2:
            experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            daily_time = st.selectbox("Daily Learning Time", ["30 minutes", "1 hour", "2 hours", "3 hours", "4+ hours"])
            duration = st.selectbox("Roadmap Duration", ["4 weeks", "8 weeks", "12 weeks", "3 months", "6 months"])
        skills = st.text_area("Your Current Skills", placeholder="Example: Python, HTML, CSS, C++, Mathematics...", height=110)
        interests = st.text_area("Your Interests", placeholder="Example: Robotics, neural networks, automation, computer vision...", height=100)
        submitted = st.form_submit_button("🚀 Generate My Career Roadmap", type="primary", use_container_width=True)

    if submitted:
        profile = {
            "name": name or "Student",
            "education": education,
            "career": career,
            "experience": experience,
            "daily_time": daily_time,
            "duration": duration,
            "skills": skills or "Not specified",
            "interests": interests or "Not specified",
        }
        st.session_state.profile = profile
        prompt = f"""
You are PathPilot AI, a supportive career mentor. Create a practical, personalized career roadmap.
Use Markdown headings, tables where useful, checklists, and clear explanations. Avoid vague advice.

Student profile:
Name: {profile['name']}
Education: {profile['education']}
Target career: {profile['career']}
Experience level: {profile['experience']}
Available study time: {profile['daily_time']} per day
Plan duration: {profile['duration']}
Current skills: {profile['skills']}
Interests: {profile['interests']}

Include these sections:
1. Career overview and why this career fits the stated interests (do not make unsupported assumptions)
2. Current strengths based on their listed skills
3. Skill gap analysis: skill, why it matters, priority (High/Medium/Low), and beginner-friendly next step
4. Personalized week-by-week learning roadmap for the chosen duration. Each week must have goals, topics, activities, and a small deliverable.
5. Three portfolio project ideas with purpose, features, tools, and what the project demonstrates
6. Recommended learning resources (give resource names and official website URLs only when confident they exist)
7. A realistic weekly routine that fits their daily time
8. Next steps and encouragement

Make the roadmap appropriate for the student's education and experience level. Be realistic and clear.
"""
        with st.spinner("PathPilot AI is creating your personalized career roadmap..."):
            try:
                st.session_state.career_plan = ask_gemini(prompt)
                st.session_state.skill_analysis = ""
                st.session_state.learning_roadmap = ""
                st.session_state.portfolio_projects = ""
                st.success("Your personalized roadmap is ready!")
            except Exception as e:
                st.error(f"Could not generate the roadmap: {e}")

    if st.session_state.career_plan:
        show_result("✨ Your Personalized Career Roadmap", st.session_state.career_plan)

# -------------------- SKILL GAP ANALYSIS --------------------
elif page == "Skill Gap Analysis":
    st.markdown('<div class="section-title">🎯 Skill Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Compare your current skills with the skills required for your target career.</div>', unsafe_allow_html=True)
    profile = st.session_state.profile
    default_career = profile.get("career", "Artificial Intelligence Engineer")
    default_skills = profile.get("skills", "")
    with st.form("skill_form"):
        target = st.text_input("Target career", value=default_career)
        current = st.text_area("Your current skills", value=default_skills, placeholder="List your skills, courses, or experience...", height=130)
        interests = st.text_area("Your interests (optional)", value=profile.get("interests", ""), height=90)
        go = st.form_submit_button("🔍 Analyze My Skill Gaps", type="primary", use_container_width=True)
    if go:
        prompt = f"""Act as a career skills mentor. Analyze the skill gaps for the target role: {target}.
Current skills: {current or 'Not provided'}
Interests: {interests or 'Not provided'}
Give:
- A short role skills overview
- Skills the student already has that are relevant
- A table with missing/next skills, importance, current level (estimate only from their information; mark unknown if unclear), and a concrete next action
- Prioritize the gaps in beginner-friendly order
- A 2-week starter plan
- A short self-assessment checklist
Be encouraging, practical, and don't claim the student has skills they didn't list."""
        with st.spinner("Analyzing your skills..."):
            try:
                st.session_state.skill_analysis = ask_gemini(prompt)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    if st.session_state.skill_analysis:
        show_result("Your Skill Gap Report", st.session_state.skill_analysis)

# -------------------- LEARNING ROADMAP --------------------
elif page == "Learning Roadmap":
    st.markdown('<div class="section-title">🗓️ Learning Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Create a structured learning schedule with weekly milestones.</div>', unsafe_allow_html=True)
    profile = st.session_state.profile
    with st.form("learning_form"):
        target = st.text_input("Career goal", value=profile.get("career", ""))
        duration = st.selectbox("Duration", ["4 weeks", "8 weeks", "12 weeks", "3 months", "6 months"])
        time = st.selectbox("Study time per day", ["30 minutes", "1 hour", "2 hours", "3 hours", "4+ hours"], index=1)
        skills = st.text_area("Starting skills", value=profile.get("skills", ""), height=100)
        goal = st.text_area("Specific learning goal (optional)", placeholder="What do you want to be able to do by the end?", height=80)
        go = st.form_submit_button("📅 Create My Learning Roadmap", type="primary", use_container_width=True)
    if go:
        prompt = f"""Build a realistic {duration} learning roadmap for a learner aiming for {target}.
Daily study time: {time}. Starting skills: {skills or 'Not provided'}. Goal: {goal or 'Build foundations and progress toward the career'}.
Provide a week-by-week table with learning objectives, topics, practice tasks, a small weekly output, and a checkpoint. Add a simple routine for each study session, review days, and free/official learning resources if known. Keep it actionable and beginner friendly."""
        with st.spinner("Building your learning roadmap..."):
            try:
                st.session_state.learning_roadmap = ask_gemini(prompt)
            except Exception as e:
                st.error(f"Could not create the roadmap: {e}")
    if st.session_state.learning_roadmap:
        show_result("Your Learning Plan", st.session_state.learning_roadmap)
    elif st.session_state.career_plan:
        st.info("Your career plan has been generated. You can also create a more focused learning schedule above.")

# -------------------- PORTFOLIO PROJECTS --------------------
elif page == "Portfolio Projects":
    st.markdown('<div class="section-title">💡 Portfolio Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Generate project ideas that help you demonstrate your skills and build a portfolio.</div>', unsafe_allow_html=True)
    profile = st.session_state.profile
    with st.form("portfolio_form"):
        target = st.text_input("Target career", value=profile.get("career", ""))
        skills = st.text_area("Skills/tools you know", value=profile.get("skills", ""), height=100)
        level = st.selectbox("Project difficulty", ["Beginner", "Beginner to Intermediate", "Intermediate", "Advanced"])
        number = st.selectbox("Number of ideas", [3, 5, 8], index=0)
        interests = st.text_area("Topics you enjoy (optional)", value=profile.get("interests", ""), height=80)
        go = st.form_submit_button("💡 Generate Portfolio Projects", type="primary", use_container_width=True)
    if go:
        prompt = f"""Suggest {number} portfolio projects for a student aiming for {target}.
Their skills/tools: {skills or 'Beginner; not specified'}.
Difficulty: {level}. Interests: {interests or 'Not specified'}.
For every project provide title, problem it solves, purpose, features, tools/technologies, build steps, and what skills it demonstrates. Make the projects distinct, feasible, and progressively challenging. Include one project that can be completed as a small first project. Give ideas for README contents and a demo presentation. Do not require paid services."""
        with st.spinner("Creating project ideas..."):
            try:
                st.session_state.portfolio_projects = ask_gemini(prompt)
            except Exception as e:
                st.error(f"Could not generate projects: {e}")
    if st.session_state.portfolio_projects:
        show_result("Your Portfolio Project Ideas", st.session_state.portfolio_projects)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown('<p class="small-muted">🚀 PathPilot AI · Plan your learning, build your skills, and take your next step.</p>', unsafe_allow_html=True)
