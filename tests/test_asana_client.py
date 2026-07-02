import pytest
from unittest.mock import patch, MagicMock
from asana_client import AsanaClient


class TestAsanaClient:
    """Unit tests for AsanaClient wrapper class."""

    def test_init(self):
        """Verify ApiClient is initialized with access token."""
        access_token = "test_token_123"

        with patch("asana_client.asana.Configuration") as mock_config, \
             patch("asana_client.asana.ApiClient") as mock_api_client:
            
            # Setup mock configuration instance
            mock_config_instance = MagicMock()
            mock_config.return_value = mock_config_instance
            
            # Setup mock ApiClient instance
            mock_api_client_instance = MagicMock()
            mock_api_client.return_value = mock_api_client_instance
            
            # Create AsanaClient
            client = AsanaClient(access_token)
            
            # Verify Configuration was created
            mock_config.assert_called_once()
            
            # Verify access_token was set on configuration
            assert mock_config_instance.access_token == access_token
            
            # Verify ApiClient was created with configuration
            mock_api_client.assert_called_once_with(mock_config_instance)
            
            # Verify api_client is stored
            assert client.api_client == mock_api_client_instance

    def test_get_tasks_api(self):
        """Verify TasksApi instance is returned."""
        with patch("asana_client.asana.Configuration") as mock_config, \
             patch("asana_client.asana.ApiClient") as mock_api_client, \
             patch("asana_client.asana.TasksApi") as mock_tasks_api:
            
            # Setup mocks
            mock_config_instance = MagicMock()
            mock_config.return_value = mock_config_instance
            
            mock_api_client_instance = MagicMock()
            mock_api_client.return_value = mock_api_client_instance
            
            mock_tasks_api_instance = MagicMock()
            mock_tasks_api.return_value = mock_tasks_api_instance
            
            # Create AsanaClient
            client = AsanaClient("test_token")
            
            # Call get_tasks_api
            tasks_api = client.get_tasks_api()
            
            # Verify TasksApi was called with api_client
            mock_tasks_api.assert_called_once_with(client.api_client)
            
            # Verify the returned instance is the mock
            assert tasks_api == mock_tasks_api_instance

    def test_get_stories_api(self):
        """Verify StoriesApi instance is returned."""
        with patch("asana_client.asana.Configuration") as mock_config, \
             patch("asana_client.asana.ApiClient") as mock_api_client, \
             patch("asana_client.asana.StoriesApi") as mock_stories_api:
            
            # Setup mocks
            mock_config_instance = MagicMock()
            mock_config.return_value = mock_config_instance
            
            mock_api_client_instance = MagicMock()
            mock_api_client.return_value = mock_api_client_instance
            
            mock_stories_api_instance = MagicMock()
            mock_stories_api.return_value = mock_stories_api_instance
            
            # Create AsanaClient
            client = AsanaClient("test_token")
            
            # Call get_stories_api
            stories_api = client.get_stories_api()
            
            # Verify StoriesApi was called with api_client
            mock_stories_api.assert_called_once_with(client.api_client)
            
            # Verify the returned instance is the mock
            assert stories_api == mock_stories_api_instance

