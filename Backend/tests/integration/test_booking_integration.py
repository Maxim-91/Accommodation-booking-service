import unittest
from tests.integration.test_helpers import create_migrated_test_database, get_test_database_url
import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import select
from custom_exceptions.booking_conflict_exception import BookingConflictException
from models import Accommodation, Booking, User
from services.booking_service import BookingService


@unittest.skipUnless(get_test_database_url(),"Set TEST_DATABASE_URL to run PostgreSQL integration tests.")
class BookingDatabaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine, cls.session_local = create_migrated_test_database()

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        self.session = self.session_local()
        self.service = BookingService(self.session)
        unique = uuid.uuid4().hex
        self.owner = User(full_name="Integration Owner", email=f"owner-{unique}@example.com", password_hash="integration-hash")
        self.guest = User(full_name="Integration Guest", email=f"guest-{unique}@example.com", password_hash="integration-hash")
        self.second_guest = User(full_name="Second Integration Guest", email=f"second-{unique}@example.com", password_hash="integration-hash")
        self.session.add_all([self.owner, self.guest, self.second_guest])
        self.session.flush()
        self.accommodation = Accommodation(
            owner_id=self.owner.id,
            title="Integration Booking Apartment",
            location="Helsinki",
            price_per_night=Decimal("110.00"),
            max_guests=3,
            is_active=True,
        )
        self.session.add(self.accommodation)
        self.session.commit()
        # Save IDs before the session is closed.
        self.owner_id = self.owner.id
        self.guest_id = self.guest.id
        self.second_guest_id = self.second_guest.id
        self.accommodation_id = self.accommodation.id

    def tearDown(self):
        # Delete only records created by this test.
        self.session.rollback()
        self.session.query(Booking).filter(Booking.accommodation_id == self.accommodation_id).delete(synchronize_session=False)
        self.session.query(Accommodation).filter(Accommodation.id == self.accommodation_id).delete(synchronize_session=False)
        self.session.query(User).filter(User.id.in_([self.owner_id, self.guest_id, self.second_guest_id])).delete(synchronize_session=False)
        self.session.commit()
        self.session.close()

    def test_booking_is_persisted_and_can_be_read_in_new_session(self):
        booking = self.service.create_booking(
            user_id=self.guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 10),
            check_out=date(2027, 7, 13),
            guests=2,
        )
        booking_id = booking.id
        self.session.close()

        with self.session_local() as verification_session:
            persisted = verification_session.get(Booking, booking_id)
            self.assertIsNotNone(persisted)
            self.assertEqual(persisted.status, "pending")
            self.assertEqual(persisted.user_id, self.guest_id)
            self.assertEqual(persisted.accommodation_id, self.accommodation_id)

    def test_overlapping_booking_is_rejected_by_service_using_postgresql(self):
        self.service.create_booking(
            user_id=self.guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 10),
            check_out=date(2027, 7, 13),
            guests=2,
        )

        with self.assertRaises(BookingConflictException):
            self.service.create_booking(
                user_id=self.second_guest.id,
                accommodation_id=self.accommodation.id,
                check_in=date(2027, 7, 12),
                check_out=date(2027, 7, 15),
                guests=1,
            )

    def test_adjacent_stays_are_allowed_in_postgresql(self):
        first = self.service.create_booking(
            user_id=self.guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 10),
            check_out=date(2027, 7, 13),
            guests=2,
        )
        second = self.service.create_booking(
            user_id=self.second_guest.id,
            accommodation_id=self.accommodation.id,
            check_in=first.check_out,
            check_out=date(2027, 7, 16),
            guests=1,
        )
        self.assertNotEqual(first.id, second.id)

    def test_cancellation_is_persisted_and_dates_become_available(self):
        first = self.service.create_booking(
            user_id=self.guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 10),
            check_out=date(2027, 7, 13),
            guests=2,
        )
        self.service.cancel_booking(booking_id=first.id, user_id=self.guest.id)

        with self.session_local() as verification_session:
            persisted = verification_session.get(Booking, first.id)
            self.assertEqual(persisted.status, "cancelled")

        second = self.service.create_booking(
            user_id=self.second_guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 11),
            check_out=date(2027, 7, 14),
            guests=1,
        )
        self.assertIsNotNone(second.id)

    def test_booking_foreign_keys_reference_existing_records(self):
        booking = self.service.create_booking(
            user_id=self.guest.id,
            accommodation_id=self.accommodation.id,
            check_in=date(2027, 7, 20),
            check_out=date(2027, 7, 22),
            guests=1,
        )

        with self.session_local() as verification_session:
            row = verification_session.execute(
                select(Booking.user_id, Booking.accommodation_id)
                .where(Booking.id == booking.id)
            ).one()

        self.assertEqual(row.user_id, self.guest.id)
        self.assertEqual(row.accommodation_id, self.accommodation.id)


if __name__ == "__main__":
    unittest.main()
