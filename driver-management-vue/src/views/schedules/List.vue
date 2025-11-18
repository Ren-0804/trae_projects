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
          ">排班管理</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">管理司机排班和调度安排</p>
        </div>
        <a-space>
          <router-link to="/schedules/calendar">
            <a-button 
              type="default"
              size="large"
              style="
                border-radius: 12px;
                height: 44px;
                padding: 0 20px;
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 0, 0, 0.1);
                font-weight: 600;
              "
            >
              <template #icon><CalendarOutlined /></template>
              排班日历
            </a-button>
          </router-link>
          <router-link to="/schedules/new">
            <a-button 
              type="primary" 
              size="large"
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
              <template #icon><PlusOutlined /></template>
              新增排班
            </a-button>
          </router-link>
        </a-space>
      </div>
    </div>

    <!-- Glassmorphism Table Card -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    ">
      <a-table
        :columns="columns"
        :data-source="schedules"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        style="background: transparent;"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/schedules/${record.id}`">
                <a-button 
                  type="text" 
                  style="
                    color: #667eea;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 500;
                  "
                >
                  <template #icon><EyeOutlined /></template>
                  详情
                </a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这个排班吗？"
                @confirm="handleDelete(record.id)"
                okText="确认"
                cancelText="取消"
              >
                <a-button 
                  danger 
                  type="text"
                  style="
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 500;
                  "
                >
                  <template #icon><DeleteOutlined /></template>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag 
              :color="getStatusColor(record.status)"
              style="border-radius: 20px; padding: 4px 12px; font-weight: 500;"
            >
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver" style="font-weight: 500;">
              {{ record.driver.name }}
            </span>
            <span v-else style="color: #9ca3af; font-style: italic;">未分配</span>
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
.schedule-list {
  padding: 24px;
}
</style>