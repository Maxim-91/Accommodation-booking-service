from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from controllers.accommodations_controller import router as accommodations_router
from controllers.auth_controller import router as auth_router
from database import engine

from pathlib import Path
from dotenv import load_dotenv

# Locate the project root (move up one level from main.py)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Loading .env directly from the root folder
load_dotenv(PROJECT_ROOT / ".env")

app = FastAPI(
    title="Accommodation Booking Service API",
    version="0.1.4",
)
app.include_router(accommodations_router)
app.include_router(auth_router)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db", tags=["Health"])
def database_health_check() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )
