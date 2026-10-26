from sqlalchemy import select
from sqlalchemy.orm import Session

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

    def create(
        self, request: CreateAccommodationReq
    ) -> Accommodation:
        accommodation = Accommodation(**request.model_dump())
        self._repository.add(accommodation)
        self._repository.commit()
        self._repository.refresh(accommodation)
        return accommodation

    def update(
        self,
        accommodation_id: int,
        request: UpdateAccommodationReq,
    ) -> Accommodation:
        accommodation = self.get_by_id(accommodation_id)

        for field, value in request.model_dump().items():
            setattr(accommodation, field, value)

        self._repository.commit()
        self._repository.refresh(accommodation)
        return accommodation

    def delete(self, accommodation_id: int) -> None:
        accommodation = self.get_by_id(accommodation_id)
        self._repository.delete(accommodation)
        self._repository.commit()
