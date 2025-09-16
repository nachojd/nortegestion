import axios from 'axios';

// API Base URL - DESARROLLO LOCAL (cambiar para producción)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Debug logging
console.log('🔧 Frontend API Configuration:');
console.log('  NEXT_PUBLIC_API_URL env var:', process.env.NEXT_PUBLIC_API_URL);
console.log('  Final API_BASE_URL:', API_BASE_URL);

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage on client side only
    if (typeof window !== 'undefined') {
      const tokens = localStorage.getItem('nortegestion_tokens');
      if (tokens) {
        const parsedTokens = JSON.parse(tokens);
        if (parsedTokens.access) {
          config.headers.Authorization = `Bearer ${parsedTokens.access}`;
        }
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If token expired (401) and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== 'undefined') {
        const tokens = localStorage.getItem('nortegestion_tokens');

        if (tokens) {
          const parsedTokens = JSON.parse(tokens);

          try {
            // Attempt to refresh the token
            const refreshResponse = await axios.post(`${API_BASE_URL}/api/auth/refresh/`, {
              refresh: parsedTokens.refresh
            });

            if (refreshResponse.status === 200) {
              const newTokens = {
                access: refreshResponse.data.access,
                refresh: parsedTokens.refresh
              };

              // Update stored tokens
              localStorage.setItem('nortegestion_tokens', JSON.stringify(newTokens));

              // Update the original request with new token
              originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;

              // Retry the original request
              return apiClient(originalRequest);
            }
          } catch (refreshError) {
            // Refresh failed, clear auth data and redirect to login
            localStorage.removeItem('nortegestion_tokens');
            localStorage.removeItem('nortegestion_user');

            // Redirect to login
            if (window.location.pathname !== '/login') {
              window.location.href = '/login';
            }
          }
        } else {
          // No refresh token, redirect to login
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
        }
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;