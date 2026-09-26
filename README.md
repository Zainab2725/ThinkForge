# ThinkForge

ThinkForge helps university students practice independent problem-solving. It uses AI as a hint-first coach, not an answer machine.

## MVP features
- Five real-world student challenges
- Four-stage thinking workspace: Understand, Imagine, Reason, Test
- One Groq GPT-OSS 20B coach
- Mini-project idea and experiment plan
- New independent skill check, with AI disabled while answering
- Formative feedback and session progress
- Streamlit session-state storage (not persistent)

## Run / deploy
1. Create a GitHub repository and upload the files in this project.
2. In Streamlit Community Cloud, create an app from that repository and set the main file to `app.py`.
3. In Streamlit app settings, add a secret named `GROQ_API_KEY`:
   `GROQ_API_KEY = "your-key"`
4. Deploy.

Never commit `.streamlit/secrets.toml`. The provided `secrets.toml.example` is only a template.

## Model
The app calls Groq's OpenAI-compatible endpoint using `openai/gpt-oss-20b`. API availability, rate limits, and pricing depend on Groq's current terms and account.

## Important limitations
- Progress and saved work live in Streamlit session state and can be lost when the session resets.
- The independent check disables the in-app coach, but it cannot technically prevent students from using another tab, device, or external AI.
- AI feedback is formative and may be inaccurate. It is not a validated measure of intelligence, creativity, or long-term learning.
- This is an MVP, not a secure proctoring or research-grade assessment system.

## Project structure
- `app.py` — Streamlit interface and flow
- `challenges.py` — five starter challenges
- `coach.py` — Groq coach and formative feedback
- `requirements.txt` — dependencies
