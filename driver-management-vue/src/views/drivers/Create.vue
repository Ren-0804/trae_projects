<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">新增司机</h1>
      <router-link
        to="/drivers"
        class="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
      >
        ← 返回列表
      </router-link>
    </div>

    <a-form layout="vertical" :model="form" :rules="rules" ref="formRef" @submit.prevent>
      <div class="bg-white rounded-lg shadow p-6 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <a-form-item name="name" label="姓名" required>
            <a-input v-model:value="form.name" placeholder="请输入司机姓名" />
          </a-form-item>

          <a-form-item name="phone" label="电话" required>
            <a-input v-model:value="form.phone" placeholder="请输入手机号码" />
          </a-form-item>

          <a-form-item name="id_card" label="身份证号" required>
            <a-input v-model:value="form.id_card" placeholder="请输入身份证号" />
          </a-form-item>

          <a-form-item name="license_number" label="驾驶证号" required>
            <a-input v-model:value="form.license_number" placeholder="请输入驾驶证号" />
          </a-form-item>

          <a-form-item name="license_type" label="驾驶证类型" required>
            <a-select v-model:value="form.license_type" placeholder="请选择驾驶证类型">
              <a-select-option value="A1">A1</a-select-option>
              <a-select-option value="A2">A2</a-select-option>
              <a-select-option value="B1">B1</a-select-option>
              <a-select-option value="B2">B2</a-select-option>
              <a-select-option value="C1">C1</a-select-option>
              <a-select-option value="C2">C2</a-select-option>
            </a-select>
          </a-form-item>

          <a-form-item name="main_route" label="主要线路" required>
            <a-input v-model:value="form.main_route" placeholder="例如：北京-上海" />
          </a-form-item>

          <a-form-item name="vehicle_type" label="车辆类型" required>
            <a-select v-model:value="form.vehicle_type" placeholder="请选择车辆类型">
              <a-select-option value="厢式货车">厢式货车</a-select-option>
              <a-select-option value="平板货车">平板货车</a-select-option>
              <a-select-option value="高栏货车">高栏货车</a-select-option>
              <a-select-option value="冷藏车">冷藏车</a-select-option>
              <a-select-option value="危险品运输车">危险品运输车</a-select-option>
            </a-select>
          </a-form-item>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">车长</label>
            <select
              v-model="form.vehicle_length"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">请选择车长</option>
              <option value="4.2米">4.2米</option>
              <option value="6.8米">6.8米</option>
              <option value="9.6米">9.6米</option>
              <option value="13米">13米</option>
              <option value="17.5米">17.5米</option>
            </select>
          </div>

          <a-form-item name="price_per_km" label="每公里价格（元)">
            <a-input-number v-model:value="form.price_per_km" :min="0" :step="0.01" style="width:100%" />
          </a-form-item>

          <a-form-item name="experience_years" label="驾龄（年）">
            <a-input-number v-model:value="form.experience_years" :min="0" style="width:100%" />
          </a-form-item>

          <a-form-item name="emergency_contact" label="紧急联系人">
            <a-input v-model:value="form.emergency_contact" placeholder="请输入紧急联系人姓名" />
          </a-form-item>

          <a-form-item name="emergency_phone" label="紧急联系电话">
            <a-input v-model:value="form.emergency_phone" placeholder="请输入紧急联系电话" />
          </a-form-item>
        </div>

          <a-form-item name="remark" label="备注">
            <a-textarea v-model:value="form.remark" rows="3" placeholder="请输入备注信息" />
          </a-form-item>

        <div class="flex justify-end gap-4">
          <router-link
            to="/drivers"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            取消
          </router-link>
          <a-button type="primary" :loading="loading" @click="handleSubmit">保存</a-button>
        </div>
      </div>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { message } from 'ant-design-vue'

const router = useRouter()
const driverStore = useDriverStore()

const loading = ref(false)
const formRef = ref<FormInstance>()
const rules: Record<string, Rule[]> = {
  name: [{ required: true, message: '请输入姓名' }],
  phone: [
    { required: true, message: '请输入手机号码' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的中国手机号' },
  ],
  id_card: [
    { required: true, message: '请输入身份证号' },
    { pattern: /^\d{17}[\dXx]$/, message: '身份证号格式不正确' },
  ],
  license_number: [{ required: true, message: '请输入驾驶证号' }],
  license_type: [{ required: true, message: '请选择驾驶证类型' }],
  main_route: [{ required: true, message: '请输入主要线路' }],
  vehicle_type: [{ required: true, message: '请选择车辆类型' }],
  status: [{ required: true, message: '请选择状态' }],
  emergency_phone: [{ pattern: /^1[3-9]\d{9}$/, message: '紧急电话格式不正确' }],
}

const form = ref({
  name: '',
  phone: '',
  id_card: '',
  license_number: '',
  license_type: '',
  main_route: '',
  vehicle_type: '',
  vehicle_length: '',
  price_per_km: 0,
  experience_years: 0,
  status: 'active' as const,
  emergency_contact: '',
  emergency_phone: '',
  remark: '',
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await formRef.value?.validate()
  } catch {
    loading.value = false
    return
  }
  try {
    await driverStore.addDriver(form.value)
    message.success('司机信息保存成功')
    router.push('/drivers')
  } catch (error: any) {
    message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}
</script>
