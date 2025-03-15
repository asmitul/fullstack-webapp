import apiClient from './client';

export enum TaskStatus {
  TODO = 'todo',
  IN_PROGRESS = 'in_progress',
  DONE = 'done',
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  user_id: string;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

export const getTasks = async (): Promise<Task[]> => {
  const response = await apiClient.get<Task[]>('/tasks');
  return response.data;
};

export const getTask = async (id: string): Promise<Task> => {
  const response = await apiClient.get<Task>(`/tasks/${id}`);
  return response.data;
};

export const createTask = async (data: CreateTaskData): Promise<Task> => {
  const response = await apiClient.post<Task>('/tasks', data);
  return response.data;
};

export const updateTask = async (id: string, data: UpdateTaskData): Promise<Task> => {
  const response = await apiClient.put<Task>(`/tasks/${id}`, data);
  return response.data;
};

export const deleteTask = async (id: string): Promise<void> => {
  await apiClient.delete(`/tasks/${id}`);
}; 