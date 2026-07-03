from typing import Optional, List
from pydantic import BaseModel


class CustomField(BaseModel):
    """Pydantic model for a custom field value from Asana."""

    gid: str
    name: str
    display_value: Optional[str] = None
    type: Optional[str] = None


class TaskResponse(BaseModel):
    """Pydantic model for task data response including custom fields."""

    gid: str
    name: str
    completed: bool
    completed_at: Optional[str] = None
    assignee: Optional[dict] = None
    due_on: Optional[str] = None
    notes: Optional[str] = None
    permalink_url: Optional[str] = None
    custom_fields: List[CustomField] = []


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


class TaskCommentResponse(BaseModel):
    """Pydantic model for a task comment (story) from Asana."""

    gid: str
    text: str
    created_at: str
    created_by: Optional[dict] = None


class AttachFileRequest(BaseModel):
    """Pydantic model for a file attachment request."""

    filename: str


class AttachFileResponse(BaseModel):
    """Pydantic model for a file attachment response."""

    gid: str
    name: str
    download_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Pydantic model for error responses."""

    detail: str
