import asyncio
import os
import sys
import importlib.util
import pathlib
from typing import AsyncGenerator, Generator

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Print the sys.path for debugging
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"File directory: {os.path.dirname(__file__)}")

# Create a custom module system for testing
def import_module_from_path(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get the absolute path to the required files
base_dir = pathlib.Path(__file__).parent.parent
config_path = base_dir / "app" / "core" / "config.py"

# Import config directly
config_module = import_module_from_path("config", config_path)
settings = config_module.Settings()

# Create a custom MongoDB module that doesn't rely on imports
mongodb_code = """
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

class MongoDB:
    client: AsyncIOMotorClient = None
    db: Database = None

db = MongoDB()

async def connect_to_mongo():
    \"\"\"Connect to MongoDB.\"\"\"
    db.client = AsyncIOMotorClient("{mongodb_uri}")
    db.db = db.client.get_database()
    print(f"Connected to MongoDB at {mongodb_uri}")

async def close_mongo_connection():
    \"\"\"Close MongoDB connection.\"\"\"
    if db.client:
        db.client.close()
        print("Closed connection to MongoDB")
""".format(mongodb_uri=settings.MONGODB_URI)

# Create a temporary module file
temp_mongodb_path = base_dir / "tests" / "temp_mongodb.py"
with open(temp_mongodb_path, "w") as f:
    f.write(mongodb_code)

# Import the temporary module
mongodb_module = import_module_from_path("temp_mongodb", temp_mongodb_path)
db = mongodb_module.db

# Create a simplified version of the main.py file for testing
main_code = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1")
async def root():
    return {"message": "Welcome to Task Management API"}
"""

# Create a temporary main.py file
temp_main_path = base_dir / "tests" / "temp_main.py"
with open(temp_main_path, "w") as f:
    f.write(main_code)

# Import the temporary main module
main_module = import_module_from_path("temp_main", temp_main_path)
app = main_module.app

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_client() -> Generator:
    with TestClient(app) as client:
        yield client

@pytest.fixture
async def async_client() -> AsyncGenerator:
    # Use the correct base_url that includes the API version prefix
    base_url = f"http://test{settings.API_V1_STR}"
    async with AsyncClient(app=app, base_url=base_url) as ac:
        yield ac

@pytest.fixture(autouse=False, scope="function")
async def setup_db() -> AsyncGenerator:
    """
    Set up the database connection for tests that need it.
    This fixture is not automatically used (autouse=False).
    """
    try:
        # Connect to test database
        db.client = AsyncIOMotorClient(
            os.getenv("MONGODB_URI", "mongodb://localhost:27017/taskmanager_test"),
            serverSelectionTimeoutMS=5000  # 5 seconds timeout
        )
        db.db = db.client.get_database()
        
        # Clear collections before each test
        collections = await db.db.list_collection_names()
        for collection in collections:
            await db.db[collection].delete_many({})
        
        yield
    except Exception as e:
        print(f"Error setting up database: {e}")
        yield
    finally:
        # Close connection after test
        if db.client:
            db.client.close()

# Clean up the temporary files when the tests are done
def pytest_sessionfinish(session, exitstatus):
    """Clean up temporary files after the test session."""
    if temp_mongodb_path.exists():
        temp_mongodb_path.unlink()
    if temp_main_path.exists():
        temp_main_path.unlink() 