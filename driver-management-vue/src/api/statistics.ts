import api from './auth'

export interface StatisticsData {
  total_drivers: number
  active_drivers: number
  new_drivers_this_month: number
  drivers_by_route: Array<{ route: string; count: number }>
  drivers_by_user: Array<{ user_id: number; username: string; count: number }>
}

export async function getStatistics(): Promise<StatisticsData> {
  const response = await api.get('/statistics')
  return response.data
}
