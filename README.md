# Smart Support API

A Python API for managing support tickets, with plans for machine learning-based categorization.

## Current status

Initial FastAPI application. Ticket management and machine learning features are not implemented yet.

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

- Create and list support tickets
- Update ticket status and assign tickets
- Filter tickets by category and status
- Store tickets in SQLite
- Train and evaluate a text classification model for category suggestions
