import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_register(async_client: AsyncClient):
    # Test user registration
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data

async def test_login(async_client: AsyncClient):
    # Register a user first
    await async_client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "password123"
        }
    )
    
    # Test login
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(async_client: AsyncClient):
    # Test login with invalid credentials
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401 