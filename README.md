# Asana API

A lightweight FastAPI service that exposes REST endpoints for managing Asana tasks:

- List tasks in a project (including custom fields such as Priority and Project)
- Get all comments on a task
- Add a comment to a task
- Attach a file to a task
- Mark a task as complete

The project ID is passed as a route parameter, so a single running instance can serve multiple Asana projects without restarting.

---

## Quick start

### 1. Clone / open the project

```bash
cd D:\Projects\Asana-API
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Required packages: `fastapi`, `uvicorn[standard]`, `asana`, `pydantic`, `pydantic-settings`, `python-dotenv`, `httpx`.

### 3. Configure environment variables

Copy the example file and fill in your real Asana credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required: Asana personal access token
ASANA_ACCESS_TOKEN=your_asana_personal_access_token_here

# Optional: default project ID (can also be provided via the API route)
# ASANA_PROJECT_ID=your_asana_project_id_here

# Optional: workspace ID if needed by your Asana workflow
# ASANA_WORKSPACE_ID=your_asana_workspace_id_here

# Optional: bind host (defaults to 127.0.0.1 for local-only when running directly)
# APP_HOST=127.0.0.1
```

Only `ASANA_ACCESS_TOKEN` is required to start the server. The project ID is supplied per request in the URL path.

### 4. Run the server

```bash
python main.py
```

Uvicorn will start the application on `http://localhost:8000`.

You can also start it explicitly with Uvicorn:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

---

## Running with Docker

### 1. Build and run with Docker Compose

```bash
docker compose up
```

This will:
- Build the Docker image from the local `Dockerfile`
- Start the container with the name `asana-api`
- Map port `127.0.0.1:8000` on the host to port `8000` in the container
- Load environment variables from `.env` at runtime

The service will be accessible at `http://127.0.0.1:8000`.

### 2. Verify the server is healthy

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"status":"ok"}
```

### 3. Stop the container

```bash
docker compose down
```

### Important notes

- When running with `python main.py` directly, the app binds to `127.0.0.1` by default (local-only).
- When running with Docker, the container internally uses `APP_HOST=0.0.0.0` to accept traffic from Docker's port forwarding.
- The Docker Compose port mapping `127.0.0.1:8000:8000` ensures the service is only accessible from the host machine, not from the local network or internet.

---

## File attachments with Docker

When using the `/attach` endpoint inside Docker, the file path you provide must exist **inside the container**. The cleanest way to achieve this is to mount a folder from your host machine into the container using a Docker volume.

### How it works

The `uploads/` folder at the project root is mounted into the container at `/uploads` (read-only). Any file you place in that folder on your host becomes immediately visible to the container.

```
Host:      D:\Projects\Asana-API\uploads\report.pdf
Container: /uploads/report.pdf   ← resolved automatically by the API
```

The volume mount is already configured in `docker-compose.yml` — no extra setup needed.

### Using it

1. Copy the file you want to attach into the `uploads/` folder at the project root.
2. Call the attach endpoint with just the filename:

```bash
curl -X POST http://localhost:8000/projects/{project_id}/tasks/{task_id}/attach \
  -H "Content-Type: application/json" \
  -d '{"filename": "report.pdf"}'
```

The `:ro` (read-only) mount means the container can read files from `uploads/` but cannot write back to your host filesystem.

---

## API endpoints

All task endpoints are scoped under `/projects/{project_id}`.

### List tasks in a project

```bash
GET /projects/{project_id}/tasks
```

Example:

```bash
curl http://localhost:8000/projects/1215861189381337/tasks
```

Response (excerpt):

```json
[
  {
    "gid": "1216147669244223",
    "name": "My task",
    "completed": false,
    "completed_at": null,
    "assignee": null,
    "due_on": null,
    "notes": "Task description here",
    "permalink_url": "https://app.asana.com/0/...",
    "custom_fields": [
      {"gid": "cf1", "name": "Priority", "display_value": "High", "type": "enum"},
      {"gid": "cf2", "name": "Project", "display_value": "Alpha", "type": "enum"}
    ]
  }
]
```

`custom_fields` contains every custom field configured on your Asana project. Fields not set on a task will appear with `"display_value": null`. Tasks with no custom fields will return an empty array.

### Get comments for a task

```bash
GET /projects/{project_id}/tasks/{task_id}/comments
```

Returns all user comments on the task (system events such as assignment changes are excluded).

Example:

```bash
curl http://localhost:8000/projects/1215861189381337/tasks/1216147669244223/comments
```

Response:

```json
[
  {
    "gid": "1234567890",
    "text": "This is a comment",
    "created_at": "2026-07-03T08:22:00.000Z",
    "created_by": {"gid": "987654321", "name": "Alice"}
  }
]
```

An empty array `[]` is returned if the task has no comments.

### Add a comment to a task

```bash
POST /projects/{project_id}/tasks/{task_id}/comment
```

Request body:

```json
{"text": "This is a comment from the API"}
```

Example:

```bash
curl -X POST http://localhost:8000/projects/1215861189381337/tasks/1216147669244223/comment \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a comment from the API"}'
```

Response:

```json
{
  "gid": "...",
  "text": "This is a comment from the API",
  "created_at": "2026-07-02T..."
}
```

### Attach a file to a task

```bash
POST /projects/{project_id}/tasks/{task_id}/attach
```

Attaches a file to a task in Asana. The file is referenced by its path on the server's filesystem.

Request body:

```json
{"filename": "report.pdf"}
```

You only provide the **filename** — the API automatically looks for it inside the `uploads/` folder.

Example:

```bash
curl -X POST http://localhost:8000/projects/1215861189381337/tasks/1216147669244223/attach \
  -H "Content-Type: application/json" \
  -d '{"filename": "report.pdf"}'
```

Response:

```json
{
  "gid": "...",
  "name": "report.pdf",
  "download_url": "https://..."
}
```

> **Running with Docker:** Place the file in the `uploads/` folder at the project root on your host machine. Docker mounts that folder into the container automatically. See the [File attachments with Docker](#file-attachments-with-docker) section below.

> **Running locally (no Docker):** Place the file in the `uploads/` folder next to `main.py` and provide just the filename.

### Mark a task as complete

```bash
POST /projects/{project_id}/tasks/{task_id}/complete
```

Example:

```bash
curl -X POST http://localhost:8000/projects/1215861189381337/tasks/1216147669244223/complete
```

Response:

```json
{
  "gid": "1216147669244223",
  "name": "My task",
  "completed": true
}
```

---

## Error responses

The API returns standard FastAPI / HTTP error responses:

- `422 Unprocessable Entity` — invalid request body (e.g., missing `text` for a comment)
- `404 Not Found` — the task does not exist or is not accessible
- `500 Internal Server Error` — Asana API failure or unexpected server error

All error responses are JSON:

```json
{"detail": "Error message here"}
```

---

## Configuration reference

| Environment variable | Required | Description |
| -------------------- | -------- | ----------- |
| `ASANA_ACCESS_TOKEN` | Yes | Asana personal access token used to authenticate API calls. |
| `ASANA_PROJECT_ID` | No | Optional default project ID. The project ID is normally provided in the request URL. |
| `ASANA_WORKSPACE_ID` | No | Optional Asana workspace ID. |
| `APP_HOST` | No | Host address for the FastAPI/Uvicorn server. Defaults to `127.0.0.1` for direct runs. Docker sets this to `0.0.0.0` internally. |

---

## Running tests

```bash
python -m pytest
```

---

## End-to-end verification

An E2E plan and driver script are provided under `.agent_files/e2e_plans/` to run the three endpoints against the live Asana API. The E2E run performs real side effects (adds a comment and marks a task complete), so use a test project or test task.
