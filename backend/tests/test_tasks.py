import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def get_auth_token(async_client: AsyncClient) -> str:
    # Register a user
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "tasks@example.com",
            "username": "tasksuser",
            "password": "password123"
        }
    )
    
    # Login to get token
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "tasksuser",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    data = response.json()
    return data["access_token"]

async def test_create_task(async_client: AsyncClient):
    token = await get_auth_token(async_client)
    
    # Create a task
    response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "todo",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"
    assert "id" in data
    assert "user_id" in data

async def test_get_tasks(async_client: AsyncClient):
    token = await get_auth_token(async_client)
    
    # Create a task first
    await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task for Get Test",
            "description": "This is a task for testing get endpoint",
            "status": "todo",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get all tasks
    response = await async_client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Task for Get Test"

async def test_update_task(async_client: AsyncClient):
    token = await get_auth_token(async_client)
    
    # Create a task first
    create_response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to Update",
            "description": "This task will be updated",
            "status": "todo",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = await async_client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"
    assert data["description"] == "This task will be updated"  # Unchanged field

async def test_delete_task(async_client: AsyncClient):
    token = await get_auth_token(async_client)
    
    # Create a task first
    create_response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to Delete",
            "description": "This task will be deleted",
            "status": "todo",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = await async_client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = await async_client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404 