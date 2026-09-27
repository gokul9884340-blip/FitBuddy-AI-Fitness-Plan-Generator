from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
    get_all_users,
)

from gemini_generator import generate_workout_gemini
from gemini_flash_generator import generate_nutrition_tip_with_flash
from updated_plan import update_workout_plan


# --------------------------------------------------
# CREATE FASTAPI APP
# --------------------------------------------------

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")


# --------------------------------------------------
# TEMPLATES AND STATIC FILES
# --------------------------------------------------

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# GENERATE WORKOUT PLAN
# --------------------------------------------------

@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):

    # Import database objects
    from database import SessionLocal, User

    # Find the next available user ID
    db = SessionLocal()

    try:
        last_user = (
            db.query(User)
            .order_by(User.id.desc())
            .first()
        )

        if last_user:
            user_id = last_user.id + 1
        else:
            user_id = 1

    finally:
        db.close()

    # Create user information
    user = {
        "name": name,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
    }

    # Save user in database
    save_user(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    # Generate workout plan
    plan = generate_workout_gemini(user)

    # Save workout plan
    save_plan(
        user_id=user_id,
        plan=plan
    )

    # Generate nutrition tip
    nutrition = generate_nutrition_tip_with_flash(goal)

    # Show result page
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "user_id": user_id,
            "plan": plan,
            "nutrition": nutrition,
            "updated_plan": None,
        }
    )


# --------------------------------------------------
# UPDATE WORKOUT PLAN USING FEEDBACK
# --------------------------------------------------

@app.post(
    "/feedback/{user_id}",
    response_class=HTMLResponse
)
def feedback(
    request: Request,
    user_id: int,
    feedback: str = Form(...)
):

    # Get user
    user = get_user(user_id)

    # Get original workout plan
    original = get_original_plan(user_id)

    # If user or plan doesn't exist
    if not user or not original:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    # Generate updated workout plan
    updated = update_workout_plan(
        original_plan=original,
        user_feedback=feedback
    )

    # Save updated plan
    update_plan(
        user_id=user_id,
        updated_text=updated
    )

    # Generate fresh nutrition tip
    nutrition = generate_nutrition_tip_with_flash(
        user.goal
    )

    # Prepare user data
    user_data = {
        "name": user.name,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
    }

    # Show updated result
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user_data,
            "user_id": user_id,
            "plan": original,
            "nutrition": nutrition,
            "updated_plan": updated,
            "feedback": feedback,
        }
    )


# --------------------------------------------------
# ADMIN - VIEW ALL USERS
# --------------------------------------------------

@app.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(request: Request):

    # Get all users and their plans
    users = get_all_users()

    # Show admin page
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )