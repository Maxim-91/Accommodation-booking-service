from fastapi import APIRouter, Depends, HTTPException, status

from custom_exceptions.booking_conflict_exception import (
    BookingConflictException,
)
from custom_exceptions.not_found_exception import NotFoundException
from dependencies import get_logged_in_user
from dtos.bookings import CreateBookingRequest, BookingResponse
from factories.services import booking_service_factory
from models import User
from services.booking_service import BookingService


router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    request: CreateBookingRequest,
    current_user: User = Depends(get_logged_in_user),
    service: BookingService = Depends(booking_service_factory),
) -> BookingResponse:
    try:
        booking = service.create_booking(
            user_id=current_user.id,
            accommodation_id=request.accommodation_id,
            check_in=request.check_in,
            check_out=request.check_out,
            guests=request.guests,
        )
        return BookingResponse.model_validate(booking)

    except NotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except BookingConflictException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_logged_in_user),
    service: BookingService = Depends(booking_service_factory),
) -> list[BookingResponse]:
    bookings = service.get_bookings_by_user(current_user.id)
    return [
        BookingResponse.model_validate(booking)
        for booking in bookings
    ]
