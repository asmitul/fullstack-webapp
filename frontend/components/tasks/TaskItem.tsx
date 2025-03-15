import React from 'react';
import { Task, TaskStatus } from '@/lib/api/tasks';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

const getStatusBadgeClass = (status: TaskStatus) => {
  switch (status) {
    case TaskStatus.TODO:
      return 'bg-blue-100 text-blue-800';
    case TaskStatus.IN_PROGRESS:
      return 'bg-yellow-100 text-yellow-800';
    case TaskStatus.DONE:
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const formatDate = (dateString?: string) => {
  if (!dateString) return 'No due date';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete }) => {
  return (
    <li className="border-b border-gray-200 last:border-b-0">
      <div className="px-4 py-4 sm:px-6">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-primary-600 truncate">
            {task.title}
          </p>
          <div className="ml-2 flex-shrink-0 flex">
            <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(task.status)}`}>
              {task.status.replace('_', ' ').toUpperCase()}
            </p>
          </div>
        </div>
        <div className="mt-2 sm:flex sm:justify-between">
          <div className="sm:flex">
            <p className="flex items-center text-sm text-gray-500">
              {task.description || 'No description'}
            </p>
          </div>
          <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
            <p>
              Due date: {formatDate(task.due_date)}
            </p>
          </div>
        </div>
        <div className="mt-2 flex justify-end space-x-2">
          <button
            onClick={() => onEdit(task)}
            className="text-sm text-primary-600 hover:text-primary-900"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-sm text-red-600 hover:text-red-900"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
};

export default TaskItem; 