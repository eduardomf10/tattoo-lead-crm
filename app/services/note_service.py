"""Note service - business logic for notes."""

from sqlalchemy.orm import Session

from app.models import Note
from app.schemas.note import NoteCreate


def create_note(db: Session, lead_id: int, data: NoteCreate) -> Note | None:
    """Create a note for a lead. Returns None if lead does not exist."""
    from app.models import Lead

    if not db.query(Lead).filter(Lead.id == lead_id).first():
        return None
    note = Note(lead_id=lead_id, content=data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes_by_lead(db: Session, lead_id: int) -> list[Note]:
    """Get all notes for a lead."""
    return db.query(Note).filter(Note.lead_id == lead_id).order_by(Note.created_at.desc()).all()
