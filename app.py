import streamlit as st

from challenge_generator import generate_challenge
from coach import coach_reply
from evaluator import (
    generate_independent_check,
    generate_thinking_report
)
from skills import DOMAINS, DIFFICULTIES


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ThinkForge",
    page_icon=None,
    layout="wide"
)


# --------------------------------------------------
# STYLE
# --------------------------------------------------

PURPLE = "#7254C8"

st.markdown(
    """
    <style>

    .stApp {
        background: #FBF8F3;
        color: #28243A;
    }

    [data-testid="stSidebar"] {
        background: #F0EAFB;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #EEE7FF,
            #F8F0FF
        );
        padding: 2.2rem;
        border-radius: 22px;
        border: 1px solid #E3D8FA;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: #28243A;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #625B70;
        font-size: 1.05rem;
    }

    .panel {
        background: white;
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #EAE4F3;
        margin-bottom: 1rem;
    }

    .small-muted {
        color: #716B7D;
    }

    .challenge-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #EAE4F3;
        margin-bottom: 1rem;
    }

    div.stButton > button {
        background: #7254C8;
        color: white;
        border: 0;
        border-radius: 12px;
        padding: 0.55rem 1rem;
    }

    div.stButton > button:hover {
        background: #5D40B3;
        color: white;
        border: 0;
    }

    textarea,
    input {
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "stage": "Home",
    "current_challenge": None,
    "challenge_history": [],
    "coach_history": [],
    "thinking_report": None,
    "independent_check": None,
    "independent_answer": "",
    "generated_count": 0,

    # Student reasoning
    "observation": "",
    "hypothesis": "",
    "evidence": "",
    "alternatives": "",
    "decision": "",
    "assumption": "",

    # Experiment
    "experiment_change": "",
    "experiment_measure": "",
    "experiment_success": "",
    "experiment_failure": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

def go(stage):
    st.session_state.stage = stage
    st.rerun()


# --------------------------------------------------
# RESET WORKSPACE
# --------------------------------------------------

def reset_workspace():

    st.session_state.current_challenge = None
    st.session_state.challenge_history = []
    st.session_state.coach_history = []
    st.session_state.thinking_report = None
    st.session_state.independent_check = None
    st.session_state.independent_answer = ""

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


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## ThinkForge")

    st.caption("Build the habit of thinking.")

    st.divider()

    pages = [
        "Home",
        "Practice",
        "My Progress"
    ]

    for page in pages:

        if st.button(
            page,
            use_container_width=True,
            key=f"nav_{page}"
        ):
            go(page)

    st.divider()

    st.caption(
        "Your practice data is stored in this browser session only."
    )


# --------------------------------------------------
# HOME
# --------------------------------------------------

stage = st.session_state.stage


if stage == "Home":

    st.markdown(
        """
        <div class="hero">

            <h1>Think clearly. Build boldly.</h1>

            <p>
                Practice solving unfamiliar Data Science and AI
                problems with an AI coach that helps you think
                instead of thinking for you.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    generated = st.session_state.generated_count

    completed = (
        1
        if st.session_state.thinking_report
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Challenges generated",
        generated
    )

    c2.metric(
        "Thinking reports",
        completed
    )

    c3.metric(
        "Practice mode",
        "Coach-first"
    )

    st.subheader("Your next step")

    st.write(
        "Choose a skill and difficulty, investigate a fresh "
        "problem, explain your reasoning, design an experiment, "
        "and finish with a new problem to test transfer."
    )

    if st.button(
        "Start practicing",
        use_container_width=False
    ):
        go("Practice")

    st.subheader("How ThinkForge works")

    cols = st.columns(4)

    stages = [
        (
            "Investigate",
            "Understand the problem before jumping to a solution."
        ),
        (
            "Reason",
            "Build hypotheses, compare alternatives and examine assumptions."
        ),
        (
            "Experiment",
            "Design a small test and decide what evidence matters."
        ),
        (
            "Transfer",
            "Solve a different problem using the same underlying skill."
        )
    ]

    for col, (title, description) in zip(cols, stages):

        with col:

            st.markdown(
                f"""
                <div class="panel">

                    <h3>{title}</h3>

                    <p>
                        {description}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# PRACTICE
# --------------------------------------------------

elif stage == "Practice":

    st.title("Practice")

    st.write(
        "Choose a skill and difficulty. ThinkForge will "
        "generate a fresh problem for you."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        selected_skill = st.selectbox(
            "Choose a skill",
            list(DOMAINS.keys())
        )

    with col2:

        selected_difficulty = st.selectbox(
            "Choose difficulty",
            DIFFICULTIES
        )

    domain = DOMAINS[selected_skill]

    st.markdown(
        f"""
        <div class="panel">

            <h3>{selected_skill}</h3>

            <p>
                {domain["description"]}
            </p>

            <p>
                <strong>Concepts:</strong>
                {", ".join(domain["concepts"])}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Generate New Challenge",
        use_container_width=False
    ):

        with st.spinner(
            "ThinkForge is creating a fresh challenge..."
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


# --------------------------------------------------
# WORKSPACE
# --------------------------------------------------

elif stage == "Workspace":

    challenge = st.session_state.current_challenge

    if not challenge:

        go("Practice")

    st.title(challenge["title"])

    st.caption(
        f'{challenge.get("skill", "Data Science")} · '
        f'{challenge.get("difficulty", "Practice")}'
    )

    st.markdown("---")

    # --------------------------------------------------
    # CHALLENGE DESCRIPTION
    # --------------------------------------------------

    st.subheader("The Challenge")

    st.markdown(
        f"""
        <div class="challenge-card">

            <p>
                {challenge["scenario"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # KNOWN INFORMATION
    # --------------------------------------------------

    if challenge.get("known_information"):

        st.subheader("What you know")

        for item in challenge["known_information"]:

            st.write(f"• {item}")

    # --------------------------------------------------
    # CONSTRAINTS
    # --------------------------------------------------

    if challenge.get("constraints"):

        st.subheader("Constraints")

        for item in challenge["constraints"]:

            st.write(f"• {item}")

    st.markdown("---")

    # --------------------------------------------------
    # WORKSPACE TABS
    # --------------------------------------------------

    tabs = st.tabs(
        [
            "1 · Investigate",
            "2 · Reason",
            "3 · Experiment",
            "4 · AI Coach",
            "5 · Independent Check",
            "6 · Thinking Report"
        ]
    )


    # ==================================================
    # INVESTIGATE
    # ==================================================

    with tabs[0]:

        st.subheader("Investigate")

        st.write(
            challenge.get(
                "initial_question",
                "What do you notice about the problem?"
            )
        )

        st.text_area(
            "What do you observe?",
            key="observation",
            height=160,
            placeholder=(
                "Write what you notice before deciding "
                "what the solution should be."
            )
        )

        st.text_area(
            "What is your first hypothesis?",
            key="hypothesis",
            height=160,
            placeholder=(
                "What do you currently think might be happening?"
            )
        )


    # ==================================================
    # REASON
    # ==================================================

    with tabs[1]:

        st.subheader("Reason")

        st.text_area(
            "What evidence supports your hypothesis?",
            key="evidence",
            height=160,
            placeholder=(
                "What evidence would support or weaken "
                "your current explanation?"
            )
        )

        st.text_area(
            "What are the alternative explanations?",
            key="alternatives",
            height=160,
            placeholder=(
                "Think of at least two other possibilities."
            )
        )

        st.text_area(
            "What decision would you make right now?",
            key="decision",
            height=160,
            placeholder=(
                "Choose an approach and explain why."
            )
        )

        st.text_area(
            "What assumption could make your decision wrong?",
            key="assumption",
            height=140,
            placeholder=(
                "Identify something you are assuming."
            )
        )


    # ==================================================
    # EXPERIMENT
    # ==================================================

    with tabs[2]:

        st.subheader("Design an Experiment")

        st.write(
            "Turn your reasoning into a small test."
        )

        st.text_area(
            "What will you change or test?",
            key="experiment_change",
            height=140
        )

        st.text_area(
            "What will you measure?",
            key="experiment_measure",
            height=140
        )

        st.text_area(
            "What result would count as success?",
            key="experiment_success",
            height=140
        )

        st.text_area(
            "What result would make you reconsider?",
            key="experiment_failure",
            height=140
        )


    # ==================================================
    # AI COACH
    # ==================================================

    with tabs[3]:

        st.subheader("AI Coach")

        st.write(
            "The coach does not solve the challenge for you. "
            "It questions your reasoning, asks for evidence "
            "and helps you investigate."
        )

        question = st.text_input(
            "What are you stuck on?",
            key="coach_question"
        )

        if st.button(
            "Ask the Coach",
            key="ask_coach"
        ):

            student_state = {
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

        if st.session_state.coach_history:

            st.markdown("---")

            for message in st.session_state.coach_history:

                st.markdown(
                    f"**You:** {message['student']}"
                )

                st.markdown(
                    f"**ThinkForge Coach:** {message['coach']}"
                )

                st.markdown("---")


    # ==================================================
    # INDEPENDENT CHECK
    # ==================================================

    with tabs[4]:

        st.subheader("Independent Check")

        st.write(
            "This is a new problem designed to test whether "
            "you can transfer the same thinking skill to "
            "a different situation."
        )

        if st.session_state.independent_check is None:

            if st.button(
                "Generate Independent Check",
                key="generate_independent"
            ):

                with st.spinner(
                    "Creating a new transfer problem..."
                ):

                    check = generate_independent_check(
                        challenge
                    )

                st.session_state.independent_check = check

                st.rerun()

        else:

            check = st.session_state.independent_check

            st.markdown(
                f"""
                <div class="challenge-card">

                    <h3>{check["title"]}</h3>

                    <p>
                        {check["scenario"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.warning(
                "Try this without AI or external help."
            )

            st.text_area(
                "Your response",
                key="independent_answer",
                height=220,
                placeholder=(
                    "Explain how you would investigate "
                    "and reason through this problem."
                )
            )

            if st.button(
                "Submit Independent Response",
                key="submit_independent"
            ):

                answer = st.session_state.independent_answer

                if len(answer.strip()) < 40:

                    st.error(
                        "Write a little more so ThinkForge "
                        "can give meaningful feedback."
                    )

                else:

                    with st.spinner(
                        "Analyzing your reasoning..."
                    ):

                        report = generate_thinking_report(
                            challenge,
                            {
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
                            },
                            answer
                        )

                    st.session_state.thinking_report = report

                    st.success(
                        "Your Thinking Report is ready."
                    )


    # ==================================================
    # THINKING REPORT
    # ==================================================

    with tabs[5]:

        st.subheader("Thinking Report")

        report = st.session_state.thinking_report

        if not report:

            st.info(
                "Complete the Independent Check to generate "
                "your formative Thinking Report."
            )

        else:

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
                    f"### {title}"
                )

                st.write(
                    report.get(
                        key,
                        "No feedback available."
                    )
                )

            st.markdown("---")

            st.subheader("What you did well")

            for strength in report.get(
                "strengths",
                []
            ):

                st.write(
                    f"• {strength}"
                )

            st.subheader("Growth Opportunity")

            st.write(
                report.get(
                    "growth_opportunity",
                    "Keep testing your assumptions."
                )
            )

            st.subheader("Concepts Practiced")

            concepts = report.get(
                "concepts_practiced",
                []
            )

            if concepts:

                st.write(
                    ", ".join(concepts)
                )

            st.subheader("Next Practice")

            st.write(
                report.get(
                    "next_practice",
                    "Try another unfamiliar problem."
                )
            )

    st.markdown("---")

    if st.button(
        "Back to Practice",
        key="back_to_practice"
    ):

        go("Practice")


# --------------------------------------------------
# MY PROGRESS
# --------------------------------------------------

elif stage == "My Progress":

    st.title("My Progress")

    st.caption(
        "These are practice indicators, not a measure "
        "of intelligence or proof of lasting learning."
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Challenges generated",
        st.session_state.generated_count
    )

    col2.metric(
        "Thinking reports",
        1 if st.session_state.thinking_report else 0
    )

    st.markdown("---")

    if not st.session_state.challenge_history:

        st.info(
            "You have not generated a challenge yet."
        )

    else:

        st.subheader("Practice History")

        for index, challenge in enumerate(
            reversed(st.session_state.challenge_history),
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
                    f'Skill: {challenge.get("skill", "Data Science")}'
                )

                st.caption(
                    f'Difficulty: {challenge.get("difficulty", "Practice")}'
                )

    st.markdown("---")

    if st.session_state.thinking_report:

        st.subheader("Latest Thinking Report")

        report = st.session_state.thinking_report

        st.write(
            report.get(
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

    if st.button(
        "Start New Practice",
        key="new_practice"
    ):

        go("Practice")
