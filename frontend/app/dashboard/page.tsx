"use client";

import { useState, useEffect, Suspense } from 'react';
import { PlusIcon, ChartBarIcon, ClockIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { useRouter } from 'next/navigation';
import { Task, TaskStatus, TaskPriority } from '@/lib/api/tasks';
import StatsCard from '@/components/dashboard/StatsCard';
import TaskList from '@/components/dashboard/TaskList';
import { useAuth } from '@/lib/context/AuthContext';

// Dashboard content component
function DashboardContent() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading, user, logout } = useAuth();
  
  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // In a real app, we would use the useTasks hook
  // const { tasks, loading, error, fetchTasks, addTask, editTask, removeTask } = useTasks();
  
  // For now, we'll use the mock data
  const [tasks] = useState<Task[]>([
    { 
      id: '1', 
      title: 'Complete project proposal', 
      description: 'Finish the Q4 project proposal with budget', 
      status: TaskStatus.TODO, 
      priority: TaskPriority.HIGH,
      user_id: 'user1',
      due_date: '2023-12-31',
      created_at: '2023-11-01T00:00:00Z',
      updated_at: '2023-11-01T00:00:00Z'
    },
    { 
      id: '2', 
      title: 'Review pull requests', 
      description: 'Review and merge team PRs for the new feature', 
      status: TaskStatus.IN_PROGRESS, 
      priority: TaskPriority.MEDIUM,
      user_id: 'user1',
      due_date: '2024-01-15',
      created_at: '2023-11-05T00:00:00Z',
      updated_at: '2023-11-05T00:00:00Z'
    },
    { 
      id: '3', 
      title: 'Update documentation', 
      description: 'Update the API documentation with new endpoints', 
      status: TaskStatus.DONE, 
      priority: TaskPriority.LOW,
      user_id: 'user1',
      due_date: '2023-12-20',
      created_at: '2023-11-10T00:00:00Z',
      updated_at: '2023-11-15T00:00:00Z'
    },
    { 
      id: '4', 
      title: 'Weekly team meeting', 
      description: 'Prepare agenda for the weekly team sync', 
      status: TaskStatus.TODO, 
      priority: TaskPriority.MEDIUM,
      user_id: 'user1',
      due_date: '2024-01-05',
      created_at: '2023-11-20T00:00:00Z',
      updated_at: '2023-11-20T00:00:00Z'
    },
    { 
      id: '5', 
      title: 'Client presentation', 
      description: 'Prepare slides for the client demo', 
      status: TaskStatus.IN_PROGRESS, 
      priority: TaskPriority.HIGH,
      user_id: 'user1',
      due_date: '2024-01-10',
      created_at: '2023-11-25T00:00:00Z',
      updated_at: '2023-11-25T00:00:00Z'
    },
  ]);
  const [activeTab, setActiveTab] = useState<string | TaskStatus>('all');
  const [loading] = useState<boolean>(false);
  
  // Calculate task statistics
  const stats = {
    total: tasks.length,
    todo: tasks.filter(task => task.status === TaskStatus.TODO).length,
    inProgress: tasks.filter(task => task.status === TaskStatus.IN_PROGRESS).length,
    done: tasks.filter(task => task.status === TaskStatus.DONE).length,
  };

  // If still checking authentication or not authenticated, show loading
  if (authLoading || !isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user?.username || 'User'}</span>
            <button 
              className="px-4 py-2 bg-gray-200 rounded-md text-gray-700 hover:bg-gray-300 transition"
              onClick={() => router.push('/profile')}
            >
              Profile
            </button>
            <button 
              className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
              onClick={logout}
            >
              Logout
            </button>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <p className="text-gray-500">Loading tasks...</p>
          </div>
        ) : (
          <>
            {/* Stats Section */}
            <div className="px-4 py-6 sm:px-0">
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <StatsCard 
                  title="Total Tasks" 
                  value={stats.total} 
                  icon={<ChartBarIcon className="h-6 w-6 text-white" aria-hidden="true" />} 
                  bgColor="bg-indigo-500" 
                />
                
                <StatsCard 
                  title="To Do" 
                  value={stats.todo} 
                  icon={<ClockIcon className="h-6 w-6 text-white" aria-hidden="true" />} 
                  bgColor="bg-yellow-500" 
                />
                
                <StatsCard 
                  title="In Progress" 
                  value={stats.inProgress} 
                  icon={<ClockIcon className="h-6 w-6 text-white" aria-hidden="true" />} 
                  bgColor="bg-blue-500" 
                />
                
                <StatsCard 
                  title="Completed" 
                  value={stats.done} 
                  icon={<CheckCircleIcon className="h-6 w-6 text-white" aria-hidden="true" />} 
                  bgColor="bg-green-500" 
                />
              </div>
            </div>
            
            {/* Tasks Section */}
            <div className="px-4 py-6 sm:px-0">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-900">My Tasks</h2>
                <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                  Add Task
                </button>
              </div>
              
              <TaskList 
                tasks={tasks} 
                activeTab={activeTab} 
                setActiveTab={setActiveTab} 
              />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

// Loading fallback for Suspense
function DashboardLoading() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <p className="text-gray-500">Loading dashboard...</p>
    </div>
  );
}

// Main component that wraps DashboardContent in Suspense
export default function Dashboard() {
  return (
    <Suspense fallback={<DashboardLoading />}>
      <DashboardContent />
    </Suspense>
  );
} 