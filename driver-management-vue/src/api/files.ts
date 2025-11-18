import api from './auth'

export async function uploadFile(data: FormData): Promise<any> {
  const response = await api.post('/files', data, { headers: { 'Content-Type': 'multipart/form-data' } })
  return response.data
}

export async function getFile(id: number): Promise<any> {
  const response = await api.get(`/files/${id}`)
  return response.data
}

export async function getFiles(params?: Record<string, any>): Promise<any[]> {
  const response = await api.get('/files', { params })
  return response.data
}

export async function deleteFile(id: number): Promise<void> {
  await api.delete(`/files/${id}`)
}