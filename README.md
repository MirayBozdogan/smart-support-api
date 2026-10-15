# Smart Support API

A Python API for managing support tickets, with plans for machine learning-based categorization.

## Current status

Create and list support tickets with input validation. Tickets are temporarily stored in memory and are lost when the application restarts. Database storage and machine learning features are not implemented yet.

## Endpoints

- `GET /`: Welcome message
- `POST /tickets`: Create a ticket (title: 3–100 characters; description: 10–2000 characters)
- `GET /tickets`: List tickets

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

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 for the welcome endpoint and http://127.0.0.1:8000/docs for the interactive API documentation.

## Planned features

- Update ticket status and assign tickets
- Filter tickets by category and status
- Store tickets in SQLite
- Train and evaluate a text classification model for category suggestions
