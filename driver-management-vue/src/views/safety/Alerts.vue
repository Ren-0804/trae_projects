<template>
  <div class="safety-alerts">
    <a-card title="安全预警">
      <template #extra>
        <router-link to="/safety">
          <a-button>返回仪表板</a-button>
        </router-link>
      </template>

      <a-table
        :columns="columns"
        :data-source="alerts"
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
                title="确定要处理这个预警吗？"
                @confirm="handleProcess(record.id)"
              >
                <a-button type="link" size="small">处理</a-button>
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
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getAlerts, processAlert } from '@/api/safety'
import type { Alert } from '@/types/safety'

const loading = ref(false)
const alerts = ref<Alert[]>([])
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
    title: '预警时间',
    dataIndex: 'created_at',
    key: 'created_at',
    sorter: true
  },
  {
    title: '预警类型',
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

const fetchAlerts = async () => {
  loading.value = true
  try {
    const response = await getAlerts({
      page: pagination.value.current,
      page_size: pagination.value.pageSize
    })
    alerts.value = response.data
    pagination.value.total = response.total
  } catch (error) {
    message.error('获取预警列表失败')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (newPagination: any) => {
  pagination.value = { ...pagination.value, ...newPagination }
  fetchAlerts()
}

const handleView = (record: Alert) => {
  // 查看预警详情
  console.log('查看预警:', record)
}

const handleProcess = async (id: number) => {
  try {
    await processAlert(id)
    message.success('预警处理成功')
    fetchAlerts()
  } catch (error) {
    message.error('处理失败')
  }
}

onMounted(() => {
  fetchAlerts()
})
</script>

<style scoped>
.safety-alerts {
  padding: 24px;
}
</style>