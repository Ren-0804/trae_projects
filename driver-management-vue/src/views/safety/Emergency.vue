<template>
  <div class="emergency-alerts">
    <a-card title="紧急报警">
      <template #extra>
        <router-link to="/safety">
          <a-button>返回仪表板</a-button>
        </router-link>
      </template>

      <a-row :gutter="16" style="margin-bottom: 24px;">
        <a-col :span="8">
          <a-statistic
            title="今日报警"
            :value="stats.today_emergency"
            value-style="color: #cf1322"
          />
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="未处理报警"
            :value="stats.pending_emergency"
            value-style="color: #ff4d4f"
          />
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="已处理报警"
            :value="stats.resolved_emergency"
            value-style="color: #52c41a"
          />
        </a-col>
      </a-row>

      <a-table
        :columns="columns"
        :data-source="emergencies"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleView(record)">查看</a-button>
              <a-popconfirm
                v-if="record.status === 'active'"
                title="确定要处理这个紧急报警吗？"
                @confirm="handleProcess(record.id)"
              >
                <a-button type="link" size="small" danger>处理</a-button>
              </a-popconfirm>
            </a-space>
          </template>
          <template v-else-if="column.key === 'severity'">
            <a-tag :color="getSeverityColor(record.severity)">
              {{ getSeverityText(record.severity) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver">
              {{ record.driver.name }}
            </span>
            <span v-else style="color: #999">未知</span>
          </template>
          <template v-else-if="column.key === 'location'">
            <div v-if="record.location">
              <div>经度: {{ record.location.longitude }}</div>
              <div>纬度: {{ record.location.latitude }}</div>
            </div>
            <span v-else style="color: #999">无位置信息</span>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getEmergencyAlerts, processEmergencyAlert, getEmergencyStats } from '@/api/safety'
import type { EmergencyAlert } from '@/types/safety'

const loading = ref(false)
const emergencies = ref<EmergencyAlert[]>([])
const stats = ref({
  today_emergency: 0,
  pending_emergency: 0,
  resolved_emergency: 0
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条记录`
})

const columns = [
  {
    title: '报警时间',
    dataIndex: 'created_at',
    key: 'created_at',
    sorter: true
  },
  {
    title: '报警类型',
    dataIndex: 'alert_type',
    key: 'alert_type',
    sorter: true
  },
  {
    title: '严重程度',
    dataIndex: 'severity',
    key: 'severity',
    sorter: true
  },
  {
    title: '司机',
    key: 'driver'
  },
  {
    title: '位置',
    key: 'location'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    sorter: true
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description'
  },
  {
    title: '操作',
    key: 'action',
    width: 150
  }
]

const getSeverityColor = (severity: string) => {
  const colors: Record<string, string> = {
    'low': 'green',
    'medium': 'orange',
    'high': 'red',
    'critical': 'red'
  }
  return colors[severity] || 'default'
}

const getSeverityText = (severity: string) => {
  const texts: Record<string, string> = {
    'low': '低',
    'medium': '中',
    'high': '高',
    'critical': '严重'
  }
  return texts[severity] || severity
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'active': 'red',
    'acknowledged': 'orange',
    'resolved': 'green'
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'active': '未处理',
    'acknowledged': '已确认',
    'resolved': '已解决'
  }
  return texts[status] || status
}

const fetchEmergencies = async () => {
  loading.value = true
  try {
    const skip = (pagination.value.current - 1) * pagination.value.pageSize
    const emergenciesData = await getEmergencyAlerts(
      skip,
      pagination.value.pageSize
    )
    emergencies.value = emergenciesData
    // For now, set total to current length since API doesn't return total
    pagination.value.total = emergenciesData.length + (pagination.value.current * pagination.value.pageSize)
  } catch (error) {
    message.error('获取紧急报警列表失败')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    const response = await getEmergencyStats()
    stats.value = response
  } catch (error) {
    console.error('获取紧急报警统计失败', error)
  }
}

const handleTableChange = (newPagination: any) => {
  pagination.value = { ...pagination.value, ...newPagination }
  fetchEmergencies()
}

const handleView = (record: EmergencyAlert) => {
  // 查看紧急报警详情
  console.log('查看紧急报警:', record)
}

const handleProcess = async (id: number) => {
  try {
    await processEmergencyAlert(id)
    message.success('紧急报警处理成功')
    fetchEmergencies()
    fetchStats()
  } catch (error) {
    message.error('处理失败')
  }
}

onMounted(() => {
  fetchEmergencies()
  fetchStats()
  
  // 定时刷新数据
  setInterval(() => {
    fetchEmergencies()
    fetchStats()
  }, 30000) // 30秒刷新一次
})
</script>

<style scoped>
.emergency-alerts {
  padding: 24px;
}
</style>