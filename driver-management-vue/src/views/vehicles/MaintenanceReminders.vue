<template>
  <div class="maintenance-reminders">
    <a-card title="维护提醒">
      <template #extra>
        <a-space>
          <a-select v-model:value="daysAhead" style="width: 120px" @change="fetchReminders">
            <a-select-option :value="7">7天内</a-select-option>
            <a-select-option :value="15">15天内</a-select-option>
            <a-select-option :value="30">30天内</a-select-option>
            <a-select-option :value="60">60天内</a-select-option>
          </a-select>
          <a-button type="primary" @click="fetchReminders">刷新</a-button>
        </a-space>
      </template>

      <a-row :gutter="16">
        <a-col :span="8">
          <a-statistic
            title="即将到期维护"
            :value="maintenanceReminders.length"
            :value-style="{ color: '#cf1322' }"
          >
            <template #prefix>
              <ToolOutlined />
            </template>
          </a-statistic>
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="即将到期保险"
            :value="insuranceReminders.length"
            :value-style="{ color: '#fa8c16' }"
          >
            <template #prefix>
              <SafetyOutlined />
            </template>
          </a-statistic>
        </a-col>
        <a-col :span="8">
          <a-statistic
            title="紧急提醒"
            :value="urgentReminders.length"
            :value-style="{ color: '#f5222d' }"
          >
            <template #prefix>
              <AlertOutlined />
            </template>
          </a-statistic>
        </a-col>
      </a-row>

      <a-divider />

      <!-- 维护提醒列表 -->
      <h3>维护提醒</h3>
      <a-table
        :columns="maintenanceColumns"
        :data-source="maintenanceReminders"
        :loading="loading"
        :pagination="false"
        row-key="vehicle_id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'vehicle'">
            <router-link :to="`/vehicles/${record.vehicle_id}`">
              {{ record.plate_number }}
            </router-link>
          </template>
          <template v-else-if="column.key === 'urgency'">
            <a-tag :color="getUrgencyColor(record.urgency)">
              {{ getUrgencyText(record.urgency) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'days_until'">
            <span :style="{ color: getDaysColor(record.days_until_maintenance) }">
              {{ record.days_until_maintenance }} 天
            </span>
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/vehicles/${record.vehicle_id}/maintenance-records/new`">
                <a-button type="link" size="small">添加维护记录</a-button>
              </router-link>
              <a-button type="link" size="small" @click="scheduleMaintenance(record)">
                安排维护
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>

      <a-divider />

      <!-- 保险提醒列表 -->
      <h3>保险提醒</h3>
      <a-table
        :columns="insuranceColumns"
        :data-source="insuranceReminders"
        :loading="loading"
        :pagination="false"
        row-key="vehicle_id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'vehicle'">
            <router-link :to="`/vehicles/${record.vehicle_id}`">
              {{ record.plate_number }}
            </router-link>
          </template>
          <template v-else-if="column.key === 'urgency'">
            <a-tag :color="getUrgencyColor(record.urgency)">
              {{ getUrgencyText(record.urgency) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'days_until'">
            <span :style="{ color: getDaysColor(record.days_until_expiry) }">
              {{ record.days_until_expiry }} 天
            </span>
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="renewInsurance(record)">
                续保提醒
              </a-button>
              <a-button type="link" size="small" @click="markInsuranceRenewed(record)">
                标记已续保
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { ToolOutlined, SafetyOutlined, AlertOutlined } from '@ant-design/icons-vue'
import { getUpcomingMaintenance, getExpiringInsurance } from '@/api/vehicles'

const loading = ref(false)
const daysAhead = ref(30)
const maintenanceReminders = ref<any[]>([])
const insuranceReminders = ref<any[]>([])

const maintenanceColumns = [
  {
    title: '车辆',
    key: 'vehicle',
    width: 150
  },
  {
    title: '维护到期日期',
    dataIndex: 'maintenance_due_date',
    key: 'due_date',
    width: 120,
    customRender: ({ text }: any) => new Date(text).toLocaleDateString()
  },
  {
    title: '剩余天数',
    key: 'days_until',
    width: 100
  },
  {
    title: '紧急程度',
    key: 'urgency',
    width: 100
  },
  {
    title: '操作',
    key: 'action',
    width: 200
  }
]

const insuranceColumns = [
  {
    title: '车辆',
    key: 'vehicle',
    width: 150
  },
  {
    title: '保险到期日期',
    dataIndex: 'insurance_expiry',
    key: 'due_date',
    width: 120,
    customRender: ({ text }: any) => new Date(text).toLocaleDateString()
  },
  {
    title: '剩余天数',
    key: 'days_until',
    width: 100
  },
  {
    title: '紧急程度',
    key: 'urgency',
    width: 100
  },
  {
    title: '操作',
    key: 'action',
    width: 200
  }
]

const urgentReminders = ref<any[]>([])

const getUrgencyColor = (urgency: string) => {
  const colors: Record<string, string> = {
    'high': 'red',
    'medium': 'orange',
    'low': 'green'
  }
  return colors[urgency] || 'default'
}

const getUrgencyText = (urgency: string) => {
  const texts: Record<string, string> = {
    'high': '紧急',
    'medium': '中等',
    'low': '一般'
  }
  return texts[urgency] || urgency
}

const getDaysColor = (days: number) => {
  if (days <= 3) return '#f5222d'
  if (days <= 7) return '#fa8c16'
  if (days <= 14) return '#faad14'
  return '#52c41a'
}

const fetchReminders = async () => {
  loading.value = true
  try {
    const [maintenanceResponse, insuranceResponse] = await Promise.all([
      getUpcomingMaintenance(daysAhead.value),
      getExpiringInsurance(daysAhead.value)
    ])
    
    maintenanceReminders.value = maintenanceResponse
    insuranceReminders.value = insuranceResponse
    
    // 计算紧急提醒
    urgentReminders.value = [
      ...maintenanceResponse.filter((item: any) => item.urgency === 'high'),
      ...insuranceResponse.filter((item: any) => item.urgency === 'high')
    ]
    
    if (urgentReminders.value.length > 0) {
      message.warning(`有 ${urgentReminders.value.length} 项紧急提醒需要处理`)
    }
  } catch (error) {
    message.error('获取提醒信息失败')
    console.error('Failed to fetch reminders:', error)
  } finally {
    loading.value = false
  }
}

const scheduleMaintenance = (record: any) => {
  message.info(`安排车辆 ${record.plate_number} 的维护`)
  // 这里可以跳转到维护安排页面或打开对话框
}

const renewInsurance = (record: any) => {
  message.info(`提醒车辆 ${record.plate_number} 续保`)
  // 这里可以发送续保提醒通知
}

const markInsuranceRenewed = (record: any) => {
  message.info(`标记车辆 ${record.plate_number} 已续保`)
  // 这里可以更新保险到期日期
}

onMounted(() => {
  fetchReminders()
})
</script>

<style scoped>
.maintenance-reminders {
  padding: 24px;
}
</style>