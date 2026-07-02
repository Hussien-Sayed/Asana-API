import pytest
from pydantic import ValidationError
from models import (
    TaskResponse,
    CommentRequest,
    CommentResponse,
    TaskUpdateResponse,
    ErrorResponse,
)


class TestTaskResponse:
    def test_task_response_valid(self):
        """Test valid TaskResponse instantiation with all fields."""
        task = TaskResponse(
            gid="12345",
            name="Test Task",
            completed=False,
            completed_at="2024-01-01T00:00:00Z",
            assignee={"gid": "67890", "name": "John Doe"},
            due_on="2024-01-15",
            notes="Some notes",
            permalink_url="https://app.asana.com/0/12345/67890",
        )
        assert task.gid == "12345"
        assert task.name == "Test Task"
        assert task.completed is False
        assert task.completed_at == "2024-01-01T00:00:00Z"
        assert task.assignee == {"gid": "67890", "name": "John Doe"}
        assert task.due_on == "2024-01-15"
        assert task.notes == "Some notes"
        assert task.permalink_url == "https://app.asana.com/0/12345/67890"

    def test_task_response_serialization(self):
        """Test TaskResponse serialization with model_dump() and optional fields defaulting to None."""
        # Test with minimal required fields
        task = TaskResponse(gid="12345", name="Test Task", completed=True)
        data = task.model_dump()
        assert data == {
            "gid": "12345",
            "name": "Test Task",
            "completed": True,
            "completed_at": None,
            "assignee": None,
            "due_on": None,
            "notes": None,
            "permalink_url": None,
        }

        # Test with all fields
        task_full = TaskResponse(
            gid="12345",
            name="Test Task",
            completed=False,
            completed_at="2024-01-01T00:00:00Z",
            assignee={"gid": "67890"},
            due_on="2024-01-15",
        )
        data_full = task_full.model_dump()
        assert data_full["gid"] == "12345"
        assert data_full["name"] == "Test Task"
        assert data_full["completed"] is False
        assert data_full["completed_at"] == "2024-01-01T00:00:00Z"


class TestCommentRequest:
    def test_comment_request_valid(self):
        """Test valid CommentRequest instantiation."""
        comment = CommentRequest(text="This is a comment")
        assert comment.text == "This is a comment"

    def test_comment_request_missing_text(self):
        """Test that missing required 'text' field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            CommentRequest()
        assert "text" in str(exc_info.value).lower()
        assert "field required" in str(exc_info.value).lower()


class TestCommentResponse:
    def test_comment_response_valid(self):
        """Test valid CommentResponse instantiation."""
        comment = CommentResponse(
            gid="98765", text="This is a comment", created_at="2024-01-01T12:00:00Z"
        )
        assert comment.gid == "98765"
        assert comment.text == "This is a comment"
        assert comment.created_at == "2024-01-01T12:00:00Z"

    def test_comment_response_serialization(self):
        """Test CommentResponse serialization with model_dump()."""
        comment = CommentResponse(
            gid="98765", text="This is a comment", created_at="2024-01-01T12:00:00Z"
        )
        data = comment.model_dump()
        assert data == {
            "gid": "98765",
            "text": "This is a comment",
            "created_at": "2024-01-01T12:00:00Z",
        }


class TestTaskUpdateResponse:
    def test_task_update_response_valid(self):
        """Test valid TaskUpdateResponse instantiation."""
        update = TaskUpdateResponse(gid="12345", name="Updated Task", completed=True)
        assert update.gid == "12345"
        assert update.name == "Updated Task"
        assert update.completed is True

    def test_task_update_response_serialization(self):
        """Test TaskUpdateResponse serialization with model_dump()."""
        update = TaskUpdateResponse(gid="12345", name="Updated Task", completed=True)
        data = update.model_dump()
        assert data == {
            "gid": "12345",
            "name": "Updated Task",
            "completed": True,
        }


class TestErrorResponse:
    def test_error_response_valid(self):
        """Test valid ErrorResponse instantiation."""
        error = ErrorResponse(detail="Task not found")
        assert error.detail == "Task not found"

    def test_error_response_serialization(self):
        """Test ErrorResponse serialization with model_dump()."""
        error = ErrorResponse(detail="Task not found")
        data = error.model_dump()
        assert data == {"detail": "Task not found"}

