import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from controllers.accommodations_controller import router as accommodations_router
from controllers.auth_controller import router as auth_router
from controllers.bookings_controller import router as bookings_router
from database import engine
from pathlib import Path
from dotenv import load_dotenv
from custom_exceptions.booking_conflict_exception import BookingConflictException
from custom_exceptions.conflict_exception import ConflictException
from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.unauthorized_exception import UnauthorizedException

# Locate the project root (move up one level from main.py)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Loading .env directly from the root folder
load_dotenv(PROJECT_ROOT / ".env")

app = FastAPI(
    title="Accommodation Booking Service API",
    version="0.2.0",
)
logger = logging.getLogger(__name__)
app.include_router(accommodations_router)
app.include_router(auth_router)
app.include_router(bookings_router)


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
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"title": "not found", "detail": str(exc)},
    )

@app.exception_handler(ForbiddenException)
async def forbidden_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"title": "forbidden", "detail": str(exc)},
    )

@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"title": "unauthorized", "detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(ConflictException)
async def conflict_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"title": "conflict", "detail": str(exc)},
    )

@app.exception_handler(BookingConflictException)
async def booking_conflict_handler(request: Request, exc: BookingConflictException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"title": "booking conflict", "detail": str(exc) or "Booking violates a business rule"},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception on path %s", request.url.path, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={"title": "internal server error", "detail": "An unexpected error occurred"},
    )
