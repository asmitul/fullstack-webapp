from typing import Any, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_active_user
from app.db.mongodb import db
from app.db.redis import delete_cache, get_cache, set_cache
from app.models.task import TaskInDB
from app.models.user import UserInDB
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

@router.get("/", response_model=List[Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve tasks for the current user.
    """
    # Try to get tasks from cache
    cache_key = f"tasks:{current_user.id}"
    cached_tasks = get_cache(cache_key)
    
    if cached_tasks:
        return cached_tasks
    
    # If not in cache, get from database
    tasks = await db.db.tasks.find(
        {"user_id": current_user.id}
    ).skip(skip).limit(limit).to_list(length=limit)
    
    # Store in cache for future requests
    set_cache(cache_key, tasks, expire=300)  # Cache for 5 minutes
    
    return tasks

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create a new task.
    """
    task = TaskInDB(
        **task_in.dict(),
        user_id=current_user.id,
    )
    
    # Insert task into database
    result = await db.db.tasks.insert_one(task.dict(exclude={"id"}))
    
    # Update task with the generated ID
    task.id = str(result.inserted_id)
    
    # Update the document with the ID
    await db.db.tasks.update_one(
        {"_id": result.inserted_id},
        {"$set": {"id": str(result.inserted_id)}}
    )
    
    # Invalidate cache
    delete_cache(f"tasks:{current_user.id}")
    
    return task

@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific task by ID.
    """
    # Try to get task from cache
    cache_key = f"task:{task_id}"
    cached_task = get_cache(cache_key)
    
    if cached_task:
        # Verify that the task belongs to the current user
        if cached_task["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return cached_task
    
    # If not in cache, get from database
    task = await db.db.tasks.find_one({"_id": ObjectId(task_id)})
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Verify that the task belongs to the current user
    if task["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Store in cache for future requests
    set_cache(cache_key, task, expire=300)  # Cache for 5 minutes
    
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_in: TaskUpdate,
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a task.
    """
    # Get the task from the database
    task = await db.db.tasks.find_one({"_id": ObjectId(task_id)})
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Verify that the task belongs to the current user
    if task["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Update the task
    update_data = task_in.dict(exclude_unset=True)
    
    # Add updated_at timestamp
    from datetime import datetime
    update_data["updated_at"] = datetime.utcnow()
    
    await db.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    # Get the updated task
    updated_task = await db.db.tasks.find_one({"_id": ObjectId(task_id)})
    
    # Invalidate caches
    delete_cache(f"task:{task_id}")
    delete_cache(f"tasks:{current_user.id}")
    
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_active_user),
) -> None:
    """
    Delete a task.
    """
    # Get the task from the database
    task = await db.db.tasks.find_one({"_id": ObjectId(task_id)})
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Verify that the task belongs to the current user
    if task["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Delete the task
    await db.db.tasks.delete_one({"_id": ObjectId(task_id)})
    
    # Invalidate caches
    delete_cache(f"task:{task_id}")
    delete_cache(f"tasks:{current_user.id}") 