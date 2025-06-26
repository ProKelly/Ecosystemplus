// src/api/index.ts
// Basic API client for authentication and user profile
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const login = (data: { email: string; password: string }) =>
  axios.post(`${API_BASE}/users/auth/token/`, data);

export const register = (data: any) =>
  axios.post(`${API_BASE}/users/auth/register/`, data);

export const getProfile = (token: string) =>
  axios.get(`${API_BASE}/users/auth/profile/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const updateProfile = (data: any, token: string) =>
  axios.put(`${API_BASE}/users/auth/profile/`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const createCommunity = (data: any, token: string) =>
  axios.post(`${API_BASE}/users/communities/`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const fetchCommunities = (token: string) =>
  axios.get(`${API_BASE}/users/communities/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const fetchFarms = (token: string) =>
  axios.get(`${API_BASE}/farms/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const addFarm = (data: any, token: string) =>
  axios.post(`${API_BASE}/farms/`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const updateFarm = (uuid: string, data: any, token: string) =>
  axios.put(`${API_BASE}/farms/${uuid}/`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const deleteFarm = (uuid: string, token: string) =>
  axios.delete(`${API_BASE}/farms/${uuid}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

// Add more API functions as needed

export default {
  login,
  register,
  getProfile,
  updateProfile,
  createCommunity,
  fetchCommunities,
  fetchFarms,
  addFarm,
  updateFarm,
  deleteFarm,
};
