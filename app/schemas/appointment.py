"""Appointment schemas."""

from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    slot_id: int
    session_notes: str | None = None


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    slot_id: int
    scheduled_date: date
    scheduled_time: time
    session_notes: str | None = None
    created_at: datetime
