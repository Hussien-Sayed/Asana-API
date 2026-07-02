import uvicorn
from fastapi import FastAPI
from routes.tasks import router as tasks_router

app = FastAPI(title="Asana API", description="REST API for Asana task management", version="1.0.0")
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
