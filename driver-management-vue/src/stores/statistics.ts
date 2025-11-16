import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { StatisticsData } from '@/api/statistics'
import { getStatistics } from '@/api/statistics'

export const useStatisticsStore = defineStore('statistics', () => {
  const statistics = ref<StatisticsData>({
    total_drivers: 0,
    active_drivers: 0,
    new_drivers_this_month: 0,
    drivers_by_route: [],
    drivers_by_user: []
  })
  const loading = ref(false)

  // 计算属性
  const activeRate = computed(() => {
    if (statistics.value.total_drivers === 0) return 0
    return Math.round((statistics.value.active_drivers / statistics.value.total_drivers) * 100)
  })

  const maxRouteCount = computed(() => {
    return Math.max(...statistics.value.drivers_by_route.map(item => item.count), 1)
  })

  const maxUserCount = computed(() => {
    return Math.max(...statistics.value.drivers_by_user.map(item => item.count), 1)
  })

  // 获取统计数据
  async function fetchStatistics() {
    loading.value = true
    try {
      const data = await getStatistics()
      statistics.value = data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    statistics,
    loading,
    
    // 计算属性
    activeRate,
    maxRouteCount,
    maxUserCount,
    
    // 方法
    fetchStatistics
  }
})