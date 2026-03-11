"""Client schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClientBase(BaseModel):
    full_name: str
    instagram_handle: str | None = None
    phone: str | None = None
    email: str | None = None
    preferred_contact_method: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    full_name: str | None = None
    instagram_handle: str | None = None
    phone: str | None = None
    email: str | None = None
    preferred_contact_method: str | None = None


class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
