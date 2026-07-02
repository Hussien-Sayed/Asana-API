import asana


class AsanaClient:
    """Wrapper for the Asana API client providing access to TasksApi and StoriesApi."""

    def __init__(self, access_token: str):
        """
        Initialize the Asana API client wrapper.

        Args:
            access_token: Asana personal access token for authentication
        """
        configuration = asana.Configuration()
        configuration.access_token = access_token
        self.api_client = asana.ApiClient(configuration)

    def get_tasks_api(self) -> asana.TasksApi:
        """
        Return a TasksApi instance from the Asana client.

        Returns:
            TasksApi: Asana SDK TasksApi instance for task-related operations
        """
        return asana.TasksApi(self.api_client)

    def get_stories_api(self) -> asana.StoriesApi:
        """
        Return a StoriesApi instance from the Asana client.

        Returns:
            StoriesApi: Asana SDK StoriesApi instance for comment/story operations
        """
        return asana.StoriesApi(self.api_client)
