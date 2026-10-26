from sqlalchemy import select
from sqlalchemy.orm import Session

from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.not_found_exception import NotFoundException
from dtos.accommodations import (
    CreateAccommodationReq,
    UpdateAccommodationReq,
)
from models import Accommodation


class AccommodationService:
    def __init__(self, repository: Session):
        self._repository = repository

    def get_all(self) -> list[Accommodation]:
        statement = select(Accommodation).order_by(Accommodation.id)
        return list(self._repository.scalars(statement).all())

    def get_by_id(self, accommodation_id: int) -> Accommodation:
        accommodation = self._repository.get(
            Accommodation, accommodation_id
        )

        if accommodation is None:
            raise NotFoundException(
                f"Accommodation {accommodation_id} not found"
            )

        return accommodation

    def get_owned_by_id(
        self,
        accommodation_id: int,
        owner_id: int,
    ) -> Accommodation:
        accommodation = self.get_by_id(accommodation_id)

        if accommodation.owner_id != owner_id:
            raise ForbiddenException("You do not own this accommodation")

        return accommodation

    def create(
        self,
        request: CreateAccommodationReq,
        owner_id: int,
    ) -> Accommodation:
        accommodation = Accommodation(
            title=request.title,
            description=request.description,
            location=request.location,
            price_per_night=request.price_per_night,
            max_guests=request.max_guests,
            is_active=request.is_active,
            owner_id=owner_id,
        )

        self._repository.add(accommodation)
        self._repository.commit()
        self._repository.refresh(accommodation)

        return accommodation

    def update(
        self,
        accommodation_id: int,
        request: UpdateAccommodationReq,
        owner_id: int,
    ) -> Accommodation:
        accommodation = self.get_owned_by_id(
            accommodation_id,
            owner_id,
        )

        accommodation.title = request.title
        accommodation.description = request.description
        accommodation.location = request.location
        accommodation.price_per_night = request.price_per_night
        accommodation.max_guests = request.max_guests
        accommodation.is_active = request.is_active

        self._repository.commit()
        self._repository.refresh(accommodation)
        return accommodation

    def delete(
        self,
        accommodation_id: int,
        owner_id: int,
    ) -> None:
        accommodation = self.get_owned_by_id(
            accommodation_id,
            owner_id,
        )

        self._repository.delete(accommodation)
        self._repository.commit()
