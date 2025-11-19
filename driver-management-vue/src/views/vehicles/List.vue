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
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
          ">车辆管理</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">管理所有车辆信息和维护状态</p>
        </div>
        <a-space>
          <router-link to="/vehicles/maintenance-reminders">
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
              <template #icon><ToolOutlined /></template>
              维护提醒
            </a-button>
          </router-link>
          <router-link to="/vehicles/new">
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
              新增车辆
            </a-button>
          </router-link>
        </a-space>
      </div>
    </div>

    <!-- Glassmorphism Search Card -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
      <a-input-search
        v-model:value="searchText"
        placeholder="搜索车牌号、车辆类型、品牌型号"
        style="
          width: 320px;
          border-radius: 12px;
          border: 1px solid rgba(0, 0, 0, 0.1);
          background: rgba(255, 255, 255, 0.7);
        "
        @search="handleSearch"
      >
        <template #prefix><SearchOutlined style="color: #9ca3af" /></template>
      </a-input-search>
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
        :data-source="vehicles"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        style="background: transparent;"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/vehicles/${record.id}`">
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
              <router-link :to="`/vehicles/${record.id}/edit`">
                <a-button 
                  type="text" 
                  style="
                    color: #10b981;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 500;
                  "
                >
                  <template #icon><EditOutlined /></template>
                  编辑
                </a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这辆车吗？"
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
            <span v-if="record.current_driver" style="font-weight: 500;">
              {{ record.current_driver.name }}
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
import { getVehicles, deleteVehicle } from '@/api/vehicles'
import type { Vehicle } from '@/types/vehicle'
import {
  PlusOutlined,
  ToolOutlined,
  SearchOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'

const loading = ref(false)
const searchText = ref('')
const vehicles = ref<Vehicle[]>([])
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
    title: '车牌号',
    dataIndex: 'plate_number',
    key: 'plate_number',
    sorter: true
  },
  {
    title: '车辆类型',
    dataIndex: 'vehicle_type',
    key: 'vehicle_type',
    sorter: true
  },
  {
    title: '品牌型号',
    dataIndex: 'brand_model',
    key: 'brand_model'
  },
  {
    title: '当前司机',
    key: 'driver',
    sorter: true
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    sorter: true
  },
  {
    title: '购买日期',
    dataIndex: 'purchase_date',
    key: 'purchase_date',
    sorter: true
  },
  {
    title: '操作',
    key: 'action',
    width: 200
  }
]

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'active': 'green',
    'maintenance': 'orange',
    'inactive': 'red',
    'retired': 'gray'
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'active': '正常',
    'maintenance': '维修中',
    'inactive': '停用',
    'retired': '报废'
  }
  return texts[status] || status
}

const fetchVehicles = async () => {
  loading.value = true
  try {
    const skip = (pagination.value.current - 1) * pagination.value.pageSize
    const vehiclesData = await getVehicles(
      skip,
      pagination.value.pageSize,
      undefined,
      searchText.value || undefined
    )
    vehicles.value = vehiclesData
    // For now, set total to current page size + 1 to indicate more pages might exist
    // In a real implementation, the backend should return total count
    pagination.value.total = vehiclesData.length + (vehiclesData.length === pagination.value.pageSize ? 1 : 0)
  } catch (error) {
    message.error('获取车辆列表失败')
    console.error('Failed to fetch vehicles:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.current = 1
  fetchVehicles()
}

const handleTableChange = (newPagination: any) => {
  pagination.value = { ...pagination.value, ...newPagination }
  fetchVehicles()
}

const handleDelete = async (id: number) => {
  try {
    await deleteVehicle(id)
    message.success('删除成功')
    fetchVehicles()
  } catch (error) {
    message.error('删除失败')
  }
}

onMounted(() => {
  fetchVehicles()
})
</script>

<style scoped>
.vehicle-list {
  padding: 24px;
}
</style>
