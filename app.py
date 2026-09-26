import streamlit as st

from challenge_generator import generate_challenge
from coach import coach_reply
from evaluator import (
    generate_independent_check,
    generate_thinking_report
)
from skills import DOMAINS, DIFFICULTIES


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ThinkForge",
    layout="wide"
)


# =========================================================
# SIMPLE THEME
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FBF8F3;
    }

    [data-testid="stSidebar"] {
        background-color: #F0EAFB;
    }

    div.stButton > button {
        background-color: #7254C8;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #5D40B3;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "stage": "Home",
    "current_challenge": None,
    "challenge_history": [],
    "coach_history": [],
    "thinking_report": None,
    "independent_check": None,
    "independent_answer": "",
    "generated_count": 0,

    "observation": "",
    "hypothesis": "",
    "evidence": "",
    "alternatives": "",
    "decision": "",
    "assumption": "",

    "experiment_change": "",
    "experiment_measure": "",
    "experiment_success": "",
    "experiment_failure": "",

    "coach_question": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# NAVIGATION
# =========================================================

def go(stage):
    st.session_state.stage = stage
    st.rerun()


# =========================================================
# RESET WORKSPACE
# =========================================================

def reset_workspace():

    st.session_state.current_challenge = None
    st.session_state.coach_history = []
    st.session_state.thinking_report = None
    st.session_state.independent_check = None
    st.session_state.independent_answer = ""
    st.session_state.coach_question = ""

    st.session_state.observation = ""
    st.session_state.hypothesis = ""
    st.session_state.evidence = ""
    st.session_state.alternatives = ""
    st.session_state.decision = ""
    st.session_state.assumption = ""

    st.session_state.experiment_change = ""
    st.session_state.experiment_measure = ""
    st.session_state.experiment_success = ""
    st.session_state.experiment_failure = ""


# =========================================================
# STUDENT STATE
# =========================================================

def get_student_state():

    return {
        "observation": st.session_state.observation,
        "hypothesis": st.session_state.hypothesis,
        "evidence": st.session_state.evidence,
        "alternatives": st.session_state.alternatives,
        "decision": st.session_state.decision,
        "assumption": st.session_state.assumption,
        "experiment_change": st.session_state.experiment_change,
        "experiment_measure": st.session_state.experiment_measure,
        "experiment_success": st.session_state.experiment_success,
        "experiment_failure": st.session_state.experiment_failure
    }


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ThinkForge")

    st.caption("Build the habit of thinking.")

    st.divider()

    if st.button(
        "Home",
        use_container_width=True,
        key="nav_home"
    ):
        go("Home")

    if st.button(
        "Practice",
        use_container_width=True,
        key="nav_practice"
    ):
        go("Practice")

    if st.button(
        "My Progress",
        use_container_width=True,
        key="nav_progress"
    ):
        go("My Progress")

    st.divider()

    st.caption(
        "Your practice data is stored in this browser session only."
    )


# =========================================================
# CURRENT PAGE
# =========================================================

stage = st.session_state.stage


# =========================================================
# HOME
# =========================================================

if stage == "Home":

    st.title("Think clearly. Build boldly.")

    st.write(
        "Practice solving unfamiliar Data Science and AI "
        "problems with an AI coach that helps you think "
        "instead of thinking for you."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Challenges generated",
            st.session_state.generated_count
        )

    with col2:
        st.metric(
            "Thinking reports",
            1 if st.session_state.thinking_report else 0
        )

    with col3:
        st.metric(
            "Practice mode",
            "Coach-first"
        )

    st.write("")

    st.subheader("Your next step")

    st.write(
        "Choose a skill and difficulty, investigate a fresh "
        "problem, explain your reasoning, design an experiment, "
        "and finish with a new problem to test transfer."
    )

    if st.button(
        "Start practicing",
        key="home_start"
    ):
        go("Practice")

    st.write("")

    st.subheader("How ThinkForge works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**Investigate**")
        st.write(
            "Understand the problem before jumping "
            "to a solution."
        )

    with col2:
        st.markdown("**Reason**")
        st.write(
            "Build hypotheses, compare alternatives "
            "and examine assumptions."
        )

    with col3:
        st.markdown("**Experiment**")
        st.write(
            "Design a small test and decide what "
            "evidence matters."
        )

    with col4:
        st.markdown("**Transfer**")
        st.write(
            "Solve a different problem using the "
            "same underlying skill."
        )


# =========================================================
# PRACTICE
# =========================================================

elif stage == "Practice":

    st.title("Choose your practice")

    st.write(
        "Select a skill and difficulty. ThinkForge will "
        "generate a fresh problem for you."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        selected_skill = st.selectbox(
            "Skill",
            list(DOMAINS.keys())
        )

    with col2:

        selected_difficulty = st.selectbox(
            "Difficulty",
            DIFFICULTIES
        )

    domain = DOMAINS[selected_skill]

    st.write("")

    st.markdown(f"**{selected_skill}**")

    st.write(domain["description"])

    st.markdown("**Concepts practiced**")

    st.write(
        ", ".join(domain["concepts"])
    )

    st.write("")

    if st.button(
        "Generate New Challenge",
        key="generate_challenge"
    ):

        with st.spinner(
            "Creating your challenge..."
        ):

            challenge = generate_challenge(
                domain,
                selected_difficulty
            )

        reset_workspace()

        st.session_state.current_challenge = challenge

        st.session_state.challenge_history.append(
            challenge
        )

        st.session_state.generated_count += 1

        st.session_state.stage = "Workspace"

        st.rerun()


# =========================================================
# WORKSPACE
# =========================================================

elif stage == "Workspace":

    challenge = st.session_state.current_challenge

    if challenge is None:
        go("Practice")

    st.title(
        challenge.get(
            "title",
            "ThinkForge Challenge"
        )
    )

    st.caption(
        f'{challenge.get("skill", "Data Science")} · '
        f'{challenge.get("difficulty", "Practice")}'
    )

    st.divider()

    st.subheader("The Challenge")

    st.write(
        challenge.get(
            "scenario",
            ""
        )
    )

    if challenge.get("known_information"):

        st.subheader("What you know")

        for item in challenge["known_information"]:
            st.write(f"• {item}")

    if challenge.get("constraints"):

        st.subheader("Constraints")

        for item in challenge["constraints"]:
            st.write(f"• {item}")

    st.divider()

    tabs = st.tabs(
        [
            "Investigate",
            "Reason",
            "Experiment",
            "AI Coach",
            "Independent Check",
            "Thinking Report"
        ]
    )


    # =====================================================
    # INVESTIGATE
    # =====================================================

    with tabs[0]:

        st.subheader("Investigate")

        st.write(
            challenge.get(
                "initial_question",
                "What do you notice about this problem?"
            )
        )

        st.text_area(
            "What do you observe?",
            key="observation",
            height=150
        )

        st.text_area(
            "What is your first hypothesis?",
            key="hypothesis",
            height=150
        )


    # =====================================================
    # REASON
    # =====================================================

    with tabs[1]:

        st.subheader("Reason")

        st.text_area(
            "What evidence supports your hypothesis?",
            key="evidence",
            height=150
        )

        st.text_area(
            "What are the alternative explanations?",
            key="alternatives",
            height=150
        )

        st.text_area(
            "What decision would you make right now?",
            key="decision",
            height=150
        )

        st.text_area(
            "What assumption could make your decision wrong?",
            key="assumption",
            height=130
        )


    # =====================================================
    # EXPERIMENT
    # =====================================================

    with tabs[2]:

        st.subheader("Design an Experiment")

        st.write(
            "Turn your reasoning into a small test."
        )

        st.text_area(
            "What will you change or test?",
            key="experiment_change",
            height=130
        )

        st.text_area(
            "What will you measure?",
            key="experiment_measure",
            height=130
        )

        st.text_area(
            "What result would count as success?",
            key="experiment_success",
            height=130
        )

        st.text_area(
            "What result would make you reconsider?",
            key="experiment_failure",
            height=130
        )


    # =====================================================
    # AI COACH
    # =====================================================

    with tabs[3]:

        st.subheader("AI Coach")

        st.write(
            "The coach helps you investigate your reasoning "
            "without giving you the complete solution."
        )

        question = st.text_input(
            "What are you stuck on?",
            key="coach_question"
        )

        if st.button(
            "Ask the Coach",
            key="ask_coach"
        ):

            student_state = get_student_state()

            reply = coach_reply(
                challenge,
                student_state,
                question,
                st.session_state.coach_history
            )

            st.session_state.coach_history.append(
                {
                    "student": question,
                    "coach": reply
                }
            )

            st.rerun()

        if st.session_state.coach_history:

            st.divider()

            for message in st.session_state.coach_history:

                st.markdown(
                    f"**You:** {message['student']}"
                )

                st.write(
                    message["coach"]
                )

                st.write("")


    # =====================================================
    # INDEPENDENT CHECK
    # =====================================================

    with tabs[4]:

        st.subheader("Independent Check")

        st.write(
            "You will receive a completely different problem "
            "that tests the same underlying thinking skill."
        )

        if st.session_state.independent_check is None:

            if st.button(
                "Generate Independent Check",
                key="generate_independent"
            ):

                with st.spinner(
                    "Creating a new transfer challenge..."
                ):

                    check = generate_independent_check(
                        challenge
                    )

                st.session_state.independent_check = check

                st.rerun()

        else:

            check = st.session_state.independent_check

            st.markdown(
                f"**{check.get('title', 'Independent Check')}**"
            )

            st.write(
                check.get(
                    "scenario",
                    ""
                )
            )

            st.info(
                "Try this without AI or external help."
            )

            st.text_area(
                "Your response",
                key="independent_answer",
                height=220
            )

            if st.button(
                "Submit Independent Response",
                key="submit_independent"
            ):

                answer = (
                    st.session_state.independent_answer
                )

                if len(answer.strip()) < 40:

                    st.error(
                        "Write a little more so ThinkForge "
                        "can provide meaningful feedback."
                    )

                else:

                    student_state = get_student_state()

                    with st.spinner(
                        "Preparing your Thinking Report..."
                    ):

                        report = generate_thinking_report(
                            challenge,
                            student_state,
                            answer
                        )

                    st.session_state.thinking_report = report

                    st.success(
                        "Your Thinking Report is ready."
                    )


    # =====================================================
    # THINKING REPORT
    # =====================================================

    with tabs[5]:

        st.subheader("Thinking Report")

        report = st.session_state.thinking_report

        if not report:

            st.info(
                "Complete the Independent Check to "
                "generate your Thinking Report."
            )

        else:

            st.write(
                "This is formative feedback on your reasoning. "
                "It is not an intelligence score."
            )

            sections = [
                (
                    "Problem Investigation",
                    "problem_investigation"
                ),
                (
                    "Data Reasoning",
                    "data_reasoning"
                ),
                (
                    "Evidence Usage",
                    "evidence_usage"
                ),
                (
                    "Alternative Thinking",
                    "alternative_thinking"
                ),
                (
                    "Experiment Design",
                    "experiment_design"
                ),
                (
                    "Technical Trade-offs",
                    "technical_tradeoffs"
                )
            ]

            for title, key in sections:

                st.markdown(
                    f"**{title}**"
                )

                st.write(
                    report.get(
                        key,
                        "No feedback available."
                    )
                )

                st.write("")

            st.divider()

            st.markdown("**What you did well**")

            strengths = report.get(
                "strengths",
                []
            )

            for strength in strengths:

                st.write(
                    f"• {strength}"
                )

            st.write("")

            st.markdown("**Growth Opportunity**")

            st.write(
                report.get(
                    "growth_opportunity",
                    ""
                )
            )

            st.write("")

            st.markdown("**Concepts Practiced**")

            concepts = report.get(
                "concepts_practiced",
                []
            )

            if concepts:

                st.write(
                    ", ".join(concepts)
                )

            st.write("")

            st.markdown("**Next Practice**")

            st.write(
                report.get(
                    "next_practice",
                    "Try another unfamiliar problem."
                )
            )

    st.divider()

    if st.button(
        "Back to Practice",
        key="back_to_practice"
    ):
        go("Practice")


# =========================================================
# MY PROGRESS
# =========================================================

elif stage == "My Progress":

    st.title("My Progress")

    st.caption(
        "Practice indicators only. They are not a measure "
        "of intelligence or proof of lasting learning."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Challenges generated",
            st.session_state.generated_count
        )

    with col2:

        st.metric(
            "Thinking reports",
            1 if st.session_state.thinking_report else 0
        )

    st.divider()

    if not st.session_state.challenge_history:

        st.info(
            "You have not generated a challenge yet."
        )

    else:

        st.subheader("Practice History")

        for index, challenge in enumerate(
            reversed(
                st.session_state.challenge_history
            ),
            start=1
        ):

            with st.expander(
                challenge.get(
                    "title",
                    f"Challenge {index}"
                )
            ):

                st.write(
                    challenge.get(
                        "scenario",
                        ""
                    )
                )

                st.caption(
                    f"Skill: {challenge.get(
                        'skill',
                        'Data Science'
                    )}"
                )

                st.caption(
                    f"Difficulty: {challenge.get(
                        'difficulty',
                        'Practice'
                    )}"
                )

    st.divider()

    if st.session_state.thinking_report:

        st.subheader("Latest Thinking Report")

        st.write(
            st.session_state.thinking_report.get(
                "growth_opportunity",
                ""
            )
        )

        if st.button(
            "Open Full Thinking Report",
            key="open_report"
        ):
            go("Workspace")

    else:

        st.info(
            "Complete an Independent Check to see "
            "your Thinking Report."
        )

    st.write("")

    if st.button(
        "Start New Practice",
        key="new_practice"
    ):
        go("Practice")
