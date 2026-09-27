import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


def _fallback_plan(user):
    goal = user["goal"]
    intensity = user["intensity"]
    return f"""7-DAY FITBUDDY WORKOUT PLAN

User: {user["name"]}
Goal: {goal}
Intensity: {intensity}

DAY 1 – FULL BODY
Warm-up: 5–10 minutes brisk walking and mobility.
Main workout:
• Squats – 3 sets × 12 reps
• Push-ups – 3 sets × 8–12 reps
• Glute bridges – 3 sets × 15 reps
• Plank – 3 × 30 seconds
Cooldown: 5 minutes stretching.

DAY 2 – CARDIO
Warm-up: 5 minutes easy walking.
Main workout:
• Brisk walk/jog – 20–30 minutes
• Bodyweight lunges – 3 × 10 each leg
Cooldown: 5–10 minutes stretching.

DAY 3 – UPPER BODY
Warm-up: 5–10 minutes shoulder and arm mobility.
Main workout:
• Incline push-ups – 3 × 10
• Backpack rows – 3 × 12
• Shoulder taps – 3 × 10 each side
Cooldown: gentle upper-body stretches.

DAY 4 – ACTIVE RECOVERY
20–30 minutes easy walking plus mobility or beginner yoga.

DAY 5 – LOWER BODY
Warm-up: 5–10 minutes.
Main workout:
• Squats – 3 × 12
• Reverse lunges – 3 × 10 each leg
• Calf raises – 3 × 15
• Glute bridges – 3 × 15
Cooldown: lower-body stretching.

DAY 6 – FULL BODY
Warm-up: 5–10 minutes.
Main workout:
• Step-ups – 3 × 10 each leg
• Push-ups – 3 × 8–12
• Backpack rows – 3 × 12
• Plank – 3 × 30–45 seconds
Cooldown: 5 minutes.

DAY 7 – REST & RECOVERY
Easy walking, hydration and gentle stretching.

SAFETY
Start at a comfortable level, maintain good form, and stop if you feel pain, dizziness, or unusual shortness of breath. This is general fitness information, not medical advice.
"""


def generate_workout_gemini(user: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return _fallback_plan(user)

    try:
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
        prompt = f"""
You are FitBuddy, a professional fitness trainer assistant.
Create a personalized 7-day workout plan.

User:
Name: {user["name"]}
Age: {user["age"]}
Weight: {user["weight"]} kg
Goal: {user["goal"]}
Intensity: {user["intensity"]}

For every day include:
- Warm-up (5–10 minutes)
- Main workout with exercise details, sets and reps
- Cooldown or recovery tip

Include one rest/recovery day. Keep the plan practical and beginner-friendly.
Do not diagnose medical conditions or prescribe treatment.
"""
        response = client.models.generate_content(model=model, contents=prompt)
        return (response.text or "").strip() or _fallback_plan(user)
    except Exception as exc:
        return _fallback_plan(user) + f"\n\n[Gemini unavailable; fallback plan used: {exc}]"
