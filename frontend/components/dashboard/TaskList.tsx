import React from 'react';
import { Task, TaskStatus } from '@/lib/api/tasks';

interface TaskListProps {
  tasks: Task[];
  activeTab: string | TaskStatus;
  setActiveTab: (tab: string | TaskStatus) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, activeTab, setActiveTab }) => {
  // Filter tasks based on active tab
  const filteredTasks = activeTab === 'all' 
    ? tasks 
    : tasks.filter(task => task.status === activeTab);

  return (
    <div>
      {/* Task Filter Tabs */}
      <div className="border-b border-gray-200 mb-5">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {['all', TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}
              `}
            >
              {tab === 'all' ? 'All Tasks' : 
               tab === TaskStatus.TODO ? 'To Do' : 
               tab === TaskStatus.IN_PROGRESS ? 'In Progress' : 'Completed'}
            </button>
          ))}
        </nav>
      </div>
      
      {/* Task List */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => (
              <li key={task.id}>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-indigo-600 truncate">
                      {task.title}
                    </p>
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${task.status === TaskStatus.TODO ? 'bg-yellow-100 text-yellow-800' : 
                          task.status === TaskStatus.IN_PROGRESS ? 'bg-blue-100 text-blue-800' : 
                          'bg-green-100 text-green-800'}`}>
                        {task.status === TaskStatus.TODO ? 'To Do' : 
                         task.status === TaskStatus.IN_PROGRESS ? 'In Progress' : 'Completed'}
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
                        Due date: {task.due_date ? 
                          <time dateTime={task.due_date}>{new Date(task.due_date).toLocaleDateString()}</time> : 
                          'No due date'}
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 flex justify-end space-x-2">
                    <button
                      className="text-sm text-indigo-600 hover:text-indigo-900"
                    >
                      Edit
                    </button>
                    <button
                      className="text-sm text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </li>
            ))
          ) : (
            <li className="px-4 py-5 sm:px-6 text-center text-gray-500">
              No tasks found in this category.
            </li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default TaskList; 