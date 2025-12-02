# Spy Cat Agency API

![ruff](https://img.shields.io/badge/ruff-checked-40c4ff?logo=ruff&logoColor=white) ![black](https://img.shields.io/badge/black-140f46?logo=python&logoColor=white) ![fastapi](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![postgres](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

Async FastAPI backend for managing spy cats, missions, and targets. PostgreSQL via SQLAlchemy async; breeds validated live against TheCatAPI. Licensed under [MIT](LICENSE).

## Requirements
- Python 3.11
- PostgreSQL running locally (or connection string via `DATABASE_URL`)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
cp .env.example .env
```

Update `.env` to match your database settings.

## Run
```bash
uvicorn app.main:app --reload
```

## Linting
```bash
ruff check .
black --check .
```

## Manual API smoke (httpie)
```bash
# Health
http GET :8000/health

# Create cat (breed is validated via TheCatAPI)
http POST :8000/cats name="Kitty" years_experience:=2 breed="Abyssinian" salary="5000.00"

# Create mission with targets (1..3)
http POST :8000/missions targets:='[{"name":"Target A","country":"US","notes":"note"}]'

# Assign cat to mission
http POST :8000/missions/<mission_id>/assign cat_id=<cat_id>

# Update target notes / mark complete
http PATCH :8000/missions/<mission_id>/targets/<target_id> notes="done" complete:=true
```

## Postman
- Ready-to-use collection: `postman/SpyCat.postman_collection.json`
- Variable `base_url` defaults to `http://localhost:8000`; fill in `:cat_id`, `:mission_id`, `:target_id` with actual UUIDs before sending.
- You can also import `openapi.json` generated from `/openapi.json` if you prefer to regenerate the collection.

## Endpoint overview
- `GET /health` — service health.
- `POST /cats` — create cat (breed validation).
- `GET /cats` / `GET /cats/{cat_id}` — list or fetch cat.
- `PATCH /cats/{cat_id}/salary` — update salary.
- `DELETE /cats/{cat_id}` — remove cat (blocked if assigned).
- `POST /missions` — create mission with 1–3 targets.
- `GET /missions` / `GET /missions/{mission_id}` — list or fetch mission with targets.
- `POST /missions/{mission_id}/assign` — assign cat with busy checks.
- `PATCH /missions/{mission_id}/targets/{target_id}` — update notes/complete (guards on completed).
- `DELETE /missions/{mission_id}` — delete if no assigned cat.

## Notes
- No authentication (per requirements).
- Tables are created at startup via SQLAlchemy metadata (migrations are optional).
- Salaries use `DECIMAL(10,2)`.
