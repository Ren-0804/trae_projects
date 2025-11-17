<template>
  <div class="vehicle-detail">
    <a-card title="车辆详情">
      <template #extra>
        <a-space>
          <router-link :to="`/vehicles/${vehicleId}/assign-driver`">
            <a-button type="primary">分配司机</a-button>
          </router-link>
          <router-link :to="`/vehicles/${vehicleId}/edit`">
            <a-button>编辑</a-button>
          </router-link>
        </a-space>
      </template>
      
      <a-descriptions bordered :column="2">
        <a-descriptions-item label="车牌号">{{ vehicle?.plate_number }}</a-descriptions-item>
        <a-descriptions-item label="车辆类型">{{ getVehicleTypeText(vehicle?.vehicle_type) }}</a-descriptions-item>
        <a-descriptions-item label="品牌型号">{{ vehicle?.brand_model }}</a-descriptions-item>
        <a-descriptions-item label="购买日期">{{ vehicle?.purchase_date }}</a-descriptions-item>
        <a-descriptions-item label="当前里程">{{ vehicle?.current_mileage }} 公里</a-descriptions-item>
        <a-descriptions-item label="状态">
          <a-tag :color="getStatusColor(vehicle?.status)">
            {{ getStatusText(vehicle?.status) }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="当前司机" :span="2">
          <span v-if="vehicle?.current_driver">
            {{ vehicle.current_driver.name }} ({{ vehicle.current_driver.phone }})
          </span>
          <span v-else style="color: #999">未分配司机</span>
        </a-descriptions-item>
        <a-descriptions-item label="备注" :span="2">{{ vehicle?.notes || '无' }}</a-descriptions-item>
      </a-descriptions>
      
      <a-divider />
      
      <h3>司机使用记录概览</h3>
      <a-row :gutter="16" style="margin-bottom: 16px;">
        <a-col :span="6">
          <a-statistic
            title="总使用司机数"
            :value="usageStatistics.total_drivers"
            :precision="0"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="当前活跃司机"
            :value="usageStatistics.active_assignments"
            :precision="0"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="平均使用时长"
            :value="usageStatistics.avg_duration_days"
            :precision="1"
            suffix="天"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="最长使用记录"
            :value="usageStatistics.longest_duration_days"
            :precision="0"
            suffix="天"
          />
        </a-col>
      </a-row>
      
      <a-table
        :columns="assignmentColumns"
        :data-source="driverAssignments"
        :loading="assignmentsLoading"
        :pagination="false"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'driver_name'">
            {{ record.driver?.name }} ({{ record.driver?.phone }})
          </template>
          <template v-else-if="column.key === 'type'">
            <a-tag :color="record.assignment_type === 'primary' ? 'blue' : 'orange'">
              {{ record.assignment_type === 'primary' ? '主要司机' : '临时司机' }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="record.status === 'active' ? 'green' : 'red'">
              {{ record.status === 'active' ? '活跃' : '已结束' }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'duration'">
            {{ formatAssignmentDuration(record.start_date, record.end_date) }}
          </template>
        </template>
      </a-table>
      
      <div style="margin-top: 16px; text-align: center;">
        <router-link :to="`/vehicles/${vehicleId}/usage-history`">
          <a-button type="link">查看详细使用记录 →</a-button>
        </router-link>
      </div>
      
      <a-divider />
      
      <h3>维护记录</h3>
      <a-table
        :columns="maintenanceColumns"
        :data-source="maintenanceRecords"
        :loading="maintenanceLoading"
        :pagination="false"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getMaintenanceStatusColor(record.status)">
              {{ getMaintenanceStatusText(record.status) }}
            </a-tag>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { getVehicle, getVehicleMaintenanceRecords } from '@/api/vehicles'
import type { Vehicle, MaintenanceRecord } from '@/types/vehicle'

const route = useRoute()
const vehicleId = Number(route.params.id)

const loading = ref(false)
const maintenanceLoading = ref(false)
const assignmentsLoading = ref(false)
const vehicle = ref<Vehicle | null>(null)
const maintenanceRecords = ref<MaintenanceRecord[]>([])
const driverAssignments = ref<any[]>([])

const usageStatistics = reactive({
  total_drivers: 0,
  active_assignments: 0,
  avg_duration_days: 0,
  longest_duration_days: 0
})

const assignmentColumns = [
  {
    title: '司机',
    key: 'driver_name',
    width: 200
  },
  {
    title: '分配类型',
    dataIndex: 'assignment_type',
    key: 'type',
    width: 100
  },
  {
    title: '开始日期',
    dataIndex: 'start_date',
    key: 'start_date',
    width: 120,
    customRender: ({ text }: any) => text ? new Date(text).toLocaleDateString() : '-'
  },
  {
    title: '结束日期',
    dataIndex: 'end_date',
    key: 'end_date',
    width: 120,
    customRender: ({ text }: any) => text ? new Date(text).toLocaleDateString() : '-'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100
  },
  {
    title: '持续时间',
    key: 'duration',
    width: 150
  }
]

const maintenanceColumns = [
  {
    title: '维护类型',
    dataIndex: 'maintenance_type',
    key: 'maintenance_type'
  },
  {
    title: '维护日期',
    dataIndex: 'maintenance_date',
    key: 'maintenance_date'
  },
  {
    title: '里程数',
    dataIndex: 'mileage_at_maintenance',
    key: 'mileage_at_maintenance'
  },
  {
    title: '费用',
    dataIndex: 'cost',
    key: 'cost'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status'
  }
]

const getVehicleTypeText = (type: string | undefined) => {
  const texts: Record<string, string> = {
    'truck': '货车',
    'bus': '客车',
    'van': '面包车',
    'car': '小轿车'
  }
  return type ? (texts[type] || type) : ''
}

const getStatusColor = (status: string | undefined) => {
  const colors: Record<string, string> = {
    'active': 'green',
    'maintenance': 'orange',
    'inactive': 'red',
    'retired': 'gray'
  }
  return status ? (colors[status] || 'default') : 'default'
}

const getStatusText = (status: string | undefined) => {
  const texts: Record<string, string> = {
    'active': '正常',
    'maintenance': '维修中',
    'inactive': '停用',
    'retired': '报废'
  }
  return status ? (texts[status] || status) : ''
}

const getMaintenanceStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'scheduled': 'blue',
    'in_progress': 'orange',
    'completed': 'green',
    'cancelled': 'red'
  }
  return colors[status] || 'default'
}

const getMaintenanceStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'scheduled': '已安排',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

const formatAssignmentDuration = (startDate: string, endDate: string | null) => {
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  const diffDays = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '1天'
  if (diffDays < 30) return `${diffDays}天`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月`
  return `${Math.floor(diffDays / 365)}年`
}

const calculateUsageStatistics = (assignments: any[]) => {
  if (!assignments || assignments.length === 0) {
    usageStatistics.total_drivers = 0
    usageStatistics.active_assignments = 0
    usageStatistics.avg_duration_days = 0
    usageStatistics.longest_duration_days = 0
    return
  }

  // 计算总司机数（去重）
  const uniqueDrivers = new Set(assignments.map(a => a.driver_id))
  usageStatistics.total_drivers = uniqueDrivers.size

  // 计算活跃分配数
  usageStatistics.active_assignments = assignments.filter(a => a.status === 'active').length

  // 计算平均使用时长
  const durations = assignments.map(a => {
    const start = new Date(a.start_date)
    const end = a.end_date ? new Date(a.end_date) : new Date()
    return Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
  })
  
  const totalDays = durations.reduce((sum, days) => sum + days, 0)
  usageStatistics.avg_duration_days = totalDays / assignments.length

  // 计算最长使用时长
  usageStatistics.longest_duration_days = Math.max(...durations)
}

const fetchVehicle = async () => {
  loading.value = true
  try {
    const response = await getVehicle(vehicleId)
    vehicle.value = response
    // 假设后端返回的数据中包含 assignments 字段
    if (response.assignments) {
      driverAssignments.value = response.assignments
      calculateUsageStatistics(response.assignments)
    }
  } catch (error) {
    message.error('获取车辆信息失败')
  } finally {
    loading.value = false
  }
}

const fetchMaintenanceRecords = async () => {
  maintenanceLoading.value = true
  try {
    const response = await getVehicleMaintenanceRecords(vehicleId)
    maintenanceRecords.value = response.data
  } catch (error) {
    message.error('获取维护记录失败')
  } finally {
    maintenanceLoading.value = false
  }
}

onMounted(() => {
  fetchVehicle()
  fetchMaintenanceRecords()
})
</script>

<style scoped>
.vehicle-detail {
  padding: 24px;
}
</style>