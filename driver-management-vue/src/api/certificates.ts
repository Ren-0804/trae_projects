import axios from 'axios'
import type { 
  DriverCertificateResponse, DriverCertificateCreate, DriverCertificateUpdate 
} from '@/types/certificate'

const API_BASE = '/api/v1'

// 证书管理相关API
export async function getCertificates(
  skip = 0,
  limit = 100,
  driverId?: number,
  certificateType?: string,
  status?: string,
  expiringSoon = false,
  daysAhead = 30
): Promise<DriverCertificateResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (driverId) params.append('driver_id', driverId.toString())
  if (certificateType) params.append('certificate_type', certificateType)
  if (status) params.append('status', status)
  if (expiringSoon) params.append('expiring_soon', 'true')
  if (daysAhead) params.append('days_ahead', daysAhead.toString())
  
  const response = await axios.get(`${API_BASE}/certificates?${params}`)
  return response.data
}

export async function getCertificate(certificateId: number): Promise<DriverCertificateResponse> {
  const response = await axios.get(`${API_BASE}/certificates/${certificateId}`)
  return response.data
}

export async function createCertificate(certificate: DriverCertificateCreate): Promise<DriverCertificateResponse> {
  const response = await axios.post(`${API_BASE}/certificates`, certificate)
  return response.data
}

export async function updateCertificate(
  certificateId: number, 
  certificate: DriverCertificateUpdate
): Promise<DriverCertificateResponse> {
  const response = await axios.put(`${API_BASE}/certificates/${certificateId}`, certificate)
  return response.data
}

export async function deleteCertificate(certificateId: number): Promise<void> {
  await axios.delete(`${API_BASE}/certificates/${certificateId}`)
}

export async function getExpiringCertificates(
  daysAhead = 30,
  certificateType?: string
): Promise<any[]> {
  const params = new URLSearchParams()
  params.append('days_ahead', daysAhead.toString())
  if (certificateType) params.append('certificate_type', certificateType)
  
  const response = await axios.get(`${API_BASE}/certificates/expiring-soon?${params}`)
  return response.data
}

export async function renewCertificate(
  certificateId: number,
  newExpiryDate: Date,
  newCertificateNumber?: string
): Promise<DriverCertificateResponse> {
  const params = new URLSearchParams()
  params.append('new_expiry_date', newExpiryDate.toISOString())
  if (newCertificateNumber) params.append('new_certificate_number', newCertificateNumber)
  
  const response = await axios.post(`${API_BASE}/certificates/${certificateId}/renew?${params}`)
  return response.data
}

export async function uploadCertificateFile(
  certificateId: number,
  file: File
): Promise<{ message: string; file_path: string; file_name: string; file_size: number; content_type: string }> {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_BASE}/certificates/${certificateId}/upload-file`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export async function getDriverCertificatesSummary(driverId: number): Promise<{
  driver_id: number
  driver_name: string
  total_certificates: number
  valid_certificates: number
  expired_certificates: number
  expiring_soon: number
  certificates_by_type: Record<string, any>
  urgent_renewals: Array<{
    certificate_id: number
    certificate_type: string
    certificate_number: string
    expiry_date: Date
    days_until_expiry: number
  }>
}> {
  const response = await axios.get(`${API_BASE}/certificates/drivers/${driverId}/summary`)
  return response.data
}