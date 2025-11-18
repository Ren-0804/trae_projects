import axios from 'axios'

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

// 用户管理相关API
export interface User {
  id: number
  username: string
  email: string | null
  role: 'admin' | 'employee'
  is_active: boolean
  last_login_at: string | null
  created_at: string
}

export interface UserCreate {
  username: string
  email?: string
  password: string
  role: 'admin' | 'employee'
}

export interface UserUpdate {
  username?: string
  email?: string
  role?: 'admin' | 'employee'
  is_active?: boolean
}

export interface UserListResponse {
  data: User[]
  total: number
  page: number
  page_size: number
}

// 获取用户列表
export async function getUsers(params?: {
  page?: number
  page_size?: number
  role?: string
  is_active?: boolean
}): Promise<UserListResponse> {
  const response = await api.get('/auth', { params })
  // 后端返回的是数组，需要转换为标准格式
  const users = response.data
  return {
    data: users,
    total: users.length,
    page: params?.page || 1,
    page_size: params?.page_size || users.length
  }
}

// 获取单个用户
export async function getUser(id: number): Promise<User> {
  const response = await api.get(`/auth/${id}`)
  return response.data
}

// 创建用户
export async function createUser(data: UserCreate): Promise<User> {
  const response = await api.post('/auth/register', data)
  return response.data
}

// 更新用户
export async function updateUser(id: number, data: UserUpdate): Promise<User> {
  const response = await api.put(`/auth/${id}`, data)
  return response.data
}

// 删除/禁用用户
export async function deleteUser(id: number): Promise<{ message: string }> {
  const response = await api.delete(`/auth/${id}`)
  return response.data
}

// 永久删除用户（只能删除已禁用的用户）
export async function deleteUserPermanent(id: number): Promise<{ message: string }> {
  const response = await api.delete(`/auth/${id}/permanent`)
  return response.data
}

export default {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
}