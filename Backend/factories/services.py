from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from services.accommodation_service import AccommodationService
from services.user_service import UserService


def accommodation_service_factory(
    repository: Session = Depends(get_db),
) -> AccommodationService:
    return AccommodationService(repository)

def user_service_factory(
    repository: Session = Depends(get_db),
) -> UserService:
    return UserService(repository)
