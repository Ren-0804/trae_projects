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
            -webkit-text-fill-color: transparent;
            margin: 0;
          ">证书管理</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">管理司机证书和到期提醒</p>
        </div>
        <a-space>
          <a-input-search
            v-model:value="searchText"
            placeholder="搜索证书名称、编号或持证人"
            style="
              width: 280px;
              border-radius: 12px;
              border: 1px solid rgba(0, 0, 0, 0.1);
              background: rgba(255, 255, 255, 0.7);
            "
            @search="handleSearch"
          >
            <template #prefix><SearchOutlined style="color: #9ca3af" /></template>
          </a-input-search>
          <router-link to="/certificates/new">
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
              新增证书
            </a-button>
          </router-link>
        </a-space>
      </div>
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
        :data-source="certificates"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
        style="background: transparent;"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/certificates/${record.id}`">
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
              <a-popconfirm
                title="确定要删除这个证书吗？"
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
          <template v-else-if="column.key === 'expiry_status'">
            <a-tag 
              :color="getExpiryColor(record)"
              style="border-radius: 20px; padding: 4px 12px; font-weight: 500;"
            >
              {{ getExpiryText(record) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver" style="font-weight: 500;">
              {{ record.driver.name }}
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
.certificate-list {
  padding: 24px;
}
</style>