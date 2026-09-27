import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


def generate_nutrition_tip_with_flash(goal: str) -> str:
    fallback = {
        "weight loss": "Prioritize vegetables, protein-rich foods, whole grains, adequate water, and sensible portions. Avoid extreme restriction.",
        "muscle gain": "Include a protein source in regular meals, eat enough overall, stay hydrated, and pair nutrition with progressive resistance training.",
        "general fitness": "Aim for balanced meals with protein, vegetables, fruit, whole grains and healthy fats, plus regular hydration and recovery.",
    }
    default_tip = fallback.get(goal.lower(), fallback["general fitness"])

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return default_tip

    try:
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash")
        prompt = (
            f"Give one clear, practical nutrition or recovery tip for someone focused on "
            f"'{goal}'. Keep it friendly, concise and easy to understand. "
            "Do not provide medical treatment or extreme dieting advice."
        )
        response = client.models.generate_content(model=model, contents=prompt)
        return (response.text or "").strip() or default_tip
    except Exception:
        return default_tip
