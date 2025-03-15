import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_register(async_client: AsyncClient):
    # Test user registration
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 201  # Changed to 201 Created
    assert "id" in response.json()
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

async def test_login(async_client: AsyncClient):
    # Register a user first
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "password123"
        }
    )
    
    # Test login
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "loginuser",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

async def test_login_invalid_credentials(async_client: AsyncClient):
    # Test login with invalid credentials
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401 