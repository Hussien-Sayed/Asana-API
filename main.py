import os
import uvicorn
from fastapi import FastAPI
from routes.tasks import router as tasks_router

app = FastAPI(title="Asana API", description="REST API for Asana task management", version="1.0.0")
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {"status": "ok"}


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    uvicorn.run(app, host=app_host, port=8000)
