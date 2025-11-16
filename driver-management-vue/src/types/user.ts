export interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'employee'
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: User
  expires_in: number
}