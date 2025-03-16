"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { User, getCurrentUser, login as loginApi, logout as logoutApi, LoginCredentials } from '@/lib/api/auth';
import Cookies from 'js-cookie';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const isAuthenticated = !!user;

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      try {
        setLoading(true);
        // Check if token exists in cookies
        const token = Cookies.get('token');
        if (!token) {
          setUser(null);
          setLoading(false);
          return;
        }

        // Fetch current user
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (err) {
        console.error('Auth check error:', err);
        // Clear token if invalid
        Cookies.remove('token', { path: '/' });
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true);
      setError(null);
      
      // Call login API
      await loginApi(credentials);
      
      // Fetch user data after successful login
      const userData = await getCurrentUser();
      setUser(userData);
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: unknown) {
      console.error('Login error:', err);
      
      // Handle axios error
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosError = err as { response?: { data?: { detail?: string } } };
        setError(
          axiosError.response?.data?.detail || 
          'Failed to login. Please check your credentials and try again.'
        );
      } else {
        setError('Failed to login. Please check your credentials and try again.');
      }
      
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    logoutApi();
    setUser(null);
    router.push('/login');
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext; 