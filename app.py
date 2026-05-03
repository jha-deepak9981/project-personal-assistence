import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    /* ── Main Page ── */
    .stApp { background-color: #F0F4F8 !important; }
    .stApp .stMarkdown p, .stApp p, .stApp h1, .stApp h2, .stApp h3 { color: #1A1A2E; }

    /* ── Hero Header ── */
    .hero {
        background: linear-gradient(135deg, #1565C0, #0288D1);
        padding: 28px 32px; border-radius: 16px; margin-bottom: 24px;
    }
    .hero h1 { color: #FFFFFF; margin: 0; font-size: 2rem; }
    .hero p  { color: #E3F2FD; margin: 6px 0 0; }

    /* ── Sidebar background ── */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #1A237E !important;
    }
    /* Sidebar all text */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #C5CAE9 !important;
    }
    /* Sidebar widget labels — the "persona / choose mode" fix */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextArea label {
        color: #E8EAF6 !important;
        font-weight: 600;
    }
    /* Sidebar selectbox selected value */
    [data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
        background-color: #283593 !important;
        border-color: #5C6BC0 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #E8EAF6 !important;
    }
    /* Sidebar text inputs and text areas */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background-color: #283593 !important;
        color: #E8EAF6 !important;
        border-color: #5C6BC0 !important;
    }
    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #9FA8DA !important;
    }

    /* ── Main content inputs ── */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1A1A2E !important;
        border: 1px solid #90CAF9 !important;
        border-radius: 8px !important;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1A1A2E !important;
        border: 1px solid #90CAF9 !important;
    }
    /* Main content labels */
    .main label { color: #1A237E !important; }

    /* ── Output Box ── */
    .output-box {
        background: #FFFFFF;
        border: 2px solid #90CAF9;
        border-radius: 12px;
        padding: 20px;
        margin-top: 16px;
        color: #1A237E;
        white-space: pre-wrap;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ── Tags ── */
    .tag {
        display: inline-block; background: #E3F2FD; color: #1565C0;
        padding: 3px 10px; border-radius: 20px; font-size: 0.8rem;
        margin: 2px; font-weight: bold;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab"] { color: #1565C0 !important; }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #1565C0 !important;
        color: #0D47A1 !important;
        font-weight: bold;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #1565C0 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover {
        background-color: #0D47A1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───
st.markdown("""
<div class="hero">
    <h1>🧠 Personal AI Assistant</h1>
    <p>Your intelligent assistant for daily tasks, planning, and more — powered by Gemini</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("### 🔑 API Key")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        st.success("API key loaded from environment.")
        api_key = env_key
    else:
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")

    st.markdown("---")
    st.markdown("### 👤 About You")
    user_name  = st.text_input("Your Name", placeholder="e.g. Priya")
    user_role  = st.selectbox("Persona — Choose Mode:", ["College Student", "Working Professional", "Researcher", "Entrepreneur", "Teacher"])
    user_goals = st.text_area("Your Goals (optional)", placeholder="e.g. Crack placements, learn AI, build projects...", height=80)

    st.markdown("---")
    st.markdown("### 📅 Context")
    today = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f"**Today:** {today}")

    st.markdown("---")
    if st.button("🗑️ Clear Outputs", use_container_width=True):
        for key in ["task_output","plan_output","email_output","review_output","idea_output"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def call_gemini(api_key, prompt, system="You are a helpful personal assistant."):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-pro-latest",
        system_instruction=system
    )
    response = model.generate_content(prompt)
    return response.text

def user_context():
    ctx = ""
    if user_name: ctx += f"User's name: {user_name}. "
    if user_role: ctx += f"They are a {user_role}. "
    if user_goals: ctx += f"Their goals: {user_goals}. "
    return ctx

SYSTEM = f"You are a smart, personal AI assistant. Today is {datetime.now().strftime('%A, %B %d, %Y')}. Be concise, practical, and friendly."

# ─── TABS ───
tab1, tab2, tab3, tab4, tab5 = st.tabs(["✅ Task Manager", "📅 Day Planner", "✉️ Email Writer", "📝 Content Review", "💡 Idea Generator"])

# ─── TAB 1: TASK MANAGER ───
with tab1:
    st.markdown("### ✅ Smart Task Manager")
    st.markdown("Paste your to-do list and I'll prioritize, estimate time, and suggest how to tackle them.")

    col1, col2 = st.columns([2, 1])
    with col1:
        tasks = st.text_area("Your tasks (one per line):", height=180,
            placeholder="Submit assignment\nPrepare for interview\nCall mom\nRead 20 pages\nGo to gym\nCheck emails")
    with col2:
        available_hours = st.slider("Hours available today:", 1, 16, 6)
        focus_area      = st.selectbox("Focus on:", ["Everything", "Academic", "Career", "Health", "Personal"])
        urgency_mode    = st.checkbox("Urgent mode — deadline today!")

    if st.button("🚀 Organize My Tasks", use_container_width=True, key="btn_tasks"):
        if not api_key: st.error("Add your API key in the sidebar."); st.stop()
        if not tasks:   st.warning("Please enter at least one task."); st.stop()
        with st.spinner("Organizing your tasks..."):
            prompt = f"""{user_context()}
Tasks to organize:
{tasks}

Available hours today: {available_hours}
Focus area: {focus_area}
Urgent mode: {urgency_mode}

Please:
1. Categorize and prioritize these tasks (High/Medium/Low)
2. Estimate time for each task
3. Build an optimized schedule that fits in {available_hours} hours
4. Give 3 productivity tips specific to this list
5. Identify any tasks that can be delegated or dropped

Format clearly with sections."""
            st.session_state.task_output = call_gemini(api_key, prompt, SYSTEM)

    if "task_output" in st.session_state:
        st.markdown(f'<div class="output-box">{st.session_state.task_output}</div>', unsafe_allow_html=True)

# ─── TAB 2: DAY PLANNER ───
with tab2:
    st.markdown("### 📅 AI Day Planner")
    st.markdown("Tell me about your day and I'll build you an optimal schedule.")

    col1, col2 = st.columns(2)
    with col1:
        wake_time  = st.time_input("Wake up time:", value=None)
        sleep_time = st.time_input("Sleep time:", value=None)
        fixed_commitments = st.text_area("Fixed commitments (with times):", height=100,
            placeholder="9am - College class\n2pm - Lab session\n6pm - Gym")
    with col2:
        goals_today = st.text_area("What do you want to achieve today?", height=100,
            placeholder="Study for exam, build project, send 3 applications...")
        energy_level = st.select_slider("Your energy level:", ["Low", "Medium", "High", "Very High"], value="Medium")
        include_breaks = st.checkbox("Include breaks & meals", value=True)

    if st.button("📅 Build My Day Plan", use_container_width=True, key="btn_plan"):
        if not api_key: st.error("Add your API key in the sidebar."); st.stop()
        with st.spinner("Building your optimal day..."):
            prompt = f"""{user_context()}
Wake: {wake_time}, Sleep: {sleep_time}
Fixed: {fixed_commitments}
Goals: {goals_today}
Energy level: {energy_level}
Include breaks: {include_breaks}

Create a detailed, hour-by-hour schedule for today. Align deep work with energy peaks. Include buffer time. End with 3 evening habits for tomorrow's success."""
            st.session_state.plan_output = call_gemini(api_key, prompt, SYSTEM)

    if "plan_output" in st.session_state:
        st.markdown(f'<div class="output-box">{st.session_state.plan_output}</div>', unsafe_allow_html=True)

# ─── TAB 3: EMAIL WRITER ───
with tab3:
    st.markdown("### ✉️ Professional Email Writer")

    col1, col2 = st.columns(2)
    with col1:
        email_purpose = st.selectbox("Email purpose:", [
            "Job Application", "Internship Request", "Follow-up After Interview",
            "Professor / Faculty Request", "Apology / Clarification",
            "Project Collaboration", "Networking Outreach", "Custom"
        ])
        recipient    = st.text_input("Recipient name & role:", placeholder="e.g. Dr. Sharma, HOD of CS Dept")
        email_tone   = st.selectbox("Tone:", ["Professional & Formal", "Friendly & Warm", "Concise & Direct", "Enthusiastic"])
    with col2:
        key_points   = st.text_area("Key points to include:", height=120,
            placeholder="- I'm a final year student\n- Applying for ML internship\n- Have Python & TensorFlow skills\n- Attach resume")
        email_length = st.radio("Length:", ["Short (3-4 lines)", "Medium (2-3 paras)", "Long (detailed)"], index=1)

    if st.button("✉️ Write My Email", use_container_width=True, key="btn_email"):
        if not api_key: st.error("Add your API key in the sidebar."); st.stop()
        with st.spinner("Drafting your email..."):
            prompt = f"""{user_context()}
Write a {email_length} email for: {email_purpose}
To: {recipient}
Tone: {email_tone}
Key points: {key_points}

Include:
1. A strong subject line
2. Professional greeting
3. Body with all key points woven naturally
4. Clear call-to-action
5. Professional sign-off

Make it stand out while being appropriate."""
            st.session_state.email_output = call_gemini(api_key, prompt, SYSTEM)

    if "email_output" in st.session_state:
        st.markdown(f'<div class="output-box">{st.session_state.email_output}</div>', unsafe_allow_html=True)
        if st.button("📋 Copy to clipboard (select text above)", use_container_width=True):
            st.info("Select the text above and press Ctrl+C to copy.")

# ─── TAB 4: CONTENT REVIEW ───
with tab4:
    st.markdown("### 📝 AI Content Reviewer")
    st.markdown("Paste any content — essays, cover letters, code, reports — and get detailed feedback.")

    content_type = st.selectbox("Content type:", [
        "College Essay", "Cover Letter / SOP", "Technical Report",
        "Research Abstract", "LinkedIn Profile / Bio", "Project README", "Other"
    ])
    content_text = st.text_area("Paste your content here:", height=220,
        placeholder="Paste your essay, letter, or document here...")

    review_focus = st.multiselect("Focus on:",
        ["Grammar & Clarity", "Structure & Flow", "Tone & Voice", "Completeness", "Originality", "Impact"],
        default=["Grammar & Clarity", "Structure & Flow"])

    if st.button("🔍 Review My Content", use_container_width=True, key="btn_review"):
        if not api_key:    st.error("Add your API key in the sidebar."); st.stop()
        if not content_text: st.warning("Please paste some content to review."); st.stop()
        with st.spinner("Reviewing your content..."):
            prompt = f"""Review this {content_type}. Focus on: {', '.join(review_focus)}.

Content:
{content_text}

Provide:
1. Overall Score (out of 10) with brief justification
2. Strengths (what works well)
3. Weaknesses (what needs improvement)
4. Specific suggestions with examples
5. Improved version of the weakest paragraph/section
6. One sentence summary of how to make it excellent"""
            st.session_state.review_output = call_gemini(api_key, prompt, SYSTEM)

    if "review_output" in st.session_state:
        st.markdown(f'<div class="output-box">{st.session_state.review_output}</div>', unsafe_allow_html=True)

# ─── TAB 5: IDEA GENERATOR ───
with tab5:
    st.markdown("### 💡 AI Idea Generator")
    st.markdown("Stuck on a project, assignment, or side hustle idea? Let AI brainstorm with you.")

    col1, col2 = st.columns(2)
    with col1:
        idea_domain = st.selectbox("Domain:", [
            "Final Year Project (Tech)", "Startup / Side Project",
            "Research Topic", "Hackathon Idea", "Content / YouTube",
            "NGO / Social Impact", "App / Product Idea"
        ])
        interests = st.text_input("Your interests / skills:", placeholder="e.g. Python, ML, healthcare, finance...")
    with col2:
        constraints  = st.text_input("Constraints:", placeholder="e.g. Solo project, 2 months, no budget")
        creativity   = st.select_slider("Creativity level:", ["Safe & Proven", "Balanced", "Creative", "Wild & Experimental"], value="Creative")

    if st.button("💡 Generate Ideas", use_container_width=True, key="btn_ideas"):
        if not api_key: st.error("Add your API key in the sidebar."); st.stop()
        with st.spinner("Brainstorming ideas for you..."):
            prompt = f"""{user_context()}
Generate 5 unique {idea_domain} ideas.
Interests/Skills: {interests}
Constraints: {constraints}
Creativity level: {creativity}

For each idea:
1. Name & one-line description
2. Problem it solves
3. How it works (brief tech stack or approach)
4. Why it's viable/impactful
5. First 3 steps to get started

Make ideas specific, feasible, and genuinely useful."""
            st.session_state.idea_output = call_gemini(api_key, prompt, SYSTEM)

    if "idea_output" in st.session_state:
        st.markdown(f'<div class="output-box">{st.session_state.idea_output}</div>', unsafe_allow_html=True)
