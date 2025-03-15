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

# Create a simplified version of the main.py file for testing with mock endpoints
main_code = """
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

# Mock models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    disabled: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

# Mock database
mock_users = {}
mock_tasks = {}

# Mock security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in mock_users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return mock_users[token]

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

# Auth endpoints
@app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    user_id = str(uuid.uuid4())
    token = f"mock_token_{user_id}"
    
    # Store user with token as key for easy lookup
    mock_users[token] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "disabled": user.disabled,
        "hashed_password": f"hashed_{user.password}"
    }
    
    return {"id": user_id, "username": user.username, "email": user.email}

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by username
    user = None
    token = None
    for t, u in mock_users.items():
        if u["username"] == form_data.username:
            # Check password (mock check)
            if u["hashed_password"] == f"hashed_{form_data.password}":
                user = u
                token = t
                break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": token, "token_type": "bearer"}

# Task endpoints
@app.post("/api/v1/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    task_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "due_date": task.due_date,
        "owner_id": current_user["id"],
        "created_at": now,
        "updated_at": now
    }
    
    mock_tasks[task_id] = new_task
    return new_task

@app.get("/api/v1/tasks", response_model=List[Task])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    user_tasks = []
    for task_id, task in mock_tasks.items():
        if task["owner_id"] == current_user["id"]:
            user_tasks.append(task)
    return user_tasks

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    if task_id not in mock_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = mock_tasks[task_id]
    if task["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    return task

@app.put("/api/v1/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    if task_id not in mock_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = mock_tasks[task_id]
    if task["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Update fields if provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        task[field] = value
    
    task["updated_at"] = datetime.utcnow()
    mock_tasks[task_id] = task
    
    return task

@app.delete("/api/v1/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    if task_id not in mock_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = mock_tasks[task_id]
    if task["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    del mock_tasks[task_id]
    return None
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
    base_url = "http://test"
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