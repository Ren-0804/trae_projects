<template>
  <div class="page-container">
    <!-- Glassmorphism Header -->
    <div class="page-header glass-panel">
      <div class="header-content">
        <div class="header-title-wrapper">
          <h1 class="page-title text-gradient">排班管理</h1>
          <p class="page-subtitle">管理司机排班和调度安排</p>
        </div>
        <a-space>
          <router-link to="/schedules/calendar">
            <a-button size="large" class="action-btn-secondary">
              <template #icon><CalendarOutlined /></template>
              排班日历
            </a-button>
          </router-link>
          <router-link to="/schedules/new">
            <a-button type="primary" size="large" class="action-btn">
              <template #icon><PlusOutlined /></template>
              新增排班
            </a-button>
          </router-link>
        </a-space>
      </div>
    </div>

    <!-- Glassmorphism Table Card -->
    <div class="table-card glass-panel">
      <a-table
        :columns="columns"
        :data-source="schedules"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/schedules/${record.id}`">
                <a-button type="text" class="action-link view">
                  <template #icon><EyeOutlined /></template>
                  详情
                </a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这个排班吗？"
                @confirm="handleDelete(record.id)"
                okText="确认"
                cancelText="取消"
                :okButtonProps="{ danger: true }"
              >
                <a-button danger type="text" class="action-link delete">
                  <template #icon><DeleteOutlined /></template>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag 
              :color="getStatusColor(record.status)"
              class="status-tag"
            >
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver" class="driver-name">
              {{ record.driver.name }}
            </span>
            <span v-else class="driver-empty">未分配</span>
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getSchedules, deleteSchedule } from '@/api/schedules'
import type { Schedule } from '@/types/schedule'
import {
  PlusOutlined,
  CalendarOutlined,
  EyeOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'

const loading = ref(false)
const schedules = ref<Schedule[]>([])
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
    title: '排班日期',
    dataIndex: 'schedule_date',
    key: 'schedule_date',
    sorter: true
  },
  {
    title: '司机',
    key: 'driver',
    sorter: true
  },
  {
    title: '车辆',
    dataIndex: 'vehicle',
    key: 'vehicle',
    customRender: ({ text }: any) => text?.plate_number || '未分配'
  },
  {
    title: '班次类型',
    dataIndex: 'shift_type',
    key: 'shift_type',
    sorter: true
  },
  {
    title: '开始时间',
    dataIndex: 'start_time',
    key: 'start_time'
  },
  {
    title: '结束时间',
    dataIndex: 'end_time',
    key: 'end_time'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    sorter: true
  },
  {
    title: '操作',
    key: 'action',
    width: 150
  }
]

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'scheduled': 'blue',
    'in_progress': 'orange',
    'completed': 'green',
    'cancelled': 'red'
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'scheduled': '已安排',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

const fetchSchedules = async () => {
  loading.value = true
  try {
    const skip = (pagination.value.current - 1) * pagination.value.pageSize
    const schedulesData = await getSchedules(
      skip,
      pagination.value.pageSize
    )
    schedules.value = schedulesData
    // For now, set total to current length since API doesn't return total
    pagination.value.total = schedulesData.length + (pagination.value.current * pagination.value.pageSize)
  } catch (error) {
    message.error('获取排班列表失败')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (newPagination: any) => {
  pagination.value = { ...pagination.value, ...newPagination }
  fetchSchedules()
}

const handleDelete = async (id: number) => {
  try {
    await deleteSchedule(id)
    message.success('删除成功')
    fetchSchedules()
  } catch (error) {
    message.error('删除失败')
  }
}

onMounted(() => {
  fetchSchedules()
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
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--color-text-secondary);
  margin: var(--spacing-xs) 0 0 0;
  font-size: var(--font-size-sm);
}

.action-btn {
  border-radius: var(--radius-base);
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  height: 44px;
  padding: 0 24px;
}

.action-btn-secondary {
  border-radius: var(--radius-base);
  font-weight: 600;
  height: 44px;
  padding: 0 20px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.action-btn-secondary:hover {
  background: white;
  color: var(--color-primary-600);
  border-color: var(--color-primary-200);
}

.table-card {
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.custom-table {
  background: transparent;
}

:deep(.ant-table) {
  background: transparent;
}

:deep(.ant-table-thead > tr > th) {
  background: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  color: var(--color-text-secondary);
}

.status-tag {
  border-radius: var(--radius-full);
  padding: 2px 10px;
  font-weight: 500;
}

.driver-name {
  font-weight: 500;
  color: var(--color-text-primary);
}

.driver-empty {
  color: var(--color-text-tertiary);
  font-style: italic;
}

.action-link {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.action-link.view { color: var(--color-info); }
.action-link.delete { color: var(--color-error); }

.action-link:hover {
  background: rgba(0, 0, 0, 0.05);
}
</style>
