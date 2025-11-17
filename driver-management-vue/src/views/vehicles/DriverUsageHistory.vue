<template>
  <div class="driver-usage-history">
    <a-card title="司机使用记录">
      <template #extra>
        <a-space>
          <a-range-picker
            v-model:value="dateRange"
            @change="handleDateRangeChange"
            placeholder="选择日期范围"
          />
          <a-select
            v-model:value="filterStatus"
            placeholder="选择状态"
            style="width: 120px"
            allow-clear
          >
            <a-select-option value="active">活跃</a-select-option>
            <a-select-option value="completed">已完成</a-select-option>
            <a-select-option value="cancelled">已取消</a-select-option>
          </a-select>
          <a-button type="primary" @click="exportUsageHistory">导出记录</a-button>
        </a-space>
      </template>
      
      <a-table
        :columns="usageColumns"
        :data-source="usageRecords"
        :loading="loading"
        :pagination="paginationConfig"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'driver_info'">
            <div>
              <div class="driver-name">{{ record.driver?.name }}</div>
              <div class="driver-phone">{{ record.driver?.phone }}</div>
              <div class="license-number">驾照: {{ record.driver?.license_number }}</div>
            </div>
          </template>
          <template v-else-if="column.key === 'assignment_type'">
            <a-tag :color="getAssignmentTypeColor(record.assignment_type)">
              {{ getAssignmentTypeText(record.assignment_type) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'duration'">
            <div class="duration-info">
              <div>开始: {{ formatDate(record.start_date) }}</div>
              <div>结束: {{ record.end_date ? formatDate(record.end_date) : '进行中' }}</div>
              <div class="duration-days">
                {{ calculateDuration(record.start_date, record.end_date) }}
              </div>
            </div>
          </template>
          <template v-else-if="column.key === 'usage_stats'">
            <div class="stats-info">
              <div>总天数: {{ record.total_days }}天</div>
              <div>活跃状态: {{ record.is_active ? '是' : '否' }}</div>
              <div v-if="record.total_distance" class="distance">
                总里程: {{ record.total_distance }}公里
              </div>
            </div>
          </template>
          <template v-else-if="column.key === 'actions'">
            <a-space>
              <a-button type="link" size="small" @click="viewDriverDetails(record.driver_id)">
                查看司机
              </a-button>
              <a-button 
                v-if="record.status === 'active'" 
                type="link" 
                size="small" 
                danger
                @click="endAssignment(record.id)"
              >
                结束分配
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
      
      <a-divider />
      
      <a-row :gutter="16">
        <a-col :span="8">
          <a-statistic
            title="总使用司机数"
            :value="statistics.total_drivers"
            :precision="0"
          />
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="当前活跃司机"
            :value="statistics.active_assignments"
            :precision="0"
          />
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="平均使用时长"
            :value="statistics.avg_duration_days"
            :precision="1"
            suffix="天"
          />
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import type { Dayjs } from 'dayjs'
import { getVehicleAssignments } from '@/api/vehicles'

const router = useRouter()
const props = defineProps<{
  vehicleId: number
}>()

const loading = ref(false)
const dateRange = ref<[Dayjs, Dayjs] | null>(null)
const filterStatus = ref<string | null>(null)

const usageRecords = ref<any[]>([])
const statistics = reactive({
  total_drivers: 0,
  active_assignments: 0,
  avg_duration_days: 0
})

const paginationConfig = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number, range: [number, number]) => 
    `第 ${range[0]}-${range[1]} 条/共 ${total} 条`
})

const usageColumns = [
  {
    title: '司机信息',
    key: 'driver_info',
    width: 200,
    fixed: 'left' as const
  },
  {
    title: '分配类型',
    key: 'assignment_type',
    width: 100
  },
  {
    title: '使用时长',
    key: 'duration',
    width: 200
  },
  {
    title: '使用统计',
    key: 'usage_stats',
    width: 150
  },
  {
    title: '状态',
    key: 'status',
    width: 100
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 150,
    customRender: ({ text }: any) => formatDate(text)
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    fixed: 'right' as const
  }
]

const getAssignmentTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    'primary': 'blue',
    'temporary': 'orange',
    'backup': 'green'
  }
  return colors[type] || 'default'
}

const getAssignmentTypeText = (type: string) => {
  const texts: Record<string, string> = {
    'primary': '主要司机',
    'temporary': '临时司机',
    'backup': '备用司机'
  }
  return texts[type] || type
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'active': 'green',
    'completed': 'blue',
    'cancelled': 'red'
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'active': '活跃',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const calculateDuration = (startDate: string, endDate: string | null) => {
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  const diffDays = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '1天'
  if (diffDays < 30) return `${diffDays}天`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月`
  return `${Math.floor(diffDays / 365)}年`
}

const handleDateRangeChange = () => {
  paginationConfig.current = 1
  fetchUsageHistory()
}

const handleTableChange = (pagination: any) => {
  paginationConfig.current = pagination.current
  paginationConfig.pageSize = pagination.pageSize
  fetchUsageHistory()
}

const viewDriverDetails = (driverId: number) => {
  router.push(`/drivers/${driverId}`)
}

const endAssignment = async (assignmentId: number) => {
  try {
    // 这里需要添加结束分配的API调用
    message.success('分配已结束')
    fetchUsageHistory()
  } catch (error) {
    message.error('结束分配失败')
  }
}

const exportUsageHistory = () => {
  // 导出使用记录功能
  const data = usageRecords.value.map(record => ({
    '司机姓名': record.driver?.name,
    '司机电话': record.driver?.phone,
    '驾照号码': record.driver?.license_number,
    '分配类型': getAssignmentTypeText(record.assignment_type),
    '开始日期': formatDate(record.start_date),
    '结束日期': formatDate(record.end_date),
    '使用时长': calculateDuration(record.start_date, record.end_date),
    '状态': getStatusText(record.status),
    '创建时间': formatDate(record.created_at)
  }))
  
  // 这里可以添加实际的导出逻辑
  message.success('导出功能开发中')
}

const fetchUsageHistory = async () => {
  loading.value = true
  try {
    const params = {
      vehicle_id: props.vehicleId,
      page: paginationConfig.current,
      page_size: paginationConfig.pageSize,
      status: filterStatus.value,
      start_date: dateRange.value?.[0]?.format('YYYY-MM-DD'),
      end_date: dateRange.value?.[1]?.format('YYYY-MM-DD')
    }
    
    const response = await getVehicleAssignments(params)
    usageRecords.value = response.data
    paginationConfig.total = response.total
    
    // 计算统计数据
    calculateStatistics()
  } catch (error) {
    message.error('获取使用记录失败')
  } finally {
    loading.value = false
  }
}

const calculateStatistics = () => {
  const uniqueDrivers = new Set(usageRecords.value.map(r => r.driver_id))
  statistics.total_drivers = uniqueDrivers.size
  statistics.active_assignments = usageRecords.value.filter(r => r.status === 'active').length
  
  const totalDays = usageRecords.value.reduce((sum, record) => {
    const duration = calculateDurationInDays(record.start_date, record.end_date)
    return sum + duration
  }, 0)
  
  statistics.avg_duration_days = usageRecords.value.length > 0 
    ? totalDays / usageRecords.value.length 
    : 0
}

const calculateDurationInDays = (startDate: string, endDate: string | null) => {
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  return Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
}

onMounted(() => {
  fetchUsageHistory()
})
</script>

<style scoped>
.driver-usage-history {
  padding: 24px;
}

.driver-name {
  font-weight: 500;
  color: #1890ff;
}

.driver-phone {
  color: #666;
  font-size: 12px;
}

.license-number {
  color: #999;
  font-size: 11px;
}

.duration-info {
  font-size: 12px;
}

.duration-days {
  color: #1890ff;
  font-weight: 500;
  margin-top: 4px;
}

.stats-info {
  font-size: 12px;
}

.distance {
  color: #52c41a;
  margin-top: 4px;
}
</style>