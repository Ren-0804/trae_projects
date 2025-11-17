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
      <a-card style="margin-bottom:16px" title="数据概览">
        <a-descriptions :column="descColumns" bordered size="middle">
          <a-descriptions-item label="司机总数" :labelStyle="{width:'120px'}">{{ statisticsStore.statistics.total_drivers }}</a-descriptions-item>
          <a-descriptions-item label="活跃司机">{{ statisticsStore.statistics.active_drivers }}</a-descriptions-item>
          <a-descriptions-item label="本月新增">{{ statisticsStore.statistics.new_drivers_this_month }}</a-descriptions-item>
          <a-descriptions-item label="活跃率"><a-tag color="blue">{{ activeRate }}%</a-tag></a-descriptions-item>
          <a-descriptions-item label="数据更新时间">{{ statisticsStore.lastUpdatedAt || '-' }}</a-descriptions-item>
        </a-descriptions>
      </a-card>
      <!-- 统计卡片（Ant Design Statistic） -->
  <a-row :gutter="16" class="mb-8">
    <a-col :xs="24" :md="12" :lg="6">
      <a-card>
        <a-statistic
          title="司机总数"
          :value="statisticsStore.statistics.total_drivers"
          :valueStyle="valueStyle(totalChange)"
          :prefix="changePrefix(totalChange)"
        />
      </a-card>
    </a-col>
    <a-col :xs="24" :md="12" :lg="6">
      <a-card>
        <a-statistic
          title="活跃司机"
          :value="statisticsStore.statistics.active_drivers"
          :valueStyle="valueStyle(activeChange)"
          :prefix="changePrefix(activeChange)"
        />
      </a-card>
    </a-col>
    <a-col :xs="24" :md="12" :lg="6">
      <a-card>
        <a-statistic
          title="本月新增"
          :value="statisticsStore.statistics.new_drivers_this_month"
          :valueStyle="valueStyle(monthChange)"
          :prefix="changePrefix(monthChange)"
        />
      </a-card>
    </a-col>
    <a-col :xs="24" :md="12" :lg="6">
      <a-card>
        <a-statistic
          title="活跃率"
          :value="activeRate"
          suffix="%"
          :precision="0"
          :valueStyle="valueStyle(activeRateChange)"
          :prefix="changePrefix(activeRateChange)"
        />
      </a-card>
    </a-col>
  </a-row>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">热门线路 TOP10</h3>
          <a-table :dataSource="statisticsStore.statistics.drivers_by_route" :columns="routeColumns" :pagination="false" />
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">员工司机数量 TOP10</h3>
          <a-table :dataSource="statisticsStore.statistics.drivers_by_user" :columns="userColumns" :pagination="false" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h3 class="text-lg font-medium text-gray-900 mb-4">最近司机照片</h3>
        <a-skeleton :loading="photosLoading" :active="true">
          <a-row :gutter="16">
            <a-col v-for="p in recentPhotos" :key="p.id" :xs="12" :md="8" :lg="6">
              <a-image :src="getPhotoUrl(p.id)" :preview="true" :style="photoStyle" />
              <a-statistic :title="p.photo_type" :value="p.id" prefix="#" style="margin-top:8px" />
            </a-col>
          </a-row>
        </a-skeleton>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">热门线路详细数据</h3>
          <a-row :gutter="12">
            <a-col v-for="(item, index) in statisticsStore.statistics.drivers_by_route" :key="index" :xs="12" :md="8" :lg="6">
              <a-card size="small">
                <a-statistic :title="item.route" :value="item.count" />
              </a-card>
            </a-col>
          </a-row>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">员工司机数量详细数据</h3>
          <a-row :gutter="12">
            <a-col v-for="(item, index) in statisticsStore.statistics.drivers_by_user" :key="index" :xs="12" :md="8" :lg="6">
              <a-card size="small">
                <a-statistic :title="item.username" :value="item.count" />
              </a-card>
            </a-col>
          </a-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, ref } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { toast } from 'sonner'
import { useWindowSize } from '@vueuse/core'
import { useDriverStore } from '@/stores/drivers'
import { getDriverPhotos, getDriverPhotoBlob } from '@/api/drivers'
import { UpOutlined, DownOutlined } from '@ant-design/icons-vue'

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
const changePrefix = (delta: number) => (delta > 0 ? UpOutlined : delta < 0 ? DownOutlined : undefined)
</script>
