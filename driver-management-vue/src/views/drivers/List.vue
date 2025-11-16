<template>
  <div style="padding: 16px">
    <a-page-header title="司机列表">
      <template #extra>
        <router-link to="/drivers/new">
          <a-button type="primary">新增司机</a-button>
        </router-link>
      </template>
    </a-page-header>

    <a-space style="margin-bottom: 16px">
      <a-input
        v-model:value="searchKeyword"
        placeholder="搜索姓名、电话、线路"
        style="width: 280px"
      />
      <a-select v-model:value="selectedStatus" style="width: 160px" allowClear placeholder="状态">
        <a-select-option value="active">活跃</a-select-option>
        <a-select-option value="inactive">非活跃</a-select-option>
        <a-select-option value="blocked">已封禁</a-select-option>
      </a-select>
      <a-button type="primary" @click="handleSearch">搜索</a-button>
    </a-space>

    <a-table :dataSource="drivers" :columns="columns" :rowKey="'id'" bordered>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="statusColor(record.status)">{{ getStatusText(record.status) }}</a-tag>
        </template>
        <template v-else-if="column.key === 'actions'">
          <a-space>
            <router-link :to="`/drivers/${record.id}`">
              <a-button type="link">查看</a-button>
            </router-link>
            <a-button type="link" @click="handleEdit(record.id)">编辑</a-button>
            <a-button danger type="link" @click="handleDelete(record.id)">删除</a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <div
      style="margin-top: 16px; display: flex; justify-content: space-between; align-items: center"
    >
      <div>共 {{ total }} 条记录，当前第 {{ currentPage }} 页</div>
      <a-pagination
        :current="currentPage"
        :total="total"
        :pageSize="pageSize"
        @change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { message, Modal } from 'ant-design-vue'

const router = useRouter()
const driverStore = useDriverStore()

const searchKeyword = ref('')
const selectedStatus = ref('')

const drivers = computed(() => driverStore.drivers)
const total = computed(() => driverStore.total)
const currentPage = computed(() => driverStore.currentPage)

const pageSize = computed(() => driverStore.pageSize)

const getStatusText = (status: string) => {
  switch (status) {
    case 'active':
      return '活跃'
    case 'inactive':
      return '非活跃'
    case 'blocked':
      return '已封禁'
    default:
      return '未知'
  }
}

const fetchDrivers = async () => {
  try {
    await driverStore.fetchDrivers({
      keyword: searchKeyword.value || undefined,
      status: selectedStatus.value || undefined,
    })
  } catch (error) {
    message.error('获取司机列表失败')
    console.error('获取司机列表失败:', error)
  }
}

const handleSearch = () => {
  driverStore.setPage(1)
  fetchDrivers()
}

const handlePageChange = (page: number) => {
  driverStore.setPage(page)
  fetchDrivers()
}

const handleEdit = (id: number) => {
  router.push(`/drivers/${id}`)
}

const handleDelete = async (id: number) => {
  Modal.confirm({
    title: '确认删除',
    content: '删除后不可恢复，是否继续？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    async onOk() {
      try {
        await driverStore.removeDriver(id)
        message.success('司机删除成功')
      } catch (error) {
        message.error('删除司机失败')
        console.error('删除司机失败:', error)
      }
    },
  })
}

// 监听搜索条件变化
watch([searchKeyword, selectedStatus], () => {
  handleSearch()
})

onMounted(() => {
  fetchDrivers()
})

const columns = [
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '电话', dataIndex: 'phone', key: 'phone' },
  { title: '身份证号', dataIndex: 'id_card', key: 'id_card' },
  { title: '驾驶证号', dataIndex: 'license_number', key: 'license_number' },
  { title: '主要线路', dataIndex: 'main_route', key: 'main_route' },
  { title: '车辆类型', dataIndex: 'vehicle_type', key: 'vehicle_type' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'actions' },
]

const statusColor = (status: string) => {
  switch (status) {
    case 'active':
      return 'green'
    case 'inactive':
      return 'default'
    case 'blocked':
      return 'red'
    default:
      return 'default'
  }
}
</script>
