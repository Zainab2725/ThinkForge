import os
import json
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"


SYSTEM_PROMPT = """
You are ThinkForge, an AI thinking coach for university
Data Science and AI students.

Your job is to strengthen independent technical reasoning,
not to solve the problem for the student.

Rules:

- Be warm and concise.
- Be beginner-friendly.
- Ask one useful question at a time.
- Look at the student's actual reasoning.
- Challenge unsupported assumptions.
- Ask for evidence when claims are unsupported.
- Ask for comparisons when the student jumps to one option.
- Ask for an experiment when evidence is needed.
- Give a small hint when useful.
- Adapt to the student's current reasoning.
- Never provide the complete solution.
- Never claim that a short answer proves intelligence
  or lasting learning.
"""


def get_client():

    key = None

    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        key = os.getenv("GROQ_API_KEY")

    if not key:
        raise RuntimeError("GROQ_API_KEY is missing.")

    return OpenAI(
        api_key=key,
        base_url="https://api.groq.com/openai/v1"
    )


def coach_reply(
    challenge,
    student_state,
    question,
    history
):

    reasoning = "\n".join(
        f"{key}: {value}"
        for key, value in student_state.items()
        if value.strip()
    )

    if not reasoning:

        return (
            "Start with your own observation first. "
            "What is the most important thing you notice?"
        )

    prompt = f"""
Challenge:

{json.dumps(challenge, ensure_ascii=False)}

Student's current reasoning:

{reasoning}

Student's latest question:

{question}

Previous coaching:

{json.dumps(history[-8:], ensure_ascii=False)}

Decide the most useful next coaching move.

You may:

- ask a question
- challenge an assumption
- request evidence
- ask for comparison
- suggest a small experiment
- give a small hint

Do NOT solve the challenge.
"""

    try:

        response = get_client().chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.5,
            max_tokens=300
        )

        return (
            response.choices[0].message.content
            or "What evidence could test your current idea?"
        )

    except Exception as e:

        return (
            f"The AI coach is temporarily unavailable "
            f"({type(e).__name__}). Try identifying one "
            f"assumption you could test."
        )
