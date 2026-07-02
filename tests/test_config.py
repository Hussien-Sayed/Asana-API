import pytest
from pydantic import ValidationError

from config import Settings


class TestSettings:
    """Test cases for the Settings configuration class."""

    def test_load_settings(self, monkeypatch):
        """Verify environment variables are loaded correctly."""
        monkeypatch.setenv("ASANA_ACCESS_TOKEN", "test_token_123")
        monkeypatch.setenv("ASANA_PROJECT_ID", "project_456")
        monkeypatch.setenv("ASANA_WORKSPACE_ID", "workspace_789")

        settings = Settings(_env_file=None)

        assert settings.asana_access_token == "test_token_123"
        assert settings.asana_project_id == "project_456"
        assert settings.asana_workspace_id == "workspace_789"

    def test_load_settings_without_project_id(self, monkeypatch):
        """Verify settings load correctly when project_id is not provided (optional)."""
        monkeypatch.setenv("ASANA_ACCESS_TOKEN", "test_token_123")
        monkeypatch.delenv("ASANA_PROJECT_ID", raising=False)

        settings = Settings(_env_file=None)

        assert settings.asana_access_token == "test_token_123"
        assert settings.asana_project_id is None

    def test_missing_access_token(self, monkeypatch):
        """Verify validation error when access token is missing."""
        monkeypatch.delenv("ASANA_ACCESS_TOKEN", raising=False)
        monkeypatch.setenv("ASANA_PROJECT_ID", "project_456")

        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("asana_access_token",) for error in errors)
