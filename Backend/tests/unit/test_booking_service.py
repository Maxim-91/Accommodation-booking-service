import unittest
from datetime import date
from decimal import Decimal
from custom_exceptions.booking_conflict_exception import BookingConflictException
from custom_exceptions.not_found_exception import NotFoundException
from models import Accommodation, Booking, User
from services.booking_service import BookingService
from tests.unit.test_helpers import create_test_session


class BookingServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine, self.session = create_test_session()
        self.service = BookingService(self.session)
        self.owner = User(full_name="Owner", email="booking-owner@example.com", password_hash="test-hash")
        self.guest = User(full_name="Guest", email="booking-guest@example.com", password_hash="test-hash")
        self.other_guest = User(full_name="Other Guest", email="other-booking-guest@example.com", password_hash="test-hash")
        self.session.add_all([self.owner, self.guest, self.other_guest])
        self.session.commit()
        self.accommodation = Accommodation(
            owner_id=self.owner.id,
            title="Booking Apartment",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=3,
            is_active=True,
        )
        self.session.add(self.accommodation)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def create_booking(self, **overrides):
        values = {
            "user_id": self.guest.id,
            "accommodation_id": self.accommodation.id,
            "check_in": date(2027, 5, 10),
            "check_out": date(2027, 5, 13),
            "guests": 2,
        }
        values.update(overrides)
        return self.service.create_booking(**values)

    def test_create_booking(self):
        booking = self.create_booking()
        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.user_id, self.guest.id)
        self.assertEqual(booking.accommodation_id, self.accommodation.id)
        self.assertEqual(booking.status, "pending")

    def test_create_booking_for_missing_accommodation_raises_not_found(self):
        with self.assertRaises(NotFoundException):
            self.create_booking(accommodation_id=999999)

    def test_check_out_must_be_after_check_in(self):
        with self.assertRaises(BookingConflictException):
            self.create_booking(
                check_in=date(2027, 5, 13),
                check_out=date(2027, 5, 13),
            )

    def test_zero_guests_is_rejected(self):
        with self.assertRaises(BookingConflictException):
            self.create_booking(guests=0)

    def test_guest_count_cannot_exceed_capacity(self):
        with self.assertRaises(BookingConflictException):
            self.create_booking(guests=4)

    def test_inactive_accommodation_cannot_be_booked(self):
        self.accommodation.is_active = False
        self.session.commit()
        with self.assertRaises(BookingConflictException):
            self.create_booking()

    def test_overlapping_booking_is_rejected(self):
        self.create_booking()
        with self.assertRaises(BookingConflictException):
            self.create_booking(
                user_id=self.other_guest.id,
                check_in=date(2027, 5, 12),
                check_out=date(2027, 5, 15),
            )

    def test_adjacent_bookings_are_allowed(self):
        first = self.create_booking()
        second = self.create_booking(
            user_id=self.other_guest.id,
            check_in=first.check_out,
            check_out=date(2027, 5, 16),
        )
        self.assertIsNotNone(second.id)

    def test_cancelled_booking_does_not_block_dates(self):
        first = self.create_booking()
        self.service.cancel_booking(booking_id=first.id, user_id=self.guest.id)
        second = self.create_booking(
            user_id=self.other_guest.id,
            check_in=date(2027, 5, 11),
            check_out=date(2027, 5, 14),
        )
        self.assertIsNotNone(second.id)

    def test_get_bookings_by_user_returns_only_that_users_bookings(self):
        own_booking = self.create_booking()
        self.create_booking(user_id=self.other_guest.id)
        result = self.service.get_bookings_by_user(self.guest.id)
        self.assertEqual([booking.id for booking in result], [own_booking.id])

    def test_cancel_booking_changes_status(self):
        booking = self.create_booking()
        cancelled = self.service.cancel_booking(booking_id=booking.id, user_id=self.guest.id)
        self.assertEqual(cancelled.status, "cancelled")

    def test_user_cannot_cancel_another_users_booking(self):
        booking = self.create_booking()
        with self.assertRaises(NotFoundException):
            self.service.cancel_booking(booking_id=booking.id, user_id=self.other_guest.id)

    def test_cancel_missing_booking_raises_not_found(self):
        with self.assertRaises(NotFoundException):
            self.service.cancel_booking(booking_id=999999, user_id=self.guest.id)

    def test_cancelling_twice_raises_booking_conflict(self):
        booking = self.create_booking()
        self.service.cancel_booking(booking_id=booking.id, user_id=self.guest.id)
        with self.assertRaises(BookingConflictException):
            self.service.cancel_booking(booking_id=booking.id, user_id=self.guest.id)


if __name__ == "__main__":
    unittest.main()
