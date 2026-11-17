import unittest
from decimal import Decimal
from tests.api.test_helpers import ApiTestCaseMixin, app
from dependencies import get_logged_in_user
from models import Amenity, User


class AccommodationsApiTests(ApiTestCaseMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.owner = User(full_name="API Owner", email="api-owner@example.com", password_hash="test-hash")
        self.other_user = User(full_name="Other API User", email="api-other@example.com", password_hash="test-hash")
        self.session.add_all([self.owner, self.other_user])
        self.session.commit()
        self.current_user = self.owner
        app.dependency_overrides[get_logged_in_user] = lambda: self.current_user

    def accommodation_payload(self, **overrides):
        payload = {
            "title": "API Apartment",
            "description": "Created through API",
            "location": "Helsinki",
            "price_per_night": "100.00",
            "max_guests": 3,
            "amenity_ids": [],
            "is_active": True,
        }
        payload.update(overrides)
        return payload

    def create_accommodation(self, **overrides):
        return self.client.post(
            "/api/accommodations/",
            json=self.accommodation_payload(**overrides),
        )

    def test_list_accommodations(self):
        self.create_accommodation()
        response = self.client.get("/api/accommodations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "API Apartment")

    def test_get_accommodation_by_id(self):
        created = self.create_accommodation()
        accommodation_id = created.json()["id"]
        response = self.client.get(f"/api/accommodations/{accommodation_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], accommodation_id)

    def test_get_missing_accommodation_returns_404(self):
        response = self.client.get("/api/accommodations/999999")
        self.assertEqual(response.status_code, 404)

    def test_create_accommodation_requires_authentication(self):
        app.dependency_overrides.pop(get_logged_in_user)
        response = self.client.post(
            "/api/accommodations/",
            json=self.accommodation_payload(),
        )
        self.assertEqual(response.status_code, 401)

    def test_create_accommodation(self):
        response = self.create_accommodation()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["owner_id"], self.owner.id)
        self.assertEqual(response.json()["title"], "API Apartment")

    def test_create_accommodation_with_amenity(self):
        amenity = Amenity(name="Wi-Fi")
        self.session.add(amenity)
        self.session.commit()
        response = self.create_accommodation(amenity_ids=[amenity.id])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["amenities"][0]["name"], "Wi-Fi")

    def test_create_accommodation_with_unknown_amenity_returns_404(self):
        response = self.create_accommodation(amenity_ids=[999999])
        self.assertEqual(response.status_code, 404)

    def test_update_own_accommodation(self):
        created = self.create_accommodation()
        accommodation_id = created.json()["id"]
        response = self.client.put(
            f"/api/accommodations/{accommodation_id}",
            json=self.accommodation_payload(title="Updated Apartment"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Apartment")

    def test_update_another_users_accommodation_returns_forbidden(self):
        self.current_user = self.other_user
        created = self.create_accommodation()
        self.current_user = self.owner
        response = self.client.put(
            f"/api/accommodations/{created.json()['id']}",
            json=self.accommodation_payload(title="Not allowed"),
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_own_accommodation(self):
        created = self.create_accommodation()
        response = self.client.delete(f"/api/accommodations/{created.json()['id']}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get(f"/api/accommodations/{created.json()['id']}").status_code,404)

    def test_delete_another_users_accommodation_returns_forbidden(self):
        created = self.create_accommodation()
        self.current_user = self.other_user
        response = self.client.delete(f"/api/accommodations/{created.json()['id']}")
        self.assertEqual(response.status_code, 403)

    def test_invalid_accommodation_payload_returns_422(self):
        response = self.client.post(
            "/api/accommodations/",
            json=self.accommodation_payload(price_per_night="0"),
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
