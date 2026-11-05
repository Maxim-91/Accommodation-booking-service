
from sqlalchemy import select
from sqlalchemy.orm import Session

from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.not_found_exception import NotFoundException
from dtos.accommodations import (
    CreateAccommodationReq,
    UpdateAccommodationReq,
)
from models import Accommodation, Amenity


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
            raise ForbiddenException(
                "You do not own this accommodation"
            )

        return accommodation

    def create(
        self,
        request: CreateAccommodationReq,
        owner_id: int,
    ) -> Accommodation:
        amenities = self._get_amenities_by_ids(request.amenity_ids)

        accommodation = Accommodation(
            title=request.title,
            description=request.description,
            location=request.location,
            price_per_night=request.price_per_night,
            max_guests=request.max_guests,
            amenities=amenities,
            is_active=request.is_active,
            owner_id=owner_id,
        )

        try:
            self._repository.add(accommodation)
            self._repository.commit()
            self._repository.refresh(accommodation)
        except Exception:
            self._repository.rollback()
            raise

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

        amenities = self._get_amenities_by_ids(request.amenity_ids)

        accommodation.title = request.title
        accommodation.description = request.description
        accommodation.location = request.location
        accommodation.price_per_night = request.price_per_night
        accommodation.max_guests = request.max_guests
        accommodation.amenities = amenities
        accommodation.is_active = request.is_active

        try:
            self._repository.commit()
            self._repository.refresh(accommodation)
        except Exception:
            self._repository.rollback()
            raise

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

        try:
            self._repository.delete(accommodation)
            self._repository.commit()
        except Exception:
            self._repository.rollback()
            raise

    def _get_amenities_by_ids(
        self,
        amenity_ids: list[int],
    ) -> list[Amenity]:
        unique_ids = set(amenity_ids)

        if not unique_ids:
            return []

        statement = select(Amenity).where(
            Amenity.id.in_(unique_ids)
        )
        amenities = list(self._repository.scalars(statement).all())

        if len(amenities) != len(unique_ids):
            raise NotFoundException(
                "One or more amenities were not found"
            )

        return amenities
