"""Appointment routes (nested under leads)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services import appointment_service, lead_service, availability_slot_service

router = APIRouter(prefix="/leads", tags=["appointments"])


@router.post("/{lead_id}/appointment", response_model=AppointmentResponse)
def create_appointment_from_slot(
    lead_id: int, data: AppointmentCreate, db: Session = Depends(get_db)
):
    """Create an appointment for a lead from a specific availability slot."""
    lead = lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    existing = appointment_service.get_appointment_by_lead(db, lead_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Lead already has an appointment",
        )

    slot = availability_slot_service.get_slot(db, data.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    try:
        appointment = appointment_service.create_appointment_from_slot(
            db, lead_id, slot, data
        )
    except ValueError as exc:
        if str(exc) == "slot_already_booked":
            raise HTTPException(status_code=400, detail="Slot is already booked")
        raise

    return appointment


@router.get("/{lead_id}/appointment", response_model=AppointmentResponse | None)
def get_appointment(lead_id: int, db: Session = Depends(get_db)):
    """Get the appointment for a lead, if any."""
    if not lead_service.get_lead(db, lead_id):
        raise HTTPException(status_code=404, detail="Lead not found")
    return appointment_service.get_appointment_by_lead(db, lead_id)
