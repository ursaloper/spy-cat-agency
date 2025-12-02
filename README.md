# Spy Cat Agency API

Async FastAPI backend for managing spy cats, missions, and targets. Uses PostgreSQL via SQLAlchemy async and validates cat breeds against TheCatAPI.

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

Edit `.env` if your database credentials differ.

## Run
```bash
uvicorn app.main:app --reload
```

## Linting
```bash
ruff check .
black --check .
```

## Notes
- No authentication by design (per task).
- Migrations are optional; database tables will be created at startup in the app lifespan hook.
- Salaries use `DECIMAL(10,2)`.

Postman collection and detailed endpoint docs will be added later in the project flow.
