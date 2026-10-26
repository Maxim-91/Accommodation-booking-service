from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from services.accommodation_service import AccommodationService
from services.user_service import UserService
from tools.abc_token_tool import ABCTokenTool
from tools.symmetric_token_tool import SymmetricTokenTool


def token_tool_factory() -> ABCTokenTool:
    return SymmetricTokenTool()

def accommodation_service_factory(
    repository: Session = Depends(get_db),
) -> AccommodationService:
    return AccommodationService(repository)

def user_service_factory(
    repository: Session = Depends(get_db),
    token_tool: ABCTokenTool = Depends(token_tool_factory),
) -> UserService:
    return UserService(repository, token_tool)
