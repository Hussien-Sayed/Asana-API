# Project Tree

## Asana-API

.env.example [x]
├── Functionality:
│   - Template file for environment variables
│   - Documents required configuration variables
│   - Serves as reference for setting up the project
├── Input:
│   - None (static template file)
└── Output:
    - Template with placeholder values for ASANA_ACCESS_TOKEN, ASANA_PROJECT_ID, ASANA_WORKSPACE_ID, APP_HOST

.env [x]
├── Functionality:
│   - Stores actual environment variables
│   - Loaded by application at runtime
│   - Not committed to version control
├── Input:
│   - None (manually created by user)
└── Output:
    - Environment variables: ASANA_ACCESS_TOKEN, ASANA_PROJECT_ID, ASANA_WORKSPACE_ID, APP_HOST

Dockerfile [x]
├── Functionality:
│   - Build the FastAPI application container image
│   - Install Python dependencies from requirements.txt
│   - Copy application source into the image
│   - Set APP_HOST=0.0.0.0 for container networking
│   - Use Python 3.12 slim base image (pydantic-core wheel compatibility)
├── Input:
│   - requirements.txt, source files
└── Output:
    - Runnable container image with Uvicorn on port 8000

docker-compose.yml [x]
├── Functionality:
│   - Build and run the Asana-API container locally
│   - Map port 127.0.0.1:8000:8000 to keep it local-only
│   - Load environment variables from .env at runtime
├── Input:
│   - Dockerfile, .env
└── Output:
    - Running container accessible only at http://127.0.0.1:8000

.dockerignore [x]
├── Functionality:
│   - Exclude files from the Docker build context
│   - Prevent secrets and build artifacts from being copied into the image
├── Input:
│   - None (static file)
└── Output:
    - List of ignored patterns: .env, __pycache__, .git, .agent_files, etc.

requirements.txt [x]
├── Functionality:
│   - Lists Python package dependencies
│   - Used for reproducible environment setup
│   - Specifies exact package versions
├── Input:
│   - None (static dependency list)
└── Output:
    - Package list: fastapi, uvicorn[standard], asana, pydantic, pydantic-settings, python-dotenv, httpx, pytest

asana_client.py [x]
├── class AsanaClient [x]
│   ├── method __init__() [x]
│   │   ├── Functionality:
│   │   │   - Initialize the Asana API client wrapper
│   │   │   - Set up authentication with access token
│   │   │   - Configure the underlying Asana ApiClient
│   │   ├── Input:
│   │   │   - access_token: str — Asana personal access token for authentication
│   │   └── Output:
│   │       - None (initializes instance attributes)
│   ├── method get_tasks_api() [x]
│   │   ├── Functionality:
│   │   │   - Return a TasksApi instance from the Asana client
│   │   │   - Provides access to task-related operations
│   │   ├── Input:
│   │   │   - None
│   │   └── Output:
│   │       - TasksApi — Asana SDK TasksApi instance
│   └── method get_stories_api() [x]
│       ├── Functionality:
│       │   - Return a StoriesApi instance from the Asana client
│       │   - Provides access to comment/story operations
│       ├── Input:
│       │   - None
│       └── Output:
│           - StoriesApi — Asana SDK StoriesApi instance

config.py [x]
├── class Settings [x]
│   ├── Functionality:
│   │   - Load and validate environment variables
│   │   - Provide type-safe configuration access
│   │   - Handle optional workspace ID
│   ├── Input:
│   │   - Environment variables from system or .env file
│   └── Output:
│       - asana_access_token: str — Asana personal access token
│       - asana_project_id: Optional[str] — Optional default project ID
│       - asana_workspace_id: Optional[str] — Optional workspace ID

main.py [x]
├── function main() [x]
│   ├── Functionality:
│   │   - Entry point of the FastAPI application
│   │   - Initialize the FastAPI app instance
│   │   - Register route handlers
│   │   - Configure dependency injection
│   │   - Start the Uvicorn server
│   │   - Read APP_HOST from environment (default 127.0.0.1 for local-only)
│   ├── Input:
│   │   - APP_HOST environment variable (optional, defaults to 127.0.0.1)
│   └── Output:
│       - None (runs the web server)

models.py [x]
├── class TaskResponse [x]
│   ├── Functionality:
│   │   - Pydantic model for task data response
│   │   - Validate task structure from Asana API
│   │   - Serialize task data to JSON
│   │   - Include custom fields list
│   ├── Input:
│   │   - gid: str — Task unique identifier
│   │   - name: str — Task name/title
│   │   - completed: bool — Task completion status
│   │   - completed_at: Optional[str] — Timestamp when task was completed
│   │   - assignee: Optional[dict] — Assignee information
│   │   - due_on: Optional[str] — Due date in YYYY-MM-DD format
│   │   - notes: Optional[str] — Task description/notes
│   │   - permalink_url: Optional[str] — URL to task in Asana web UI
│   │   - custom_fields: List[CustomField] — Custom fields list (defaults to [])
│   └── Output:
│       - Validated TaskResponse instance
├── class CustomField [x]
│   ├── Functionality:
│   │   - Pydantic model for custom field data
│   │   - Represent Asana custom field values
│   │   - Validate custom field structure
│   ├── Input:
│   │   - gid: str — Custom field unique identifier
│   │   - name: str — Custom field name (e.g., "Priority", "Project")
│   │   - display_value: Optional[str] — Display value of the custom field
│   │   - type: Optional[str] — Custom field type (e.g., "enum", "text")
│   └── Output:
│       - Validated CustomField instance
├── class TaskCommentResponse [x]
│   ├── Functionality:
│   │   - Pydantic model for task comment response
│   │   - Represent individual comment items from stories
│   │   - Validate comment structure from Asana API
│   ├── Input:
│   │   - gid: str — Comment unique identifier
│   │   - text: str — Comment message text
│   │   - created_at: str — Timestamp when comment was created
│   │   - created_by: Optional[dict] — Creator information (name, gid)
│   └── Output:
│       - Validated TaskCommentResponse instance
├── class CommentRequest [x]
│   ├── Functionality:
│   │   - Pydantic model for comment creation request
│   │   - Validate incoming comment data
│   │   - Ensure required text field is present
│   ├── Input:
│   │   - text: str — Comment message text
│   └── Output:
│       - Validated CommentRequest instance
├── class CommentResponse [x]
│   ├── Functionality:
│   │   - Pydantic model for comment response
│   │   - Validate comment data from Asana API
│   │   - Serialize comment to JSON
│   ├── Input:
│   │   - gid: str — Comment unique identifier
│   │   - text: str — Comment message text
│   │   - created_at: str — Timestamp when comment was created
│   └── Output:
│       - Validated CommentResponse instance
├── class TaskUpdateResponse [x]
│   ├── Functionality:
│   │   - Pydantic model for task update response
│   │   - Validate updated task data
│   │   - Return minimal task status after update
│   ├── Input:
│   │   - gid: str — Task unique identifier
│   │   - name: str — Task name/title
│   │   - completed: bool — Updated completion status
│   └── Output:
│       - Validated TaskUpdateResponse instance
└── class ErrorResponse [x]
    ├── Functionality:
    │   - Pydantic model for error responses
    │   - Standardize error message format
    │   - Provide consistent error structure to clients
    ├── Input:
    │   - detail: str — Error message description
    └── Output:
        - Validated ErrorResponse instance

routes/
└── tasks.py [x]
    ├── variable router [x]
    │   ├── Functionality:
    │   │   - FastAPI APIRouter instance
    │   │   - Groups task-related endpoints under /projects
    │   │   - Configures prefix and tags for documentation
    │   ├── Input:
    │   │   - None (router configuration)
    │   └── Output:
    │       - APIRouter configured with prefix="/projects" and tags=["tasks"]
    ├── function get_tasks() [x]
    │   ├── Functionality:
    │   │   - GET endpoint to retrieve all tasks from a project
    │   │   - Accept project_id from the URL path
    │   │   - Call task service to fetch tasks from the specified project
    │   │   - Return list of task objects
    │   │   - Handle service errors with 500 response
    │   ├── Input:
    │   │   - project_id: str — Path parameter for project ID
    │   │   - task_service: TaskService — Injected service instance via Depends
    │   └── Output:
    │       - List[TaskResponse] — JSON array of task objects
    │       - HTTPException with status 500 on service failure
    ├── function add_comment() [x]
    │   ├── Functionality:
    │   │   - POST endpoint to add comment to a task
    │   │   - Accept project_id and task_id from the URL path
    │   │   - Validate comment request body
    │   │   - Call task service to create comment
    │   │   - Return created comment details
    │   │   - Handle 404 for missing tasks, 500 for API failures
    │   ├── Input:
    │   │   - project_id: str — Path parameter for project ID
    │   │   - task_id: str — Path parameter for task ID
    │   │   - comment: CommentRequest — Request body with comment text
    │   │   - task_service: TaskService — Injected service instance via Depends
    │   └── Output:
    │       - CommentResponse — JSON with created comment details
    │       - HTTPException with status 404 if task not found
    │       - HTTPException with status 500 on service failure
    ├── function complete_task() [x]
    │   ├── Functionality:
    │   │   - POST endpoint to mark task as complete
    │   │   - Accept project_id and task_id from the URL path
    │   │   - Call task service to update task status
    │   │   - Return updated task status
    │   │   - Handle 404 for missing tasks, 500 for API failures
    │   ├── Input:
    │   │   - project_id: str — Path parameter for project ID
    │   │   - task_id: str — Path parameter for task ID
    │   │   - task_service: TaskService — Injected service instance via Depends
    │   └── Output:
    │       - TaskUpdateResponse — JSON with updated task status
    │       - HTTPException with status 404 if task not found
    │       - HTTPException with status 500 on service failure
    └── function get_task_comments() [x]
        ├── Functionality:
        │   - GET endpoint to retrieve comments for a specific task
        │   - Accept project_id and task_id from the URL path
        │   - Call task service to fetch comments
        │   - Return list of comment objects
        │   - Handle 404 for missing tasks, 500 for API failures
        ├── Input:
        │   - project_id: str — Path parameter for project ID
        │   - task_id: str — Path parameter for task ID
        │   - task_service: TaskService — Injected service instance via Depends
        └── Output:
            - List[TaskCommentResponse] — JSON array of comment objects
            - HTTPException with status 404 if task not found
            - HTTPException with status 500 on service failure

services/
└── task_service.py [x]
    └── class TaskService [x]
        ├── method __init__() [x]
        │   ├── Functionality:
        │   │   - Initialize the task service
        │   │   - Store Asana client instance
        │   ├── Input:
        │   │   - asana_client: AsanaClient — Configured Asana client wrapper
        │   └── Output:
        │       - None (initializes instance attributes)
        ├── method list_tasks() [x]
        │   ├── Functionality:
        │   │   - Retrieve all tasks from a given Asana project
        │   │   - Use TasksApi to fetch tasks by project ID
        │   │   - Transform Asana task objects to TaskResponse models
        │   │   - Add custom_fields to opt_fields string
        │   │   - Map custom fields from response to CustomField models
        │   │   - Handle API errors and raise appropriate exceptions
        │   ├── Input:
        │   │   - project_id: str — ID of the Asana project to query
        │   └── Output:
        │       - List[TaskResponse] — List of task objects with custom fields
        │       - Raises HTTPException 500 on Asana API failure
        ├── method add_comment() [x]
        │   ├── Functionality:
        │   │   - Add a comment to a specific task
        │   │   - Use StoriesApi to create a story/comment
        │   │   - Transform response to CommentResponse model
        │   │   - Handle 404 errors for missing tasks
        │   ├── Input:
        │   │   - project_id: str — ID of the Asana project (for route consistency)
        │   │   - task_id: str — ID of the task to comment on
        │   │   - text: str — Comment message text
        │   └── Output:
        │       - CommentResponse — Created comment details
        │       - Raises HTTPException 404 if task not found
        │       - Raises HTTPException 500 on Asana API failure
        ├── method complete_task() [x]
        │   ├── Functionality:
        │   │   - Mark a specific task as complete
        │   │   - Use TasksApi to update task completed status
        │   │   - Transform response to TaskUpdateResponse model
        │   │   - Handle 404 errors for missing tasks
        │   ├── Input:
        │   │   - project_id: str — ID of the Asana project (for route consistency)
        │   │   - task_id: str — ID of the task to complete
        │   └── Output:
        │       - TaskUpdateResponse — Updated task status
        │       - Raises HTTPException 404 if task not found
        │       - Raises HTTPException 500 on Asana API failure
        └── method get_task_comments() [x]
            ├── Functionality:
            │   - Retrieve comments for a specific task
            │   - Use StoriesApi.get_stories_for_task() to fetch stories
            │   - Filter stories by resource_subtype == "comment_added"
            │   - Transform filtered stories to TaskCommentResponse models
            │   - Handle 404 errors for missing tasks
            │   - Handle API errors with 500 response
            ├── Input:
            │   - project_id: str — ID of the Asana project (for route consistency)
            │   - task_id: str — ID of the task to fetch comments for
            └── Output:
                - List[TaskCommentResponse] — List of comment objects
                - Raises HTTPException 404 if task not found
                - Raises HTTPException 500 on Asana API failure
