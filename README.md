# Tattoo Lead CRM API

A REST API for managing clients, leads, notes, and appointments for a solo tattoo artist. Built with **FastAPI**, **SQLAlchemy**, and **Pydantic** as a backend portfolio project demonstrating API design, data modeling, and clean architecture.

---

## Project Overview

This project is an **internal CRM (Customer Relationship Management) API** tailored to the workflow of an independent tattoo artist. It centralizes contact and lead data, tracks inquiry status, stores notes per lead, and manages a single appointment per lead—all through a simple, well-documented REST API.

---

## Business Problem

Solo tattoo artists often:

- Receive inquiries via Instagram DMs, email, or referrals with no single place to track them.
- Lose context when switching between conversations (idea, placement, size, budget).
- Forget which leads replied, which are scheduled, and which went cold.
- Rely on spreadsheets or scattered notes, leading to missed follow-ups and lost bookings.

**Pain points:** fragmented data, no pipeline visibility, and manual tracking that doesn’t scale.

---

## Solution

A **REST API** that:

1. **Stores clients** (name, Instagram, phone, email, preferred contact).
2. **Turns inquiries into leads** linked to a client, with tattoo details (idea, location, size, style, source, budget).
3. **Tracks lead status** through a defined pipeline: `new` → `awaiting_client_reply` → `in_conversation` → `scheduled` → `closed` or `lost`.
4. **Attaches notes** to each lead for conversation history and reminders.
5. **Manages one appointment per lead** (date, time, session notes).

The API is stateless, uses SQLite for simplicity and portability, and exposes OpenAPI docs for easy integration with a future frontend or mobile app.

---

## Features

- **Client management** — Create, list, and retrieve clients by ID.
- **Lead management** — Create leads linked to clients; list with optional status filter; get lead detail (including client); update lead status.
- **Notes** — Create and list notes per lead (nested under `/leads/{lead_id}/notes`).
- **Appointments** — Create or update one appointment per lead; get appointment by lead (returns `null` if none).
- **Automatic docs** — Swagger UI and ReDoc from OpenAPI schema.
- **Structured errors** — 404 and validation errors with clear messages.
- **Database** — SQLite with SQLAlchemy ORM; tables created on startup.

---

## Tech Stack

| Layer        | Technology |
|-------------|------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Server**    | [Uvicorn](https://www.uvicorn.org/) (ASGI) |
| **ORM**       | [SQLAlchemy](https://www.sqlalchemy.org/) 2.x |
| **Validation & serialization** | [Pydantic](https://docs.pydantic.dev/) 2.x |
| **Database**  | SQLite (file-based, no extra setup) |
| **Language**  | Python 3.10+ |

---

## Project Structure

```
tattoo-lead-crm/
├── app/
│   ├── main.py              # FastAPI app, lifespan, router registration
│   ├── database.py          # Engine, session, get_db, init_db
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── note.py
│   │   └── appointment.py
│   ├── schemas/             # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── note.py
│   │   └── appointment.py
│   ├── services/            # Business logic (no HTTP here)
│   │   ├── __init__.py
│   │   ├── client_service.py
│   │   ├── lead_service.py
│   │   ├── note_service.py
│   │   └── appointment_service.py
│   └── routers/             # API endpoints
│       ├── __init__.py
│       ├── clients.py
│       ├── leads.py
│       ├── notes.py
│       └── appointments.py
├── requirements.txt
└── README.md
```

- **Routers** — Handle HTTP, validate input via Pydantic, call services, return responses.
- **Services** — Contain business logic and database operations.
- **Models** — Define tables and relationships; **schemas** define API contracts.

---

## Database Entities

| Entity       | Table         | Description |
|-------------|---------------|-------------|
| **Client**  | `clients`     | Contact info: `full_name`, `instagram_handle`, `phone`, `email`, `preferred_contact_method`, `created_at`. |
| **Lead**    | `leads`       | One per inquiry; `client_id` (FK); fields: `original_message`, `tattoo_idea`, `body_location`, `size`, `style`, `color_type`, `design_type`, `summary`, `status`, `source`, `estimated_budget_range`; timestamps. |
| **Note**    | `notes`       | `lead_id` (FK), `content`, `created_at`. Many notes per lead. |
| **Appointment** | `appointments` | `lead_id` (FK, unique), `scheduled_date`, `scheduled_time`, `session_notes`, `created_at`. One appointment per lead. |

**Relationships:**

- **Client** → **Lead** (one-to-many).
- **Lead** → **Note** (one-to-many).
- **Lead** → **Appointment** (one-to-one).

Cascade deletes: deleting a client removes its leads; deleting a lead removes its notes and appointment.

---

## API Endpoints

### Root

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and links to docs. |

### Clients

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/clients` | Create a client. |
| GET | `/clients` | List clients (optional `skip`, `limit`). |
| GET | `/clients/{client_id}` | Get client by ID. |

### Leads

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/leads` | Create a lead (body: `client_id`, tattoo fields, `status`, `source`, etc.). |
| GET | `/leads` | List leads; optional query `?status=new` (or other status). |
| GET | `/leads/{lead_id}` | Get lead by ID (includes nested client). |
| PATCH | `/leads/{lead_id}/status` | Update lead status. |

**Lead status values:** `new`, `awaiting_client_reply`, `in_conversation`, `scheduled`, `closed`, `lost`.

### Notes (nested under leads)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/leads/{lead_id}/notes` | Create a note for the lead. |
| GET | `/leads/{lead_id}/notes` | List notes for the lead. |

### Appointments (nested under leads)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/leads/{lead_id}/appointment` | Create or update the lead’s appointment (one per lead). |
| GET | `/leads/{lead_id}/appointment` | Get the lead’s appointment (or `null`). |

---

## How to Run Locally

**Prerequisites:** Python 3.10+

1. **Clone and enter the project:**

   ```bash
   cd tattoo-lead-crm
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   API base URL: **http://127.0.0.1:8000**

5. **Open the docs:**

   - **Swagger UI:** http://127.0.0.1:8000/docs  
   - **ReDoc:** http://127.0.0.1:8000/redoc  

The SQLite database file `tattoo_crm.db` is created automatically in the project root on first request.

---

## Example Workflow

1. **Create a client** (person who inquired):

   ```bash
   curl -X POST http://127.0.0.1:8000/clients \
     -H "Content-Type: application/json" \
     -d '{"full_name": "Maria Silva", "instagram_handle": "@maria.s", "phone": "+5511999999999", "preferred_contact_method": "instagram"}'
   ```

   Use the returned `id` (e.g. `1`) as `client_id` in the next step.

2. **Create a lead** for the inquiry:

   ```bash
   curl -X POST http://127.0.0.1:8000/leads \
     -H "Content-Type: application/json" \
     -d '{"client_id": 1, "tattoo_idea": "Flor no braço", "body_location": "braço", "size": "médio", "status": "new", "source": "instagram_dm"}'
   ```

3. **List new leads:**

   ```bash
   curl "http://127.0.0.1:8000/leads?status=new"
   ```

4. **Add a note** to the lead (e.g. lead id `1`):

   ```bash
   curl -X POST http://127.0.0.1:8000/leads/1/notes \
     -H "Content-Type: application/json" \
     -d '{"content": "Cliente pediu orçamento até sexta."}'
   ```

5. **Update status** when the client replies:

   ```bash
   curl -X PATCH http://127.0.0.1:8000/leads/1/status \
     -H "Content-Type: application/json" \
     -d '{"status": "in_conversation"}'
   ```

6. **Schedule an appointment** (e.g. 2025-04-15 at 14:00):

   ```bash
   curl -X POST http://127.0.0.1:8000/leads/1/appointment \
     -H "Content-Type: application/json" \
     -d '{"scheduled_date": "2025-04-15", "scheduled_time": "14:00:00", "session_notes": "Sessão 1 - flor braço"}'
   ```

7. **Get full lead detail** (with client and status):

   ```bash
   curl http://127.0.0.1:8000/leads/1
   ```

---

## Future Improvements

- **Authentication** — JWT or API keys to protect endpoints.
- **Pagination** — Cursor or offset metadata for list endpoints.
- **Filtering and search** — Filter leads by date range, source, or client name; full-text search on notes.
- **PostgreSQL** — Switch from SQLite for production and use connection pooling.
- **Migrations** — Alembic for versioned schema changes.
- **Tests** — Unit tests for services; integration tests for routers (e.g. pytest + TestClient).
- **Soft delete** — Mark leads/clients as deleted instead of hard delete.
- **Audit fields** — `updated_at` on all entities; optional `created_by` if auth is added.
- **Rate limiting** — Per-IP or per-user limits on public endpoints.
- **Frontend** — Simple SPA or mobile app consuming this API.

---

## License

Internal use / portfolio. Feel free to use this project as reference for your own backend work.
