from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(50), nullable=False)
    intensity = Column(String(30), nullable=False)


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = name
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity
        else:
            user = User(
                id=user_id,
                name=name,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
            )
            db.add(user)
        db.commit()
    finally:
        db.close()


def save_plan(user_id: int, plan: str):
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            workout.original_plan = plan
            workout.updated_plan = None
        else:
            workout = WorkoutPlan(user_id=user_id, original_plan=plan)
            db.add(workout)
        db.commit()
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str):
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            workout.updated_plan = updated_text
            db.commit()
    finally:
        db.close()


def get_original_plan(user_id: int):
    db = SessionLocal()
    try:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        db.close()


def get_user(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id.desc()).all()
        result = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            result.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated",
            })
        return result
    finally:
        db.close()
