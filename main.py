from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
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
TicketCategory = Literal["payment", "account", "technical", "other"]


class Ticket(TicketCreate):
    id: int
    status: TicketStatus = "open"
    category: TicketCategory = "other"
    assignee: Optional[str] = None


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketCategoryUpdate(BaseModel):
    category: TicketCategory


class TicketAssigneeUpdate(BaseModel):
    assignee: Optional[str] = Field(..., min_length=2, max_length=100)

    @field_validator("assignee", mode="before")
    @classmethod
    def strip_assignee(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


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
def list_tickets(
    status: Optional[TicketStatus] = None,
    category: Optional[TicketCategory] = None,
):
    query = "SELECT * FROM tickets WHERE 1 = 1"
    parameters = []
    if status is not None:
        query += " AND status = ?"
        parameters.append(status)
    if category is not None:
        query += " AND category = ?"
        parameters.append(category)
    query += " ORDER BY id"

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
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


@app.patch("/tickets/{ticket_id}/category", response_model=Ticket)
def update_ticket_category(ticket_id: int, update: TicketCategoryUpdate):
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET category = ? WHERE id = ?",
            (update.category, ticket_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        return Ticket(**dict(row))


@app.patch("/tickets/{ticket_id}/assignee", response_model=Ticket)
def update_ticket_assignee(ticket_id: int, update: TicketAssigneeUpdate):
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET assignee = ? WHERE id = ?",
            (update.assignee, ticket_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        return Ticket(**dict(row))


@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def edit_ticket(ticket_id: int, update: TicketCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET title = ?, description = ? WHERE id = ?",
            (update.title, update.description, ticket_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        return Ticket(**dict(row))


@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tickets WHERE id = ?", (ticket_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
    return Response(status_code=204)
