import streamlit as st
from challenge_generator import generate_challenge
from coach import coach_reply

from evaluator import (
    generate_independent_check,
    generate_thinking_report
)

from skills import DOMAINS, DIFFICULTIES
st.set_page_config(page_title="ThinkForge", page_icon=None, layout="wide")

PURPLE = "#7254C8"
st.markdown("""
<style>
.stApp { background: #FBF8F3; color: #28243A; }
[data-testid="stSidebar"] { background: #F0EAFB; }
.hero { background: linear-gradient(120deg,#EEE7FF,#F8F0FF); padding: 2rem; border-radius: 22px; border: 1px solid #E3D8FA; }
.panel { background: white; padding: 1.25rem; border-radius: 18px; border: 1px solid #EAE4F3; }
.small-muted { color: #716B7D; }
div.stButton > button { background: #7254C8; color: white; border: 0; border-radius: 12px; padding: .55rem 1rem; }
div.stButton > button:hover { background: #5D40B3; color: white; border: 0; }
</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state: st.session_state.stage = "Home"
if "challenge_id" not in st.session_state: st.session_state.challenge_id = None
if "answers" not in st.session_state: st.session_state.answers = {}
if "coach_history" not in st.session_state: st.session_state.coach_history = {}
if "projects" not in st.session_state: st.session_state.projects = {}
if "assessments" not in st.session_state: st.session_state.assessments = {}

def go(stage):
    st.session_state.stage = stage
    st.rerun()

def current_challenge():
    return next((c for c in CHALLENGES if c["id"] == st.session_state.challenge_id), None)

with st.sidebar:
    st.markdown("## ThinkForge")
    st.caption("Build the habit of thinking.")
    pages = ["Home", "Challenges", "My Progress"]
    for p in pages:
        if st.button(p, use_container_width=True, key="nav_"+p):
            go(p)
    st.divider()
    st.caption("Your work is stored in this browser session only.")

stage = st.session_state.stage
if stage == "Home":
    st.markdown('<div class="hero"><h1>Think clearly. Build boldly.</h1><p>Practice solving unfamiliar problems—then prove what you can do independently.</p></div>', unsafe_allow_html=True)
    st.write("")
    done = len(st.session_state.assessments)
    c1,c2,c3 = st.columns(3)
    c1.metric("Challenges", len(CHALLENGES))
    c2.metric("Skill checks completed", done)
    c3.metric("Practice mode", "Hint-first")
    st.subheader("Your next step")
    st.write("Choose a real-world student problem. Think first, use AI as a coach, make a small plan, and finish with a new problem without AI.")
    if st.button("Explore challenges"):
        go("Challenges")
    st.subheader("How ThinkForge works")
    cols = st.columns(4)
    for col, title, desc in zip(cols, ["Understand","Imagine","Reason","Test"], [
        "Frame the problem and question assumptions.",
        "Generate multiple possible approaches.",
        "Compare trade-offs and choose deliberately.",
        "Plan an experiment and learn from evidence."]):
        with col:
            st.markdown(f'<div class="panel"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif stage == "Challenges":
    st.title("Choose a challenge")
    st.write("Start with your own thinking. You can ask the coach for hints after recording your first ideas.")
    for c in CHALLENGES:
        with st.container(border=True):
            st.subheader(c["title"])
            st.write(c["summary"])
            st.caption(c["tag"])
            if st.button("Start challenge", key="start_"+c["id"]):
                st.session_state.challenge_id = c["id"]
                st.session_state.stage = "Workspace"
                st.rerun()

elif stage == "Workspace":
    ch = current_challenge()
    if not ch:
        go("Challenges")
    st.title(ch["title"])
    st.caption("Work through each stage. Your first thoughts are saved before coaching.")
    tabs = st.tabs(["1 · Understand", "2 · Imagine", "3 · Reason", "4 · Test", "AI Coach", "Mini Project", "Independent Check"])
    prompts = [
        ("What exactly is the problem? Who experiences it, and when?", "problem"),
        ("List at least three different ways to address it. Include one unusual idea.", "ideas"),
        ("What assumptions are you making? Compare options and explain your choice.", "reasoning"),
        ("What small experiment could test your idea? Define evidence of success.", "test")
    ]
    with tabs[0]:
        st.write(ch["prompt"])
        st.text_area(prompts[0][0], key=f"{ch['id']}_problem", height=150)
    with tabs[1]:
        st.text_area(prompts[1][0], key=f"{ch['id']}_ideas", height=170)
    with tabs[2]:
        st.text_area(prompts[2][0], key=f"{ch['id']}_reasoning", height=170)
    with tabs[3]:
        st.text_area(prompts[3][0], key=f"{ch['id']}_test", height=170)
    with tabs[4]:
        st.write("The coach should help you think—not do the thinking for you.")
        q = st.text_input("What are you stuck on?", key=f"{ch['id']}_coach_q")
        if st.button("Ask for a hint", key=f"{ch['id']}_ask"):
            initial = st.session_state.get(f"{ch['id']}_problem","")
            history = st.session_state.coach_history.setdefault(ch["id"], [])
            reply = coach_reply(ch, initial, q, history)
            history.append(("You", q)); history.append(("Coach", reply))
        for who, msg in st.session_state.coach_history.get(ch["id"], []):
            st.markdown(f"**{who}:** {msg}")
    with tabs[5]:
        st.write("Turn your idea into a small, testable project.")
        st.text_input("Project / solution name", key=f"{ch['id']}_project_name")
        st.text_area("What will you make or change?", key=f"{ch['id']}_project_idea")
        st.text_area("Experiment and success criteria", key=f"{ch['id']}_project_test")
        if st.button("Save mini project", key=f"{ch['id']}_saveproject"):
            st.session_state.projects[ch["id"]] = {
                "name": st.session_state.get(f"{ch['id']}_project_name",""),
                "idea": st.session_state.get(f"{ch['id']}_project_idea",""),
                "test": st.session_state.get(f"{ch['id']}_project_test","")
            }
            st.success("Mini project saved for this session.")
    with tabs[6]:
        st.warning("Independent check: do not use AI or external help while answering.")
        st.write(ch["assessment"])
        answer = st.text_area("Your independent response", key=f"{ch['id']}_assessment", height=200)
        if st.button("Submit for feedback", key=f"{ch['id']}_submit"):
            if len(answer.strip()) < 30:
                st.error("Please write a little more so you can receive meaningful feedback.")
            else:
                result = evaluate_independent_attempt(ch, answer)
                st.session_state.assessments[ch["id"]] = {"answer": answer, "feedback": result}
                st.success("Submitted. Feedback is below.")
        saved = st.session_state.assessments.get(ch["id"])
        if saved:
            st.markdown("### Feedback")
            st.write(saved["feedback"])
    if st.button("Back to challenges"):
        go("Challenges")

elif stage == "My Progress":
    st.title("My Progress")
    st.caption("These are practice indicators, not a measure of intelligence or proof of lasting learning.")
    st.metric("Independent checks completed", len(st.session_state.assessments))
    if not st.session_state.assessments:
        st.info("Complete an independent check to see your progress here.")
    for cid, data in st.session_state.assessments.items():
        ch = next(c for c in CHALLENGES if c["id"] == cid)
        with st.expander(ch["title"]):
            st.write(data["feedback"])
            st.caption("Session-only data: it disappears when the session resets.")
    if st.button("Return home"):
        go("Home")
