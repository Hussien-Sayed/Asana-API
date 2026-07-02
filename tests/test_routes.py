import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from routes.tasks import router, get_task_service
from models import TaskResponse, CommentResponse, TaskUpdateResponse


@pytest.fixture
def mock_task_service():
    return MagicMock()


@pytest.fixture
def client(mock_task_service):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_task_service] = lambda: mock_task_service
    return TestClient(app)


class TestGetTasks:
    def test_get_tasks_success(self, client, mock_task_service):
        """Test GET /projects/{project_id}/tasks returns list of tasks successfully."""
        mock_task_service.list_tasks.return_value = [
            TaskResponse(
                gid="123",
                name="Task 1",
                completed=False,
                completed_at=None,
                assignee=None,
                due_on=None,
                notes=None,
                permalink_url=None
            )
        ]

        response = client.get("/projects/proj123/tasks")

        assert response.status_code == 200
        assert response.json() == [
            {
                "gid": "123",
                "name": "Task 1",
                "completed": False,
                "completed_at": None,
                "assignee": None,
                "due_on": None,
                "notes": None,
                "permalink_url": None
            }
        ]
        mock_task_service.list_tasks.assert_called_once_with("proj123")

    def test_get_tasks_service_error(self, client, mock_task_service):
        """Test GET /projects/{project_id}/tasks returns 500 when service raises HTTPException."""
        mock_task_service.list_tasks.side_effect = HTTPException(
            status_code=500, detail="error"
        )

        response = client.get("/projects/proj123/tasks")

        assert response.status_code == 500
        assert response.json() == {"detail": "error"}


class TestAddComment:
    def test_add_comment_success(self, client, mock_task_service):
        """Test POST /projects/{project_id}/tasks/{task_id}/comment adds comment successfully."""
        mock_task_service.add_comment.return_value = CommentResponse(
            gid="456",
            text="A comment",
            created_at="2024-01-01T00:00:00Z"
        )

        response = client.post(
            "/projects/proj123/tasks/123/comment",
            json={"text": "A comment"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "gid": "456",
            "text": "A comment",
            "created_at": "2024-01-01T00:00:00Z"
        }
        mock_task_service.add_comment.assert_called_once_with("proj123", "123", "A comment")

    def test_add_comment_invalid_input(self, client, mock_task_service):
        """Test POST /projects/{project_id}/tasks/{task_id}/comment returns 422 when text field is missing."""
        response = client.post(
            "/projects/proj123/tasks/123/comment",
            json={}
        )

        assert response.status_code == 422
        mock_task_service.add_comment.assert_not_called()

    def test_add_comment_task_not_found(self, client, mock_task_service):
        """Test POST /projects/{project_id}/tasks/{task_id}/comment returns 404 when task not found."""
        mock_task_service.add_comment.side_effect = HTTPException(
            status_code=404, detail="Task not found"
        )

        response = client.post(
            "/projects/proj123/tasks/123/comment",
            json={"text": "A comment"}
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}


class TestCompleteTask:
    def test_complete_task_success(self, client, mock_task_service):
        """Test POST /projects/{project_id}/tasks/{task_id}/complete marks task as complete successfully."""
        mock_task_service.complete_task.return_value = TaskUpdateResponse(
            gid="123",
            name="Task 1",
            completed=True
        )

        response = client.post("/projects/proj123/tasks/123/complete")

        assert response.status_code == 200
        assert response.json() == {
            "gid": "123",
            "name": "Task 1",
            "completed": True
        }
        mock_task_service.complete_task.assert_called_once_with("proj123", "123")

    def test_complete_task_task_not_found(self, client, mock_task_service):
        """Test POST /projects/{project_id}/tasks/{task_id}/complete returns 404 when task not found."""
        mock_task_service.complete_task.side_effect = HTTPException(
            status_code=404, detail="Task not found"
        )

        response = client.post("/projects/proj123/tasks/123/complete")

        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

