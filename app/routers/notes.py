"""Note routes (nested under leads)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.note import NoteCreate, NoteResponse
from app.services import lead_service, note_service

router = APIRouter(prefix="/leads", tags=["notes"])


@router.post("/{lead_id}/notes", response_model=NoteResponse)
def create_note(lead_id: int, data: NoteCreate, db: Session = Depends(get_db)):
    """Add a note to a lead."""
    note = note_service.create_note(db, lead_id, data)
    if not note:
        raise HTTPException(status_code=404, detail="Lead not found")
    return note


@router.get("/{lead_id}/notes", response_model=list[NoteResponse])
def list_notes(lead_id: int, db: Session = Depends(get_db)):
    """List all notes for a lead."""
    if not lead_service.get_lead(db, lead_id):
        raise HTTPException(status_code=404, detail="Lead not found")
    return note_service.get_notes_by_lead(db, lead_id)
