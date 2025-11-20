<template>
  <div class="page-container">
    <!-- Glassmorphism Header -->
    <div class="page-header glass-panel">
      <div class="header-content">
        <div class="header-title-wrapper">
          <h1 class="page-title text-gradient">证书管理</h1>
          <p class="page-subtitle">管理司机证书和到期提醒</p>
        </div>
        <a-space>
          <a-input-search
            v-model:value="searchText"
            placeholder="搜索证书名称、编号或持证人"
            class="custom-search-input"
            @search="handleSearch"
          >
            <template #prefix><SearchOutlined class="input-icon" /></template>
          </a-input-search>
          <router-link to="/certificates/new">
            <a-button type="primary" size="large" class="action-btn">
              <template #icon><PlusOutlined /></template>
              新增证书
            </a-button>
          </router-link>
        </a-space>
      </div>
    </div>

    <!-- Glassmorphism Table Card -->
    <div class="table-card glass-panel">
      <a-table
        :columns="columns"
        :data-source="certificates"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        class="custom-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/certificates/${record.id}`">
                <a-button type="text" class="action-link view">
                  <template #icon><EyeOutlined /></template>
                  详情
                </a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这个证书吗？"
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
          <template v-else-if="column.key === 'expiry_status'">
            <a-tag 
              :color="getExpiryColor(record)"
              class="status-tag"
            >
              {{ getExpiryText(record) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver" class="driver-name">
              {{ record.driver.name }}
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
import { getCertificates, deleteCertificate } from '@/api/certificates'
import type { Certificate } from '@/types/certificate'
import dayjs from 'dayjs'
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'

const loading = ref(false)
const searchText = ref('')
const certificates = ref<Certificate[]>([])
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
    title: '证书名称',
    dataIndex: 'certificate_name',
    key: 'certificate_name',
    sorter: true
  },
  {
    title: '证书编号',
    dataIndex: 'certificate_number',
    key: 'certificate_number',
    sorter: true
  },
  {
    title: '持证人',
    key: 'driver',
    sorter: true
  },
  {
    title: '颁发机构',
    dataIndex: 'issuing_authority',
    key: 'issuing_authority'
  },
  {
    title: '颁发日期',
    dataIndex: 'issue_date',
    key: 'issue_date',
    sorter: true
  },
  {
    title: '到期日期',
    dataIndex: 'expiry_date',
    key: 'expiry_date',
    sorter: true
  },
  {
    title: '到期状态',
    key: 'expiry_status'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    sorter: true
  },
  {
    title: '操作',
    key: 'action',
    width: 150
  }
]

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'active': 'green',
    'expired': 'red',
    'revoked': 'gray',
    'pending': 'orange'
  }
  return colors[status] || 'default'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    'active': '有效',
    'expired': '已过期',
    'revoked': '已吊销',
    'pending': '待审核'
  }
  return texts[status] || status
}

const getExpiryColor = (record: Certificate) => {
  if (!record.expiry_date) return 'default'
  
  const expiryDate = dayjs(record.expiry_date)
  const now = dayjs()
  const daysDiff = expiryDate.diff(now, 'days')
  
  if (daysDiff < 0) return 'red'
  if (daysDiff <= 30) return 'orange'
  if (daysDiff <= 90) return 'gold'
  return 'green'
}

const getExpiryText = (record: Certificate) => {
  if (!record.expiry_date) return '无到期日期'
  
  const expiryDate = dayjs(record.expiry_date)
  const now = dayjs()
  const daysDiff = expiryDate.diff(now, 'days')
  
  if (daysDiff < 0) return '已过期'
  if (daysDiff === 0) return '今天到期'
  if (daysDiff <= 30) return `${daysDiff}天后到期`
  if (daysDiff <= 90) return '即将到期'
  return '正常'
}

const fetchCertificates = async () => {
  loading.value = true
  try {
    const skip = (pagination.value.current - 1) * pagination.value.pageSize
    const certificatesData = await getCertificates(
      skip,
      pagination.value.pageSize,
      undefined,
      undefined,
      undefined,
      false,
      30
    )
    certificates.value = certificatesData
    // For now, set total to current length since API doesn't return total
    // In a real app, you'd want to add a count endpoint
    pagination.value.total = certificatesData.length + (pagination.value.current * pagination.value.pageSize)
  } catch (error) {
    message.error('获取证书列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.current = 1
  fetchCertificates()
}

const handleTableChange = (newPagination: any) => {
  pagination.value = { ...pagination.value, ...newPagination }
  fetchCertificates()
}

const handleDelete = async (id: number) => {
  try {
    await deleteCertificate(id)
    message.success('删除成功')
    fetchCertificates()
  } catch (error) {
    message.error('删除失败')
  }
}

onMounted(() => {
  fetchCertificates()
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

.custom-search-input {
  width: 280px;
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
.action-link.delete { color: var(--color-error); }

.action-link:hover {
  background: rgba(0, 0, 0, 0.05);
}
</style>
