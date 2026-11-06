from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Table,
    Column,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

accommodation_amenities = Table(
    "accommodation_amenities",
    Base.metadata,
    Column(
        "accommodation_id",
        ForeignKey("accommodations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "amenity_id",
        ForeignKey("amenities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    accommodations: Mapped[list["Accommodation"]] = relationship(
        back_populates="owner",
    )
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user",
    )


class Accommodation(Base):
    __tablename__ = "accommodations"

    __table_args__ = (
        CheckConstraint(
            "price_per_night > 0",
            name="ck_accommodations_price_positive",
        ),
        CheckConstraint(
            "max_guests >= 1",
            name="ck_accommodations_max_guests_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    price_per_night: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    max_guests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    owner: Mapped["User"] = relationship(
        back_populates="accommodations",
    )
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="accommodation",
    )
    amenities: Mapped[list["Amenity"]] = relationship(
        secondary=accommodation_amenities,
        back_populates="accommodations",
    )


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "check_out > check_in",
            name="ck_bookings_checkout_after_checkin",
        ),
        CheckConstraint(
            "guests >= 1",
            name="ck_bookings_guests_positive",
        ),
        CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled')",
            name="ck_bookings_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    accommodation_id: Mapped[int] = mapped_column(
        ForeignKey("accommodations.id"),
        nullable=False,
        index=True,
    )
    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)
    guests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="bookings",
    )
    accommodation: Mapped["Accommodation"] = relationship(
        back_populates="bookings",
    )

class Amenity(Base):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )
    accommodations: Mapped[list["Accommodation"]] = relationship(
        secondary=accommodation_amenities,
        back_populates="amenities",
    )
