from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


def error(message, status):
    return jsonify({"error": message}), status


def save(obj):
    """Add and commit an object, translating DB/model errors into responses."""
    try:
        db.session.add(obj)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return error(str(e), 400)
    except IntegrityError:
        db.session.rollback()
        return error("Violates a database constraint (duplicate or invalid value).", 409)
    return None


# ---------- Workouts ----------
@app.get("/workouts")
def list_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error("Workout not found.", 404)
    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
    except ValidationError as e:
        return error(e.messages, 400)
    try:
        workout = Workout(**data)
    except ValueError as e:
        return error(str(e), 400)
    failure = save(workout)
    if failure:
        return failure
    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error("Workout not found.", 404)
    db.session.delete(workout)
    db.session.commit()
    return "", 204


# ---------- Exercises ----------
@app.get("/exercises")
def list_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error("Exercise not found.", 404)
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
    except ValidationError as e:
        return error(e.messages, 400)
    try:
        exercise = Exercise(**data)
    except ValueError as e:
        return error(str(e), 400)
    failure = save(exercise)
    if failure:
        return failure
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error("Exercise not found.", 404)
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


# ---------- Add exercise to workout ----------
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return error("Workout or exercise not found.", 404)

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
    except ValidationError as e:
        return error(e.messages, 400)

    try:
        link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValueError as e:
        return error(str(e), 400)
    failure = save(link)
    if failure:
        return failure
    return jsonify(workout_exercise_schema.dump(link)), 201


if __name__ == "__main__":
    app.run(debug=True)