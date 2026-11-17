import unittest
from decimal import Decimal

from tests.unit.test_helpers import create_test_session
from services.accommodation_service import AccommodationService
from models import User, Accommodation, Amenity
from dtos.accommodations import CreateAccommodationReq, UpdateAccommodationReq
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.forbidden_exception import ForbiddenException


class AccommodationServiceTests(unittest.TestCase):

    def setUp(self):
        self.engine, self.session = create_test_session()
        self.service = AccommodationService(self.session)
        self.user = User(full_name="Test Owner", email="owner@example.com", password_hash="test-hash")
        self.session.add(self.user)
        self.session.commit()

    # def tearDown for close and destroy the engine
    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    # Check accommodation creation
    def test_create_accommodation(self):
        request = CreateAccommodationReq(
            title="Test Apartment",
            description="Test description",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=3,
            amenity_ids=[],
            is_active=True,
        )
        accommodation = self.service.create(request, owner_id=self.user.id)
        self.assertIsNotNone(accommodation.id)
        self.assertEqual(accommodation.title, "Test Apartment")
        self.assertEqual(accommodation.owner_id, self.user.id)
        self.assertEqual(accommodation.price_per_night, Decimal("100.00"))

    # Check receipt of accommodation
    def test_get_accommodation_by_id(self):
        accommodation = Accommodation(
            title="Test Apartment",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=2,
            owner_id=self.user.id,
        )
        self.session.add(accommodation)
        self.session.commit()
        result = self.service.get_by_id(accommodation.id)
        self.assertEqual(result.id, accommodation.id)
        self.assertEqual(result.title, "Test Apartment")

    # Check for missing accommodation
    def test_get_missing_accommodation_raises_not_found(self):
        with self.assertRaises(NotFoundException):
            self.service.get_by_id(9999)

    # Check the restriction on editing another user's accommodation
    def test_update_other_users_accommodation_raises_forbidden(self):
        other_user = User(full_name="Other User", email="other@example.com", password_hash="test-hash")
        self.session.add(other_user)
        self.session.commit()
        accommodation = Accommodation(
            title="Other Apartment",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=2,
            owner_id=other_user.id,
        )
        self.session.add(accommodation)
        self.session.commit()
        request = UpdateAccommodationReq(
            title="Updated Apartment",
            description="Updated",
            location="Helsinki",
            price_per_night=Decimal("120.00"),
            max_guests=2,
            amenity_ids=[],
            is_active=True,
        )
        with self.assertRaises(ForbiddenException):
            self.service.update(accommodation.id, request, owner_id=self.user.id)

    # Check deletion: create a accommodation, delete the accommodation and check that this accommodation no longer exists
    def test_delete_accommodation(self):
        request = self.create_accommodation_request()
        accommodation = self.service.create( request, owner_id=self.user.id)
        accommodation_id = accommodation.id
        self.service.delete(accommodation_id, owner_id=self.user.id)
        with self.assertRaises(NotFoundException):
            self.service.get_by_id(accommodation_id)

    # Check for an incorrect amenity ID
    def test_create_accommodation_with_invalid_amenity_id(self):
        request = self.create_accommodation_request(amenity_ids=[9999])
        with self.assertRaises(NotFoundException):
            self.service.create(request, owner_id=self.user.id)


    def create_accommodation_request(self, amenity_ids=None):
        return CreateAccommodationReq(
            title="Test Apartment",
            description="Test description",
            location="Helsinki",
            price_per_night=Decimal("100.00"),
            max_guests=3,
            amenity_ids=amenity_ids if amenity_ids is not None else [],
            is_active=True,
        )


if __name__ == "__main__":
    unittest.main()
