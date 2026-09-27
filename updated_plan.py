import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    if not user_feedback.strip():
        return original_plan

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return original_plan + f"\n\nFEEDBACK UPDATE:\n{user_feedback}\n\nSuggested change: Adjust the relevant exercises while keeping the remaining weekly structure unchanged."

    try:
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
        prompt = f"""
You are a professional fitness trainer assistant.

Here is the original 7-day workout plan:
{original_plan}

User feedback:
{user_feedback}

Revise only the relevant parts of the workout plan according to the feedback.
Keep the 7-day structure and all useful parts unchanged where possible.
Return the complete updated plan.
"""
        response = client.models.generate_content(model=model, contents=prompt)
        return (response.text or "").strip() or original_plan
    except Exception:
        return original_plan + f"\n\nFEEDBACK UPDATE:\n{user_feedback}"
