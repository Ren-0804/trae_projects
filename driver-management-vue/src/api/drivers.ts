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
  const driverId = Number(id)
  if (!Number.isFinite(driverId)) throw new Error('Invalid driver id')
  const response = await api.get(`/drivers/${driverId}`)
  return response.data
}

export async function createDriver(data: DriverCreate): Promise<Driver> {
  const payload: any = { ...data }
  Object.keys(payload).forEach((k) => {
    const v = (payload as any)[k]
    if (typeof v === 'string' && v.trim() === '') {
      delete (payload as any)[k]
    }
  })
  if (typeof payload.emergency_phone === 'string') {
    const digits = payload.emergency_phone.replace(/\D/g, '')
    if (digits.length === 11) payload.emergency_phone = digits
    else delete payload.emergency_phone
  }
  const response = await api.post('/drivers/', payload)
  return response.data
}

export async function updateDriver(id: number, data: DriverUpdate): Promise<Driver> {
  const payload: any = { ...data }
  Object.keys(payload).forEach((k) => {
    const v = (payload as any)[k]
    if (typeof v === 'string' && v.trim() === '') {
      delete (payload as any)[k]
    }
  })
  if (typeof payload.emergency_phone === 'string') {
    const digits = payload.emergency_phone.replace(/\D/g, '')
    if (digits.length === 11) payload.emergency_phone = digits
    else delete payload.emergency_phone
  }
  const driverId = Number(id)
  if (!Number.isFinite(driverId)) throw new Error('Invalid driver id')
  const response = await api.put(`/drivers/${driverId}`, payload)
  return response.data
}

export async function deleteDriver(id: number): Promise<void> {
  const driverId = Number(id)
  if (!Number.isFinite(driverId)) throw new Error('Invalid driver id')
  await api.delete(`/drivers/${driverId}`)
}

export async function uploadDriverPhoto(
  driverId: number,
  photoType: string,
  file: File,
): Promise<any> {
  const idNum = Number(driverId)
  if (!Number.isFinite(idNum)) throw new Error('Invalid driver id')
  const formData = new FormData()
  formData.append('photo_type', photoType)
  formData.append('file', file)

  const response = await api.post(`/drivers/${idNum}/photos`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export async function getDriverPhotos(driverId: number): Promise<any[]> {
  const idNum = Number(driverId)
  if (!Number.isFinite(idNum)) throw new Error('Invalid driver id')
  const response = await api.get(`/drivers/${idNum}/photos`)
  return response.data
}

export async function getDriverPhotoBlob(photoId: number): Promise<Blob> {
  const idNum = Number(photoId)
  if (!Number.isFinite(idNum)) throw new Error('Invalid photo id')
  const response = await api.get(`/drivers/photos/${idNum}`, {
    responseType: 'blob',
  })
  return response.data as Blob
}
