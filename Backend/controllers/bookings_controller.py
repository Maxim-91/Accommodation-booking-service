from fastapi import APIRouter, Depends, status
from dependencies import get_logged_in_user
from dtos.bookings import CreateBookingRequest, BookingResponse
from factories.services import booking_service_factory
from models import User
from services.booking_service import BookingService

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    request: CreateBookingRequest,
    current_user: User = Depends(get_logged_in_user),
    service: BookingService = Depends(booking_service_factory),
) -> BookingResponse:
    booking = service.create_booking(
        user_id=current_user.id,
        accommodation_id=request.accommodation_id,
        check_in=request.check_in,
        check_out=request.check_out,
        guests=request.guests,
    )
    return BookingResponse.model_validate(booking)

@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_logged_in_user),
    service: BookingService = Depends(booking_service_factory),
) -> list[BookingResponse]:
    bookings = service.get_bookings_by_user(current_user.id)
    return [BookingResponse.model_validate(booking) for booking in bookings]

@router.delete("/{booking_id}", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def cancel_my_booking(
    booking_id: int,
    current_user: User = Depends(get_logged_in_user),
    service: BookingService = Depends(booking_service_factory),
) -> BookingResponse:
    booking = service.cancel_booking(booking_id=booking_id, user_id=current_user.id)
    return BookingResponse.model_validate(booking)
