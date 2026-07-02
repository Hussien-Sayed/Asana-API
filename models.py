from typing import Optional
from pydantic import BaseModel


class TaskResponse(BaseModel):
    """Pydantic model for task data response."""

    gid: str
    name: str
    completed: bool
    completed_at: Optional[str] = None
    assignee: Optional[dict] = None
    due_on: Optional[str] = None
    notes: Optional[str] = None
    permalink_url: Optional[str] = None


class CommentRequest(BaseModel):
    """Pydantic model for comment creation request."""

    text: str


class CommentResponse(BaseModel):
    """Pydantic model for comment response."""

    gid: str
    text: str
    created_at: str


class TaskUpdateResponse(BaseModel):
    """Pydantic model for task update response."""

    gid: str
    name: str
    completed: bool


class ErrorResponse(BaseModel):
    """Pydantic model for error responses."""

    detail: str
