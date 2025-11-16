<template>
  <div style="padding: 16px">
    <a-page-header title="编辑司机">
      <template #extra>
        <router-link :to="`/drivers/${route.params.id}`">
          <a-button>返回详情</a-button>
        </router-link>
      </template>
    </a-page-header>

    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-500">加载中...</div>
    </div>

    <div v-else-if="!driver && !loading" class="text-center py-8">
      <div class="text-red-500">司机信息加载失败</div>
      <router-link
        to="/drivers"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors mt-4"
      >
        返回列表
      </router-link>
    </div>

    <a-card v-else-if="driver">
      <a-form layout="vertical" :model="form" :rules="rules" ref="formRef">
        <a-descriptions bordered :column="2" size="middle">
          <a-descriptions-item label="姓名">
            <a-input v-model:value="form.name" placeholder="请输入司机姓名" />
          </a-descriptions-item>
          <a-descriptions-item label="电话">
            <a-input v-model:value="form.phone" placeholder="请输入手机号码" />
          </a-descriptions-item>
          <a-descriptions-item label="身份证号">
            <a-input v-model:value="form.id_card" placeholder="请输入身份证号" />
          </a-descriptions-item>
          <a-descriptions-item label="驾驶证号">
            <a-input v-model:value="form.license_number" placeholder="请输入驾驶证号" />
          </a-descriptions-item>
          <a-descriptions-item label="驾驶证类型">
            <a-select v-model:value="form.license_type" placeholder="请选择驾驶证类型">
              <a-select-option value="A1">A1</a-select-option>
              <a-select-option value="A2">A2</a-select-option>
              <a-select-option value="B1">B1</a-select-option>
              <a-select-option value="B2">B2</a-select-option>
              <a-select-option value="C1">C1</a-select-option>
              <a-select-option value="C2">C2</a-select-option>
            </a-select>
          </a-descriptions-item>
          <a-descriptions-item label="主要线路">
            <a-input v-model:value="form.main_route" placeholder="例如：北京-上海" />
          </a-descriptions-item>
          <a-descriptions-item label="车辆类型">
            <a-select v-model:value="form.vehicle_type" placeholder="请选择车辆类型">
              <a-select-option value="厢式货车">厢式货车</a-select-option>
              <a-select-option value="平板货车">平板货车</a-select-option>
              <a-select-option value="高栏货车">高栏货车</a-select-option>
              <a-select-option value="冷藏车">冷藏车</a-select-option>
              <a-select-option value="危险品运输车">危险品运输车</a-select-option>
            </a-select>
          </a-descriptions-item>
          <a-descriptions-item label="车长">
            <a-select v-model:value="form.vehicle_length" placeholder="请选择车长">
              <a-select-option value="4.2米">4.2米</a-select-option>
              <a-select-option value="6.8米">6.8米</a-select-option>
              <a-select-option value="9.6米">9.6米</a-select-option>
              <a-select-option value="13米">13米</a-select-option>
              <a-select-option value="17.5米">17.5米</a-select-option>
            </a-select>
          </a-descriptions-item>
          <a-descriptions-item label="每公里价格（元）">
            <a-input-number v-model:value="form.price_per_km" :min="0" :step="0.01" placeholder="请输入每公里价格" />
          </a-descriptions-item>
          <a-descriptions-item label="驾龄（年）">
            <a-input-number v-model:value="form.experience_years" :min="0" placeholder="请输入驾龄" />
          </a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-select v-model:value="form.status" placeholder="请选择状态">
              <a-select-option value="active">活跃</a-select-option>
              <a-select-option value="inactive">非活跃</a-select-option>
              <a-select-option value="blocked">已封禁</a-select-option>
            </a-select>
          </a-descriptions-item>
          <a-descriptions-item label="紧急联系人">
            <a-input v-model:value="form.emergency_contact" placeholder="请输入紧急联系人姓名" />
          </a-descriptions-item>
          <a-descriptions-item label="紧急联系电话">
            <a-input v-model:value="form.emergency_phone" placeholder="请输入紧急联系电话" />
          </a-descriptions-item>
        </a-descriptions>
        
        <a-descriptions bordered :column="1" size="middle" class="mt-4">
          <a-descriptions-item label="备注">
            <a-textarea v-model:value="form.remark" :rows="3" placeholder="请输入备注信息" />
          </a-descriptions-item>
        </a-descriptions>

        <div class="flex justify-end gap-4 mt-6">
          <router-link
            :to="`/drivers/${route.params.id}`"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            取消
          </router-link>
          <a-button type="primary" :loading="loading" @click="handleSubmit">保存</a-button>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import { useRoute, useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { toast } from 'sonner'
import type { Driver, DriverUpdate } from '@/api/drivers'

const route = useRoute()
const router = useRouter()
const driverStore = useDriverStore()

const loading = ref(false)
const driver = ref<Driver | null>(null)

const form = ref<DriverUpdate>({})

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
  emergency_phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的中国手机号' },
  ],
  remark: [
    {
      validator: (_rule: any, value: any) => {
        if (form.value.status === 'blocked' && (!value || String(value).trim() === '')) {
          return Promise.reject('封禁状态必须填写备注')
        }
        return Promise.resolve()
      },
    },
  ],
}

const fetchDriver = async () => {
  try {
    driver.value = await driverStore.fetchDriver(Number(route.params.id))
    if (driver.value) {
      // 使用对象展开来确保只包含有效的更新字段
      form.value = {
        name: driver.value.name || undefined,
        phone: driver.value.phone || undefined,
        id_card: driver.value.id_card || undefined,
        license_number: driver.value.license_number || undefined,
        license_type: driver.value.license_type || undefined,
        main_route: driver.value.main_route || undefined,
        vehicle_type: driver.value.vehicle_type || undefined,
        vehicle_length: driver.value.vehicle_length || undefined,
        price_per_km: driver.value.price_per_km || undefined,
        experience_years: driver.value.experience_years || undefined,
        status: driver.value.status || undefined,
        emergency_contact: driver.value.emergency_contact || undefined,
        emergency_phone: driver.value.emergency_phone || undefined,
        remark: driver.value.remark || undefined,
      }
    }
  } catch (error) {
    console.error('获取司机信息失败:', error)
    toast.error('获取司机信息失败')
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    await formRef.value?.validate()
    // 过滤掉空值和undefined值，只提交有实际值的字段
    const updateData: DriverUpdate = {}
    Object.keys(form.value).forEach((key) => {
      const value = form.value[key as keyof DriverUpdate]
      if (value !== undefined && value !== null && value !== '') {
        ;(updateData as any)[key] = value
      }
    })

    await driverStore.modifyDriver(Number(route.params.id), updateData)
    toast.success('司机信息更新成功')
    router.push(`/drivers/${route.params.id}`)
  } catch (error: unknown) {
    console.error('更新司机信息失败:', error)
    const errorMessage = error instanceof Error ? error.message : '未知错误'
    toast.error('更新失败: ' + errorMessage)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDriver()
})
</script>
