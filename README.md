# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for personal trainers to track
workouts and the reusable exercises inside them.

## Installation
```
pipenv install
pipenv shell
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial schema"
flask db upgrade
python seed.py
```

## Run
```
flask run
```

## Models
- **Workout**: date, duration_minutes, notes
- **Exercise**: name (unique), category, equipment_needed
- **WorkoutExercise**: joins a workout and exercise, with reps, sets, duration_seconds

## Endpoints
| Method | Route | Description |
|---|---|---|
| GET | /workouts | List all workouts with their exercises |
| GET | /workouts/<id> | Get one workout |
| POST | /workouts | Create a workout (`date`, `duration_minutes`, optional `notes`) |
| DELETE | /workouts/<id> | Delete a workout |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Get one exercise |
| POST | /exercises | Create an exercise (`name`, `category`, optional `equipment_needed`) |
| DELETE | /exercises/<id> | Delete an exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout (`reps` + `sets`, or `duration_seconds`) |

## Validations
- **Table constraints:** unique exercise name, positive duration/reps/sets (CHECK), unique workout/exercise pair
- **Model validations:** non-blank name, valid category, positive numbers, notes length
- **Schema validations:** length/range/choice checks, plus a rule requiring reps and sets, or a duration