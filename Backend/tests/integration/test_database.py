import unittest
from tests.integration.test_helpers import create_migrated_test_database, get_test_database_url
import uuid
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from models import Accommodation, Amenity, User


@unittest.skipUnless(get_test_database_url(), "Set TEST_DATABASE_URL to run PostgreSQL integration tests.")
class DatabaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine, cls.session_local = create_migrated_test_database()

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        self.session = self.session_local()
        self.email_prefix = f"db-test-{uuid.uuid4().hex}"

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_migrations_created_expected_tables(self):
        inspector = inspect(self.engine)
        tables = set(inspector.get_table_names())
        self.assertTrue({"users", "accommodations", "bookings", "amenities", "accommodation_amenities", "alembic_version"}.issubset(tables))

    def test_user_and_accommodation_persist_after_session_is_reopened(self):
        user = User(full_name="Database Integration User", email=f"{self.email_prefix}@example.com", password_hash="integration-test-hash")
        self.session.add(user)
        self.session.commit()
        user_id = user.id
        self.session.close()

        with self.session_local() as verification_session:
            persisted_user = verification_session.get(User, user_id)
            self.assertIsNotNone(persisted_user)
            self.assertEqual(persisted_user.full_name, "Database Integration User")
            accommodation = Accommodation(
                owner_id=persisted_user.id,
                title="Persistent Apartment",
                location="Helsinki",
                price_per_night=100,
                max_guests=2,
                is_active=True,
            )
            verification_session.add(accommodation)
            verification_session.commit()
            accommodation_id = accommodation.id

        with self.session_local() as verification_session:
            persisted_accommodation = verification_session.get(Accommodation, accommodation_id)
            self.assertIsNotNone(persisted_accommodation)
            self.assertEqual(persisted_accommodation.title, "Persistent Apartment")

    def test_user_email_unique_constraint_is_enforced(self):
        email = f"{self.email_prefix}@example.com"
        self.session.add(User(full_name="First", email=email, password_hash="hash"))
        self.session.commit()
        self.session.add(User(full_name="Second", email=email, password_hash="hash"))
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

    def test_many_to_many_accommodation_amenities_persist(self):
        user = User(full_name="Amenity Integration User", email=f"{self.email_prefix}-amenity@example.com", password_hash="hash")
        amenity = Amenity(name=f"Integration Wi-Fi {uuid.uuid4().hex}")
        self.session.add_all([user, amenity])
        self.session.flush()
        accommodation = Accommodation(
            owner_id=user.id,
            title="Amenity Integration Apartment",
            location="Espoo",
            price_per_night=80,
            max_guests=2,
            is_active=True,
            amenities=[amenity],
        )
        self.session.add(accommodation)
        self.session.commit()
        accommodation_id = accommodation.id
        amenity_id = amenity.id
        self.session.close()

        with self.session_local() as verification_session:
            persisted = verification_session.get(Accommodation, accommodation_id)
            self.assertEqual([item.id for item in persisted.amenities], [amenity_id])

    def test_database_accepts_select_one(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
