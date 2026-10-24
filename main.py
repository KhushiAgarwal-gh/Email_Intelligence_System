import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_ORIGINS
from app.database import Base, database_is_reachable, engine
from app.models import Email  # noqa: F401
from app.routers import emails

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    reachable, error = database_is_reachable()
    if reachable:
        Base.metadata.create_all(bind=engine)
        logger.info("Database connected and tables are ready.")
    else:
        logger.warning("Database is not reachable yet: %s", error)
    yield


app = FastAPI(
    title="Email Intelligence System",
    description="API for email classification, priority detection, and summarization.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emails.router)


@app.get("/")
def root():
    return {"message": "Email Intelligence System API is running", "docs": "/docs"}


@app.get("/health")
def health():
    reachable, error = database_is_reachable()
    if reachable:
        return {"status": "ok", "database": "connected"}
    return {
        "status": "degraded",
        "database": "unavailable",
        "detail": error,
        "hint": "Start PostgreSQL with: docker compose up db -d",
    }
