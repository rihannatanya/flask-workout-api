from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1, max=1000), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1, max=100), allow_none=True)
    duration_seconds = fields.Int(
        validate=validate.Range(min=1, max=36000), allow_none=True
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_reps_sets_or_duration(self, data, **kwargs):
        has_reps_sets = data.get("reps") is not None and data.get("sets") is not None
        has_duration = data.get("duration_seconds") is not None
        if not (has_reps_sets or has_duration):
            raise ValidationError(
                "Provide both reps and sets, or a duration_seconds value."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True, validate=validate.Range(min=1, max=600)
    )
    notes = fields.Str(validate=validate.Length(max=500), allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()