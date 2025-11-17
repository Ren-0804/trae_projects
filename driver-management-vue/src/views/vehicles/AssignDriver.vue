<template>
  <div class="assign-driver">
    <a-card title="分配司机">
      <a-form
        :model="formState"
        :rules="rules"
        @finish="handleSubmit"
        layout="vertical"
      >
        <a-form-item label="选择司机" name="driverId">
          <a-select
            v-model:value="formState.driverId"
            placeholder="请选择司机"
            :loading="driversLoading"
            show-search
            :filter-option="filterDriverOption"
          >
            <a-select-option
              v-for="driver in availableDrivers"
              :key="driver.id"
              :value="driver.id"
            >
              {{ driver.name }} - {{ driver.license_number }}
              <div style="font-size: 12px; color: #999">
                电话: {{ driver.phone }}
              </div>
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="分配类型" name="assignmentType">
          <a-radio-group v-model:value="formState.assignmentType">
            <a-radio value="primary">主要司机</a-radio>
            <a-radio value="temporary">临时司机</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item
          v-if="formState.assignmentType === 'temporary'"
          label="结束日期"
          name="endDate"
        >
          <a-date-picker
            v-model:value="formState.endDate"
            style="width: 100%"
            placeholder="选择结束日期"
            :disabled-date="disabledEndDate"
          />
        </a-form-item>

        <a-form-item>
          <a-space>
            <a-button type="primary" html-type="submit" :loading="submitting">
              确认分配
            </a-button>
            <a-button @click="handleCancel">取消</a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 当前分配信息 -->
    <a-card title="当前分配信息" style="margin-top: 16px" v-if="currentAssignments.length > 0">
      <a-table
        :columns="assignmentColumns"
        :data-source="currentAssignments"
        :pagination="false"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-popconfirm
              title="确定要解除这个分配吗？"
              @confirm="handleUnassign(record.id)"
            >
              <a-button type="link" danger size="small">解除分配</a-button>
            </a-popconfirm>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="record.status === 'active' ? 'green' : 'red'">
              {{ record.status === 'active' ? '活跃' : '已结束' }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'type'">
            <span>{{ record.assignment_type === 'primary' ? '主要' : '临时' }}</span>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'
import { assignDriverToVehicle, getVehicle, endDriverAssignment } from '@/api/vehicles'
import { getDrivers } from '@/api/drivers'
import type { Vehicle } from '@/types/vehicle'
import type { Driver } from '@/types/driver'

const route = useRoute()
const router = useRouter()
const vehicleId = Number(route.params.id)

const formState = reactive({
  driverId: null as number | null,
  assignmentType: 'primary' as 'primary' | 'temporary',
  endDate: null as Dayjs | null
})

const rules = {
  driverId: [{ required: true, message: '请选择司机' }],
  assignmentType: [{ required: true, message: '请选择分配类型' }],
  endDate: [{
    validator: (_: any, value: Dayjs | null) => {
      if (formState.assignmentType === 'temporary' && !value) {
        return Promise.reject(new Error('请选择结束日期'))
      }
      return Promise.resolve()
    }
  }]
}

const vehicle = ref<Vehicle | null>(null)
const availableDrivers = ref<Driver[]>([])
const driversLoading = ref(false)
const submitting = ref(false)
const currentAssignments = ref<any[]>([])

const assignmentColumns = [
  {
    title: '司机姓名',
    dataIndex: ['driver', 'name'],
    key: 'driver_name'
  },
  {
    title: '分配类型',
    dataIndex: 'assignment_type',
    key: 'type'
  },
  {
    title: '开始日期',
    dataIndex: 'start_date',
    key: 'start_date',
    customRender: ({ text }: any) => dayjs(text).format('YYYY-MM-DD')
  },
  {
    title: '结束日期',
    dataIndex: 'end_date',
    key: 'end_date',
    customRender: ({ text }: any) => text ? dayjs(text).format('YYYY-MM-DD') : '-'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status'
  },
  {
    title: '操作',
    key: 'action',
    width: 120
  }
]

const disabledEndDate = (current: Dayjs) => {
  return current && current < dayjs().startOf('day')
}

const filterDriverOption = (input: string, option: any) => {
  const driver = availableDrivers.value.find(d => d.id === option.value)
  if (!driver) return false
  return driver.name.toLowerCase().includes(input.toLowerCase()) ||
         driver.license_number.toLowerCase().includes(input.toLowerCase())
}

const fetchVehicleInfo = async () => {
  try {
    const data = await getVehicle(vehicleId)
    vehicle.value = data
    // 获取当前分配信息（这里假设车辆数据包含 assignments 字段）
    if (data.assignments) {
      currentAssignments.value = data.assignments
    }
  } catch (error) {
    message.error('获取车辆信息失败')
    console.error('Failed to fetch vehicle info:', error)
  }
}

const fetchAvailableDrivers = async () => {
  driversLoading.value = true
  try {
    const drivers = await getDrivers(0, 100)
    availableDrivers.value = drivers
  } catch (error) {
    message.error('获取司机列表失败')
    console.error('Failed to fetch drivers:', error)
  } finally {
    driversLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!formState.driverId) return
  
  submitting.value = true
  try {
    const endDate = formState.endDate ? formState.endDate.toDate() : undefined
    await assignDriverToVehicle(
      vehicleId,
      formState.driverId,
      formState.assignmentType,
      endDate
    )
    message.success('司机分配成功')
    router.push(`/vehicles/${vehicleId}`)
  } catch (error) {
    message.error('司机分配失败')
    console.error('Failed to assign driver:', error)
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  router.push(`/vehicles/${vehicleId}`)
}

const handleUnassign = async (assignmentId: number) => {
  try {
    await endDriverAssignment(vehicleId, assignmentId)
    message.success('分配已解除')
    fetchVehicleInfo()
  } catch (error) {
    message.error('解除分配失败')
    console.error('Failed to unassign driver:', error)
  }
}

onMounted(() => {
  fetchVehicleInfo()
  fetchAvailableDrivers()
})
</script>

<style scoped>
.assign-driver {
  padding: 24px;
}
</style>