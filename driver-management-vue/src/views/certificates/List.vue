<template>
  <div class="certificate-list">
    <a-card title="证书管理">
      <template #extra>
        <a-space>
          <a-input-search
            v-model:value="searchText"
            placeholder="搜索证书"
            style="width: 200px"
            @search="handleSearch"
          />
          <router-link to="/certificates/new">
            <a-button type="primary">新增证书</a-button>
          </router-link>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="certificates"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <router-link :to="`/certificates/${record.id}`">
                <a-button type="link" size="small">详情</a-button>
              </router-link>
              <a-popconfirm
                title="确定要删除这个证书吗？"
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
          <template v-else-if="column.key === 'expiry_status'">
            <a-tag :color="getExpiryColor(record)">
              {{ getExpiryText(record) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'driver'">
            <span v-if="record.driver">
              {{ record.driver.name }}
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
import { getCertificates, deleteCertificate } from '@/api/certificates'
import type { Certificate } from '@/types/certificate'
import dayjs from 'dayjs'

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
    const response = await getCertificates({
      page: pagination.value.current,
      page_size: pagination.value.pageSize,
      search: searchText.value
    })
    certificates.value = response.data
    pagination.value.total = response.total
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