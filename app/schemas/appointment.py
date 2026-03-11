"""Appointment schemas."""

from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    scheduled_date: date
    scheduled_time: time
    session_notes: str | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_date: date | None = None
    scheduled_time: time | None = None
    session_notes: str | None = None


class AppointmentResponse(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    created_at: datetime
