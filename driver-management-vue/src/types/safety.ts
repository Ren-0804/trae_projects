// 安全管理相关类型定义

// GPS记录类型
export interface GPSRecordBase {
  vehicle_id: number
  driver_id?: number
  latitude: number
  longitude: number
  speed: number
  heading?: number
  altitude?: number
  accuracy?: number
  timestamp: Date
  address?: string
  status?: 'normal' | 'speeding' | 'idle'
}

export interface GPSRecordCreate extends GPSRecordBase {}

export interface GPSRecordResponse extends GPSRecordBase {
  id: number
  created_at: Date
  vehicle?: {
    id: number
    plate_number: string
    vehicle_type: string
  }
  driver?: {
    id: number
    name: string
    phone: string
  }
}

// 驾驶行为类型
export interface DrivingBehaviorBase {
  driver_id: number
  vehicle_id?: number
  behavior_type: 'harsh_braking' | 'speeding' | 'sharp_turn'
  severity: 'low' | 'medium' | 'high'
  latitude?: number
  longitude?: number
  speed_at_event?: number
  timestamp: Date
  description?: string
  processed: boolean
}

export interface DrivingBehaviorCreate extends DrivingBehaviorBase {}

export interface DrivingBehaviorUpdate {
  processed: boolean
}

export interface DrivingBehaviorResponse extends DrivingBehaviorBase {
  id: number
  created_at: Date
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

// 紧急警报类型
export interface EmergencyAlertBase {
  driver_id: number
  vehicle_id?: number
  alert_type: 'accident' | 'medical' | 'security'
  severity: 'low' | 'medium' | 'high' | 'critical'
  latitude?: number
  longitude?: number
  description?: string
  status: 'active' | 'responded' | 'resolved'
  responded_by?: number
  response_time?: Date
}

export interface EmergencyAlertCreate extends EmergencyAlertBase {}

export interface EmergencyAlertUpdate {
  status: 'active' | 'responded' | 'resolved'
  responded_by?: number
  response_time?: Date
}

export interface EmergencyAlertResponse extends EmergencyAlertBase {
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
  responder?: {
    id: number
    username: string
  }
}

// 简化类型别名，便于组件使用
export type GPSRecord = GPSRecordResponse
export type DrivingBehavior = DrivingBehaviorResponse
export type EmergencyAlert = EmergencyAlertResponse
export type Alert = EmergencyAlertResponse