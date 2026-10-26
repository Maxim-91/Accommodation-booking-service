from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccommodationDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str | None
    location: str
    price_per_night: Decimal
    max_guests: int
    is_active: bool
    created_at: datetime


class CreateAccommodationReq(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    location: str = Field(min_length=1, max_length=255)
    price_per_night: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2
    )
    max_guests: int = Field(gt=0)
    is_active: bool = True


class UpdateAccommodationReq(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    location: str = Field(min_length=1, max_length=255)
    price_per_night: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2
    )
    max_guests: int = Field(gt=0)
    is_active: bool = True
