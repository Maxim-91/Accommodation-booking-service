from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Accommodation, Booking
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.booking_conflict_exception import BookingConflictException


class BookingService:
    def __init__(self, repository: Session):
        self._repository = repository

    def create_booking(
        self,
        *,
        user_id: int,
        accommodation_id: int,
        check_in: date,
        check_out: date,
        guests: int,
    ) -> Booking:
        # 1. Validate the date range.
        if check_out <= check_in:
            raise BookingConflictException(
                "Check-out must be later than check-in"
            )

        # 2. Validate the number of guests.
        if guests < 1:
            raise BookingConflictException(
                "At least one guest is required"
            )

        # 3. Find the accommodation.
        accommodation = self._repository.get(
            Accommodation, accommodation_id
        )

        if accommodation is None:
            raise NotFoundException("Accommodation not found")

        # 4. Check whether it is available for booking.
        if not accommodation.is_active:
            raise BookingConflictException(
                "Accommodation is not available for booking"
            )

        if guests > accommodation.max_guests:
            raise BookingConflictException(
                "Number of guests exceeds accommodation capacity"
            )

        # 5. Find overlapping bookings.
        # Cancelled bookings do not block the requested dates.
        overlapping_statement = select(Booking).where(
            Booking.accommodation_id == accommodation_id,
            Booking.status != "cancelled",
            Booking.check_in < check_out,
            Booking.check_out > check_in,
        )

        overlapping_booking = self._repository.scalars(
            overlapping_statement
        ).first()

        if overlapping_booking is not None:
            raise BookingConflictException(
                "Accommodation is already booked for these dates"
            )

        # 6. Create the booking for the authenticated user.
        booking = Booking(
            user_id=user_id,
            accommodation_id=accommodation_id,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
        )

        try:
            self._repository.add(booking)
            self._repository.commit()
            self._repository.refresh(booking)
            return booking
        except Exception:
            self._repository.rollback()
            raise

    def get_bookings_by_user(self, user_id: int) -> list[Booking]:
        statement = (
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.created_at.desc())
        )

        return list(self._repository.scalars(statement).all())
    