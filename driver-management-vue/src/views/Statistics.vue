<template>
  <div style="padding: 24px">
    <!-- Glassmorphism Header -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <div>
          <h1 style="
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
          ">数据统计</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">全面的数据分析和趋势洞察</p>
        </div>
        <a-button 
          type="primary" 
          @click="fetchStatistics"
          style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            height: 44px;
            padding: 0 24px;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
          "
        >
          <template #icon><ReloadOutlined /></template>
          刷新数据
        </a-button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="statisticsStore.loading" style="display: flex; justify-content: center; align-items: center; padding: 48px 0;">
      <div style="
        width: 48px;
        height: 48px;
        border: 3px solid rgba(102, 126, 234, 0.1);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      "></div>
    </div>

    <div v-else>
      <!-- Glassmorphism Overview Card -->
      <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      ">
        <h2 style="
          font-size: 20px;
          font-weight: 600;
          color: #2c3e50;
          margin: 0 0 16px 0;
        ">数据概览</h2>
        <a-descriptions :column="descColumns" bordered size="middle">
          <a-descriptions-item label="司机总数" :labelStyle="{width:'120px', background: 'rgba(102, 126, 234, 0.05)'}">
            <span style="font-weight: 600; color: #667eea;">{{ statisticsStore.statistics.total_drivers }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="活跃司机" :labelStyle="{background: 'rgba(102, 126, 234, 0.05)'}">
            <span style="font-weight: 600; color: #10b981;">{{ statisticsStore.statistics.active_drivers }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="本月新增" :labelStyle="{background: 'rgba(102, 126, 234, 0.05)'}">
            <span style="font-weight: 600; color: #f59e0b;">{{ statisticsStore.statistics.new_drivers_this_month }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="活跃率" :labelStyle="{background: 'rgba(102, 126, 234, 0.05)'}">
            <a-tag color="blue" style="border-radius: 12px; font-weight: 600;">{{ activeRate }}%</a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="数据更新时间" :labelStyle="{background: 'rgba(102, 126, 234, 0.05)'}">
            <span style="color: #6b7280;">{{ statisticsStore.lastUpdatedAt || '-' }}</span>
          </a-descriptions-item>
        </a-descriptions>
      </div>
      
      <!-- Glassmorphism Statistics Cards -->
      <a-row :gutter="16" style="margin-bottom: 24px;">
        <a-col :xs="24" :md="12" :lg="6">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
          "
          @mouseenter="hoverUp4"
          @mouseleave="hoverDown"
          >
            <a-statistic
              title="司机总数"
              :value="statisticsStore.statistics.total_drivers"
              :valueStyle="valueStyle(totalChange)"
              :prefix="changePrefix(totalChange)"
            />
          </div>
        </a-col>
        <a-col :xs="24" :md="12" :lg="6">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
          "
          @mouseenter="hoverUp4"
          @mouseleave="hoverDown"
          >
            <a-statistic
              title="活跃司机"
              :value="statisticsStore.statistics.active_drivers"
              :valueStyle="valueStyle(activeChange)"
              :prefix="changePrefix(activeChange)"
            />
          </div>
        </a-col>
        <a-col :xs="24" :md="12" :lg="6">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
          "
          @mouseenter="hoverUp4"
          @mouseleave="hoverDown"
          >
            <a-statistic
              title="本月新增"
              :value="statisticsStore.statistics.new_drivers_this_month"
              :valueStyle="valueStyle(monthChange)"
              :prefix="changePrefix(monthChange)"
            />
          </div>
        </a-col>
        <a-col :xs="24" :md="12" :lg="6">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
          "
          @mouseenter="hoverUp4"
          @mouseleave="hoverDown"
          >
            <a-statistic
              title="活跃率"
              :value="activeRate"
              suffix="%"
              :precision="0"
              :valueStyle="valueStyle(activeRateChange)"
              :prefix="changePrefix(activeRateChange)"
            />
          </div>
        </a-col>
      </a-row>

      <!-- Glassmorphism Charts -->
      <a-row :gutter="16" style="margin-bottom: 24px;">
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            height: 400px;
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">热门线路分布图</h3>
            <BarChart 
              :data="routeChartData" 
              title="热门线路司机数量"
              xAxisName="线路"
              yAxisName="司机数量"
              height="320px"
            />
          </div>
        </a-col>
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            height: 400px;
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">员工司机分布图</h3>
            <PieChart 
              :data="userChartData" 
              title="员工司机数量占比"
              height="320px"
              :showLegend="true"
            />
          </div>
        </a-col>
      </a-row>

      <!-- Glassmorphism Trend Charts -->
      <a-row :gutter="16" style="margin-bottom: 24px;">
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            height: 370px;
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">司机增长趋势</h3>
            <LineChart 
              :data="growthTrendData" 
              title="司机数量增长趋势"
              xAxisName="月份"
              yAxisName="司机数量"
              height="290px"
              :showArea="true"
              color="#10b981"
            />
          </div>
        </a-col>
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            height: 370px;
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">活跃率趋势</h3>
            <LineChart 
              :data="activeRateTrendData" 
              title="司机活跃率变化"
              xAxisName="月份"
              yAxisName="活跃率 (%)"
              height="290px"
              :showArea="true"
              color="#3b82f6"
            />
          </div>
        </a-col>
      </a-row>

      <!-- Glassmorphism Data Tables -->
      <a-row :gutter="16" style="margin-bottom: 24px;">
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">热门线路 TOP10</h3>
            <a-table 
              :dataSource="statisticsStore.statistics.drivers_by_route" 
              :columns="routeColumns" 
              :pagination="false"
              style="background: transparent;"
            />
          </div>
        </a-col>
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">员工司机数量 TOP10</h3>
            <a-table 
              :dataSource="statisticsStore.statistics.drivers_by_user" 
              :columns="userColumns" 
              :pagination="false"
              style="background: transparent;"
            />
          </div>
        </a-col>
      </a-row>

      <!-- Glassmorphism Photo Gallery -->
      <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      ">
        <h3 style="
          font-size: 18px;
          font-weight: 600;
          color: #2c3e50;
          margin: 0 0 16px 0;
        ">最近司机照片</h3>
        <a-skeleton :loading="photosLoading" :active="true">
          <a-row :gutter="16">
            <a-col v-for="p in recentPhotos" :key="p.id" :xs="12" :md="8" :lg="6">
              <div style="
                background: rgba(255, 255, 255, 0.6);
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 16px;
                transition: all 0.3s ease;
              "
              @mouseenter="hoverUp2"
              @mouseleave="hoverDown"
              >
                <a-image :src="getPhotoUrl(p.id)" :preview="true" :style="photoStyle" />
                <a-statistic :title="p.photo_type" :value="p.id" prefix="#" style="margin-top: 8px;" />
              </div>
            </a-col>
          </a-row>
        </a-skeleton>
      </div>

      <!-- Glassmorphism Detailed Data Cards -->
      <a-row :gutter="16">
        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">热门线路详细数据</h3>
            <a-row :gutter="12">
              <a-col v-for="(item, index) in statisticsStore.statistics.drivers_by_route.slice(0, 8)" :key="index" :xs="12" :md="8" :lg="6">
                <div style="
                  background: rgba(102, 126, 234, 0.1);
                  border-radius: 8px;
                  padding: 12px;
                  margin-bottom: 8px;
                  text-align: center;
                  transition: all 0.3s ease;
                "
                @mouseenter="bgBlueEnter"
                @mouseleave="bgBlueLeave"
                >
                  <div style="font-size: 12px; color: #6b7280; margin-bottom: 4px;">{{ item.route }}</div>
                  <div style="font-size: 16px; font-weight: 600; color: #667eea;">{{ item.count }}</div>
                </div>
              </a-col>
            </a-row>
          </div>
        </a-col>

        <a-col :xs="24" :lg="12">
          <div style="
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          ">
            <h3 style="
              font-size: 18px;
              font-weight: 600;
              color: #2c3e50;
              margin: 0 0 16px 0;
            ">员工司机数量详细数据</h3>
            <a-row :gutter="12">
              <a-col v-for="(item, index) in statisticsStore.statistics.drivers_by_user.slice(0, 8)" :key="index" :xs="12" :md="8" :lg="6">
                <div style="
                  background: rgba(16, 185, 129, 0.1);
                  border-radius: 8px;
                  padding: 12px;
                  margin-bottom: 8px;
                  text-align: center;
                  transition: all 0.3s ease;
                "
                @mouseenter="bgGreenEnter"
                @mouseleave="bgGreenLeave"
                >
                  <div style="font-size: 12px; color: #6b7280; margin-bottom: 4px;">{{ item.username }}</div>
                  <div style="font-size: 16px; font-weight: 600; color: #10b981;">{{ item.count }}</div>
                </div>
              </a-col>
            </a-row>
          </div>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, ref, h } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { toast } from 'sonner'
import { useWindowSize } from '@vueuse/core'
import { useDriverStore } from '@/stores/drivers'
import { getDriverPhotos, getDriverPhotoBlob } from '@/api/drivers'
import { UpOutlined, DownOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { BarChart, PieChart, LineChart } from '@/components/charts'
import { formatStatisticsToChartData, generateTimeSeriesData, filterAndSortData as _unused } from '@/utils/chartUtils'
const hoverUp4 = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.transform = 'translateY(-4px)' }
const hoverDown = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.transform = 'translateY(0)' }
const hoverUp2 = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.transform = 'translateY(-2px)' }
const bgBlueEnter = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(102, 126, 234, 0.2)' }
const bgBlueLeave = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(102, 126, 234, 0.1)' }
const bgGreenEnter = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(16, 185, 129, 0.2)' }
const bgGreenLeave = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(16, 185, 129, 0.1)' }

const statisticsStore = useStatisticsStore()
const driverStore = useDriverStore()

const activeRate = computed(() => statisticsStore.activeRate)
const previousActiveRate = computed(() => statisticsStore.previousActiveRate)
const totalChange = computed(() => {
  const prev = statisticsStore.previous
  if (!prev) return 0
  return statisticsStore.statistics.total_drivers - prev.total_drivers
})
const activeChange = computed(() => {
  const prev = statisticsStore.previous
  if (!prev) return 0
  return statisticsStore.statistics.active_drivers - prev.active_drivers
})
const monthChange = computed(() => {
  const prev = statisticsStore.previous
  if (!prev) return 0
  return statisticsStore.statistics.new_drivers_this_month - prev.new_drivers_this_month
})
const activeRateChange = computed(() => activeRate.value - previousActiveRate.value)
const maxRouteCount = computed(() => statisticsStore.maxRouteCount)
const maxUserCount = computed(() => statisticsStore.maxUserCount)
const { width } = useWindowSize()
const descColumns = computed(() => (width.value >= 768 ? 2 : 1))
const routeColumns = [
  { title: '线路', dataIndex: 'route', key: 'route' },
  { title: '数量', dataIndex: 'count', key: 'count' },
]
const userColumns = [
  { title: '员工', dataIndex: 'username', key: 'username' },
  { title: '数量', dataIndex: 'count', key: 'count' },
]

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

const recentPhotos = ref<any[]>([])
const photoUrls = ref<Record<number, string>>({})
const photosLoading = ref(false)
const hydratorRunning = ref(false)
const imageFallback =
  'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 24 24" fill="none" stroke="%23ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>'
const photoStyle = { width: '100%', height: '120px', objectFit: 'cover', borderRadius: '8px' } as any

const hydratePhotoUrls = async () => {
  if (hydratorRunning.value) return
  hydratorRunning.value = true
  try {
    for (const p of recentPhotos.value) {
      if (!photoUrls.value[p.id]) {
        try {
          const blob = await getDriverPhotoBlob(p.id)
          photoUrls.value[p.id] = blob && blob.size > 0 ? URL.createObjectURL(blob) : imageFallback
        } catch {
          photoUrls.value[p.id] = imageFallback
        }
      }
    }
  } finally {
    hydratorRunning.value = false
  }
}

const getPhotoUrl = (id: number) => {
  const url = photoUrls.value[id]
  return url && url.length > 0 ? url : imageFallback
}

const fetchRecentDriverPhotos = async () => {
  photosLoading.value = true
  try {
    await driverStore.fetchDrivers({ page: 1, page_size: 6 })
    const drivers = driverStore.drivers.slice(0, 6)
    const photos: any[] = []
    for (const d of drivers) {
      try {
        const list = await getDriverPhotos(d.id)
        const vehicle = list.find((x: any) => x.photo_type === 'vehicle')
        const picked = vehicle || list[0]
        if (picked) photos.push(picked)
      } catch {
      }
    }
    recentPhotos.value = photos
    await hydratePhotoUrls()
  } finally {
    photosLoading.value = false
  }
}

onMounted(() => {
  fetchRecentDriverPhotos()
})

onBeforeUnmount(() => {
  Object.values(photoUrls.value).forEach((u) => u && URL.revokeObjectURL(u))
})

const valueStyle = (delta: number) => ({ color: delta > 0 ? '#16a34a' : delta < 0 ? '#dc2626' : '#0f172a' }) as any

// 修复：返回组件实例而不是组件函数
const changePrefix = (delta: number) => {
  if (delta > 0) return h(UpOutlined)
  if (delta < 0) return h(DownOutlined)
  return undefined
}

// 图表数据计算属性
const routeChartData = computed(() => {
  return formatStatisticsToChartData(
    statisticsStore.statistics.drivers_by_route.map(item => ({
      name: item.route,
      count: item.count
    })),
    10
  )
})

const userChartData = computed(() => {
  return formatStatisticsToChartData(
    statisticsStore.statistics.drivers_by_user.map(item => ({
      name: item.username,
      count: item.count
    })),
    8
  )
})

// 模拟增长趋势数据
const growthTrendData = computed(() => {
  const currentMonth = new Date().getMonth()
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const data: Array<{ name: string; value: number }> = []
  
  // 基于当前数据生成过去6个月的趋势
  const baseCount = statisticsStore.statistics.total_drivers
  for (let i = 5; i >= 0; i--) {
    const monthIndex = (currentMonth - i + 12) % 12
    const growthFactor = 1 + (5 - i) * 0.1 // 模拟增长
    data.push({
      name: months[monthIndex] || '未知月份',
      value: Math.floor(baseCount / growthFactor)
    })
  }
  
  return data
})

// 模拟活跃率趋势数据
const activeRateTrendData = computed(() => {
  const currentMonth = new Date().getMonth()
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const data: Array<{ name: string; value: number }> = []
  
  const currentActiveRate = activeRate.value
  for (let i = 5; i >= 0; i--) {
    const monthIndex = (currentMonth - i + 12) % 12
    const variation = (Math.random() - 0.5) * 10 // 随机波动
    data.push({
      name: months[monthIndex] || '未知月份',
      value: Math.max(0, Math.min(100, currentActiveRate + variation))
    })
  }
  
  return data
})
</script>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 全局动画 */
.glass-card {
  animation: fadeIn 0.6s ease-out;
}
</style>
