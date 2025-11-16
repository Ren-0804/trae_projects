import axios from 'axios'
import type { LoginRequest, LoginResponse } from '@/types/user'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const response = await api.post('/auth/login', data)
  return response.data
}

export async function getCurrentUser(): Promise<{ user: any }> {
  const response = await api.get('/auth/me')
  return response.data
}

export default api