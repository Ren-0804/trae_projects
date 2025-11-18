import api from './auth'
import type { 
  GPSRecordResponse, GPSRecordCreate,
  DrivingBehaviorResponse, DrivingBehaviorCreate, DrivingBehaviorUpdate,
  EmergencyAlertResponse, EmergencyAlertCreate, EmergencyAlertUpdate 
} from '@/types/safety'

// 使用统一的axios实例，自动携带认证信息

// GPS轨迹管理相关API
export async function createGPSRecord(gpsRecord: GPSRecordCreate): Promise<GPSRecordResponse> {
  const response = await api.post(`/safety/gps-records`, gpsRecord)
  return response.data
}

export async function getGPSRecords(
  skip = 0,
  limit = 100,
  vehicleId?: number,
  driverId?: number,
  startTime?: Date,
  endTime?: Date
): Promise<GPSRecordResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (vehicleId) params.append('vehicle_id', vehicleId.toString())
  if (driverId) params.append('driver_id', driverId.toString())
  if (startTime) params.append('start_time', startTime.toISOString())
  if (endTime) params.append('end_time', endTime.toISOString())
  
  const response = await api.get(`/safety/gps-records`, { params })
  return response.data
}

export async function getVehicleTrack(
  vehicleId: number,
  startTime: Date,
  endTime: Date
): Promise<{
  vehicle_id: number
  plate_number: string
  start_time: Date
  end_time: Date
  total_points: number
  total_distance: number
  max_speed: number
  avg_speed: number
  idle_time: number
  track: Array<{
    latitude: number
    longitude: number
    speed: number
    timestamp: Date
    address: string
    status: string
  }>
}> {
  const params = new URLSearchParams()
  params.append('start_time', startTime.toISOString())
  params.append('end_time', endTime.toISOString())
  
  const response = await api.get(`/safety/vehicles/${vehicleId}/track`, { params })
  return response.data
}

// 驾驶行为管理相关API
export async function createDrivingBehavior(behavior: DrivingBehaviorCreate): Promise<DrivingBehaviorResponse> {
  const response = await api.post(`/safety/driving-behaviors`, behavior)
  return response.data
}

export async function getDrivingBehaviors(
  skip = 0,
  limit = 100,
  driverId?: number,
  vehicleId?: number,
  behaviorType?: 'harsh_braking' | 'speeding' | 'sharp_turn',
  severity?: 'low' | 'medium' | 'high',
  processed?: boolean,
  startTime?: Date,
  endTime?: Date
): Promise<DrivingBehaviorResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (driverId) params.append('driver_id', driverId.toString())
  if (vehicleId) params.append('vehicle_id', vehicleId.toString())
  if (behaviorType) params.append('behavior_type', behaviorType)
  if (severity) params.append('severity', severity)
  if (processed !== undefined) params.append('processed', processed.toString())
  if (startTime) params.append('start_time', startTime.toISOString())
  if (endTime) params.append('end_time', endTime.toISOString())
  
  const response = await api.get(`/safety/driving-behaviors`, { params })
  return response.data
}

export async function updateDrivingBehavior(
  behaviorId: number,
  behaviorUpdate: DrivingBehaviorUpdate
): Promise<DrivingBehaviorResponse> {
  const response = await api.put(`/safety/driving-behaviors/${behaviorId}`, behaviorUpdate)
  return response.data
}

export async function getDrivingBehaviorSummary(
  driverId?: number,
  vehicleId?: number,
  startDate?: Date,
  endDate?: Date
): Promise<{
  total_behaviors: number
  by_type: Record<string, number>
  by_severity: Record<string, number>
  processed_count: number
  unprocessed_count: number
  high_risk_percentage: number
}> {
  const params = new URLSearchParams()
  if (driverId) params.append('driver_id', driverId.toString())
  if (vehicleId) params.append('vehicle_id', vehicleId.toString())
  if (startDate) params.append('start_date', startDate.toISOString())
  if (endDate) params.append('end_date', endDate.toISOString())
  
  const response = await api.get(`/safety/driving-behaviors/summary`, { params })
  return response.data
}

// 紧急警报管理相关API
export async function createEmergencyAlert(alert: EmergencyAlertCreate): Promise<EmergencyAlertResponse> {
  const response = await api.post(`/safety/emergency-alerts`, alert)
  return response.data
}

export async function getEmergencyAlerts(
  skip = 0,
  limit = 100,
  driverId?: number,
  vehicleId?: number,
  alertType?: 'accident' | 'medical' | 'security',
  severity?: 'low' | 'medium' | 'high' | 'critical',
  status?: 'active' | 'responded' | 'resolved'
): Promise<EmergencyAlertResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (driverId) params.append('driver_id', driverId.toString())
  if (vehicleId) params.append('vehicle_id', vehicleId.toString())
  if (alertType) params.append('alert_type', alertType)
  if (severity) params.append('severity', severity)
  if (status) params.append('status', status)
  
  const response = await api.get(`/safety/emergency-alerts`, { params })
  return response.data
}

export async function updateEmergencyAlert(
  alertId: number,
  alertUpdate: EmergencyAlertUpdate
): Promise<EmergencyAlertResponse> {
  const response = await api.put(`/safety/emergency-alerts/${alertId}`, alertUpdate)
  return response.data
}

export async function getActiveEmergencyAlertsSummary(): Promise<{
  total_active_alerts: number
  by_type: Record<string, number>
  by_severity: Record<string, number>
  latest_alerts: Array<{
    id: number
    driver_name: string
    alert_type: string
    severity: string
    description: string
    created_at: Date
    latitude: number
    longitude: number
  }>
}> {
  const response = await api.get(`/safety/emergency-alerts/active-summary`)
  return response.data
}

// 新增用于仪表板的API函数
export async function getSafetyStats(): Promise<{
  online_drivers: number
  active_vehicles: number
  today_alerts: number
  emergency_alerts: number
}> {
  const response = await api.get(`/safety/stats`)
  return response.data
}

export async function getRecentAlerts(params?: {
  limit?: number
  severity?: string
  status?: string
}): Promise<{
  data: Array<{
    id: number
    alert_type: string
    severity: string
    status: string
    description: string
    created_at: string
    driver?: {
      id: number
      name: string
    }
  }>
  total: number
}> {
  const queryParams = new URLSearchParams()
  if (params?.limit) queryParams.append('limit', params.limit.toString())
  if (params?.severity) queryParams.append('severity', params.severity)
  if (params?.status) queryParams.append('status', params.status)
  
  const response = await api.get(`/safety/alerts/recent?${queryParams}`)
  return response.data
}

export async function getAlerts(params?: {
  page?: number
  page_size?: number
  severity?: string
  status?: string
  driver_id?: number
}): Promise<{
  data: Array<{
    id: number
    alert_type: string
    severity: string
    status: string
    description: string
    created_at: string
    driver?: {
      id: number
      name: string
    }
  }>
  total: number
}> {
  const queryParams = new URLSearchParams()
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.page_size) queryParams.append('page_size', params.page_size.toString())
  if (params?.severity) queryParams.append('severity', params.severity)
  if (params?.status) queryParams.append('status', params.status)
  if (params?.driver_id) queryParams.append('driver_id', params.driver_id.toString())
  
  const response = await api.get(`/safety/alerts?${queryParams}`)
  return response.data
}

export async function processAlert(alertId: number): Promise<void> {
  await api.put(`/safety/alerts/${alertId}/process`)
}

export async function getEmergencyStats(): Promise<{
  today_emergency: number
  pending_emergency: number
  resolved_emergency: number
}> {
  const response = await api.get(`/safety/emergency-alerts/stats`)
  return response.data
}

export async function processEmergencyAlert(alertId: number): Promise<void> {
  await api.put(`/safety/emergency-alerts/${alertId}/process`)
}