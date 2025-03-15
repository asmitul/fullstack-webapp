from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.task import TaskPriority, TaskStatus

# Shared properties
class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

# Properties to receive via API on creation
class TaskCreate(TaskBase):
    title: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM

# Properties to receive via API on update
class TaskUpdate(TaskBase):
    pass

# Properties to return via API
class Task(TaskBase):
    id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties stored in DB
class TaskInDB(Task):
    pass 