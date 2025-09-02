# Shelter Capacity API (Boilerplate)

## Quickstart
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

## Test
curl http://localhost:8000/health
curl http://localhost:8000/version

## Notes
- Dev DB: SQLite (file dev.db).
- Prod: set `DATABASE_URL` to Postgres on Railway/Render.
