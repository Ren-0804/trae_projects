<template>
  <div class="vehicle-list">
    <a-card title="车辆管理">
      <template #extra>
        <a-space>
          <a-input-search
            v-model:value="searchText"
            placeholder="搜索车辆"
            style="width: 200px"
            @search="handleSearch"
          />
          <router-link to="/vehicles/maintenance-reminders">
            <a-button type="default">维护提醒</a-button>
          </router-link>
          <router-link to="/vehicles/new">
            <a-button type="primary">新增车辆</a-button>
          </router-link>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="vehicles"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/vehicles/${record.id}`">
                <a-button type="link" size="small">详情</a-button>
              </router-link>
              <router-link :to="`/vehicles/${record.id}/edit`">
                <a-button type="link" size="small">编辑</a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这辆车吗？"
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
            <span v-if="record.current_driver">
              {{ record.current_driver.name }}
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
import { getVehicles, deleteVehicle } from '@/api/vehicles'
import type { Vehicle } from '@/types/vehicle'

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