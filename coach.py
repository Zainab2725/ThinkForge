import os
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You are ThinkForge, a thinking coach for university students.
Your job is to strengthen independent problem-solving, not to hand over answers.
Be warm, concise, and beginner-friendly.
Use hint-first coaching: ask one useful question, offer a small hint, or point out an assumption.
Do not write a complete solution or project for the student.
If the student has not attempted the problem, ask them to make a first attempt.
Encourage multiple options, evidence, trade-offs, and small tests.
Never claim that a brief answer proves intelligence or lasting learning."""

def _client():
    key = None
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to Streamlit secrets.")
    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")

def coach_reply(challenge, initial_thought, question, history):
    if not initial_thought.strip():
        return "Before I give a hint, write down your first guess: what do you think is causing the problem?"
    messages = [{"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":f"Challenge: {challenge['title']}\\nPrompt: {challenge['prompt']}\\nStudent's current thinking: {initial_thought}\\nQuestion: {question}"}]
    for role, content in history[-6:]:
        messages.append({"role":"assistant" if role == "Coach" else "user", "content": content})
    try:
        response = _client().chat.completions.create(model=MODEL, messages=messages, temperature=0.5, max_tokens=350)
        return response.choices[0].message.content or "Try naming one assumption you could check."
    except Exception as e:
        return f"I couldn't reach the AI coach right now ({type(e).__name__}). Try again, or continue using the prompts in the workspace."

def evaluate_independent_attempt(challenge, answer):
    prompt = f"""Give feedback on this student's independent response. Do not rewrite it for them.
Use these criteria: problem framing, assumptions/alternatives, reasoning/evidence, testability.
Return: (1) two specific strengths, (2) one next step, (3) a short note on which criteria are visible.
Be encouraging and calibrated; this is formative feedback, not a validated assessment.
Challenge: {challenge['assessment']}
Student response: {answer}"""
    try:
        response = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt}],
            temperature=0.3, max_tokens=450
        )
        return response.choices[0].message.content or "Your response is saved. Review whether you considered causes, evidence, and a test."
    except Exception as e:
        return f"Your response is saved, but AI feedback is unavailable ({type(e).__name__}). Review: did you frame the problem, consider alternatives, use evidence, and propose a test?"
