from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from contextlib import asynccontextmanager

from database import get_connection, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(title="Smart Support API", lifespan=lifespan)


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=2000)


TicketStatus = Literal["open", "in_progress", "resolved"]


class Ticket(TicketCreate):
    id: int
    status: TicketStatus = "open"


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


@app.get("/")
def home():
    return {"message": "Smart Support API çalışıyor."}


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tickets (title, description) VALUES (?, ?)",
            (ticket.title, ticket.description),
        )
        return Ticket(id=cursor.lastrowid, **ticket.model_dump())


@app.get("/tickets", response_model=list[Ticket])
def list_tickets():
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM tickets ORDER BY id").fetchall()
        return [Ticket(**dict(row)) for row in rows]


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        return Ticket(**dict(row))


@app.patch("/tickets/{ticket_id}/status", response_model=Ticket)
def update_ticket_status(ticket_id: int, update: TicketStatusUpdate):
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (update.status, ticket_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        return Ticket(**dict(row))
