# Tattoo Lead CRM API

A REST API for a solo tattoo artist to manage clients, leads, notes, and appointments in one place. Built with **Python**, **FastAPI**, **SQLAlchemy**, **Pydantic**, and **SQLite**. Inquiries become leads, move through a status pipeline, and can be annotated and scheduled from a single backend.

[![Demo Video](https://img.shields.io/badge/▶_Demo_Video-YouTube-red?style=for-the-badge&logo=youtube)](https://youtu.be/S7l67Tlu-Os)

---

## Project Overview

This API is an internal backend that centralizes client and lead data for an independent tattoo artist. It acts as a single source of truth for who inquired, what they want, where each lead stands in the pipeline, conversation notes, and scheduled sessions. The API is stateless, uses SQLite for portability, and exposes OpenAPI docs for integration with a frontend or other clients.

---

## Business Problem

Solo tattoo artists often get inquiries from multiple channels—Instagram DMs, email, referrals—with no single place to track them. Context (tattoo idea, placement, size, budget) ends up scattered across conversations. It becomes hard to see which leads are new, which have replied, which are scheduled, and which have gone cold. Many rely on spreadsheets or ad-hoc notes, which leads to missed follow-ups and lost bookings. The core challenges are fragmented data, no visible pipeline, and manual tracking that does not scale.

---

## Solution

This API addresses those challenges by:

1. **Storing clients** — Contact details (name, Instagram, phone, email, preferred contact method).
2. **Turning inquiries into leads** — Each inquiry is a lead linked to a client, with tattoo details (idea, body location, size, style, source, estimated budget).
3. **Tracking lead status** — A defined pipeline: `new` → `awaiting_client_reply` → `in_conversation` → `scheduled` → `closed` or `lost`.
4. **Attaching notes to leads** — Conversation history and reminders per lead.
5. **Managing one appointment per lead** — Simple scheduling based on predefined availability slots, with date, time, and session notes.

Everything is exposed via a REST API with request/response validation and automatic OpenAPI docs.

---

### Scheduling flow (simple availability-based booking)

The API uses a straightforward scheduling model:

1. The artist creates **availability slots** with a single `start_time` (`POST /slots`).
2. Clients can only book from **available slots** (`GET /slots/available`).
3. To schedule a session, the client creates an **appointment from a slot** (`POST /leads/{lead_id}/appointment`), passing the `slot_id`.
4. The system creates an `Appointment` tied to that slot, copies the date and time from the slot, and marks the slot as booked.
5. Each lead can have at most one appointment, and each slot can be booked at most once.

This keeps the scheduling logic easy to reason about without implementing a full calendar system.

---

## What This Project Demonstrates

- **REST API design with FastAPI** — Resource-oriented endpoints, appropriate HTTP methods, and status codes.
- **Relational data modeling with SQLAlchemy** — Entities, foreign keys, and one-to-many / one-to-one relationships.
- **CRUD operations** — Create, read, update (where applicable) across clients, leads, notes, and appointments.
- **Service-layer architecture** — Business logic in services; routers handle only HTTP and delegation.
- **API validation with Pydantic** — Request bodies and response shapes with type safety and clear validation errors.
- **Workflow state management** — Lead status lifecycle and nested resources (notes and appointment under a lead).
- **OpenAPI documentation** — Auto-generated Swagger UI and ReDoc from the FastAPI application.

---

## Architecture Overview

The codebase is split into four layers:

| Layer | Role |
|-------|------|
| **Routers** | HTTP layer: parse requests, validate input via Pydantic schemas, call services, return responses. No business logic. |
| **Services** | Business logic and database access. Services receive a DB session and data; routers never touch the ORM directly. |
| **Models** | SQLAlchemy ORM: table definitions, columns, and relationships. Single source of truth for the database schema. |
| **Schemas** | Pydantic models: API contracts for request bodies and responses. Separate from persistence so the API can evolve independently. |

Dependencies flow in one direction: **routers → services → models**. This separation keeps the HTTP layer, business logic, and persistence distinct so each layer has a single responsibility and the codebase stays easier to maintain. Schemas are used at the router boundary (input/output) and are not tied to database columns.

---

## Features

- **Client management** — Create, list, and retrieve clients by ID.
- **Lead management** — Create leads linked to clients; list with optional status filter; get lead by ID (including nested client); update lead status.
- **Notes** — Create and list notes per lead (nested under `/leads/{lead_id}/notes`).
- **Availability & appointments** — Artist creates availability slots; clients book from available slots to create one appointment per lead; get appointment by lead (returns `null` if none).
- **OpenAPI docs** — Swagger UI and ReDoc generated from the FastAPI app.
- **Structured errors** — 404 and validation errors with clear messages.
- **Database** — SQLite with SQLAlchemy ORM; tables created on application startup.

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Server | [Uvicorn](https://www.uvicorn.org/) (ASGI) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) 2.x |
| Validation & serialization | [Pydantic](https://docs.pydantic.dev/) 2.x |
| Database | SQLite (file-based) |
| Language | Python 3.10+ |

---

## Database Entities

**Client** — A person who has inquired or been referred. Stored once; multiple leads can reference the same client. Fields: `full_name`, `instagram_handle`, `phone`, `email`, `preferred_contact_method`, `created_at`.

**Lead** — A single tattoo inquiry tied to one client. Stores the request details: `original_message`, `tattoo_idea`, `body_location`, `size`, `style`, `color_type`, `design_type`, `summary`, `status`, `source`, `estimated_budget_range`, plus `created_at` and `updated_at`. Each lead has a lifecycle status and can have many notes and at most one appointment.

**Note** — A note attached to a lead (e.g. conversation summary or reminder). Fields: `lead_id`, `content`, `created_at`. Many notes per lead.

**AvailabilitySlot** — A single available time slot for the artist. Fields: `start_time`, `is_booked`, `created_at`. Each slot can be used at most once for an appointment.

**Appointment** — A scheduled session for a lead, created from an availability slot. One appointment per lead (`lead_id` is unique) and one appointment per slot (`slot_id` is unique). Fields: `lead_id`, `slot_id`, `scheduled_date`, `scheduled_time`, `session_notes`, `created_at`.

**Relationships**

- **Client** → **Lead**: one-to-many. A client can have multiple leads (e.g. multiple ideas or follow-up projects).
- **Lead** → **Note**: one-to-many. A lead can have many notes.
- **Lead** → **Appointment**: one-to-one. A lead has at most one appointment.
- **AvailabilitySlot** → **Appointment**: one-to-one. A slot can be booked for at most one appointment.

Deleting a client cascades to its leads; deleting a lead cascades to its notes and appointment.

---

## Project Structure

```
tattoo-lead-crm/
├── app/
│   ├── main.py              # FastAPI app, lifespan, router registration
│   ├── database.py          # Engine, session factory, get_db, init_db
│   ├── models/              # SQLAlchemy ORM (database tables)
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── note.py
│   │   ├── appointment.py
│   │   └── availability_slot.py
│   ├── schemas/             # Pydantic (API request/response contracts)
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── note.py
│   │   ├── appointment.py
│   │   └── availability_slot.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── client_service.py
│   │   ├── lead_service.py
│   │   ├── note_service.py
│   │   ├── appointment_service.py
│   │   └── availability_slot_service.py
│   └── routers/             # HTTP endpoints
│       ├── __init__.py
│       ├── clients.py
│       ├── leads.py
│       ├── notes.py
│       ├── appointments.py
│       └── availability_slots.py
├── requirements.txt
└── README.md
```

---

## API Endpoints

**Root**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check and links to docs. |

**Clients**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/clients` | Create a client. |
| GET | `/clients` | List clients (optional `skip`, `limit`). |
| GET | `/clients/{client_id}` | Get client by ID. |

**Leads**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/leads` | Create a lead (body: `client_id`, tattoo fields, `status`, `source`, etc.). |
| GET | `/leads` | List leads; optional query `?status=<status>`. |
| GET | `/leads/{lead_id}` | Get lead by ID (includes nested client). |
| PATCH | `/leads/{lead_id}/status` | Update lead status. |

Lead status values: `new`, `awaiting_client_reply`, `in_conversation`, `scheduled`, `closed`, `lost`.

**Notes** (nested under leads)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/leads/{lead_id}/notes` | Create a note for the lead. |
| GET | `/leads/{lead_id}/notes` | List notes for the lead. |

**Appointments** (nested under leads)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/leads/{lead_id}/appointment` | Create the lead’s appointment from an availability slot (one per lead). |
| GET | `/leads/{lead_id}/appointment` | Get the lead’s appointment (or `null`). |

**Availability slots**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/slots` | Create an availability slot for the artist. |
| GET | `/slots/available` | List all availability slots that are not yet booked. |

---

## How to Run Locally

**Prerequisites:** Python 3.10+

```bash
cd tattoo-lead-crm
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API base: **http://127.0.0.1:8000**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The SQLite database file `tattoo_crm.db` is created in the project root on first request.

---

## Example Workflow

This example walks through how a single tattoo inquiry moves from first contact to a scheduled appointment using availability slots.

**1. Create the client** (person who inquired)

```bash
curl -X POST http://127.0.0.1:8000/clients \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Jane Smith", "instagram_handle": "@jane.smith", "phone": "+15551234567", "preferred_contact_method": "instagram"}'
```

Use the returned `id` (e.g. `1`) as `client_id` in the next step.

**2. Create a lead** for the inquiry

```bash
curl -X POST http://127.0.0.1:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "tattoo_idea": "Small rose on forearm", "body_location": "forearm", "size": "small", "status": "new", "source": "instagram_dm"}'
```

**3. List new leads**

```bash
curl "http://127.0.0.1:8000/leads?status=new"
```

**4. Add a note** after talking to the client (e.g. lead ID `1`)

```bash
curl -X POST http://127.0.0.1:8000/leads/1/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "Client asked for quote by Friday. Prefers black and grey."}'
```

**5. Update status** when the client replies

```bash
curl -X PATCH http://127.0.0.1:8000/leads/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_conversation"}'
```

**6. Create an availability slot** (done by the artist/admin)

```bash
curl -X POST http://127.0.0.1:8000/slots \
  -H "Content-Type: application/json" \
  -d '{"start_time": "2025-04-15T14:00:00"}'
```

Use the returned `id` (e.g. `1`) as `slot_id` in the next step.

**7. List available slots** (for the client to choose)

```bash
curl http://127.0.0.1:8000/slots/available
```

**8. Schedule the appointment from a slot**

```bash
curl -X POST http://127.0.0.1:8000/leads/1/appointment \
  -H "Content-Type: application/json" \
  -d '{"slot_id": 1, "session_notes": "Session 1 - forearm rose"}'
```

**9. Get full lead detail** (with client and status)

```bash
curl http://127.0.0.1:8000/leads/1
```

---

## Future Improvements

- **Authentication** — JWT or API keys to secure endpoints and support multi-tenant or multi-user use.
- **Pagination** — Standardized pagination (e.g. offset/limit or cursor) with metadata on list endpoints.
- **Filtering and search** — Filter leads by date range, source, or client name; full-text search on notes.
- **PostgreSQL** — Move to PostgreSQL for production with connection pooling and better concurrency.
- **Migrations** — Alembic (or similar) for versioned schema changes and repeatable deployments.
- **Tests** — Unit tests for services and integration tests for routers (e.g. pytest with FastAPI TestClient).
- **Soft delete** — Mark clients and leads as deleted instead of hard delete for audit and recovery.
- **Audit fields** — Consistent `updated_at` (and optionally `created_by` once auth exists) across entities.
- **Rate limiting** — Per-IP or per-token limits on public or unauthenticated endpoints.
- **Frontend** — Web or mobile client consuming this API for day-to-day use by the artist.

---

## License

Internal use / portfolio. You may use this project as reference for your own work.
