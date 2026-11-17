import unittest
from decimal import Decimal
from custom_exceptions.not_found_exception import NotFoundException
from dtos.accommodations import CreateAccommodationReq, UpdateAccommodationReq
from models import Amenity, User
from services.accommodation_service import AccommodationService
from tests.unit.test_helpers import create_test_session


class AccommodationAmenitiesTests(unittest.TestCase):
    def setUp(self):
        self.engine, self.session = create_test_session()
        self.service = AccommodationService(self.session)
        self.owner = User(full_name="Amenity Owner", email="amenity-owner@example.com", password_hash="test-hash")
        self.session.add(self.owner)
        self.session.commit()
        self.wifi = Amenity(name="Wi-Fi")
        self.parking = Amenity(name="Parking")
        self.pool = Amenity(name="Swimming pool")
        self.session.add_all([self.wifi, self.parking, self.pool])
        self.session.commit()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def create_accommodation(self, amenity_ids):
        request = CreateAccommodationReq(
            title="Amenity Test Apartment",
            description=None,
            location="Helsinki",
            price_per_night=Decimal("90.00"),
            max_guests=4,
            amenity_ids=amenity_ids,
            is_active=True,
        )
        return self.service.create(request, self.owner.id)

    def test_create_accommodation_with_multiple_amenities(self):
        accommodation = self.create_accommodation([self.wifi.id, self.parking.id])
        self.assertEqual(
            {amenity.name for amenity in accommodation.amenities},
            {"Wi-Fi", "Parking"},
        )

    def test_same_amenity_can_be_shared_by_multiple_accommodations(self):
        first = self.create_accommodation([self.wifi.id])
        second = self.create_accommodation([self.wifi.id])
        self.assertEqual([item.id for item in first.amenities], [self.wifi.id])
        self.assertEqual([item.id for item in second.amenities], [self.wifi.id])

    def test_create_with_empty_amenity_list(self):
        accommodation = self.create_accommodation([])
        self.assertEqual(accommodation.amenities, [])

    def test_duplicate_amenity_ids_are_deduplicated(self):
        accommodation = self.create_accommodation([self.wifi.id, self.wifi.id])
        self.assertEqual(len(accommodation.amenities), 1)
        self.assertEqual(accommodation.amenities[0].id, self.wifi.id)

    def test_create_with_unknown_amenity_id_raises_not_found(self):
        with self.assertRaises(NotFoundException):
            self.create_accommodation([self.wifi.id, 999999])

    def test_update_replaces_amenities(self):
        accommodation = self.create_accommodation([self.wifi.id, self.parking.id])
        request = UpdateAccommodationReq(
            title="Amenity Test Apartment",
            description=None,
            location="Helsinki",
            price_per_night=Decimal("90.00"),
            max_guests=4,
            amenity_ids=[self.pool.id],
            is_active=True,
        )
        updated = self.service.update(accommodation.id, request, self.owner.id)
        self.assertEqual([item.id for item in updated.amenities], [self.pool.id])

    def test_update_with_empty_list_removes_all_amenities(self):
        accommodation = self.create_accommodation([self.wifi.id])
        request = UpdateAccommodationReq(
            title="Amenity Test Apartment",
            description=None,
            location="Helsinki",
            price_per_night=Decimal("90.00"),
            max_guests=4,
            amenity_ids=[],
            is_active=True,
        )
        updated = self.service.update(accommodation.id, request, self.owner.id)
        self.assertEqual(updated.amenities, [])

    def test_get_by_id_loads_amenities(self):
        accommodation = self.create_accommodation([self.wifi.id, self.pool.id])
        loaded = self.service.get_by_id(accommodation.id)
        self.assertEqual(
            {item.name for item in loaded.amenities},
            {"Wi-Fi", "Swimming pool"},
        )

    def test_get_all_loads_amenities(self):
        self.create_accommodation([self.wifi.id])
        self.create_accommodation([self.parking.id])
        accommodations = self.service.get_all()
        self.assertEqual(
            [{item.name for item in accommodation.amenities} for accommodation in accommodations],
            [{"Wi-Fi"}, {"Parking"}],
        )


if __name__ == "__main__":
    unittest.main()
