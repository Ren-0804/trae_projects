import api from './auth'

// 用户管理相关API
export interface User {
  id: number
  username: string
  email: string | null
  role: 'superadmin' | 'admin' | 'dispatcher' | 'manager' | 'driver' | 'auditor' | 'employee'
  is_active: boolean
  last_login_at: string | null
  created_at: string
}

export interface UserCreate {
  username: string
  email?: string
  password: string
  role: 'superadmin' | 'admin' | 'dispatcher' | 'manager' | 'driver' | 'auditor' | 'employee'
}

export interface UserUpdate {
  username?: string
  email?: string
  role?: 'superadmin' | 'admin' | 'dispatcher' | 'manager' | 'driver' | 'auditor' | 'employee'
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