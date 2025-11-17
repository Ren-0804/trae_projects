<template>
  <div class="schedule-create">
    <a-card title="新增排班">
      <a-form
        :model="form"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 12 }"
        @finish="handleSubmit"
      >
        <a-form-item label="排班日期" name="schedule_date">
          <a-date-picker v-model:value="form.schedule_date" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="司机" name="driver_id">
          <a-select v-model:value="form.driver_id" placeholder="请选择司机">
            <a-select-option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="车辆" name="vehicle_id">
          <a-select v-model:value="form.vehicle_id" placeholder="请选择车辆">
            <a-select-option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
              {{ vehicle.plate_number }} - {{ vehicle.brand_model }}
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="班次类型" name="shift_type">
          <a-select v-model:value="form.shift_type" placeholder="请选择班次类型">
            <a-select-option value="morning">早班</a-select-option>
            <a-select-option value="afternoon">中班</a-select-option>
            <a-select-option value="evening">晚班</a-select-option>
            <a-select-option value="night">夜班</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="开始时间" name="start_time">
          <a-time-picker v-model:value="form.start_time" format="HH:mm" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="结束时间" name="end_time">
          <a-time-picker v-model:value="form.end_time" format="HH:mm" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="备注" name="notes">
          <a-textarea v-model:value="form.notes" placeholder="请输入备注信息" :rows="4" />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 6, span: 12 }">
          <a-space>
            <a-button type="primary" html-type="submit">提交</a-button>
            <router-link to="/schedules">
              <a-button>取消</a-button>
            </router-link>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { createSchedule } from '@/api/schedules'
import { getDrivers } from '@/api/drivers'
import { getVehicles } from '@/api/vehicles'
import type { ScheduleCreateRequest } from '@/types/schedule'
import type { Driver } from '@/types/user'
import type { Vehicle } from '@/types/vehicle'
import dayjs from 'dayjs'

const router = useRouter()

const form = ref<Partial<ScheduleCreateRequest>>({
  schedule_date: undefined,
  driver_id: undefined,
  vehicle_id: undefined,
  shift_type: '',
  start_time: undefined,
  end_time: undefined,
  notes: ''
})

const drivers = ref<Driver[]>([])
const vehicles = ref<Vehicle[]>([])

const rules = {
  schedule_date: [{ required: true, message: '请选择排班日期' }],
  driver_id: [{ required: true, message: '请选择司机' }],
  vehicle_id: [{ required: true, message: '请选择车辆' }],
  shift_type: [{ required: true, message: '请选择班次类型' }],
  start_time: [{ required: true, message: '请选择开始时间' }],
  end_time: [{ required: true, message: '请选择结束时间' }]
}

const fetchDrivers = async () => {
  try {
    const response = await getDrivers({ page_size: 100 })
    drivers.value = response.data
  } catch (error) {
    message.error('获取司机列表失败')
  }
}

const fetchVehicles = async () => {
  try {
    const response = await getVehicles({ page_size: 100 })
    vehicles.value = response.data
  } catch (error) {
    message.error('获取车辆列表失败')
  }
}

const handleSubmit = async () => {
  try {
    const submitData = {
      ...form.value,
      schedule_date: form.value.schedule_date ? dayjs(form.value.schedule_date).format('YYYY-MM-DD') : undefined,
      start_time: form.value.start_time ? dayjs(form.value.start_time).format('HH:mm:ss') : undefined,
      end_time: form.value.end_time ? dayjs(form.value.end_time).format('HH:mm:ss') : undefined
    }
    
    await createSchedule(submitData as ScheduleCreateRequest)
    message.success('排班创建成功')
    router.push('/schedules')
  } catch (error) {
    message.error('创建失败，请重试')
  }
}

onMounted(() => {
  fetchDrivers()
  fetchVehicles()
})
</script>

<style scoped>
.schedule-create {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}
</style>