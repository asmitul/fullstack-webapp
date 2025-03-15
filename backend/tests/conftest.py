import asyncio
import os
import sys
from typing import AsyncGenerator, Generator

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongodb import db
from main import app

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_client() -> Generator:
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True, scope="function")
async def setup_db() -> AsyncGenerator:
    # Connect to test database
    db.client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/taskmanager_test"))
    db.db = db.client.get_database()
    
    # Clear collections before each test
    collections = await db.db.list_collection_names()
    for collection in collections:
        await db.db[collection].delete_many({})
    
    yield
    
    # Close connection after test
    db.client.close() 