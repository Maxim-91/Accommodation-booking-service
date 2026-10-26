from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateBookingRequest(BaseModel):
    accommodation_id: int = Field(gt=0)
    check_in: date
    check_out: date
    guests: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be later than check_in")
        return self


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    accommodation_id: int
    check_in: date
    check_out: date
    guests: int
    status: str
    created_at: datetime
