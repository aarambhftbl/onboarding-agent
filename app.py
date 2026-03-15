"""
AI-Powered Autonomous Developer Onboarding Agent
Main Streamlit Application
"""

import time
import streamlit as st

from onboarding_agent import (
    load_knowledge_base,
    get_ai_response,
    generate_onboarding_path,
    generate_onboarding_summary,
)
from checklist_manager import (
    calculate_progress,
    get_progress_label,
    get_progress_color,
    get_next_task,
)
from notification_service import send_hr_notification

# ───────────────────────────────────────────────────────
# Page Config & Global CSS
# ───────────────────────────────────────────────────────

st.set_page_config(
    page_title="DevOnboard AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── Dark background ── */
  .stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #0d1b2a 50%, #0a1628 100%);
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #121929 100%);
    border-right: 1px solid rgba(99, 179, 237, 0.15);
  }

  /* ── Hero banner ── */
  .hero-banner {
    background: linear-gradient(135deg, #1a1f3c 0%, #0d2137 50%, #0f1e35 100%);
    border: 1px solid rgba(99, 179, 237, 0.2);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #63b3ed, #7c3aed, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
  }
  .hero-subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 400;
  }

  /* ── Section cards ── */
  .card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
  }
  .card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #63b3ed;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* ── Chat bubbles ── */
  .chat-user {
    background: linear-gradient(135deg, #1e3a5f, #1a305a);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    margin: 0.75rem 0;
    color: #e2e8f0;
    font-size: 0.95rem;
    max-width: 85%;
    margin-left: auto;
    line-height: 1.55;
  }
  .chat-ai {
    background: linear-gradient(135deg, #1a1f3c, #151d38);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 4px 16px 16px 16px;
    padding: 0.9rem 1.2rem;
    margin: 0.75rem 0;
    color: #e2e8f0;
    font-size: 0.95rem;
    max-width: 90%;
    line-height: 1.55;
  }
  .chat-label-user {
    font-size: 0.72rem;
    color: #63b3ed;
    font-weight: 600;
    text-align: right;
    margin-bottom: 0.25rem;
    letter-spacing: 0.05em;
  }
  .chat-label-ai {
    font-size: 0.72rem;
    color: #a78bfa;
    font-weight: 600;
    margin-bottom: 0.25rem;
    letter-spacing: 0.05em;
  }

  /* ── Progress bar ── */
  .progress-container {
    background: rgba(255,255,255,0.06);
    border-radius: 50px;
    height: 12px;
    width: 100%;
    margin: 0.5rem 0 1rem 0;
    overflow: hidden;
  }

  /* ── Task item ── */
  .task-done {
    color: #86efac;
    text-decoration: line-through;
    opacity: 0.65;
    font-size: 0.92rem;
  }
  .task-pending {
    color: #e2e8f0;
    font-size: 0.92rem;
  }

  /* ── Stat card ── */
  .stat-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
  }
  .stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
  }
  .stat-label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 0.4rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  /* ── Success banner ── */
  .success-banner {
    background: linear-gradient(135deg, #052e16, #064e3b);
    border: 1px solid #22c55e;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
  }

  /* ── Demo pill ── */
  .demo-pill {
    background: linear-gradient(90deg, #7c3aed, #6d28d9);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.5rem;
  }

  /* ── Streamlit overrides ── */
  .stTextInput > div > div > input,
  .stSelectbox > div > div > div,
  .stMultiSelect > div > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
  }
  div[data-testid="stMarkdownContainer"] h3 {
    color: #63b3ed !important;
  }
  .stCheckbox > label {
    color: #e2e8f0 !important;
  }
  label {
    color: #94a3b8 !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
  }
  div[data-testid="stExpander"] {
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.03) !important;
  }
  .stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-weight: 500 !important;
  }
  .stTabs [aria-selected="true"] {
    color: #63b3ed !important;
    border-bottom-color: #63b3ed !important;
  }
  .stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(99,179,237,0.15) !important;
    gap: 0.5rem !important;
  }
  .element-container:has(> .stAlert) {
    margin-bottom: 0.5rem;
  }
  /* Hide default Streamlit decoration */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────
# Session State Initialization
# ───────────────────────────────────────────────────────

def init_session():
    defaults = {
        "profile": None,
        "onboarding_started": False,
        "tasks": [],
        "completed_tasks": [],
        "chat_history": [],
        "hr_notified": False,
        "kb": load_knowledge_base(),
        "demo_running": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ───────────────────────────────────────────────────────
# Sidebar — Developer Profile Form
# ───────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
      <div style="font-size:2.5rem;">🤖</div>
      <div style="font-weight:800; font-size:1.2rem; color:#63b3ed;">DevOnboard AI</div>
      <div style="font-size:0.75rem; color:#64748b; margin-top:0.25rem;">Autonomous Onboarding Agent</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-title">👤 Developer Profile</div>', unsafe_allow_html=True)

    with st.form("profile_form"):
        name = st.text_input("Full Name", placeholder="e.g. Akshay Sharma")
        role = st.selectbox("Role", ["Backend", "Frontend", "DevOps"])
        level = st.selectbox("Experience Level", ["Intern", "Junior", "Senior"])
        tech_options = {
            "Backend": ["Python", "Java", "Go", "Node.js", "SQL", "Docker"],
            "Frontend": ["React", "TypeScript", "Vue.js", "CSS", "GraphQL", "Figma"],
            "DevOps": ["Kubernetes", "Terraform", "Docker", "AWS", "CI/CD", "Helm"],
        }
        tech_stack = st.multiselect(
            "Tech Stack",
            options=tech_options[role],
            default=tech_options[role][:2],
        )
        submitted = st.form_submit_button("🚀 Start Onboarding", use_container_width=True)

        if submitted and name.strip():
            profile = {
                "name": name.strip(),
                "role": role,
                "level": level,
                "tech_stack": tech_stack,
            }
            tasks = generate_onboarding_path(profile)
            st.session_state["profile"] = profile
            st.session_state["tasks"] = tasks
            st.session_state["completed_tasks"] = [False] * len(tasks)
            st.session_state["onboarding_started"] = True
            st.session_state["hr_notified"] = False
            st.session_state["chat_history"] = [
                {
                    "role": "ai",
                    "content": (
                        f"👋 Welcome aboard, **{name}**! I'm your AI Onboarding Assistant.\n\n"
                        f"I've generated your personalized **{level} {role}** onboarding path with **{len(tasks)} tasks**.\n\n"
                        "Explore the tabs above to see your tasks, ask me questions anytime, and "
                        "track your journey to becoming sprint-ready! 🚀"
                    ),
                }
            ]
            st.rerun()
        elif submitted:
            st.error("Please enter your name.")

    # Progress summary in sidebar
    if st.session_state["onboarding_started"]:
        stats = calculate_progress(st.session_state["completed_tasks"])
        pct = stats["percentage"]
        color = get_progress_color(pct)

        st.markdown("---")
        st.markdown(f'<div class="card-title">📊 Quick Stats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:0.5rem;">
          <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#94a3b8; margin-bottom:0.3rem;">
            <span>Progress</span><span style="color:{color}; font-weight:700;">{pct}%</span>
          </div>
          <div class="progress-container">
            <div style="height:100%; width:{pct}%; background:linear-gradient(90deg, {color}, {color}cc);
                        border-radius:50px; transition:width 0.5s ease;"></div>
          </div>
          <div style="font-size:0.8rem; color:#64748b; text-align:center;">{get_progress_label(pct)}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
              <div class="stat-number" style="color:#22c55e;">{stats['completed']}</div>
              <div class="stat-label">Done</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
              <div class="stat-number" style="color:#f97316;">{stats['remaining']}</div>
              <div class="stat-label">Left</div>
            </div>""", unsafe_allow_html=True)

        # Readiness score
        readiness = min(100, pct + (5 if len(st.session_state["profile"].get("tech_stack", [])) >= 2 else 0))
        score_color = "#22c55e" if readiness >= 80 else "#f97316" if readiness >= 40 else "#ef4444"
        st.markdown(f"""
        <div style="margin-top:1rem; text-align:center;">
          <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:0.06em;">Readiness Score</div>
          <div style="font-size:2.8rem; font-weight:900; color:{score_color}; line-height:1.1;">{readiness}</div>
          <div style="font-size:0.72rem; color:#64748b;">/100</div>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────
# Main Content
# ───────────────────────────────────────────────────────

# Hero Banner
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">🤖 Autonomous Developer Onboarding Agent</div>
  <div class="hero-subtitle">
    AI-powered personalized onboarding · Knowledge retrieval · Smart task tracking · HR automation
  </div>
</div>
""", unsafe_allow_html=True)


# ── Demo Mode Button ──
col_demo, col_space = st.columns([1, 3])
with col_demo:
    if st.button("⚡ Start Demo Walkthrough", use_container_width=True):
        st.session_state["demo_running"] = True
        # Set up demo profile
        demo_profile = {
            "name": "Akshay Sharma",
            "role": "Backend",
            "level": "Intern",
            "tech_stack": ["Python", "Docker"],
        }
        demo_tasks = generate_onboarding_path(demo_profile)
        st.session_state["profile"] = demo_profile
        st.session_state["tasks"] = demo_tasks
        st.session_state["completed_tasks"] = [False] * len(demo_tasks)
        st.session_state["hr_notified"] = False
        st.session_state["onboarding_started"] = True
        st.session_state["chat_history"] = [
            {
                "role": "ai",
                "content": (
                    "🎬 **Demo Mode Active!**\n\n"
                    "Welcome, **Akshay Sharma**! I'm your AI Onboarding Assistant.\n\n"
                    "I've generated a personalized **Backend Intern** onboarding path. "
                    "Watch as the system automatically guides you through setup, documentation, and tasks! 🚀"
                ),
            }
        ]
        st.rerun()


# ── Guard: show landing if no profile ──
if not st.session_state["onboarding_started"]:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color:#64748b;">
      <div style="font-size:4rem; margin-bottom:1rem;">👈</div>
      <div style="font-size:1.3rem; font-weight:600; color:#94a3b8; margin-bottom:0.5rem;">
        Fill in your profile to begin
      </div>
      <div style="font-size:0.95rem;">
        Enter your name, role, and tech stack in the sidebar, then click <strong style="color:#63b3ed">Start Onboarding</strong>.
      </div>
      <div style="margin-top:1.5rem; font-size:0.85rem; color:#475569;">
        Or click <strong style="color:#a78bfa">⚡ Start Demo Walkthrough</strong> above to see it in action!
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ───────────────────────────────────────────────────────
# Profile is active — show tabs
# ───────────────────────────────────────────────────────

profile = st.session_state["profile"]
tasks = st.session_state["tasks"]
completed_tasks = st.session_state["completed_tasks"]
stats = calculate_progress(completed_tasks)

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 AI Assistant",
    "✅ Onboarding Tasks",
    "📊 Dashboard",
    "📄 Report",
])


# ══════════════════════════════════════════════
# TAB 1 — AI CHAT ASSISTANT
# ══════════════════════════════════════════════

with tab1:
    st.markdown(f"""
    <div class="card" style="margin-bottom:1rem;">
      <div style="display:flex; align-items:center; gap:0.8rem;">
        <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#7c3aed);
                    display:flex;align-items:center;justify-content:center;font-size:1.3rem;">🤖</div>
        <div>
          <div style="font-weight:700;color:#e2e8f0;font-size:1rem;">DevOnboard Assistant</div>
          <div style="font-size:0.78rem;color:#22c55e;">● Online · Ready to help {profile['name']}</div>
        </div>
        <div style="margin-left:auto;font-size:0.8rem;color:#64748b;">
          {profile['level']} {profile['role']} · {', '.join(profile.get('tech_stack', [])[:2])}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-label-user">YOU</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-label-ai">🤖 AI ASSISTANT</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-ai">', unsafe_allow_html=True)
                st.markdown(msg["content"])
                st.markdown('</div>', unsafe_allow_html=True)

    # Suggested quick questions
    st.markdown('<div style="font-size:0.78rem;color:#64748b;margin-top:0.75rem;margin-bottom:0.4rem;">💡 Suggested questions</div>', unsafe_allow_html=True)
    quick_cols = st.columns(3)
    suggestions = [
        "How do I set up my environment?",
        "What is the system architecture?",
        "Where can I find coding standards?",
        "How do I run the backend service?",
        "What are the security policies?",
        "How do I clone the repository?",
    ]
    for i, suggestion in enumerate(suggestions):
        with quick_cols[i % 3]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state["chat_history"].append({"role": "user", "content": suggestion})
                response = get_ai_response(suggestion, profile, st.session_state["kb"])
                st.session_state["chat_history"].append({"role": "ai", "content": response})
                st.rerun()

    # Chat input
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Ask anything...",
                placeholder="e.g. How do I run tests? What is our CI/CD pipeline?",
                label_visibility="collapsed",
            )
        with col_send:
            send_btn = st.form_submit_button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("Thinking..."):
            time.sleep(0.3)
            response = get_ai_response(user_input.strip(), profile, st.session_state["kb"])
        st.session_state["chat_history"].append({"role": "ai", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state["chat_history"] = []
        st.rerun()


# ══════════════════════════════════════════════
# TAB 2 — ONBOARDING CHECKLIST
# ══════════════════════════════════════════════

with tab2:
    pct = stats["percentage"]
    color = get_progress_color(pct)

    # Big progress bar + label
    st.markdown(f"""
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
        <div style="font-size:1rem; font-weight:600; color:#e2e8f0;">{get_progress_label(pct)}</div>
        <div style="font-size:1.8rem; font-weight:900; color:{color};">{pct}%</div>
      </div>
      <div class="progress-container" style="height:18px;">
        <div style="height:100%; width:{pct}%;
                    background:linear-gradient(90deg, {color}, {color}99);
                    border-radius:50px; transition:width 0.6s ease;"></div>
      </div>
      <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
        <span style="font-size:0.78rem; color:#64748b;">{stats['completed']} of {stats['total']} tasks complete</span>
        <span style="font-size:0.78rem; color:#64748b;">{stats['remaining']} remaining</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Completion success or next task
    if stats["is_complete"]:
        st.markdown("""
        <div class="success-banner">
          <div style="font-size:2rem;">🎉</div>
          <div style="font-size:1.2rem; font-weight:700; color:#22c55e; margin-top:0.5rem;">
            Onboarding Complete!</div>
          <div style="color:#86efac; font-size:0.9rem; margin-top:0.25rem;">
            You're fully onboarded and sprint-ready. Great work!</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state["hr_notified"]:
            if st.button("📧 Send HR Notification", use_container_width=True):
                msg = send_hr_notification(profile, stats)
                st.session_state["hr_notified"] = True
                st.session_state["chat_history"].append({
                    "role": "ai",
                    "content": f"🎉 **Onboarding complete!**\n\n✉️ HR has been notified:\n> *{msg}*\n\nWelcome to the team! You're sprint-ready. 🚀",
                })
                st.success(f"✅ {msg}")
                st.rerun()
        else:
            st.success("✅ HR has been notified. You're sprint-ready!")
    else:
        next_task = get_next_task(tasks, completed_tasks)
        if next_task:
            st.info(f"⬇️ **Next up**: {next_task}")

    # Task list
    st.markdown(f"""
    <div class="card-title" style="margin-top:1rem;">
      📋 {profile['level']} {profile['role']} Onboarding Path
    </div>
    """, unsafe_allow_html=True)

    updated = False
    for i, task in enumerate(tasks):
        col_check, col_task = st.columns([0.08, 0.92])
        with col_check:
            checked = st.checkbox("", value=completed_tasks[i], key=f"task_{i}", label_visibility="collapsed")
        with col_task:
            if completed_tasks[i]:
                st.markdown(f'<div class="task-done">~~{task}~~ ✓</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="task-pending">{task}</div>', unsafe_allow_html=True)
        if checked != completed_tasks[i]:
            st.session_state["completed_tasks"][i] = checked
            updated = True

    if updated:
        new_stats = calculate_progress(st.session_state["completed_tasks"])
        if new_stats["is_complete"] and not st.session_state["hr_notified"]:
            st.balloons()
        st.rerun()

    # Bulk actions
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    col_all, col_none = st.columns(2)
    with col_all:
        if st.button("✅ Complete All (Demo)", use_container_width=True):
            st.session_state["completed_tasks"] = [True] * len(tasks)
            msg = send_hr_notification(profile, calculate_progress([True] * len(tasks)))
            st.session_state["hr_notified"] = True
            st.session_state["chat_history"].append({
                "role": "ai",
                "content": f"🎉 **All tasks completed!**\n\n✉️ {msg}",
            })
            st.balloons()
            st.rerun()
    with col_none:
        if st.button("↺ Reset All Tasks", use_container_width=True):
            st.session_state["completed_tasks"] = [False] * len(tasks)
            st.session_state["hr_notified"] = False
            st.rerun()


# ══════════════════════════════════════════════
# TAB 3 — DASHBOARD
# ══════════════════════════════════════════════

with tab3:
    st.markdown(f"""
    <div class="card">
      <div class="card-title">👤 Developer Profile</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
        <div>
          <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Name</div>
          <div style="font-size:1.1rem; font-weight:600; color:#e2e8f0;">{profile['name']}</div>
        </div>
        <div>
          <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Role</div>
          <div style="font-size:1.1rem; font-weight:600; color:#63b3ed;">{profile['level']} {profile['role']}</div>
        </div>
        <div>
          <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Tech Stack</div>
          <div style="font-size:1rem; color:#a78bfa;">{', '.join(profile.get('tech_stack', ['N/A']))}</div>
        </div>
        <div>
          <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Status</div>
          <div style="font-size:1rem; color:{'#22c55e' if stats['is_complete'] else '#f97316'};">
            {'✅ Onboarding Complete' if stats['is_complete'] else '🔄 In Progress'}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    readiness = min(100, stats["percentage"] + (5 if len(profile.get("tech_stack", [])) >= 2 else 0))
    score_color = "#22c55e" if readiness >= 80 else "#f97316" if readiness >= 40 else "#ef4444"

    c1, c2, c3, c4 = st.columns(4)
    boxes = [
        (str(stats["total"]), "Total Tasks", "#63b3ed"),
        (str(stats["completed"]), "Completed", "#22c55e"),
        (str(stats["remaining"]), "Remaining", "#f97316"),
        (str(readiness), "Readiness Score", score_color),
    ]
    for col, (num, label, color) in zip([c1, c2, c3, c4], boxes):
        with col:
            st.markdown(f"""
            <div class="stat-box">
              <div class="stat-number" style="color:{color};">{num}</div>
              <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    # Progress chart (using Streamlit's built-in progress bar)
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 Progress Overview</div>', unsafe_allow_html=True)
    pct = stats["percentage"]
    color_bar = get_progress_color(pct)
    task_grid_html = "".join(
        f'<div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:0.8rem;text-align:center;">'
        f'<div style="font-size:1.6rem;">{"✅" if done else "⏳"}</div>'
        f'<div style="font-size:0.7rem;color:#94a3b8;margin-top:0.3rem;line-height:1.3;">'
        f'{task[:35]}{"..." if len(task) > 35 else ""}</div></div>'
        for task, done in zip(tasks, completed_tasks)
    )
    st.markdown(f"""
    <div class="card">
      <div style="margin-bottom:1rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
          <span style="color:#94a3b8; font-size:0.88rem;">Overall Progress</span>
          <span style="color:{color_bar}; font-weight:700;">{pct}%</span>
        </div>
        <div class="progress-container" style="height:20px;">
          <div style="height:100%; width:{pct}%; background:linear-gradient(90deg,{color_bar},{color_bar}99);
                      border-radius:50px;"></div>
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.8rem; margin-top:1rem;">
        {task_grid_html}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Completed vs pending
    st.markdown('<div class="card-title" style="margin-top:1rem;">📋 Task Breakdown</div>', unsafe_allow_html=True)
    col_done, col_pend = st.columns(2)
    with col_done:
        st.markdown("**✅ Completed Tasks**")
        done_tasks = [t for t, c in zip(tasks, completed_tasks) if c]
        if done_tasks:
            for t in done_tasks:
                st.markdown(f'<div class="task-done">~~{t}~~</div>', unsafe_allow_html=True)
        else:
            st.caption("No tasks completed yet.")
    with col_pend:
        st.markdown("**⏳ Pending Tasks**")
        pend_tasks = [t for t, c in zip(tasks, completed_tasks) if not c]
        if pend_tasks:
            for t in pend_tasks:
                st.markdown(f'<div class="task-pending">{t}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="task-done">All done! 🎉</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — ONBOARDING REPORT
# ══════════════════════════════════════════════

with tab4:
    st.markdown('<div class="card-title">📄 AI-Generated Onboarding Report</div>', unsafe_allow_html=True)

    if st.button("🔄 Generate / Refresh Report", use_container_width=True):
        st.session_state["_report_generated"] = True

    if st.session_state.get("_report_generated", False) or stats["is_complete"]:
        report = generate_onboarding_summary(profile, completed_tasks)
        st.markdown(f"""
        <div class="card">
        """, unsafe_allow_html=True)
        st.markdown(report)
        st.markdown("</div>", unsafe_allow_html=True)

        # Suggested next resources
        st.markdown('<div class="card-title" style="margin-top:1rem;">🎓 Suggested Next Learning Resources</div>', unsafe_allow_html=True)
        resources = {
            "Backend": [
                ("FastAPI Documentation", "https://fastapi.tiangolo.com"),
                ("System Design Primer", "https://github.com/donnemartin/system-design-primer"),
                ("Python Best Practices", "https://docs.python-guide.org"),
                ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com"),
            ],
            "Frontend": [
                ("React Official Docs", "https://react.dev"),
                ("TypeScript Handbook", "https://www.typescriptlang.org/docs"),
                ("Web Accessibility Guide", "https://www.w3.org/WAI/WCAG21/quickref"),
                ("Storybook for Components", "https://storybook.js.org"),
            ],
            "DevOps": [
                ("Kubernetes Docs", "https://kubernetes.io/docs"),
                ("Terraform Getting Started", "https://developer.hashicorp.com/terraform"),
                ("GitHub Actions Docs", "https://docs.github.com/en/actions"),
                ("AWS Well-Architected", "https://aws.amazon.com/architecture/well-architected"),
            ],
        }
        role_resources = resources.get(profile["role"], resources["Backend"])
        cols = st.columns(2)
        for i, (title, url) in enumerate(role_resources):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="card" style="padding:1rem;">
                  <div style="font-size:0.9rem;font-weight:600;color:#e2e8f0;">📖 {title}</div>
                  <div style="font-size:0.78rem;color:#63b3ed;margin-top:0.3rem;">{url}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:3rem;">
          <div style="font-size:3rem;">📄</div>
          <div style="color:#94a3b8; font-size:1rem; margin-top:0.75rem;">
            Click <strong>Generate Report</strong> to create your AI onboarding summary.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Demo auto-walkthrough ──
if st.session_state.get("demo_running") and st.session_state["onboarding_started"]:
    st.session_state["demo_running"] = False
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1f3c,#0d1b2a);border:1px solid rgba(124,58,237,0.3);
                border-radius:16px;padding:1.5rem;margin-top:1rem;text-align:center;">
      <div class="demo-pill">DEMO MODE</div>
      <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-top:0.5rem;">
        🎬 Demo Profile Loaded!</div>
      <div style="font-size:0.9rem;color:#94a3b8;margin-top:0.4rem;">
        Akshay Sharma · Backend Intern · Python & Docker<br/>
        Navigate the tabs above to explore all features. Use <em>Complete All</em> in Tasks tab to trigger HR notification!
      </div>
    </div>
    """, unsafe_allow_html=True)
