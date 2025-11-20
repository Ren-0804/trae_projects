<template>
  <div class="page-container">
    <!-- Glassmorphism Header -->
    <div class="page-header glass-panel">
      <div class="header-content">
        <div class="header-title-wrapper">
          <h1 class="page-title text-gradient">车辆管理</h1>
          <p class="page-subtitle">管理所有车辆信息和维护状态</p>
        </div>
        <a-space>
          <router-link to="/vehicles/maintenance-reminders">
            <a-button size="large" class="action-btn-secondary">
              <template #icon><ToolOutlined /></template>
              维护提醒
            </a-button>
          </router-link>
          <router-link to="/vehicles/new">
            <a-button type="primary" size="large" class="action-btn">
              <template #icon><PlusOutlined /></template>
              新增车辆
            </a-button>
          </router-link>
        </a-space>
      </div>
    </div>

    <!-- Glassmorphism Search Card -->
    <div class="search-card glass-panel">
      <a-input-search
        v-model:value="searchText"
        placeholder="搜索车牌号、车辆类型、品牌型号"
        class="custom-search-input"
        @search="handleSearch"
      >
        <template #prefix><SearchOutlined class="input-icon" /></template>
      </a-input-search>
    </div>

    <!-- Glassmorphism Table Card -->
    <div class="table-card glass-panel">
      <a-table
        :columns="columns"
        :data-source="vehicles"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/vehicles/${record.id}`">
                <a-button type="text" class="action-link view">
                  <template #icon><EyeOutlined /></template>
                  详情
                </a-button>
              </router-link>
              <router-link :to="`/vehicles/${record.id}/edit`">
                <a-button type="text" class="action-link edit">
                  <template #icon><EditOutlined /></template>
                  编辑
                </a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这辆车吗？"
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
            <span v-if="record.current_driver" class="driver-name">
              {{ record.current_driver.name }}
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

.search-card {
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
}

.custom-search-input {
  width: 320px;
  border-radius: var(--radius-base);
}

:deep(.ant-input-search .ant-input) {
  border-radius: var(--radius-base) !important;
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
.action-link.edit { color: var(--color-success); }
.action-link.delete { color: var(--color-error); }

.action-link:hover {
  background: rgba(0, 0, 0, 0.05);
}
</style>
