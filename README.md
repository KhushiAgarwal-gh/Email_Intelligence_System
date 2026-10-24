# Email Intelligence System

A beginner-friendly full-stack app that **classifies emails**, **detects priority**, **summarizes** them, and shows the results on a dashboard.

## Architecture

```
Browser (Next.js dashboard)
        |
        |  HTTP JSON
        v
FastAPI backend
        |
        +-- PostgreSQL (emails table)
        +-- LLM API if LLM_API_KEY is set
        +-- Rule-based fallback if the key is missing
```

| Layer | Technology | Why |
|---|---|---|
| Dashboard | Next.js, React, TypeScript, Tailwind | Modern, easy to show as a portfolio UI |
| API | Python, FastAPI | Simple, auto docs at `/docs` |
| Database | PostgreSQL + SQLAlchemy + Alembic | Reliable storage and migrations |
| AI | OpenAI-compatible LLM **or** keyword rules | Works without a paid API key |
| Run locally | Docker Compose | Postgres without a manual Windows install |
| CI | GitHub Actions | Tests and image builds on every push |

## Folder structure

```
.
├── backend/                 FastAPI app, tests, Alembic
│   ├── app/
│   │   ├── main.py          App, CORS, health
│   │   ├── config.py        Environment variables
│   │   ├── database.py      SQLAlchemy engine
│   │   ├── models.py        Email table
│   │   ├── schemas.py       Request/response shapes
│   │   ├── routers/emails.py
│   │   └── services/        classify, priority, summarize, LLM
│   ├── scripts/seed.py      Demo emails (safe to re-run)
│   └── tests/
├── frontend/                Next.js dashboard
├── docker-compose.yml       db + backend + frontend
├── .github/workflows/       CI and optional deploy reminder
├── render.yaml              Cloud blueprint (do not apply until you want an account)
└── docs/DEPLOYMENT.md
```

## Prerequisites

- Docker Desktop for Windows (recommended: includes PostgreSQL)
- Or: Python 3.11+, Node.js 20+, and a running Postgres
- Optional: an OpenAI (or compatible) API key

## Fastest start (Docker)

In PowerShell, from this folder:

```powershell
cd "c:\Users\Khushi Agarwal\Desktop\Email Intelligence System"
docker compose up --build
```

Then open:

- Dashboard: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

Load demo emails (in a second PowerShell window):

```powershell
docker compose exec backend python -m scripts.seed
```

Stop:

```powershell
docker compose down
```

Keep the database:

```powershell
docker compose down
# data stays in the postgres_data volume
```

## Environment variables

Copy examples. **Never commit `.env` files with real keys.**

Root `.env` (used by Compose for the LLM key):

```
LLM_API_KEY=
LLM_API_BASE=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

`backend/.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/email_intelligence
FRONTEND_ORIGINS=http://localhost:3000
LLM_API_KEY=
LLM_API_BASE=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

`frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If `LLM_API_KEY` is empty, every analysis uses the **rule-based fallback**. The API stores `analysis_source` as `llm`, `fallback`, or `manual`.

## Run without Docker (API + dashboard only)

PostgreSQL must already be running on port 5432, **or** start just the database:

```powershell
docker compose up db -d
```

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

If PowerShell blocks venv scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Frontend (new window):

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | API + database status |
| POST | `/emails` | Create and auto-analyze |
| GET | `/emails` | List with `search`, `category`, `priority`, `page`, `page_size` |
| GET | `/emails/stats` | Dashboard counts |
| GET | `/emails/{id}` | One email |
| PATCH | `/emails/{id}` | Update fields |
| POST | `/emails/{id}/analyze` | Run analysis again |
| DELETE | `/emails/{id}` | Delete |

Interactive docs: http://127.0.0.1:8000/docs

## Tests

Backend (SQLite in-memory; **no live LLM required**):

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

Frontend:

```powershell
cd frontend
npm run lint
npm run build
```

GitHub Actions (`.github/workflows/ci.yml`) runs those checks **after you push** to GitHub. They have not run on GitHub until that happens.

## Cloud deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). Nothing is deployed from this repo automatically. Do not apply `render.yaml` until you explicitly want a Render account.

Suggested GitHub Secrets later: `LLM_API_KEY`, plus any host-specific tokens. Keep them in GitHub Secrets, never in files.

## Troubleshooting

| Problem | What to try |
|---|---|
| `/health` says database unavailable | `docker compose up db -d` and wait until healthy |
| Dashboard shows demo inbox | API is down or the database is empty; seed with `python -m scripts.seed` |
| CORS error in the browser | Set `FRONTEND_ORIGINS` to the exact frontend origin |
| LLM errors / 429 | App falls back to rules; check `analysis_source` |
| Alembic fails because tables exist | `alembic stamp head` |
| Port 5432 already in use | Stop local Postgres or change the Compose port mapping |

## What you still do manually

1. Install Docker Desktop (or Postgres) and start it.
2. Optional: add `LLM_API_KEY` for LLM summaries.
3. Push to GitHub to actually run CI.
4. Create a Render/Railway account only when you want cloud hosting.
