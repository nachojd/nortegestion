'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '@/lib/axios';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
}

interface AuthTokens {
  access: string;
  refresh: string;
}

interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API Base URL - USAR DESDE apiClient
// const API_BASE_URL removido - ahora usamos apiClient directamente

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!tokens?.access && !!user;

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedTokens = localStorage.getItem('nortegestion_tokens');
        const storedUser = localStorage.getItem('nortegestion_user');

        if (storedTokens && storedUser) {
          const parsedTokens = JSON.parse(storedTokens);
          const parsedUser = JSON.parse(storedUser);

          // Validate token by making a test request
          try {
            const response = await apiClient.get('/api/products/');
            console.log('✅ TOKEN VALIDATION: Success');

            if (response.status === 200) {
              setTokens(parsedTokens);
              setUser(parsedUser);
            } else {
              // Token invalid, try refresh
              await attemptTokenRefresh(parsedTokens);
            }
          } catch (error) {
            // Try refresh token
            await attemptTokenRefresh(parsedTokens);
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        clearAuthData();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const attemptTokenRefresh = async (currentTokens: AuthTokens) => {
    try {
      console.log('🔄 TOKEN REFRESH: Enviando petición a:', '/api/auth/refresh/');
      const response = await apiClient.post('/api/auth/refresh/', {
        refresh: currentTokens.refresh
      });

      if (response.status === 200) {
        const newTokens = {
          access: response.data.access,
          refresh: currentTokens.refresh
        };

        setTokens(newTokens);
        localStorage.setItem('nortegestion_tokens', JSON.stringify(newTokens));
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      clearAuthData();
    }
    return false;
  };

  const clearAuthData = () => {
    setUser(null);
    setTokens(null);
    localStorage.removeItem('nortegestion_tokens');
    localStorage.removeItem('nortegestion_user');
    // Clear cookie
    document.cookie = 'nortegestion_tokens=; path=/; max-age=0';
  };

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      setIsLoading(true);

      console.log('🔐 LOGIN: Enviando petición a:', '/api/auth/login/');
      const response = await apiClient.post('/api/auth/login/', {
        username,
        password
      });

      if (response.status === 200) {
        const { access, refresh } = response.data;
        const newTokens = { access, refresh };

        // Extract user info - try to get a meaningful display name
        let displayName = 'Usuario';
        if (username.includes('@')) {
          // If it's an email, use the part before @
          displayName = username.split('@')[0];
        } else {
          displayName = username;
        }

        const userData: User = {
          id: 0, // Will be populated when we decode token or make user API call
          username,
          email: username,
          first_name: displayName
        };

        setTokens(newTokens);
        setUser(userData);

        // Store in localStorage and cookies
        localStorage.setItem('nortegestion_tokens', JSON.stringify(newTokens));
        localStorage.setItem('nortegestion_user', JSON.stringify(userData));

        // Set cookie for middleware
        document.cookie = `nortegestion_tokens=${JSON.stringify(newTokens)}; path=/; max-age=${30 * 24 * 60 * 60}`; // 30 days

        return true;
      }
    } catch (error) {
      console.error('Login failed:', error);
      clearAuthData();
    } finally {
      setIsLoading(false);
    }
    return false;
  };

  const logout = () => {
    clearAuthData();
    // Redirect to login will be handled by the component using this context
  };

  const refreshToken = async (): Promise<boolean> => {
    if (!tokens?.refresh) return false;
    return await attemptTokenRefresh(tokens);
  };

  // Auto-refresh token when it's about to expire
  useEffect(() => {
    if (!tokens?.access) return;

    const scheduleTokenRefresh = () => {
      // Refresh token 5 minutes before expiration (JWT default is 8 hours)
      const refreshTime = 8 * 60 * 60 * 1000 - 5 * 60 * 1000; // 7h 55min

      const timeoutId = setTimeout(() => {
        refreshToken();
      }, refreshTime);

      return timeoutId;
    };

    const timeoutId = scheduleTokenRefresh();
    return () => clearTimeout(timeoutId);
  }, [tokens]);

  const value: AuthContextType = {
    user,
    tokens,
    isAuthenticated,
    isLoading,
    login,
    logout,
    refreshToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}