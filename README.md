# Tattoo Lead CRM API

Internal REST API for a solo tattoo artist to manage clients, leads, notes, and appointments. Built with **Python**, **FastAPI**, **SQLAlchemy**, **Pydantic**, and **SQLite**. Inquiries become leads, move through a status pipeline, and can be annotated and scheduled—all via a single backend service.

---

## Project Overview

The **Tattoo Lead CRM API** is an internal backend service that centralizes customer and lead data for an independent tattoo artist. It provides a single source of truth for who inquired, what they want, where each lead stands in the pipeline, notes from conversations, and scheduled sessions. The API is stateless, uses SQLite for portability, and exposes OpenAPI documentation for integration with a frontend or other clients.

---

## Business Problem

Solo tattoo artists typically receive inquiries across multiple channels—Instagram DMs, email, and referrals—with no unified place to track them. Context (tattoo idea, placement, size, budget) is scattered across conversations. It becomes hard to see which leads are new, which replied, which are scheduled, and which went cold. Many rely on spreadsheets or ad-hoc notes, leading to missed follow-ups and lost bookings. The core challenges are fragmented data, no visible pipeline, and manual tracking that does not scale.

---

## Solution

This API addresses those challenges by:

1. **Storing clients** — Contact details (name, Instagram, phone, email, preferred contact method).
2. **Turning inquiries into leads** — Each inquiry is a lead linked to a client, with tattoo details (idea, body location, size, style, source, estimated budget).
3. **Tracking lead status** — A defined pipeline: `new` → `awaiting_client_reply` → `in_conversation` → `scheduled` → `closed` or `lost`.
4. **Attaching notes to leads** — Conversation history and reminders per lead.
5. **Managing one appointment per lead** — Date, time, and session notes.

All of this is exposed through a REST API with request/response validation and automatic OpenAPI docs.

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

Dependencies flow in one direction: **routers → services → models**. Schemas are used at the router boundary (input/output) and are not tied to database columns.

---

## Features

- **Client management** — Create, list, and retrieve clients by ID.
- **Lead management** — Create leads linked to clients; list with optional status filter; get lead by ID (including nested client); update lead status.
- **Notes** — Create and list notes per lead (nested under `/leads/{lead_id}/notes`).
- **Appointments** — Create or update one appointment per lead; get appointment by lead (returns `null` if none).
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

**Lead** — A single tattoo inquiry tied to one client. Holds the request details: `original_message`, `tattoo_idea`, `body_location`, `size`, `style`, `color_type`, `design_type`, `summary`, `status`, `source`, `estimated_budget_range`, plus `created_at` and `updated_at`. Each lead has a lifecycle status and can have many notes and at most one appointment.

**Note** — A note attached to a lead (e.g. conversation summary or reminder). Fields: `lead_id`, `content`, `created_at`. Many notes per lead.

**Appointment** — A scheduled session for a lead. One appointment per lead (`lead_id` is unique). Fields: `lead_id`, `scheduled_date`, `scheduled_time`, `session_notes`, `created_at`.

**Relationships**

- **Client** → **Lead**: one-to-many. A client can have multiple leads (e.g. multiple ideas or follow-up projects).
- **Lead** → **Note**: one-to-many. A lead can have many notes.
- **Lead** → **Appointment**: one-to-one. A lead has at most one appointment.

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
│   │   └── appointment.py
│   ├── schemas/             # Pydantic (API request/response contracts)
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── note.py
│   │   └── appointment.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── client_service.py
│   │   ├── lead_service.py
│   │   ├── note_service.py
│   │   └── appointment_service.py
│   └── routers/             # HTTP endpoints
│       ├── __init__.py
│       ├── clients.py
│       ├── leads.py
│       ├── notes.py
│       └── appointments.py
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
| POST | `/leads/{lead_id}/appointment` | Create or update the lead’s appointment (one per lead). |
| GET | `/leads/{lead_id}/appointment` | Get the lead’s appointment (or `null`). |

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

This example shows how a single tattoo inquiry moves through the system from first contact to a scheduled appointment.

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

**4. Add a note** after talking to the client (e.g. lead id `1`)

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

**6. Schedule the appointment**

```bash
curl -X POST http://127.0.0.1:8000/leads/1/appointment \
  -H "Content-Type: application/json" \
  -d '{"scheduled_date": "2025-04-15", "scheduled_time": "14:00:00", "session_notes": "Session 1 - forearm rose"}'
```

**7. Get full lead detail** (with client and status)

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
