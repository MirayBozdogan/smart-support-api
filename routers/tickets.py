from typing import Optional

from fastapi import APIRouter, HTTPException, Response

from database import get_connection
from schemas import (
    Ticket,
    TicketAssigneeUpdate,
    TicketCategory,
    TicketCategoryUpdate,
    TicketCreate,
    TicketStatus,
    TicketStatusUpdate,
)


router = APIRouter(prefix="/tickets")


@router.post("", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tickets (title, description) VALUES (?, ?)",
            (ticket.title, ticket.description),
        )
        return Ticket(id=cursor.lastrowid, **ticket.model_dump())


@router.get("", response_model=list[Ticket])
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


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
        return Ticket(**dict(row))


@router.patch("/{ticket_id}/status", response_model=Ticket)
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


@router.patch("/{ticket_id}/category", response_model=Ticket)
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


@router.patch("/{ticket_id}/assignee", response_model=Ticket)
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


@router.patch("/{ticket_id}", response_model=Ticket)
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


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tickets WHERE id = ?", (ticket_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")
    return Response(status_code=204)
