# Asana API

A lightweight FastAPI service that exposes three REST endpoints for managing Asana tasks:

- List tasks in a project
- Add a comment to a task
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
```

Only `ASANA_ACCESS_TOKEN` is required to start the server. The project ID is supplied per request in the URL path.

### 4. Run the server

```bash
python main.py
```

Uvicorn will start the application on `http://localhost:8000`.

You can also start it explicitly with Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Verify the server is healthy

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"status":"ok"}
```

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
    "notes": null,
    "permalink_url": "https://app.asana.com/0/..."
  }
]
```

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

---

## Running tests

```bash
python -m pytest
```

---

## End-to-end verification

An E2E plan and driver script are provided under `.agent_files/e2e_plans/` to run the three endpoints against the live Asana API. The E2E run performs real side effects (adds a comment and marks a task complete), so use a test project or test task.
