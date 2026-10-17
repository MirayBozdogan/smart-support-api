# Smart Support API

A Python API for managing support tickets, with plans for machine learning-based categorization.

## Current status

Create, list and view support tickets, and update their status with input validation. Tickets are stored in SQLite and persist across application restarts. Machine learning features are not implemented yet.

## Endpoints

- `GET /`: Welcome message
- `POST /tickets`: Create a ticket (title: 3–100 characters; description: 10–2000 characters)
- `GET /tickets`: List all tickets, or filter by status (for example, `/tickets?status=open`). Allowed values: `open`, `in_progress`, `resolved`. Invalid values return 422; no matches return an empty list.
- `GET /tickets/{ticket_id}`: Get a ticket; returns 404 if it does not exist
- `PATCH /tickets/{ticket_id}/status`: Update status to `open`, `in_progress`, or `resolved`; returns 404 if the ticket does not exist

Example request body for updating a ticket's status:

```json
{
  "status": "in_progress"
}
```

Example request body for `POST /tickets`:

```json
{
  "title": "Payment issue",
  "description": "Payment was charged but my order was not created."
}
```

## Technologies

- Python
- FastAPI
- Uvicorn
- SQLite (via Python's built-in `sqlite3` module)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 for the welcome endpoint and http://127.0.0.1:8000/docs for the interactive API documentation.

The application automatically creates `support.db` in the project folder on startup. No separate database server is required. Local database files are excluded from Git. Tickets previously held in memory are not migrated.

## Planned features

- Assign tickets
- Filter tickets by category
- Train and evaluate a text classification model for category suggestions
