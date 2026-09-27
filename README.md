# FitBuddy – AI Fitness Plan Generator

## Features
- FastAPI backend
- HTML + Jinja2 frontend
- SQLite + SQLAlchemy persistence
- Gemini workout generation
- Gemini Flash nutrition/recovery tip
- Feedback-based plan update
- Admin page showing all users and original/updated plans
- Local fallback plan if no Gemini API key is configured

## Run in VS Code

1. Open this folder in VS Code.
2. Open Terminal.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it on Windows:
   `venv\Scripts\activate`
5. Install packages:
   `pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `.env`.
8. Start:
   `uvicorn main:app --reload`
9. Open:
   `http://127.0.0.1:8000`

If you do not have an API key yet, the app still runs using the built-in fallback generator.
