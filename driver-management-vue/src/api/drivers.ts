import api from './auth'

export interface Driver {
  id: number
  user_id: number
  name: string
  phone: string
  id_card: string
  license_number: string
  license_type: string
  main_route: string
  vehicle_type: string
  vehicle_length?: string
  price_per_km: number
  experience_years: number
  status: 'active' | 'inactive' | 'blocked'
  emergency_contact?: string
  emergency_phone?: string
  remark?: string
  created_at: string
  updated_at: string
  user?: any
}

export interface DriverCreate {
  name: string
  phone: string
  id_card: string
  license_number: string
  license_type: string
  main_route: string
  vehicle_type: string
  vehicle_length?: string
  price_per_km?: number
  experience_years?: number
  status?: 'active' | 'inactive' | 'blocked'
  emergency_contact?: string
  emergency_phone?: string
  remark?: string
}

export interface DriverUpdate {
  name?: string
  phone?: string
  id_card?: string
  license_number?: string
  license_type?: string
  main_route?: string
  vehicle_type?: string
  vehicle_length?: string
  price_per_km?: number
  experience_years?: number
  status?: 'active' | 'inactive' | 'blocked'
  emergency_contact?: string
  emergency_phone?: string
  remark?: string
}

export interface DriverListResponse {
  data: Driver[]
  total: number
  page: number
  page_size: number
}

export interface DriverQuery {
  page?: number
  page_size?: number
  keyword?: string
  route?: string
  status?: string
}

export async function getDrivers(query?: DriverQuery): Promise<DriverListResponse> {
  const response = await api.get('/drivers', { params: query })
  return response.data
}

export async function getDriver(id: number): Promise<Driver> {
  const response = await api.get(`/drivers/${id}`)
  return response.data
}

export async function createDriver(data: DriverCreate): Promise<Driver> {
  const response = await api.post('/drivers/', data)
  return response.data
}

export async function updateDriver(id: number, data: DriverUpdate): Promise<Driver> {
  const response = await api.put(`/drivers/${id}`, data)
  return response.data
}

export async function deleteDriver(id: number): Promise<void> {
  await api.delete(`/drivers/${id}`)
}

export async function uploadDriverPhoto(driverId: number, photoType: string, file: File): Promise<any> {
  const formData = new FormData()
  formData.append('photo_type', photoType)
  formData.append('file', file)
  
  const response = await api.post(`/drivers/${driverId}/photos`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export async function getDriverPhotos(driverId: number): Promise<any[]> {
  const response = await api.get(`/drivers/${driverId}/photos`)
  return response.data
}