import pytest
from fastapi.testclient import TestClient

def test_read_root(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Task Management API"} 