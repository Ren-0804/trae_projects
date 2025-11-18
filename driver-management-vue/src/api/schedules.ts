import api from './auth'
import type { 
  ScheduleResponse, ScheduleCreate, ScheduleUpdate 
} from '@/types/schedule'

// 使用统一的axios实例，自动携带认证信息

// 排班管理相关API
export async function getSchedules(
  skip = 0,
  limit = 100,
  driverId?: number,
  vehicleId?: number,
  scheduleDate?: Date,
  startDate?: Date,
  endDate?: Date,
  status?: string,
  taskType?: string
): Promise<ScheduleResponse[]> {
  const params = new URLSearchParams()
  params.append('skip', skip.toString())
  params.append('limit', limit.toString())
  if (driverId) params.append('driver_id', driverId.toString())
  if (vehicleId) params.append('vehicle_id', vehicleId.toString())
  if (scheduleDate) params.append('schedule_date', scheduleDate?.toISOString().split('T')[0] || '')
  if (startDate) params.append('start_date', startDate?.toISOString().split('T')[0] || '')
  if (endDate) params.append('end_date', endDate?.toISOString().split('T')[0] || '')
  if (status) params.append('status', status)
  if (taskType) params.append('task_type', taskType)
  
  const response = await api.get(`/schedules`, { params })
  return response.data
}

export async function getSchedule(scheduleId: number): Promise<ScheduleResponse> {
  const response = await api.get(`/schedules/${scheduleId}`)
  return response.data
}

export async function createSchedule(schedule: ScheduleCreate): Promise<ScheduleResponse> {
  const response = await api.post(`/schedules`, schedule)
  return response.data
}

export async function updateSchedule(
  scheduleId: number, 
  schedule: ScheduleUpdate
): Promise<ScheduleResponse> {
  const response = await api.put(`/schedules/${scheduleId}`, schedule)
  return response.data
}

export async function deleteSchedule(scheduleId: number): Promise<void> {
  await api.delete(`/schedules/${scheduleId}`)
}

export async function getScheduleCalendar(
  year: number,
  month: number,
  driverId?: number
): Promise<Record<string, any[]>> {
  const params = new URLSearchParams()
  if (driverId) params.append('driver_id', driverId.toString())
  
  const response = await api.get(`/schedules/calendar/${year}/${month}`, { params })
  return response.data
}

export async function checkScheduleConflicts(
  driverId: number,
  startTime: Date,
  endTime: Date,
  scheduleDate: Date,
  excludeScheduleId?: number
): Promise<{ has_conflicts: boolean; conflicts: any[] }> {
  const params = new URLSearchParams()
  params.append('driver_id', driverId.toString())
  params.append('start_time', startTime?.toISOString() || '')
  params.append('end_time', endTime?.toISOString() || '')
  params.append('schedule_date', scheduleDate?.toISOString().split('T')[0] || '')
  if (excludeScheduleId) params.append('exclude_schedule_id', excludeScheduleId.toString())
  
  const response = await api.get(`/schedules/conflicts/check`, { params })
  return response.data
}

export async function getDriverAvailability(
  driverId: number,
  date: Date
): Promise<{
  driver_id: number
  driver_name: string
  date: Date
  available_slots: Array<{ start_time: Date; end_time: Date; duration_minutes: number }>
  total_available_minutes: number
}> {
  const params = new URLSearchParams()
  params.append('driver_id', driverId.toString())
  params.append('date', date?.toISOString().split('T')[0] || '')
  
  const response = await api.get(`/schedules/drivers/${driverId}/availability`, { params })
  return response.data
}