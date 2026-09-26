import json
import os
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"


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


def parse_json(text):

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)


def generate_independent_check(challenge):

    prompt = f"""
Create a NEW independent transfer challenge.

Original challenge:

{json.dumps(challenge, ensure_ascii=False)}

Requirements:

- Test the same underlying skill.
- Use a completely different context.
- Do not reuse the original scenario.
- Do not give the answer.
- Require reasoning rather than memorization.

Return ONLY valid JSON:

{{
    "title": "...",
    "scenario": "..."
}}
"""

    try:

        response = get_client().chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Create concise transfer-learning "
                        "challenges. Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.8,
            max_tokens=450
        )

        return parse_json(
            response.choices[0].message.content or ""
        )

    except Exception:

        return {
            "title": "Transfer Challenge",

            "scenario": (
                "A different AI system shows unexpected "
                "performance in real-world use. Explain "
                "how you would investigate the issue before "
                "choosing a solution. Identify possible "
                "causes, evidence and one test."
            )
        }


def generate_thinking_report(
    challenge,
    student_state,
    independent_answer
):

    prompt = f"""
Give formative feedback on this student's
Data Science / AI reasoning.

Original challenge:

{json.dumps(challenge, ensure_ascii=False)}

Student reasoning:

{json.dumps(student_state, ensure_ascii=False)}

Independent response:

{independent_answer}

Do NOT give a numerical score.

Do NOT claim this proves intelligence or lasting learning.

Give specific evidence-based feedback.

Return ONLY valid JSON:

{{
    "problem_investigation": "...",
    "data_reasoning": "...",
    "evidence_usage": "...",
    "alternative_thinking": "...",
    "experiment_design": "...",
    "technical_tradeoffs": "...",
    "strengths": [
        "...",
        "..."
    ],
    "growth_opportunity": "...",
    "concepts_practiced": [
        "...",
        "..."
    ],
    "next_practice": "..."
}}
"""

    try:

        response = get_client().chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You provide calibrated formative "
                        "feedback for Data Science learning. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            max_tokens=750
        )

        return parse_json(
            response.choices[0].message.content or ""
        )

    except Exception:

        return {
            "problem_investigation": (
                "You attempted to investigate before "
                "jumping directly to a solution."
            ),

            "data_reasoning": (
                "Connect technical claims to measurable evidence."
            ),

            "evidence_usage": (
                "Identify evidence that distinguishes "
                "between competing explanations."
            ),

            "alternative_thinking": (
                "Consider at least two plausible explanations."
            ),

            "experiment_design": (
                "Define what changes and what you will measure."
            ),

            "technical_tradeoffs": (
                "Explain what you gain and give up "
                "with your chosen approach."
            ),

            "strengths": [
                "You formed an initial explanation.",
                "You identified a direction for investigation."
            ],

            "growth_opportunity": (
                "State what result would change your mind."
            ),

            "concepts_practiced": [
                challenge.get("skill", "Data Science reasoning")
            ],

            "next_practice": (
                "Try another scenario with competing "
                "explanations."
            )
        }
