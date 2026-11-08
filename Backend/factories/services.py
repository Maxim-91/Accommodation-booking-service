from fastapi import Depends
from sqlalchemy.orm import Session
import os
from database import get_db
from services.accommodation_service import AccommodationService
from services.user_service import UserService
from tools.abc_token_tool import ABCTokenTool
from tools.symmetric_token_tool import SymmetricTokenTool
from tools.asymmetric_token_tool import AsymmetricTokenTool
from services.booking_service import BookingService


def token_tool_factory() -> ABCTokenTool:
    algorithm = os.getenv("TOKEN_ALGORITHM", "HS512").upper()

    if algorithm == "HS512":
        return SymmetricTokenTool()

    if algorithm == "RS256":
        return AsymmetricTokenTool()

    raise ValueError(f"Unsupported token algorithm: {algorithm}")

def accommodation_service_factory(
    repository: Session = Depends(get_db),
) -> AccommodationService:
    return AccommodationService(repository)

def user_service_factory(
    repository: Session = Depends(get_db),
    token_tool: ABCTokenTool = Depends(token_tool_factory),
) -> UserService:
    return UserService(repository, token_tool)

def booking_service_factory(
    repository: Session = Depends(get_db),
) -> BookingService:
    return BookingService(repository)
