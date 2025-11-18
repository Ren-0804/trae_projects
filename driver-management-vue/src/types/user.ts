export interface User {
  id: number
  username: string
  email: string
  role: 'superadmin' | 'admin' | 'dispatcher' | 'manager' | 'driver' | 'auditor'
  is_active: boolean
  is_admin?: boolean
  last_login_at?: string | null
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

export interface Driver {
  id: number
  name: string
  phone: string
  license_number?: string
  license_type?: string
  status?: string
}
