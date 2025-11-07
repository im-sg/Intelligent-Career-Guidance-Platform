import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API methods
export const resumeAPI = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getParsed: async (resumeId) => {
    const response = await api.get(`/resume/parsed/${resumeId}`);
    return response.data;
  },

  delete: async (resumeId) => {
    const response = await api.delete(`/resume/${resumeId}`);
    return response.data;
  },
};

export const rolesAPI = {
  getRecommendations: async (resumeId, limit = 5) => {
    const response = await api.get(`/roles/recommendations/${resumeId}?limit=${limit}`);
    return response.data;
  },
};

export const authAPI = {
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
};

export default api;