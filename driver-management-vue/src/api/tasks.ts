import api from './auth'

export async function createTask(data: any): Promise<any> {
  const response = await api.post('/tasks', data)
  return response.data
}

export async function getTask(id: number): Promise<any> {
  const response = await api.get(`/tasks/${id}`)
  return response.data
}

export async function assignTask(id: number, payload: any): Promise<any> {
  const response = await api.put(`/tasks/${id}/assign`, payload)
  return response.data
}

export async function postTaskEvent(id: number, event: any): Promise<any> {
  const response = await api.post(`/tasks/${id}/event`, event)
  return response.data
}

export async function getTasks(params?: { status?: string }): Promise<any[]> {
  const response = await api.get('/tasks', { params })
  return response.data
}