from datetime import date
from decimal import Decimal

from database import SessionLocal
from models import User, Accommodation, Booking

db = SessionLocal()

try:
    user = User(
        full_name="Test User",
        email="relationship-test@example.com",
        password_hash="test-hash-not-for-real-login",
    )

    accommodation = Accommodation(
        title="Test Accommodation",
        location="Helsinki",
        price_per_night=Decimal("75.00"),
        max_guests=2,
        owner=user,
    )

    booking = Booking(
        user=user,
        accommodation=accommodation,
        check_in=date(2027, 5, 10),
        check_out=date(2027, 5, 13),
        guests=2,
    )

    db.add(booking)
    db.flush()

    print("User bookings:", len(user.bookings))
    print("Owner accommodations:", len(user.accommodations))
    print("Accommodation bookings:", len(accommodation.bookings))
    print("Booking user:", booking.user.full_name)
    print("Booking accommodation:", booking.accommodation.title)

finally:
    db.rollback()
    db.close()
