from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models import TaskResponse, CommentRequest, CommentResponse, TaskUpdateResponse, TaskCommentResponse, AttachFileRequest, AttachFileResponse
from services.task_service import TaskService
from config import get_settings
from asana_client import AsanaClient

router = APIRouter(prefix="/projects", tags=["tasks"])


def get_task_service() -> TaskService:
    settings = get_settings()
    client = AsanaClient(settings.asana_access_token)
    return TaskService(client)


@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(project_id: str, task_service: TaskService = Depends(get_task_service)) -> List[TaskResponse]:
    try:
        return task_service.list_tasks(project_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")


@router.post("/{project_id}/tasks/{task_id}/comment", response_model=CommentResponse)
async def add_comment(
    project_id: str,
    task_id: str,
    comment: CommentRequest,
    task_service: TaskService = Depends(get_task_service)
) -> CommentResponse:
    try:
        return task_service.add_comment(project_id, task_id, comment.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add comment: {str(e)}")


@router.post("/{project_id}/tasks/{task_id}/complete", response_model=TaskUpdateResponse)
async def complete_task(
    project_id: str,
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
) -> TaskUpdateResponse:
    try:
        return task_service.complete_task(project_id, task_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete task: {str(e)}")


@router.post("/{project_id}/tasks/{task_id}/attach", response_model=AttachFileResponse)
async def attach_file(
    project_id: str,
    task_id: str,
    request: AttachFileRequest,
    task_service: TaskService = Depends(get_task_service)
) -> AttachFileResponse:
    try:
        return task_service.attach_file_to_task(project_id, task_id, request.filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to attach file: {str(e)}")


@router.get("/{project_id}/tasks/{task_id}/comments", response_model=List[TaskCommentResponse])
async def get_task_comments(
    project_id: str,
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
) -> List[TaskCommentResponse]:
    try:
        return task_service.get_task_comments(project_id, task_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve comments: {str(e)}")
