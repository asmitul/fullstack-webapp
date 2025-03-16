import { useState, useEffect } from 'react';
import { Task, getTasks, createTask, updateTask, deleteTask, CreateTaskData, UpdateTaskData } from '@/lib/api/tasks';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await getTasks();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (taskData: CreateTaskData) => {
    try {
      setLoading(true);
      const newTask = await createTask(taskData);
      setTasks(prev => [...prev, newTask]);
      return newTask;
    } catch (err) {
      setError('Failed to create task');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const editTask = async (id: string, taskData: UpdateTaskData) => {
    try {
      setLoading(true);
      const updatedTask = await updateTask(id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      return updatedTask;
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const removeTask = async (id: string) => {
    try {
      setLoading(true);
      await deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    addTask,
    editTask,
    removeTask
  };
}; 