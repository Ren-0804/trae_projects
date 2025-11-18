import axios from 'axios'
import type { LoginRequest, LoginResponse, User } from '@/types/user'

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  withCredentials: true,
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
  async (error) => {
    const config: any = error.config || {}
    
    // 处理401未授权错误
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
      return Promise.reject(error)
    }
    
    // 处理422验证错误
    if (error.response?.status === 422) {
      const detail = error.response?.data?.detail
      if (Array.isArray(detail)) {
        const errorMessages = detail.map((item: any) => {
          const loc = item.loc?.join('.') || '字段'
          return `${loc}: ${item.msg}`
        }).join(', ')
        console.error('验证错误:', errorMessages)
      } else {
        console.error('验证错误:', detail)
      }
      return Promise.reject(error)
    }
    
    // 处理网络错误和重试
    if (error.code === 'ERR_NETWORK' && !config.__retry && (config.__retryCount || 0) < 2) {
      config.__retry = true
      config.__retryCount = (config.__retryCount || 0) + 1
      console.log(`网络错误重试第${config.__retryCount}次...`)
      await new Promise((r) => setTimeout(r, 300 * config.__retryCount))
      return api(config)
    }
    
    // 记录详细的错误信息
    console.error('API请求错误:', {
      url: config.url,
      method: config.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      code: error.code,
      message: error.message
    })
    
    return Promise.reject(error)
  },
)

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const response = await api.post('/auth/login', data)
  return response.data
}

export async function getCurrentUser(): Promise<{ user: any }> {
  const response = await api.get('/auth/me')
  return response.data
}

export async function refreshToken(): Promise<{ token: string; expires_in: number }> {
  const response = await api.post('/auth/refresh')
  return response.data
}

export async function logout(): Promise<{ message: string }> {
  const response = await api.post('/auth/logout')
  return response.data
}

export async function getSessions(): Promise<Array<{ id: string; device: string; ip: string; created_at: string; last_active_at: string }>> {
  const response = await api.get('/auth/sessions')
  return response.data
}

export async function revokeSession(sessionId: string): Promise<{ message: string }> {
  const response = await api.post('/auth/revoke-session', { session_id: sessionId })
  return response.data
}

export async function loginWithSms(phone: string, code: string): Promise<LoginResponse> {
  const response = await api.post('/auth/login', { phone, code, method: 'sms' })
  return response.data
}

export default api
