<template>
  <div class="schedule-list">
    <a-card title="排班管理">
      <template #extra>
        <a-space>
          <router-link to="/schedules/calendar">
            <a-button>排班日历</a-button>
          </router-link>
          <router-link to="/schedules/new">
            <a-button type="primary">新增排班</a-button>
          </router-link>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="schedules"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/schedules/${record.id}`">
                <a-button type="link" size="small">详情</a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这个排班吗？"
                @confirm="handleDelete(record.id)"
              >
                <a-button type="link" danger size="small">删除</a-button>
              </a-popconfirm>
            </a-space>
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
            <span v-else style="color: #999">未分配</span>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getSchedules, deleteSchedule } from '@/api/schedules'
import type { Schedule } from '@/types/schedule'

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
    const response = await getSchedules({
      page: pagination.value.current,
      page_size: pagination.value.pageSize
    })
    schedules.value = response.data
    pagination.value.total = response.total
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