import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from asana.rest import ApiException

from services.task_service import TaskService
from models import TaskResponse, CommentResponse, TaskUpdateResponse, TaskCommentResponse


def make_api_exception(status: int, reason: str) -> ApiException:
    """Create a real ApiException with given status and reason."""
    exc = ApiException(status=status, reason=reason)
    exc.status = status
    exc.reason = reason
    return exc


class TestTaskService:
    """Test suite for TaskService class."""

    def test_init(self):
        """Test that TaskService initializes with asana_client."""
        mock_asana_client = MagicMock()
        service = TaskService(mock_asana_client)
        assert service.asana_client == mock_asana_client

    def test_list_tasks_success(self):
        """Test successful task listing."""
        mock_asana_client = MagicMock()
        mock_tasks_api = MagicMock()
        mock_asana_client.get_tasks_api.return_value = mock_tasks_api

        task_dict = {
            "gid": "123", "name": "Test Task", "completed": False,
            "completed_at": None, "assignee": None, "due_on": None,
            "notes": None, "permalink_url": None,
            "custom_fields": [{"gid": "cf1", "name": "Priority", "display_value": "High", "type": "enum"}]
        }
        mock_tasks_api.get_tasks_for_project.return_value = [task_dict]

        service = TaskService(mock_asana_client)
        result = service.list_tasks("proj123")

        assert len(result) == 1
        assert isinstance(result[0], TaskResponse)
        assert result[0].gid == "123"
        assert result[0].name == "Test Task"
        assert len(result[0].custom_fields) == 1
        assert result[0].custom_fields[0].name == "Priority"
        assert result[0].custom_fields[0].display_value == "High"
        expected_opts = {
            "opt_fields": "gid,name,completed,completed_at,assignee,due_on,notes,permalink_url,custom_fields"
        }
        mock_tasks_api.get_tasks_for_project.assert_called_once_with(project_gid="proj123", opts=expected_opts)

    def test_list_tasks_api_error(self):
        """Test list_tasks raises HTTPException 500 on ApiException."""
        mock_asana_client = MagicMock()
        mock_tasks_api = MagicMock()
        mock_asana_client.get_tasks_api.return_value = mock_tasks_api
        mock_tasks_api.get_tasks_for_project.side_effect = make_api_exception(500, "Internal Server Error")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.list_tasks("proj123")

        assert exc_info.value.status_code == 500
        assert "Asana API error" in exc_info.value.detail

    def test_add_comment_success(self):
        """Test successful comment addition."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api

        story_dict = {"gid": "456", "text": "My comment", "created_at": "2024-01-01T00:00:00Z"}
        mock_stories_api.create_story_for_task.return_value = story_dict

        service = TaskService(mock_asana_client)
        result = service.add_comment("proj123", "task123", "My comment")

        assert isinstance(result, CommentResponse)
        assert result.gid == "456"
        assert result.text == "My comment"
        expected_body = {"data": {"text": "My comment"}}
        mock_stories_api.create_story_for_task.assert_called_once_with(body=expected_body, task_gid="task123", opts={})

    def test_add_comment_task_not_found(self):
        """Test add_comment raises HTTPException 404 when task not found."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api
        mock_stories_api.create_story_for_task.side_effect = make_api_exception(404, "Not Found")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.add_comment("proj123", "task123", "My comment")

        assert exc_info.value.status_code == 404
        assert "Task not found" in exc_info.value.detail

    def test_add_comment_api_error(self):
        """Test add_comment raises HTTPException 500 on non-404 ApiException."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api
        mock_stories_api.create_story_for_task.side_effect = make_api_exception(500, "Internal Server Error")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.add_comment("proj123", "task123", "My comment")

        assert exc_info.value.status_code == 500
        assert "Asana API error" in exc_info.value.detail

    def test_complete_task_success(self):
        """Test successful task completion."""
        mock_asana_client = MagicMock()
        mock_tasks_api = MagicMock()
        mock_asana_client.get_tasks_api.return_value = mock_tasks_api

        task_update_dict = {"gid": "123", "name": "Test Task", "completed": True}
        mock_tasks_api.update_task.return_value = task_update_dict

        service = TaskService(mock_asana_client)
        result = service.complete_task("proj123", "task123")

        assert isinstance(result, TaskUpdateResponse)
        assert result.gid == "123"
        assert result.completed is True
        expected_body = {"data": {"completed": True}}
        mock_tasks_api.update_task.assert_called_once_with(body=expected_body, task_gid="task123", opts={})

    def test_complete_task_task_not_found(self):
        """Test complete_task raises HTTPException 404 when task not found."""
        mock_asana_client = MagicMock()
        mock_tasks_api = MagicMock()
        mock_asana_client.get_tasks_api.return_value = mock_tasks_api
        mock_tasks_api.update_task.side_effect = make_api_exception(404, "Not Found")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.complete_task("proj123", "task123")

        assert exc_info.value.status_code == 404
        assert "Task not found" in exc_info.value.detail

    def test_complete_task_api_error(self):
        """Test complete_task raises HTTPException 500 on non-404 ApiException."""
        mock_asana_client = MagicMock()
        mock_tasks_api = MagicMock()
        mock_asana_client.get_tasks_api.return_value = mock_tasks_api
        mock_tasks_api.update_task.side_effect = make_api_exception(500, "Internal Server Error")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.complete_task("proj123", "task123")

        assert exc_info.value.status_code == 500
        assert "Asana API error" in exc_info.value.detail

    def test_get_task_comments_success(self):
        """Test successful retrieval of task comments, filtering non-comment stories."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api

        stories = [
            {"gid": "s1", "text": "A comment", "created_at": "2024-01-01T00:00:00Z",
             "created_by": {"gid": "u1", "name": "Alice"}, "resource_subtype": "comment_added"},
            {"gid": "s2", "text": "Task created", "created_at": "2024-01-01T00:00:00Z",
             "created_by": None, "resource_subtype": "assigned"},
        ]
        mock_stories_api.get_stories_for_task.return_value = stories

        service = TaskService(mock_asana_client)
        result = service.get_task_comments("proj123", "task123")

        assert len(result) == 1
        assert isinstance(result[0], TaskCommentResponse)
        assert result[0].gid == "s1"
        assert result[0].text == "A comment"
        assert result[0].created_by == {"gid": "u1", "name": "Alice"}
        expected_opts = {"opt_fields": "gid,text,created_at,created_by,resource_subtype"}
        mock_stories_api.get_stories_for_task.assert_called_once_with(task_gid="task123", opts=expected_opts)

    def test_get_task_comments_task_not_found(self):
        """Test get_task_comments raises HTTPException 404 when task not found."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api
        mock_stories_api.get_stories_for_task.side_effect = make_api_exception(404, "Not Found")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.get_task_comments("proj123", "task123")

        assert exc_info.value.status_code == 404
        assert "Task not found" in exc_info.value.detail

    def test_get_task_comments_api_error(self):
        """Test get_task_comments raises HTTPException 500 on non-404 ApiException."""
        mock_asana_client = MagicMock()
        mock_stories_api = MagicMock()
        mock_asana_client.get_stories_api.return_value = mock_stories_api
        mock_stories_api.get_stories_for_task.side_effect = make_api_exception(500, "Internal Server Error")

        service = TaskService(mock_asana_client)

        with pytest.raises(HTTPException) as exc_info:
            service.get_task_comments("proj123", "task123")

        assert exc_info.value.status_code == 500
        assert "Asana API error" in exc_info.value.detail
