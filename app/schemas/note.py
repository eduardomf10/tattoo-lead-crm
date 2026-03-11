"""Note schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    created_at: datetime
