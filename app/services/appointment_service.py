"""Appointment service - business logic for appointments."""

from sqlalchemy.orm import Session

from app.models import Appointment, AvailabilitySlot
from app.schemas.appointment import AppointmentCreate


def create_appointment_from_slot(
    db: Session, lead_id: int, slot: AvailabilitySlot, data: AppointmentCreate
) -> Appointment:
    """Create an appointment for a lead from a specific availability slot.

    Assumes the lead exists and does not already have an appointment.
    """
    if slot.is_booked:
        raise ValueError("slot_already_booked")

    appointment = Appointment(
        lead_id=lead_id,
        slot_id=slot.id,
        scheduled_date=slot.start_time.date(),
        scheduled_time=slot.start_time.time(),
        session_notes=data.session_notes,
    )
    slot.is_booked = True

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment_by_lead(db: Session, lead_id: int) -> Appointment | None:
    """Get the appointment for a lead, if any."""
    return db.query(Appointment).filter(Appointment.lead_id == lead_id).first()
