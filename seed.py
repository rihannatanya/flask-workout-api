from datetime import date, timedelta

from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    run = Exercise(name="Running", category="cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="balance", equipment_needed=False)
    stretch = Exercise(name="Hamstring Stretch", category="flexibility")
    db.session.add_all([squat, pushup, run, plank, stretch])

    today = date.today()
    leg_day = Workout(date=today, duration_minutes=45, notes="Leg day")
    cardio = Workout(date=today - timedelta(days=2), duration_minutes=30)
    db.session.add_all([leg_day, cardio])
    db.session.flush()

    db.session.add_all([
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, sets=4, reps=8),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=plank.id, duration_seconds=60),
        WorkoutExercise(workout_id=cardio.id, exercise_id=run.id, duration_seconds=1200),
        WorkoutExercise(workout_id=cardio.id, exercise_id=pushup.id, sets=3, reps=15),
    ])
    db.session.commit()
    print("Database seeded.")