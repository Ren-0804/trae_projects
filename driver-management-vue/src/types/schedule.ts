// 排班相关类型定义
export interface ScheduleBase {
  driver_id: number
  vehicle_id?: number
  schedule_date: Date
  start_time: Date
  end_time: Date
  route?: string
  task_type: 'delivery' | 'pickup' | 'transport'
  shift_type?: string
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled'
  notes?: string
}

export interface ScheduleCreate extends ScheduleBase {}

export interface ScheduleUpdate extends Partial<ScheduleBase> {}

export interface ScheduleResponse extends ScheduleBase {
  id: number
  created_at: Date
  updated_at: Date
  driver?: {
    id: number
    name: string
    phone: string
  }
  vehicle?: {
    id: number
    plate_number: string
    vehicle_type: string
  }
}

// 简化类型别名，便于组件使用
export type Schedule = ScheduleResponse
export type ScheduleCreateRequest = ScheduleCreate
export type ScheduleUpdateRequest = ScheduleUpdate