<template>
  <div class="certificate-detail">
    <a-card title="证书详情">
      <template #extra>
        <router-link :to="`/certificates/${certificateId}/edit`">
          <a-button type="primary">编辑</a-button>
        </router-link>
      </template>
      
      <a-descriptions bordered :column="2">
        <a-descriptions-item label="证书名称">{{ certificate?.certificate_name }}</a-descriptions-item>
        <a-descriptions-item label="证书编号">{{ certificate?.certificate_number }}</a-descriptions-item>
        <a-descriptions-item label="持证人">{{ certificate?.driver?.name }}</a-descriptions-item>
        <a-descriptions-item label="证书类型">{{ getCertificateTypeText(certificate?.certificate_type) }}</a-descriptions-item>
        <a-descriptions-item label="颁发机构">{{ certificate?.issuing_authority }}</a-descriptions-item>
        <a-descriptions-item label="颁发日期">{{ certificate?.issue_date }}</a-descriptions-item>
        <a-descriptions-item label="到期日期">{{ certificate?.expiry_date }}</a-descriptions-item>
        <a-descriptions-item label="状态">
          <a-tag :color="getStatusColor(certificate?.status)">
            {{ getStatusText(certificate?.status) }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="备注" :span="2">{{ certificate?.notes || '无' }}</a-descriptions-item>
      </a-descriptions>
      
      <a-divider />
      
      <h3>证书文件</h3>
      <div v-if="certificate?.file_path" class="certificate-file">
        <a-button type="link" @click="downloadCertificate">
          <DownloadOutlined />
          下载证书文件
        </a-button>
      </div>
      <div v-else class="no-file">
        <a-empty description="暂无证书文件" />
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { DownloadOutlined } from '@ant-design/icons-vue'
import { getCertificate } from '@/api/certificates'
import type { Certificate } from '@/types/certificate'

const route = useRoute()
const certificateId = Number(route.params.id)

const loading = ref(false)
const certificate = ref<Certificate | null>(null)

const getCertificateTypeText = (type: string | undefined) => {
  const texts: Record<string, string> = {
    'driver_license': '驾驶证',
    'transport_permit': '运输许可证',
    'dangerous_goods': '危险品运输证',
    'professional_qualification': '从业资格证'
  }
  return type ? (texts[type] || type) : ''
}

const getStatusColor = (status: string | undefined) => {
  const colors: Record<string, string> = {
    'active': 'green',
    'expired': 'red',
    'revoked': 'gray',
    'pending': 'orange'
  }
  return status ? (colors[status] || 'default') : 'default'
}

const getStatusText = (status: string | undefined) => {
  const texts: Record<string, string> = {
    'active': '有效',
    'expired': '已过期',
    'revoked': '已吊销',
    'pending': '待审核'
  }
  return status ? (texts[status] || status) : ''
}

const downloadCertificate = () => {
  if (certificate.value?.file_path) {
    window.open(certificate.value.file_path, '_blank')
  }
}

const fetchCertificate = async () => {
  loading.value = true
  try {
    const response = await getCertificate(certificateId)
    certificate.value = response
  } catch (error) {
    message.error('获取证书信息失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCertificate()
})
</script>

<style scoped>
.certificate-detail {
  padding: 24px;
}

.certificate-file {
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  text-align: center;
}

.no-file {
  padding: 32px;
  text-align: center;
}
</style>