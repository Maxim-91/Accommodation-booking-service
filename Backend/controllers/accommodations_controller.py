from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from custom_exceptions.not_found_exception import NotFoundException
from dependencies import get_logged_in_user
from dtos.accommodations import (
    AccommodationDto,
    CreateAccommodationReq,
    UpdateAccommodationReq,
)
from factories.services import accommodation_service_factory
from models import User
from services.accommodation_service import AccommodationService

router = APIRouter(
    prefix="/api/accommodations",
    tags=["accommodations"],
)

AccommodationServ = Annotated[
    AccommodationService,
    Depends(accommodation_service_factory),
]

CurrentUser = Annotated[User, Depends(get_logged_in_user)]


@router.get("/", response_model=list[AccommodationDto])
def get_all_accommodations(
    service: AccommodationServ,
) -> list[AccommodationDto]:
    return service.get_all()


@router.get(
    "/{accommodation_id}",
    response_model=AccommodationDto,
)
def get_accommodation_by_id(
    accommodation_id: int,
    service: AccommodationServ,
) -> AccommodationDto:
    try:
        return service.get_by_id(accommodation_id)
    except NotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "/",
    response_model=AccommodationDto,
    status_code=status.HTTP_201_CREATED,
)
def create_accommodation(
    request: CreateAccommodationReq,
    current_user: CurrentUser,
    service: AccommodationServ,
) -> AccommodationDto:
    return service.create(
        request,
        owner_id=current_user.id,
    )


@router.put(
    "/{accommodation_id}",
    response_model=AccommodationDto,
)
def update_accommodation(
    accommodation_id: int,
    request: UpdateAccommodationReq,
    service: AccommodationServ,
) -> AccommodationDto:
    try:
        return service.update(accommodation_id, request)
    except NotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.delete(
    "/{accommodation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_accommodation(
    accommodation_id: int,
    service: AccommodationServ,
) -> None:
    try:
        service.delete(accommodation_id)
    except NotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    