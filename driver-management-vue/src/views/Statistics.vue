<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">数据统计</h1>
    </div>

    <!-- 加载状态 -->
    <div v-if="statisticsStore.loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else>
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">司机总数</p>
              <p class="text-3xl font-bold text-gray-900">{{ statisticsStore.statistics.total_drivers }}</p>
            </div>
            <div class="text-blue-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">活跃司机</p>
              <p class="text-3xl font-bold text-gray-900">{{ statisticsStore.statistics.active_drivers }}</p>
            </div>
            <div class="text-green-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">本月新增</p>
              <p class="text-3xl font-bold text-gray-900">{{ statisticsStore.statistics.new_drivers_this_month }}</p>
            </div>
            <div class="text-purple-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">活跃率</p>
              <p class="text-3xl font-bold text-gray-900">{{ activeRate }}%</p>
            </div>
            <div class="text-orange-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 热门线路图表 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">热门线路 TOP10</h3>
          <div class="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart :data="statisticsStore.statistics.drivers_by_route">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="route" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <!-- 员工司机数量图表 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">员工司机数量 TOP10</h3>
          <div class="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart :data="statisticsStore.statistics.drivers_by_user">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="username" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <!-- 详细列表 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">热门线路详细数据</h3>
          <div class="space-y-3 max-h-80 overflow-y-auto">
            <div 
              v-for="(item, index) in statisticsStore.statistics.drivers_by_route" 
              :key="index" 
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center">
                <span class="text-sm font-bold text-gray-500 w-8">{{ index + 1 }}.</span>
                <span class="text-sm font-medium text-gray-900">{{ item.route }}</span>
              </div>
              <div class="flex items-center">
                <div class="w-20 bg-gray-200 rounded-full h-2 mr-3">
                  <div 
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                    :style="{ width: `${(item.count / maxRouteCount) * 100}%` }"
                  ></div>
                </div>
                <span class="text-sm font-bold text-gray-700 w-8 text-right">{{ item.count }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">员工司机数量详细数据</h3>
          <div class="space-y-3 max-h-80 overflow-y-auto">
            <div 
              v-for="(item, index) in statisticsStore.statistics.drivers_by_user" 
              :key="index" 
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center">
                <span class="text-sm font-bold text-gray-500 w-8">{{ index + 1 }}.</span>
                <span class="text-sm font-medium text-gray-900">{{ item.username }}</span>
              </div>
              <div class="flex items-center">
                <div class="w-20 bg-gray-200 rounded-full h-2 mr-3">
                  <div 
                    class="bg-green-600 h-2 rounded-full transition-all duration-300" 
                    :style="{ width: `${(item.count / maxUserCount) * 100}%` }"
                  ></div>
                </div>
                <span class="text-sm font-bold text-gray-700 w-8 text-right">{{ item.count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { toast } from 'sonner'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const statisticsStore = useStatisticsStore()

const activeRate = computed(() => statisticsStore.activeRate)
const maxRouteCount = computed(() => statisticsStore.maxRouteCount)
const maxUserCount = computed(() => statisticsStore.maxUserCount)

const fetchStatistics = async () => {
  try {
    await statisticsStore.fetchStatistics()
  } catch (error) {
    console.error('获取统计数据失败:', error)
    toast.error('获取统计数据失败')
  }
}

onMounted(() => {
  fetchStatistics()
})
</script>