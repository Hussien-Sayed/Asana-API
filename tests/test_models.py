import pytest
from pydantic import ValidationError
from models import (
    TaskResponse,
    CommentRequest,
    CommentResponse,
    TaskUpdateResponse,
    ErrorResponse,
    CustomField,
    TaskCommentResponse,
)


class TestCustomField:
    def test_custom_field_valid(self):
        """Test valid CustomField instantiation with all fields."""
        custom_field = CustomField(
            gid="cf1",
            name="Priority",
            display_value="High",
            type="enum"
        )
        assert custom_field.gid == "cf1"
        assert custom_field.name == "Priority"
        assert custom_field.display_value == "High"
        assert custom_field.type == "enum"

    def test_custom_field_serialization(self):
        """Test CustomField serialization with optional fields defaulting to None."""
        custom_field = CustomField(gid="cf1", name="Priority")
        assert custom_field.display_value is None
        assert custom_field.type is None


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
            custom_fields=[{"gid": "cf1", "name": "Priority", "display_value": "High", "type": "enum"}]
        )
        assert task.gid == "12345"
        assert task.name == "Test Task"
        assert task.completed is False
        assert task.completed_at == "2024-01-01T00:00:00Z"
        assert task.assignee == {"gid": "67890", "name": "John Doe"}
        assert task.due_on == "2024-01-15"
        assert task.notes == "Some notes"
        assert task.permalink_url == "https://app.asana.com/0/12345/67890"
        assert task.custom_fields[0].name == "Priority"

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
            "custom_fields": [],
        }
        assert task.custom_fields == []

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


class TestTaskCommentResponse:
    def test_task_comment_response_valid(self):
        """Test valid TaskCommentResponse instantiation with all fields."""
        comment = TaskCommentResponse(
            gid="s1",
            text="Hello",
            created_at="2024-01-01T00:00:00Z",
            created_by={"gid": "u1", "name": "Alice"}
        )
        assert comment.gid == "s1"
        assert comment.text == "Hello"
        assert comment.created_at == "2024-01-01T00:00:00Z"
        assert comment.created_by == {"gid": "u1", "name": "Alice"}

    def test_task_comment_response_serialization(self):
        """Test TaskCommentResponse serialization with optional field defaulting to None."""
        comment = TaskCommentResponse(
            gid="s1",
            text="Hello",
            created_at="2024-01-01T00:00:00Z"
        )
        assert comment.created_by is None


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

