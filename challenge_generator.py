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
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Secrets."
        )

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


def generate_challenge(domain, difficulty):

    prompt = f"""
Create one fresh practical Data Science / AI thinking challenge.

SKILL:
{domain["description"]}

CONCEPTS:
{", ".join(domain["concepts"])}

DIFFICULTY:
{difficulty}

Requirements:

- Create a realistic university-level Data Science or AI scenario.
- The problem should require investigation and reasoning.
- There should NOT be one immediately obvious answer.
- Give incomplete information so the student must investigate.
- Include realistic constraints.
- Do not turn it into a simple definition question.
- Do not reveal the intended solution.
- Do not solve the problem.
- Keep the scenario understandable for a student.
- Make it different from common textbook examples.
- The challenge should encourage evidence, assumptions,
  alternatives and experiments.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "...",
    "skill": "...",
    "difficulty": "...",
    "scenario": "...",
    "known_information": [
        "...",
        "..."
    ],
    "constraints": [
        "...",
        "..."
    ],
    "initial_question": "...",
    "learning_goal": "..."
}}
"""

    try:

        response = get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create high-quality practical "
                        "Data Science learning challenges. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=700
        )

        content = response.choices[0].message.content or ""

        return parse_json(content)

    except Exception:

        return {
            "title": "Investigate a Model Performance Mystery",

            "skill": "Data Science",

            "difficulty": difficulty,

            "scenario": (
                "An ML model performs well during testing, "
                "but users report that some predictions are "
                "incorrect in real-world use. You have limited "
                "information and need to investigate before "
                "changing the system."
            ),

            "known_information": [
                "Overall performance looks acceptable.",
                "Some user groups report more errors."
            ],

            "constraints": [
                "You cannot immediately collect a large new dataset.",
                "You need evidence before changing the model."
            ],

            "initial_question": (
                "What would you investigate first, and why?"
            ),

            "learning_goal": (
                "Practice evidence-based investigation before "
                "selecting a solution."
            )
        }
