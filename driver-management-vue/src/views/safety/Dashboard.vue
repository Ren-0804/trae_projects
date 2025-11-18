<template>
  <div class="safety-dashboard">
    <div style="margin-bottom: 24px;">
      <h1 style="
        margin: 0 0 8px 0;
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      ">安全监控中心</h1>
      <p style="
        margin: 0;
        color: #718096;
        font-size: 16px;
        font-weight: 500;
      ">实时监控车队安全状况</p>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="alertsLoading && !recentAlerts.length" style="
      text-align: center;
      padding: 40px;
      color: #a0aec0;
    ">
      <div class="loading-spinner" style="
        width: 40px;
        height: 40px;
        border: 3px solid rgba(102, 126, 234, 0.1);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 16px;
      "></div>
      <p>正在加载安全数据...</p>
    </div>
    
    <a-row :gutter="[24, 24]">
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <UserOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">在线司机</div>
            <div class="stat-value" style="color: #43e97b;">{{ stats?.online_drivers || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <CarOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">活跃车辆</div>
            <div class="stat-value" style="color: #4facfe;">{{ stats?.active_vehicles || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <WarningOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">今日预警</div>
            <div class="stat-value" style="color: #fa709a;">{{ stats?.today_alerts || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);">
            <AlertOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">紧急报警</div>
            <div class="stat-value" style="color: #ff6b6b;">{{ stats?.emergency_alerts || 0 }}</div>
          </div>
        </div>
      </a-col>
    </a-row>
    
    <a-row :gutter="[24, 24]" style="margin-top: 24px;">
      <a-col :xs="24" :lg="16">
        <div class="glass-card">
          <div class="card-header">
            <h3 class="card-title">实时地图</h3>
            <div class="card-actions">
              <a-button type="text" size="small">
                <template #icon>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </template>
              </a-button>
            </div>
          </div>
          <div class="map-container">
            <div class="map-placeholder">
              <div class="map-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </div>
              <p>实时地图功能开发中</p>
              <span>车辆位置将在此显示</span>
            </div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :lg="8">
        <div class="glass-card">
          <div class="card-header">
            <h3 class="card-title">最近预警</h3>
            <a-badge :count="recentAlerts?.length || 0" :offset="[8, 0]">
              <WarningOutlined />
            </a-badge>
          </div>
          <div class="alerts-list">
            <a-list
              :data-source="recentAlerts"
              :loading="alertsLoading"
            >
              <template #renderItem="{ item }">
                <div class="alert-item">
                  <div class="alert-avatar" :style="{ backgroundColor: getAlertColor(item?.severity) }">
                    <WarningOutlined />
                  </div>
                  <div class="alert-content">
                    <div class="alert-title">{{ item?.alert_type || '未知类型' }}</div>
                  <div class="alert-desc">{{ item?.description || '暂无描述' }}</div>
                  <div class="alert-time">{{ item?.created_at || '' }}</div>
                  </div>
                  <div class="alert-severity" :class="item?.severity">
                    {{ getSeverityText(item?.severity) }}
                  </div>
                </div>
              </template>
              <template #empty>
                <div class="empty-state">
                  <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a0aec0" stroke-width="2">
                      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg>
                  </div>
                  <p>暂无预警信息</p>
                  <span>系统运行正常</span>
                </div>
              </template>
            </a-list>
          </div>
        </div>
      </a-col>
    </a-row>
    
    <a-row :gutter="[24, 24]" style="margin-top: 24px;">
      <a-col :span="24">
        <div class="glass-card">
          <div class="card-header">
            <h3 class="card-title">驾驶行为统计</h3>
            <div class="card-actions">
              <a-button type="text" size="small">
                <template #icon>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </template>
              </a-button>
            </div>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">
              <div class="chart-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2">
                  <path d="M3 3v18h18"></path>
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
                </svg>
              </div>
              <p>驾驶行为分析图表</p>
              <span>数据统计功能开发中</span>
            </div>
          </div>
        </div>
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

const recentAlerts = ref<Array<{
  id: number
  alert_type: string
  severity: string
  status: string
  description: string
  created_at: string
  driver?: {
    id: number
    name: string
  }
}>>([])
const alertsLoading = ref(false)

const getAlertColor = (severity: string) => {
  const colors = {
    'low': '#43e97b',
    'medium': '#fee140',
    'high': '#fa709a',
    'critical': '#ff6b6b'
  }
  return colors[severity as keyof typeof colors] || '#a0aec0'
}

const getSeverityText = (severity: string) => {
  const texts = {
    'low': '低',
    'medium': '中',
    'high': '高',
    'critical': '紧急'
  }
  return texts[severity as keyof typeof texts] || '未知'
}

const fetchSafetyStats = async () => {
  try {
    const response = await getSafetyStats()
    console.log('获取安全统计响应:', response)
    if (response && typeof response === 'object') {
      stats.value = {
        online_drivers: Number(response.online_drivers) || 0,
        active_vehicles: Number(response.active_vehicles) || 0,
        today_alerts: Number(response.today_alerts) || 0,
        emergency_alerts: Number(response.emergency_alerts) || 0
      }
    } else {
      console.warn('获取安全统计数据格式不正确:', response)
      stats.value = {
        online_drivers: 0,
        active_vehicles: 0,
        today_alerts: 0,
        emergency_alerts: 0
      }
    }
  } catch (error) {
    console.error('获取安全统计失败', error)
    stats.value = {
      online_drivers: 0,
      active_vehicles: 0,
      today_alerts: 0,
      emergency_alerts: 0
    }
  }
}

const fetchRecentAlerts = async () => {
  alertsLoading.value = true
  try {
    const response = await getRecentAlerts({ limit: 10 })
    console.log('获取最近预警响应:', response)
    
    // Handle different response formats
    if (Array.isArray(response)) {
      // Backend returns direct array
      recentAlerts.value = response
    } else if (response && response.data && Array.isArray(response.data)) {
      // Expected format with data wrapper
      recentAlerts.value = response.data
    } else {
      console.warn('获取最近预警数据格式不正确:', response)
      recentAlerts.value = []
    }
  } catch (error) {
    console.error('获取最近预警失败', error)
    recentAlerts.value = []
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
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.stat-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  animation: slideInUp 0.6s ease-out;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #718096;
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: slideInUp 0.8s ease-out;
}

.card-header {
  padding: 24px 24px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.card-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.map-container {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 0 0 16px 16px;
  position: relative;
  overflow: hidden;
}

.map-placeholder {
  text-align: center;
  color: #a0aec0;
}

.map-icon {
  margin-bottom: 16px;
  animation: pulse 2s infinite;
}

.map-placeholder p {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #4a5568;
}

.map-placeholder span {
  font-size: 14px;
  color: #718096;
}

.alerts-list {
  padding: 16px;
  max-height: 336px;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  margin-bottom: 12px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.alert-item:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateX(4px);
}

.alert-item:last-child {
  margin-bottom: 0;
}

.alert-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-title {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-desc {
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-time {
  font-size: 12px;
  color: #a0aec0;
}

.alert-severity {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.alert-severity.low {
  background: rgba(67, 233, 123, 0.1);
  color: #43e97b;
}

.alert-severity.medium {
  background: rgba(254, 225, 64, 0.1);
  color: #fee140;
}

.alert-severity.high {
  background: rgba(250, 112, 154, 0.1);
  color: #fa709a;
}

.alert-severity.critical {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #a0aec0;
}

.empty-icon {
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #718096;
}

.empty-state span {
  font-size: 14px;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 0 0 16px 16px;
}

.chart-placeholder {
  text-align: center;
  color: #a0aec0;
}

.chart-icon {
  margin-bottom: 16px;
  animation: pulse 2s infinite;
}

.chart-placeholder p {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #4a5568;
}

.chart-placeholder span {
  font-size: 14px;
  color: #718096;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

:deep(.ant-list-empty-text) {
  padding: 0;
}

:deep(.ant-badge-count) {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
}
</style>
