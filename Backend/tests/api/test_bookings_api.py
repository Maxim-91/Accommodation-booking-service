import unittest
from datetime import date
from decimal import Decimal
from tests.api.test_helpers import ApiTestCaseMixin, app
from dependencies import get_logged_in_user
from models import Accommodation, User


class BookingsApiTests(ApiTestCaseMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.owner = User(full_name="Booking API Owner", email="booking-api-owner@example.com", password_hash="test-hash")
        self.guest = User(full_name="Booking API Guest", email="booking-api-guest@example.com", password_hash="test-hash")
        self.other_guest = User(full_name="Other Booking Guest", email="booking-api-other@example.com", password_hash="test-hash")
        self.session.add_all([self.owner, self.guest, self.other_guest])
        self.session.commit()
        self.current_user = self.guest
        self.accommodation = Accommodation(
            owner_id=self.owner.id,
            title="Booking API Apartment",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=3,
            is_active=True,
        )
        self.session.add(self.accommodation)
        self.session.commit()
        app.dependency_overrides[get_logged_in_user] = lambda: self.current_user

    def booking_payload(self, **overrides):
        payload = {
            "accommodation_id": self.accommodation.id,
            "check_in": "2027-06-10",
            "check_out": "2027-06-13",
            "guests": 2,
        }
        payload.update(overrides)
        return payload

    def create_booking(self, **overrides):
        return self.client.post(
            "/api/bookings/",
            json=self.booking_payload(**overrides),
        )

    def test_create_booking(self):
        response = self.create_booking()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user_id"], self.guest.id)
        self.assertEqual(response.json()["status"], "pending")

    def test_create_booking_with_invalid_dates_returns_422(self):
        response = self.create_booking(
            check_in="2027-06-13",
            check_out="2027-06-10",
        )
        self.assertEqual(response.status_code, 422)

    def test_create_booking_for_missing_accommodation_returns_404(self):
        response = self.create_booking(accommodation_id=999999)
        self.assertEqual(response.status_code, 404)

    def test_create_booking_for_inactive_accommodation_returns_conflict(self):
        self.accommodation.is_active = False
        self.session.commit()
        response = self.create_booking()
        self.assertEqual(response.status_code, 409)

    def test_create_booking_exceeding_capacity_returns_conflict(self):
        response = self.create_booking(guests=4)
        self.assertEqual(response.status_code, 409)

    def test_overlapping_booking_returns_conflict(self):
        self.assertEqual(self.create_booking().status_code, 201)
        self.current_user = self.other_guest
        response = self.create_booking(
            check_in="2027-06-11",
            check_out="2027-06-14",
        )
        self.assertEqual(response.status_code, 409)

    def test_get_my_bookings_returns_only_current_users_bookings(self):
        self.create_booking()
        self.current_user = self.other_guest
        self.create_booking()
        self.current_user = self.guest
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["user_id"], self.guest.id)

    def test_cancel_booking(self):
        created = self.create_booking()
        booking_id = created.json()["id"]
        response = self.client.delete(f"/api/bookings/{booking_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "cancelled")

    def test_user_cannot_cancel_another_users_booking(self):
        created = self.create_booking()
        self.current_user = self.other_guest
        response = self.client.delete(f"/api/bookings/{created.json()['id']}")
        self.assertEqual(response.status_code, 404)

    def test_cancel_booking_twice_returns_conflict(self):
        created = self.create_booking()
        booking_id = created.json()["id"]
        self.assertEqual(self.client.delete(f"/api/bookings/{booking_id}").status_code, 200)
        response = self.client.delete(f"/api/bookings/{booking_id}")
        self.assertEqual(response.status_code, 409)

    def test_bookings_endpoints_require_authentication(self):
        app.dependency_overrides.pop(get_logged_in_user)
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
