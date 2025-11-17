import axios from 'axios'
import type { 
  VehicleResponse, VehicleCreate, VehicleUpdate,
  MaintenanceRecordResponse, MaintenanceRecordCreate, MaintenanceRecordUpdate 
} from '@/types/vehicle'

const API_BASE = '/api/v1'

// 车辆管理相关API
export async function getVehicles(
  skip = 0,
  limit = 100,
  status?: string,
  vehicleType?: string
): Promise<VehicleResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (status) params.append('status', status)
  if (vehicleType) params.append('vehicle_type', vehicleType)
  
  const response = await axios.get(`${API_BASE}/vehicles?${params}`)
  return response.data
}

export async function getVehicle(vehicleId: number): Promise<VehicleResponse> {
  const response = await axios.get(`${API_BASE}/vehicles/${vehicleId}`)
  return response.data
}

export async function createVehicle(vehicle: VehicleCreate): Promise<VehicleResponse> {
  const response = await axios.post(`${API_BASE}/vehicles`, vehicle)
  return response.data
}

export async function updateVehicle(
  vehicleId: number, 
  vehicle: VehicleUpdate
): Promise<VehicleResponse> {
  const response = await axios.put(`${API_BASE}/vehicles/${vehicleId}`, vehicle)
  return response.data
}

export async function deleteVehicle(vehicleId: number): Promise<void> {
  await axios.delete(`${API_BASE}/vehicles/${vehicleId}`)
}

export async function assignDriverToVehicle(
  vehicleId: number,
  driverId: number,
  assignmentType: 'primary' | 'temporary' = 'primary',
  endDate?: Date
): Promise<any> {
  const params = new URLSearchParams()
  params.append('driver_id', driverId.toString())
  params.append('assignment_type', assignmentType)
  if (endDate) params.append('end_date', endDate.toISOString())
  
  const response = await axios.post(`${API_BASE}/vehicles/${vehicleId}/assign-driver?${params}`)
  return response.data
}

export async function endDriverAssignment(
  vehicleId: number,
  assignmentId: number
): Promise<any> {
  const response = await axios.put(`${API_BASE}/vehicles/${vehicleId}/assignments/${assignmentId}/end`)
  return response.data
}

export async function getVehicleMaintenanceRecords(
  vehicleId: number,
  skip = 0,
  limit = 50
): Promise<MaintenanceRecordResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  
  const response = await axios.get(`${API_BASE}/vehicles/${vehicleId}/maintenance-records?${params}`)
  return response.data
}

export async function createMaintenanceRecord(
  vehicleId: number,
  record: MaintenanceRecordCreate
): Promise<MaintenanceRecordResponse> {
  const response = await axios.post(`${API_BASE}/vehicles/${vehicleId}/maintenance-records`, record)
  return response.data
}

export async function getUpcomingMaintenance(daysAhead = 30): Promise<any[]> {
  const params = new URLSearchParams()
  params.append('days_ahead', daysAhead.toString())
  
  const response = await axios.get(`${API_BASE}/vehicles/maintenance/upcoming?${params}`)
  return response.data
}

export async function getExpiringInsurance(daysAhead = 30): Promise<any[]> {
  const params = new URLSearchParams()
  params.append('days_ahead', daysAhead.toString())
  
  const response = await axios.get(`${API_BASE}/vehicles/insurance/expiring?${params}`)
  return response.data
}

export async function getVehicleAssignments(params: {
  vehicle_id: number
  page?: number
  page_size?: number
  status?: string | null
  start_date?: string
  end_date?: string
}): Promise<{
  data: any[]
  total: number
  page: number
  page_size: number
}> {
  const queryParams = new URLSearchParams()
  queryParams.append('vehicle_id', params.vehicle_id.toString())
  if (params.page) queryParams.append('page', params.page.toString())
  if (params.page_size) queryParams.append('page_size', params.page_size.toString())
  if (params.status) queryParams.append('status', params.status)
  if (params.start_date) queryParams.append('start_date', params.start_date)
  if (params.end_date) queryParams.append('end_date', params.end_date)
  
  const response = await axios.get(`${API_BASE}/vehicles/assignments?${queryParams}`)
  return response.data
}