<template>
  <div class="page-container">
    <div class="page-header glass-panel">
      <div class="header-content">
        <div class="header-title-wrapper">
          <h1 class="page-title text-gradient">安全监控中心</h1>
          <p class="page-subtitle">实时监控车队安全状况</p>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="alertsLoading && !recentAlerts.length" class="loading-container">
      <div class="loading-spinner"></div>
      <p>正在加载安全数据...</p>
    </div>
    
    <a-row :gutter="[24, 24]">
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card glass-panel">
          <div class="stat-icon icon-online">
            <UserOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">在线司机</div>
            <div class="stat-value text-online">{{ stats?.online_drivers || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card glass-panel">
          <div class="stat-icon icon-active">
            <CarOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">活跃车辆</div>
            <div class="stat-value text-active">{{ stats?.active_vehicles || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card glass-panel">
          <div class="stat-icon icon-warning">
            <WarningOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">今日预警</div>
            <div class="stat-value text-warning">{{ stats?.today_alerts || 0 }}</div>
          </div>
        </div>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card glass-panel">
          <div class="stat-icon icon-emergency">
            <AlertOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-title">紧急报警</div>
            <div class="stat-value text-emergency">{{ stats?.emergency_alerts || 0 }}</div>
          </div>
        </div>
      </a-col>
    </a-row>
    
    <a-row :gutter="[24, 24]" class="mt-lg">
      <a-col :xs="24" :lg="16">
        <div class="glass-panel full-height">
          <div class="panel-header">
            <h3 class="panel-title">实时地图</h3>
            <div class="panel-actions">
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
            <div class="placeholder-content">
              <div class="placeholder-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
        <div class="glass-panel full-height">
          <div class="panel-header">
            <h3 class="panel-title">最近预警</h3>
            <a-badge :count="recentAlerts?.length || 0" :offset="[8, 0]" class="custom-badge">
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
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
    
    <a-row :gutter="[24, 24]" class="mt-lg">
      <a-col :span="24">
        <div class="glass-panel">
          <div class="panel-header">
            <h3 class="panel-title">驾驶行为统计</h3>
            <div class="panel-actions">
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
            <div class="placeholder-content">
              <div class="placeholder-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
.page-container {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.page-header {
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--color-text-secondary);
  margin: 0;
  font-size: var(--font-size-md);
  font-weight: 500;
}

.mt-lg {
  margin-top: var(--spacing-lg);
}

.full-height {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.stat-card {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
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

.icon-online { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.icon-active { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.icon-warning { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.icon-emergency { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }

.stat-content { flex: 1; }

.stat-title {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.text-online { color: #43e97b; }
.text-active { color: #4facfe; }
.text-warning { color: #fa709a; }
.text-emergency { color: #ff6b6b; }

.panel-header {
  padding: 24px 24px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.panel-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.map-container, .chart-container {
  flex: 1;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  position: relative;
  overflow: hidden;
}

.chart-container { min-height: 300px; }

.placeholder-content {
  text-align: center;
  color: var(--color-text-tertiary);
}

.placeholder-icon {
  margin-bottom: 16px;
  animation: pulse 2s infinite;
  color: var(--color-primary-500);
}

.placeholder-content p {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--color-text-secondary);
}

.placeholder-content span {
  font-size: 14px;
  color: var(--color-text-tertiary);
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
  color: var(--color-text-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-time {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.alert-severity {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.alert-severity.low { background: rgba(67, 233, 123, 0.1); color: #43e97b; }
.alert-severity.medium { background: rgba(254, 225, 64, 0.1); color: #fee140; }
.alert-severity.high { background: rgba(250, 112, 154, 0.1); color: #fa709a; }
.alert-severity.critical { background: rgba(255, 107, 107, 0.1); color: #ff6b6b; }

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-text-tertiary);
}

.empty-icon {
  margin-bottom: 16px;
  color: var(--color-text-tertiary);
}

.empty-state p {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--color-text-secondary);
}

.loading-container {
  text-align: center;
  padding: 40px;
  color: var(--color-text-tertiary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(102, 126, 234, 0.1);
  border-top: 3px solid var(--color-primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

:deep(.ant-list-empty-text) { padding: 0; }

:deep(.ant-badge-count) {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
}
</style>
