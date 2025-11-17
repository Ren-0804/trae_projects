<template>
  <div class="safety-dashboard">
    <a-row :gutter="16">
      <a-col :span="6">
        <a-card>
          <a-statistic
            title="在线司机"
            :value="stats.online_drivers"
            value-style="color: #3f8600"
          >
            <template #prefix>
              <UserOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <a-statistic
            title="活跃车辆"
            :value="stats.active_vehicles"
            value-style="color: #1890ff"
          >
            <template #prefix>
              <CarOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <a-statistic
            title="今日预警"
            :value="stats.today_alerts"
            value-style="color: #cf1322"
          >
            <template #prefix>
              <WarningOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <a-statistic
            title="紧急报警"
            :value="stats.emergency_alerts"
            value-style="color: #ff4d4f"
          >
            <template #prefix>
              <AlertOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
    </a-row>
    
    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="16">
        <a-card title="实时地图" style="height: 500px;">
          <div class="map-container">
            <a-empty description="地图加载中..." />
          </div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="最近预警" style="height: 500px;">
          <a-list
            :data-source="recentAlerts"
            :loading="alertsLoading"
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta
                  :title="item.alert_type"
                  :description="item.description"
                >
                  <template #avatar>
                    <a-avatar :style="{ backgroundColor: getAlertColor(item.severity) }">
                      <WarningOutlined />
                    </a-avatar>
                  </template>
                </a-list-item-meta>
                <div>{{ item.created_at }}</div>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
    
    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="24">
        <a-card title="驾驶行为统计">
          <div style="height: 300px;">
            <a-empty description="图表加载中..." />
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { UserOutlined, CarOutlined, WarningOutlined, AlertOutlined } from '@ant-design/icons-vue'
import { getSafetyStats, getRecentAlerts } from '@/api/safety'

const stats = ref({
  online_drivers: 0,
  active_vehicles: 0,
  today_alerts: 0,
  emergency_alerts: 0
})

const recentAlerts = ref([])
const alertsLoading = ref(false)

const getAlertColor = (severity: string) => {
  const colors = {
    'low': '#52c41a',
    'medium': '#faad14',
    'high': '#ff4d4f',
    'critical': '#cf1322'
  }
  return colors[severity as keyof typeof colors] || '#999'
}

const fetchSafetyStats = async () => {
  try {
    const response = await getSafetyStats()
    stats.value = response
  } catch (error) {
    console.error('获取安全统计失败', error)
  }
}

const fetchRecentAlerts = async () => {
  alertsLoading.value = true
  try {
    const response = await getRecentAlerts({ limit: 10 })
    recentAlerts.value = response.data
  } catch (error) {
    console.error('获取最近预警失败', error)
  } finally {
    alertsLoading.value = false
  }
}

onMounted(() => {
  fetchSafetyStats()
  fetchRecentAlerts()
  
  // 定时刷新数据
  setInterval(() => {
    fetchSafetyStats()
    fetchRecentAlerts()
  }, 30000) // 30秒刷新一次
})
</script>

<style scoped>
.safety-dashboard {
  padding: 24px;
}

.map-container {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>