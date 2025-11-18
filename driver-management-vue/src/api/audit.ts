import api from './auth'

export async function getAuditLogs(params?: Record<string, any>): Promise<any[]> {
  const response = await api.get('/audit/logs', { params })
  return response.data
}

export async function getAuditLog(id: number): Promise<any> {
  const response = await api.get(`/audit/logs/${id}`)
  return response.data
}

export async function exportAuditLogs(params?: Record<string, any>): Promise<Blob> {
  const response = await api.get('/audit/logs', { params: { ...(params || {}), format: 'csv' }, responseType: 'blob' })
  return response.data
}

export async function createAuditLog(payload: {
  action: string
  actor_id?: number
  actor_name?: string
  resource?: string
  resource_id?: string | number
  content?: any
  severity?: 'low' | 'medium' | 'high' | 'critical'
}): Promise<{ id: number }> {
  const response = await api.post('/audit/logs', payload)
  return response.data
}

export async function createAuditAlert(payload: {
  action: string
  resource?: string
  resource_id?: string | number
  description?: string
  severity: 'low' | 'medium' | 'high' | 'critical'
}): Promise<{ id: number }> {
  const response = await api.post('/audit/alerts', payload)
  return response.data
}