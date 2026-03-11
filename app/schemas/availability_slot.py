"""AvailabilitySlot schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AvailabilitySlotBase(BaseModel):
    start_time: datetime


class AvailabilitySlotCreate(AvailabilitySlotBase):
    pass


class AvailabilitySlotResponse(AvailabilitySlotBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_booked: bool
    created_at: datetime

