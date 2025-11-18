import api from './auth'
import type { AxiosResponse } from 'axios'

export interface SmartScheduleParams {
  schedule_date: string
  shift_start: string
  shift_end: string
  task_type: 'delivery' | 'pickup' | 'transport'
  required_drivers: number
  prefer_experienced?: boolean
  prefer_high_rating?: boolean
}

export interface ScheduleOption {
  driver: {
    id: number
    name: string
    phone: string
  }
  vehicle: {
    id: number
    plate_number: string
    vehicle_type?: string
  }
  start_time?: string
  end_time?: string
  score?: number
}

export interface ConflictCheckParams {
  driver_id: number
  vehicle_id: number
  schedule_date: string
  start_time: string
  end_time: string
}

export async function generateSmartSchedule(params: SmartScheduleParams): Promise<{ success: boolean; schedules: ScheduleOption[]; total_options: number }>{
  const res = await api.post('/schedules/smart/generate', undefined, { params })
  return (res as AxiosResponse).data
}

export async function checkScheduleConflicts(params: ConflictCheckParams): Promise<{ success: boolean; conflicts: any; can_schedule: boolean }>{
  const res = await api.post('/schedules/smart/check-conflicts', undefined, { params })
  return (res as AxiosResponse).data
}

export async function getDriverAvailability(params: { schedule_date: string; shift_start: string; shift_end: string }): Promise<any>{
  const res = await api.get('/schedules/smart/driver-availability', { params })
  return (res as AxiosResponse).data
}

export async function getVehicleAvailability(params: { schedule_date: string; shift_start: string; shift_end: string; task_type?: 'delivery' | 'pickup' | 'transport' }): Promise<any>{
  const res = await api.get('/schedules/smart/vehicle-availability', { params })
  return (res as AxiosResponse).data
}