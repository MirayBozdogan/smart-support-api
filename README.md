# Smart Support API

A Python API for managing support tickets, with plans for machine learning-based categorization.

## Current status

Create, list, view and permanently delete support tickets, and update their status with input validation. Tickets are stored in SQLite and persist across application restarts. Machine learning features are not implemented yet.

## Endpoints

- `GET /`: Welcome message
- `POST /tickets`: Create a ticket (title: 3–100 characters; description: 10–2000 characters)
- `GET /tickets`: List all tickets, or filter by status (for example, `/tickets?status=open`). Allowed values: `open`, `in_progress`, `resolved`. Invalid values return 422; no matches return an empty list.
- `GET /tickets/{ticket_id}`: Get a ticket; returns 404 if it does not exist
- `PATCH /tickets/{ticket_id}/category`: Set category to `payment`, `account`, `technical`, or `other`; returns 404 if the ticket does not exist, or 422 for invalid input.
- `PATCH /tickets/{ticket_id}`: Edit title and description (both required, using the same validation as creation). Preserves ID and status; returns 404 if the ticket does not exist.
- `PATCH /tickets/{ticket_id}/status`: Update status to `open`, `in_progress`, or `resolved`; returns 404 if the ticket does not exist
- `DELETE /tickets/{ticket_id}`: Permanently delete a ticket; returns 204 with no response body, or 404 if it does not exist

Tickets start in category `other`. To change it, send `{"category": "payment"}` to `PATCH /tickets/{ticket_id}/category`. Filter with `/tickets?category=payment`, or combine filters: `/tickets?status=open&category=payment`. Both filters must match when combined; no matches return an empty list. Invalid categories return 422.

Existing databases are updated automatically on startup: the category column is added if missing, existing tickets receive `other`, and their other fields are preserved. Category selection is currently manual; no model inference is performed.

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
- Train and evaluate a text classification model for category suggestions
