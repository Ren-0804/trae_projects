// 证书相关类型定义
export interface DriverCertificateBase {
  driver_id: number
  certificate_type: string
  certificate_number: string
  issue_date?: Date
  expiry_date: Date
  issuing_authority?: string
  status: 'valid' | 'expired' | 'suspended'
  file_path?: string
}

export interface DriverCertificateCreate extends DriverCertificateBase {}

export interface DriverCertificateUpdate extends Partial<DriverCertificateBase> {}

export interface DriverCertificateResponse extends DriverCertificateBase {
  id: number
  created_at: Date
  updated_at: Date
  driver?: {
    id: number
    name: string
    phone: string
  }
}