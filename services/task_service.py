from typing import List
from fastapi import HTTPException
import asana
from asana.rest import ApiException

from asana_client import AsanaClient
from models import TaskResponse, CommentResponse, TaskUpdateResponse, TaskCommentResponse, AttachFileResponse


class TaskService:
    """Service for interacting with Asana tasks."""

    def __init__(self, asana_client: AsanaClient):
        """
        Initialize the task service.

        Args:
            asana_client: AsanaClient instance for API access
        """
        self.asana_client = asana_client

    def list_tasks(self, project_id: str) -> List[TaskResponse]:
        """
        Get all tasks in the project.

        Args:
            project_id: ID of the Asana project to get tasks from

        Returns:
            List[TaskResponse]: List of tasks in the project

        Raises:
            HTTPException: 500 on Asana API error
        """
        tasks_api = self.asana_client.get_tasks_api()
        opts = {
            "opt_fields": "gid,name,completed,completed_at,assignee,due_on,notes,permalink_url,custom_fields"
        }

        try:
            result = tasks_api.get_tasks_for_project(project_gid=project_id, opts=opts)
            tasks = list(result)
            return [TaskResponse(**task) for task in tasks]
        except ApiException as e:
            raise HTTPException(status_code=500, detail=f"Asana API error: {e.reason}")

    def add_comment(self, project_id: str, task_id: str, text: str) -> CommentResponse:
        """
        Add a comment to a task.

        Args:
            project_id: ID of the Asana project (for route consistency, not used in API call)
            task_id: ID of the task to comment on
            text: Comment text

        Returns:
            CommentResponse: Created comment details

        Raises:
            HTTPException: 404 if task not found, 500 on other errors
        """
        stories_api = self.asana_client.get_stories_api()
        body = {"data": {"text": text}}
        
        try:
            result = stories_api.create_story_for_task(body=body, task_gid=task_id, opts={})
            return CommentResponse(**result)
        except ApiException as e:
            if e.status == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            raise HTTPException(status_code=500, detail=f"Asana API error: {e.reason}")

    def get_task_comments(self, project_id: str, task_id: str) -> List[TaskCommentResponse]:
        """
        Get all comments on a task.

        Args:
            project_id: ID of the Asana project (for route consistency, not used in API call)
            task_id: ID of the task to get comments for

        Returns:
            List[TaskCommentResponse]: List of comments on the task

        Raises:
            HTTPException: 404 if task not found, 500 on other errors
        """
        stories_api = self.asana_client.get_stories_api()
        opts = {
            "opt_fields": "gid,text,created_at,created_by,resource_subtype"
        }

        try:
            result = stories_api.get_stories_for_task(task_gid=task_id, opts=opts)
            comments = [
                TaskCommentResponse(**story)
                for story in result
                if story.get("resource_subtype") == "comment_added"
            ]
            return comments
        except ApiException as e:
            if e.status == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            raise HTTPException(status_code=500, detail=f"Asana API error: {e.reason}")

    def attach_file_to_task(self, project_id: str, task_id: str, filename: str) -> AttachFileResponse:
        """
        Attach a file from the uploads folder to a task.

        Args:
            project_id: ID of the Asana project (for route consistency, not used in API call)
            task_id: ID of the task to attach the file to
            filename: Name of the file inside the uploads folder (e.g. "report.pdf")

        Returns:
            AttachFileResponse: Created attachment details

        Raises:
            HTTPException: 404 if task or file not found, 500 on other errors
        """
        import os
        file_path = os.path.join("/uploads", filename)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found in uploads folder")

        attachments_api = self.asana_client.get_attachments_api()
        opts = {
            "resource_subtype": "asana",
            "file": file_path,
            "parent": task_id,
        }

        try:
            result = attachments_api.create_attachment_for_object(opts)
            return AttachFileResponse(**result)
        except ApiException as e:
            if e.status == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            raise HTTPException(status_code=500, detail=f"Asana API error: {e.reason}")

    def complete_task(self, project_id: str, task_id: str) -> TaskUpdateResponse:
        """
        Mark a task as complete.

        Args:
            project_id: ID of the Asana project (for route consistency, not used in API call)
            task_id: ID of the task to mark complete

        Returns:
            TaskUpdateResponse: Updated task status

        Raises:
            HTTPException: 404 if task not found, 500 on other errors
        """
        tasks_api = self.asana_client.get_tasks_api()
        body = {"data": {"completed": True}}
        
        try:
            result = tasks_api.update_task(body=body, task_gid=task_id, opts={})
            return TaskUpdateResponse(**result)
        except ApiException as e:
            if e.status == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            raise HTTPException(status_code=500, detail=f"Asana API error: {e.reason}")
