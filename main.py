from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI(title="Smart Support API")


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=2000)


TicketStatus = Literal["open", "in_progress", "resolved"]


class Ticket(TicketCreate):
    id: int
    status: TicketStatus = "open"


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


# Temporary storage: restarting the application clears all tickets.
tickets: list[Ticket] = []


@app.get("/")
def home():
    return {"message": "Smart Support API çalışıyor."}


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate):
    new_ticket = Ticket(id=len(tickets) + 1, **ticket.model_dump())
    tickets.append(new_ticket)
    return new_ticket


@app.get("/tickets", response_model=list[Ticket])
def list_tickets():
    return tickets


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Destek talebi bulunamadı.")


@app.patch("/tickets/{ticket_id}/status", response_model=Ticket)
def update_ticket_status(ticket_id: int, update: TicketStatusUpdate):
    ticket = get_ticket(ticket_id)
    ticket.status = update.status
    return ticket
