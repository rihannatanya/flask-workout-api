from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

CATEGORIES = ("strength", "cardio", "flexibility", "balance")


class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        db.CheckConstraint("length(name) >= 2", name="ck_exercise_name_length"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(20), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    workouts = db.relationship(
        "Workout", secondary="workout_exercises", viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be blank.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise", secondary="workout_exercises", viewonly=True
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is not None and len(value) > 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
        db.CheckConstraint("reps IS NULL OR reps > 0", name="ck_reps_positive"),
        db.CheckConstraint("sets IS NULL OR sets > 0", name="ck_sets_positive"),
        db.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_duration_seconds_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps", "sets", "duration_seconds")
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0.")
        return value