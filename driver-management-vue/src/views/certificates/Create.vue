<template>
  <div class="certificate-create">
    <a-card title="新增证书">
      <a-form
        :model="form"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 12 }"
        @finish="handleSubmit"
      >
        <a-form-item label="证书名称" name="certificate_name">
          <a-input v-model:value="form.certificate_name" placeholder="请输入证书名称" />
        </a-form-item>
        
        <a-form-item label="证书编号" name="certificate_number">
          <a-input v-model:value="form.certificate_number" placeholder="请输入证书编号" />
        </a-form-item>
        
        <a-form-item label="司机" name="driver_id">
          <a-select v-model:value="form.driver_id" placeholder="请选择司机">
            <a-select-option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="证书类型" name="certificate_type">
          <a-select v-model:value="form.certificate_type" placeholder="请选择证书类型">
            <a-select-option value="driver_license">驾驶证</a-select-option>
            <a-select-option value="transport_permit">运输许可证</a-select-option>
            <a-select-option value="dangerous_goods">危险品运输证</a-select-option>
            <a-select-option value="professional_qualification">从业资格证</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="颁发机构" name="issuing_authority">
          <a-input v-model:value="form.issuing_authority" placeholder="请输入颁发机构" />
        </a-form-item>
        
        <a-form-item label="颁发日期" name="issue_date">
          <a-date-picker v-model:value="form.issue_date" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="到期日期" name="expiry_date">
          <a-date-picker v-model:value="form.expiry_date" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="备注" name="notes">
          <a-textarea v-model:value="form.notes" placeholder="请输入备注信息" :rows="4" />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 6, span: 12 }">
          <a-space>
            <a-button type="primary" html-type="submit">提交</a-button>
            <router-link to="/certificates">
              <a-button>取消</a-button>
            </router-link>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { createCertificate } from '@/api/certificates'
import { getDrivers } from '@/api/drivers'
import type { CertificateCreateRequest } from '@/types/certificate'
import type { Driver } from '@/types/user'
import dayjs from 'dayjs'

const router = useRouter()

const form = ref<Partial<CertificateCreateRequest>>({
  certificate_name: '',
  certificate_number: '',
  driver_id: undefined,
  certificate_type: '',
  issuing_authority: '',
  issue_date: undefined,
  expiry_date: undefined,
  notes: ''
})

const drivers = ref<Driver[]>([])

const rules = {
  certificate_name: [{ required: true, message: '请输入证书名称' }],
  certificate_number: [{ required: true, message: '请输入证书编号' }],
  driver_id: [{ required: true, message: '请选择司机' }],
  certificate_type: [{ required: true, message: '请选择证书类型' }],
  issuing_authority: [{ required: true, message: '请输入颁发机构' }],
  issue_date: [{ required: true, message: '请选择颁发日期' }],
  expiry_date: [{ required: true, message: '请选择到期日期' }]
}

const fetchDrivers = async () => {
  try {
    const response = await getDrivers({ page_size: 100 })
    drivers.value = response.data
  } catch (error) {
    message.error('获取司机列表失败')
  }
}

const handleSubmit = async () => {
  try {
    const submitData = {
      ...form.value,
      issue_date: form.value.issue_date ? dayjs(form.value.issue_date).toDate() : undefined,
      expiry_date: form.value.expiry_date ? dayjs(form.value.expiry_date).toDate() : undefined
    }
    
    await createCertificate(submitData as CertificateCreateRequest)
    message.success('证书创建成功')
    router.push('/certificates')
  } catch (error) {
    message.error('创建失败，请重试')
  }
}

onMounted(() => {
  fetchDrivers()
})
</script>

<style scoped>
.certificate-create {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}
</style>