<template>
  <div class="page-container">
    <!-- Glassmorphism Header -->
    <div class="page-header glass-panel">
      <div class="header-content">
        <div class="header-title-wrapper">
          <h1 class="page-title text-gradient">司机管理</h1>
          <p class="page-subtitle">管理所有司机信息和状态</p>
        </div>
        <router-link to="/drivers/new">
          <a-button type="primary" size="large" class="action-btn">
            <template #icon><PlusOutlined /></template>
            新增司机
          </a-button>
        </router-link>
      </div>
    </div>

    <!-- Glassmorphism Search Card -->
    <div class="search-card glass-panel">
      <a-space class="search-space" wrap>
        <a-input
          v-model:value="searchKeyword"
          placeholder="搜索姓名、电话、线路"
          class="custom-input"
        >
          <template #prefix><SearchOutlined class="input-icon" /></template>
        </a-input>
        <a-select 
          v-model:value="selectedStatus" 
          class="custom-select"
          allowClear 
          placeholder="状态筛选"
        >
          <a-select-option value="active">活跃</a-select-option>
          <a-select-option value="inactive">非活跃</a-select-option>
          <a-select-option value="blocked">已封禁</a-select-option>
        </a-select>
        <a-button type="primary" @click="handleSearch" class="search-btn">
          <template #icon><SearchOutlined /></template>
          搜索
        </a-button>
      </a-space>
    </div>

    <!-- Glassmorphism Table Card -->
    <div class="table-card glass-panel">
      <a-table 
        :dataSource="drivers" 
        :columns="columns" 
        :rowKey="'id'" 
        :pagination="false"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag 
              :color="statusColor(record.status)"
              class="status-tag"
            >
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'actions'">
            <a-space>
              <router-link :to="`/drivers/${record.id}`">
                <a-button type="text" class="action-link view">
                  <template #icon><EyeOutlined /></template>
                  查看
                </a-button>
              </router-link>
              <a-button type="text" @click="handleEdit(record.id)" class="action-link edit">
                <template #icon><EditOutlined /></template>
                编辑
              </a-button>
              <a-popconfirm
                title="确认删除此司机？"
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
        </template>
      </a-table>

      <div class="pagination-wrapper">
        <div class="pagination-info">
          共 <span class="highlight">{{ total }}</span> 条记录，当前第 <span class="highlight">{{ currentPage }}</span> 页
        </div>
        <a-pagination
          :current="currentPage"
          :total="total"
          :pageSize="pageSize"
          @change="handlePageChange"
          :showSizeChanger="false"
          :showQuickJumper="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { message, Modal } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'

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
  router.push(`/drivers/${id}/edit`)
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

.search-card {
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
}

.search-space {
  width: 100%;
}

.custom-input {
  width: 280px;
  border-radius: var(--radius-base);
}

.custom-select {
  width: 160px;
}

:deep(.ant-select-selector) {
  border-radius: var(--radius-base) !important;
}

.search-btn {
  border-radius: var(--radius-base);
  height: 32px;
  font-weight: 600;
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

.pagination-wrapper {
  padding: var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.3);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.pagination-info {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.highlight {
  font-weight: 600;
  color: var(--color-text-primary);
}
</style>
