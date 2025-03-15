import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio

# Helper function to register and login a user
async def get_auth_token(async_client: AsyncClient) -> str:
    # Register a user
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "tasksuser@example.com",
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
    # Get auth token
    token = await get_auth_token(async_client)
    
    # Create a task
    response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False,
            "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] == False
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data
    assert "updated_at" in data

async def test_get_tasks(async_client: AsyncClient):
    # Get auth token
    token = await get_auth_token(async_client)
    
    # Create a task
    create_response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task for Get Test",
            "description": "This is a task for testing get tasks",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    created_task_id = create_response.json()["id"]
    
    # Get tasks
    response = await async_client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Find our created task in the list
    created_task = None
    for task in data:
        if task["id"] == created_task_id:
            created_task = task
            break
    
    assert created_task is not None
    assert created_task["title"] == "Task for Get Test"

async def test_update_task(async_client: AsyncClient):
    # Get auth token
    token = await get_auth_token(async_client)
    
    # Create a task
    create_response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to Update",
            "description": "This task will be updated",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    task_id = create_response.json()["id"]
    
    # Update the task
    response = await async_client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "completed": True
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "This task will be updated"
    assert data["completed"] == True

async def test_delete_task(async_client: AsyncClient):
    # Get auth token
    token = await get_auth_token(async_client)
    
    # Create a task
    create_response = await async_client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to Delete",
            "description": "This task will be deleted",
            "completed": False
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