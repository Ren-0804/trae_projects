// 车辆相关类型定义
export interface VehicleBase {
  plate_number: string
  vehicle_type: string
  brand?: string
  model?: string
  year?: number
  color?: string
  engine_number?: string
  vin_number?: string
  purchase_date?: Date
  registration_date?: Date
  insurance_expiry?: Date
  annual_inspection_date?: Date
  maintenance_due_date?: Date
  mileage: number
  current_mileage?: number
  fuel_type?: string
  fuel_consumption: number
  status: 'active' | 'maintenance' | 'retired'
  current_driver_id?: number
  notes?: string
}

export interface VehicleCreate extends VehicleBase {}

export interface VehicleUpdate extends Partial<VehicleBase> {}

export interface VehicleResponse extends VehicleBase {
  id: number
  created_at: Date
  updated_at: Date
  current_driver?: {
    id: number
    name: string
    phone: string
  }
  assignments?: Array<{
    id: number
    driver_id: number
    driver_name: string
    start_date: Date
    end_date?: Date
    status: string
  }>
  brand_model?: string
}

// 简化类型别名，便于组件使用
export type Vehicle = VehicleResponse
export type VehicleCreateRequest = VehicleCreate
export type VehicleUpdateRequest = VehicleUpdate

// 维护记录相关类型定义
export interface MaintenanceRecordBase {
  vehicle_id: number
  maintenance_type: 'routine' | 'repair' | 'inspection'
  description?: string
  cost: number
  mileage_at_service?: number
  service_date: Date
  next_service_date?: Date
  service_provider?: string
  invoice_number?: string
  status: 'scheduled' | 'in_progress' | 'completed'
}

export interface MaintenanceRecordCreate extends MaintenanceRecordBase {}

export interface MaintenanceRecordUpdate extends Partial<MaintenanceRecordBase> {}

export interface MaintenanceRecordResponse extends MaintenanceRecordBase {
  id: number
  created_at: Date
  updated_at: Date
  vehicle?: VehicleResponse
}

// 简化类型别名，便于组件使用
export type MaintenanceRecord = MaintenanceRecordResponse