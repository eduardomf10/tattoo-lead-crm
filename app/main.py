"""Tattoo Lead CRM API - FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import clients, leads, notes, appointments


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="Tattoo Lead CRM API",
    description="Internal API for managing clients, leads, notes, and appointments for a solo tattoo artist.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(clients.router)
app.include_router(leads.router)
app.include_router(notes.router)
app.include_router(appointments.router)


@app.get("/")
def root():
    """Health check and API info."""
    return {
        "message": "Tattoo Lead CRM API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
