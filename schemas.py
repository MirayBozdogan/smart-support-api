from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


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
