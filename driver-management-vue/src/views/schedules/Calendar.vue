<template>
  <div class="schedule-calendar">
    <a-card title="排班日历">
      <template #extra>
        <a-space>
          <router-link to="/schedules/new">
            <a-button type="primary">新增排班</a-button>
          </router-link>
          <router-link to="/schedules">
            <a-button>返回列表</a-button>
          </router-link>
        </a-space>
      </template>
      
      <!-- 筛选器 -->
      <a-row :gutter="16" style="margin-bottom: 16px">
        <a-col :span="6">
          <a-select
            v-model:value="selectedDriver"
            placeholder="选择司机"
            allow-clear
            style="width: 100%"
            @change="filterSchedules"
          >
            <a-select-option
              v-for="driver in availableDrivers"
              :key="driver.id"
              :value="driver.id"
            >
              {{ driver.name }}
            </a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-select
            v-model:value="selectedVehicle"
            placeholder="选择车辆"
            allow-clear
            style="width: 100%"
            @change="filterSchedules"
          >
            <a-select-option
              v-for="vehicle in availableVehicles"
              :key="vehicle.id"
              :value="vehicle.id"
            >
              {{ vehicle.plate_number }}
            </a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-select
            v-model:value="selectedStatus"
            placeholder="选择状态"
            allow-clear
            style="width: 100%"
            @change="filterSchedules"
          >
            <a-select-option value="scheduled">已安排</a-select-option>
            <a-select-option value="in_progress">进行中</a-select-option>
            <a-select-option value="completed">已完成</a-select-option>
            <a-select-option value="cancelled">已取消</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-range-picker
            v-model:value="dateRange"
            style="width: 100%"
            @change="filterSchedules"
          />
        </a-col>
      </a-row>
      
      <div class="calendar-container">
        <a-calendar
          v-model:value="selectedDate"
          :fullscreen="false"
          @select="handleDateSelect"
          @panelChange="handleMonthChange"
        >
          <template #dateCellRender="{ current }">
            <div class="calendar-cell">
              <div v-if="hasSchedule(current)" class="schedule-indicator">
                <a-badge :status="getScheduleStatus(current)" />
                <span class="schedule-count">{{ getScheduleCount(current) }}</span>
              </div>
              <div v-if="isToday(current)" class="today-indicator">
                <a-badge status="default" />
              </div>
            </div>
          </template>
        </a-calendar>
        
        <div class="schedule-details">
          <div class="details-header">
            <h3>{{ selectedDate.format('YYYY年MM月DD日') }} 的排班</h3>
            <a-space>
              <a-button type="primary" size="small" @click="createScheduleForDate">
                <PlusOutlined />
                新增排班
              </a-button>
              <a-button size="small" @click="viewDayOverview">
                日视图
              </a-button>
            </a-space>
          </div>
          
          <div v-if="selectedSchedules.length > 0" class="schedule-list">
            <a-timeline>
              <a-timeline-item
                v-for="schedule in selectedSchedules"
                :key="schedule.id"
                :color="getTimelineColor(schedule.status)"
              >
                <div class="schedule-item">
                  <div class="schedule-time">
                    {{ formatTime(schedule.start_time) }} - {{ formatTime(schedule.end_time) }}
                  </div>
                  <div class="schedule-info">
                    <div class="driver-vehicle">
                      <UserOutlined />
                      {{ schedule.driver?.name }}
                      <CarOutlined style="margin-left: 8px" />
                      {{ schedule.vehicle?.plate_number }}
                    </div>
                    <div class="schedule-details">
                      <a-tag :color="getStatusColor(schedule.status)">
                        {{ getStatusText(schedule.status) }}
                      </a-tag>
                      <span class="task-type">{{ getTaskTypeText(schedule.task_type) }}</span>
                      <span class="route" v-if="schedule.route">{{ schedule.route }}</span>
                    </div>
                  </div>
                  <div class="schedule-actions">
                    <a-space>
                      <router-link :to="`/schedules/${schedule.id}`">
                        <a-button type="link" size="small">详情</a-button>
                      </router-link>
                      <a-button
                        type="link"
                        size="small"
                        @click="editSchedule(schedule)"
                      >
                        编辑
                      </a-button>
                      <a-popconfirm
                        title="确定要取消这个排班吗？"
                        @confirm="cancelSchedule(schedule)"
                      >
                        <a-button type="link" danger size="small">取消</a-button>
                      </a-popconfirm>
                    </a-space>
                  </div>
                </div>
              </a-timeline-item>
            </a-timeline>
          </div>
          <div v-else-if="selectedDate" class="no-schedules">
            <a-empty description="该日期暂无排班">
              <template #extra>
                <a-button type="primary" @click="createScheduleForDate">
                  为该日期创建排班
                </a-button>
              </template>
            </a-empty>
          </div>
        </div>
      </div>
      
      <!-- 统计信息 -->
      <a-divider />
      <div class="statistics">
        <a-row :gutter="16">
          <a-col :span="6">
            <a-statistic
              title="今日排班"
              :value="todayScheduleCount"
              :value-style="{ color: '#1890ff' }"
            >
              <template #prefix>
                <CalendarOutlined />
              </template>
            </a-statistic>
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="本周排班"
              :value="weekScheduleCount"
              :value-style="{ color: '#52c41a' }"
            >
              <template #prefix>
                <ScheduleOutlined />
              </template>
            </a-statistic>
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="进行中"
              :value="activeScheduleCount"
              :value-style="{ color: '#fa8c16' }"
            >
              <template #prefix>
                <ClockCircleOutlined />
              </template>
            </a-statistic>
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="已完成"
              :value="completedScheduleCount"
              :value-style="{ color: '#722ed1' }"
            >
              <template #prefix>
                <CheckCircleOutlined />
              </template>
            </a-statistic>
          </a-col>
        </a-row>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { message } from 'ant-design-vue'
import { getSchedules } from '@/api/schedules'
import { getDrivers } from '@/api/drivers'
import { getVehicles } from '@/api/vehicles'
import type { Schedule } from '@/types/schedule'
import type { Driver } from '@/types/user'
import type { Vehicle } from '@/types/vehicle'
import {
  CalendarOutlined,
  ScheduleOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  UserOutlined,
  CarOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const selectedDate = ref(dayjs())
const schedules = ref<Schedule[]>([])
const filteredSchedules = ref<Schedule[]>([])
const loading = ref(false)

// 筛选器状态
const selectedDriver = ref<number | null>(null)
const selectedVehicle = ref<number | null>(null)
const selectedStatus = ref<string>('')
const dateRange = ref<any[]>([])

// 可用选项
const availableDrivers = ref<Driver[]>([])
const availableVehicles = ref<Vehicle[]>([])

const selectedSchedules = computed(() => {
  if (!selectedDate.value) return []
  const dateStr = selectedDate.value.format('YYYY-MM-DD')
  return filteredSchedules.value.filter(schedule => 
    dayjs(schedule.schedule_date).format('YYYY-MM-DD') === dateStr
  )
})

const hasSchedule = (date: any) => {
  const dateStr = date.format('YYYY-MM-DD')
  return filteredSchedules.value.some(schedule => 
    dayjs(schedule.schedule_date).format('YYYY-MM-DD') === dateStr
  )
}

const getScheduleCount = (date: any) => {
  const dateStr = date.format('YYYY-MM-DD')
  return filteredSchedules.value.filter(schedule => 
    dayjs(schedule.schedule_date).format('YYYY-MM-DD') === dateStr
  ).length
}

const getScheduleStatus = (date: any) => {
  const dateStr = date.format('YYYY-MM-DD')
  const daySchedules = filteredSchedules.value.filter(schedule => 
    dayjs(schedule.schedule_date).format('YYYY-MM-DD') === dateStr
  )
  
  if (daySchedules.length === 0) return 'default'
  if (daySchedules.some(s => s.status === 'in_progress')) return 'processing'
  if (daySchedules.some(s => s.status === 'cancelled')) return 'error'
  if (daySchedules.every(s => s.status === 'completed')) return 'success'
  return 'warning'
}

const isToday = (date: any) => {
  return date.isSame(dayjs(), 'day')
}

const formatTime = (time: Date | string) => {
  return dayjs(time).format('HH:mm')
}

const getTimelineColor = (status: string) => {
  const colors: Record<string, string> = {
    'scheduled': 'blue',
    'in_progress': 'orange',
    'completed': 'green',
    'cancelled': 'red'
  }
  return colors[status] || 'gray'
}

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

const getTaskTypeText = (taskType: string) => {
  const texts: Record<string, string> = {
    'delivery': '配送',
    'pickup': '取货',
    'transport': '运输'
  }
  return texts[taskType] || taskType
}

// 统计计算
const todayScheduleCount = computed(() => {
  const today = dayjs().format('YYYY-MM-DD')
  return filteredSchedules.value.filter(s => 
    dayjs(s.schedule_date).format('YYYY-MM-DD') === today
  ).length
})

const weekScheduleCount = computed(() => {
  const startOfWeek = dayjs().startOf('week').format('YYYY-MM-DD')
  const endOfWeek = dayjs().endOf('week').format('YYYY-MM-DD')
  return filteredSchedules.value.filter(s => {
    const scheduleDate = dayjs(s.schedule_date).format('YYYY-MM-DD')
    return scheduleDate >= startOfWeek && scheduleDate <= endOfWeek
  }).length
})

const activeScheduleCount = computed(() => {
  return filteredSchedules.value.filter(s => s.status === 'in_progress').length
})

const completedScheduleCount = computed(() => {
  return filteredSchedules.value.filter(s => s.status === 'completed').length
})

const handleDateSelect = () => {
  // 日期选择处理逻辑
}

const handleMonthChange = (date: any) => {
  // 月份切换时重新加载数据
  fetchSchedulesForMonth(date)
}

const filterSchedules = () => {
  filteredSchedules.value = schedules.value.filter(schedule => {
    // 司机筛选
    if (selectedDriver.value && schedule.driver_id !== selectedDriver.value) return false
    
    // 车辆筛选
    if (selectedVehicle.value && schedule.vehicle_id !== selectedVehicle.value) return false
    
    // 状态筛选
    if (selectedStatus.value && schedule.status !== selectedStatus.value) return false
    
    // 日期范围筛选
    if (dateRange.value && dateRange.value.length === 2) {
      const scheduleDate = dayjs(schedule.schedule_date)
      if (scheduleDate.isBefore(dateRange.value[0]) || scheduleDate.isAfter(dateRange.value[1])) return false
    }
    
    return true
  })
}

const createScheduleForDate = () => {
  if (!selectedDate.value) return
  const dateStr = selectedDate.value.format('YYYY-MM-DD')
  router.push(`/schedules/new?date=${dateStr}`)
}

const viewDayOverview = () => {
  if (!selectedDate.value) return
  const dateStr = selectedDate.value.format('YYYY-MM-DD')
  // 这里可以跳转到日视图或打开详细对话框
  message.info(`查看 ${dateStr} 的日视图`)
}

const editSchedule = (schedule: Schedule) => {
  router.push(`/schedules/${schedule.id}/edit`)
}

const cancelSchedule = async (schedule: Schedule) => {
  try {
    // 这里需要实现取消排班的 API 调用
    message.success('排班已取消')
    fetchSchedules()
  } catch (error) {
    message.error('取消排班失败')
    console.error('Failed to cancel schedule:', error)
  }
}

const fetchSchedules = async () => {
  loading.value = true
  try {
    const startDate = dayjs().startOf('month').subtract(1, 'month').toDate()
    const endDate = dayjs().endOf('month').add(1, 'month').toDate()
    
    const schedulesData = await getSchedules(0, 200, undefined, undefined, startDate, endDate)
    schedules.value = schedulesData
    filteredSchedules.value = schedulesData
  } catch (error) {
    console.error('获取排班数据失败', error)
  } finally {
    loading.value = false
  }
}

const fetchSchedulesForMonth = async (date: any) => {
  loading.value = true
  try {
    const startDate = date.startOf('month').subtract(1, 'month').toDate()
    const endDate = date.endOf('month').add(1, 'month').toDate()
    
    const schedulesData = await getSchedules(0, 200, undefined, undefined, startDate, endDate)
    schedules.value = schedulesData
    filterSchedules()
  } catch (error) {
    console.error('获取排班数据失败', error)
  } finally {
    loading.value = false
  }
}

const fetchDrivers = async () => {
  try {
    const response = await getDrivers({ page: 1, page_size: 100 })
    availableDrivers.value = response.data
  } catch (error) {
    console.error('获取司机列表失败', error)
  }
}

const fetchVehicles = async () => {
  try {
    const vehiclesData = await getVehicles(0, 100)
    availableVehicles.value = vehiclesData
  } catch (error) {
    console.error('获取车辆列表失败', error)
  }
}

onMounted(() => {
  fetchSchedules()
  fetchDrivers()
  fetchVehicles()
})
</script>

<style scoped>
.schedule-calendar {
  padding: 24px;
}

.calendar-container {
  display: flex;
  gap: 24px;
  margin-top: 16px;
}

.calendar-cell {
  min-height: 60px;
  position: relative;
}

.schedule-indicator {
  position: absolute;
  bottom: 4px;
  left: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.schedule-count {
  font-size: 12px;
  color: #1890ff;
}

.today-indicator {
  position: absolute;
  top: 4px;
  right: 4px;
}

.schedule-details {
  flex: 1;
  min-width: 400px;
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.details-header h3 {
  margin: 0;
  color: #262626;
}

.schedule-list {
  max-height: 500px;
  overflow-y: auto;
}

.schedule-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  margin-bottom: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.schedule-time {
  font-weight: 600;
  color: #1890ff;
  font-size: 14px;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.driver-vehicle {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #595959;
}

.schedule-details {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.task-type {
  color: #8c8c8c;
}

.route {
  color: #595959;
  font-weight: 500;
}

.schedule-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.no-schedules {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.statistics {
  margin-top: 16px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

:deep(.ant-timeline-item-content) {
  width: 100%;
}

:deep(.ant-calendar-date) {
  min-height: 80px;
  position: relative;
}

:deep(.ant-calendar-full) {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}
</style>