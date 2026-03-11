"""Appointment service - business logic for appointments."""

from sqlalchemy.orm import Session

from app.models import Appointment
from app.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, lead_id: int, data: AppointmentCreate) -> Appointment | None:
    """Create or replace appointment for a lead. One appointment per lead. Returns None if lead does not exist."""
    from app.models import Lead

    if not db.query(Lead).filter(Lead.id == lead_id).first():
        return None
    existing = db.query(Appointment).filter(Appointment.lead_id == lead_id).first()
    if existing:
        existing.scheduled_date = data.scheduled_date
        existing.scheduled_time = data.scheduled_time
        existing.session_notes = data.session_notes
        db.commit()
        db.refresh(existing)
        return existing
    appointment = Appointment(lead_id=lead_id, **data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment_by_lead(db: Session, lead_id: int) -> Appointment | None:
    """Get the appointment for a lead, if any."""
    return db.query(Appointment).filter(Appointment.lead_id == lead_id).first()
