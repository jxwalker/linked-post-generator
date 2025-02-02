import axios from 'axios';
import { getAuthToken } from './authService';

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
apiClient.interceptors.request.use(config => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const generatePosts = async (sources, platforms, schedule = null, notifyEmail = null) => {
  try {
    const response = await apiClient.post('/generate', {
      sources,
      platforms,
      schedule,
      notify_email: notifyEmail,
    });
    return response.data;
  } catch (error) {
    console.error('Error generating posts:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// Add more API endpoints as needed
export const getPostHistory = async (page = 1, limit = 10) => {
  try {
    const response = await apiClient.get('/posts/history', {
      params: { page, limit }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching post history:', error);
    throw error;
  }
};

export const deletePost = async (postId) => {
  try {
    await apiClient.delete(`/posts/${postId}`);
  } catch (error) {
    console.error('Error deleting post:', error);
    throw error;
  }
}; 