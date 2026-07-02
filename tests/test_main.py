from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from routes.tasks import get_task_service


def test_main():
    mock_service = MagicMock()
    app.dependency_overrides[get_task_service] = lambda: mock_service
    client = TestClient(app)
    # Test GET / returns 200 and {"status": "ok"}
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # Test that /projects/{project_id}/tasks route is registered
    mock_service.list_tasks.return_value = []
    response = client.get("/projects/test-project/tasks")
    assert response.status_code == 200
    app.dependency_overrides.clear()
