from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load and validate environment variables for Asana API configuration."""

    asana_access_token: str
    asana_project_id: Optional[str] = None
    asana_workspace_id: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    """Return a Settings instance (used for dependency injection)."""
    return Settings()
