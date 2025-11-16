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

    <form @submit.prevent="handleSubmit" class="max-w-2xl">
      <div class="bg-white rounded-lg shadow p-6 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">姓名 *</label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入司机姓名"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">电话 *</label>
            <input
              v-model="form.phone"
              type="tel"
              required
              pattern="^1[3-9]\\d{9}$"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入手机号码"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">身份证号 *</label>
            <input
              v-model="form.id_card"
              type="text"
              required
              pattern="^\\d{17}[\\dXx]$"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入身份证号"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">驾驶证号 *</label>
            <input
              v-model="form.license_number"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入驾驶证号"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">驾驶证类型 *</label>
            <select
              v-model="form.license_type"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">请选择驾驶证类型</option>
              <option value="A1">A1</option>
              <option value="A2">A2</option>
              <option value="B1">B1</option>
              <option value="B2">B2</option>
              <option value="C1">C1</option>
              <option value="C2">C2</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">主要线路 *</label>
            <input
              v-model="form.main_route"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="例如：北京-上海"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">车辆类型 *</label>
            <select
              v-model="form.vehicle_type"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">请选择车辆类型</option>
              <option value="厢式货车">厢式货车</option>
              <option value="平板货车">平板货车</option>
              <option value="高栏货车">高栏货车</option>
              <option value="冷藏车">冷藏车</option>
              <option value="危险品运输车">危险品运输车</option>
            </select>
          </div>
          
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
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">每公里价格（元）</label>
            <input
              v-model.number="form.price_per_km"
              type="number"
              step="0.01"
              min="0"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入每公里价格"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">驾龄（年）</label>
            <input
              v-model.number="form.experience_years"
              type="number"
              min="0"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入驾龄"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">紧急联系人</label>
            <input
              v-model="form.emergency_contact"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入紧急联系人姓名"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">紧急联系电话</label>
            <input
              v-model="form.emergency_phone"
              type="tel"
              pattern="^1[3-9]\\d{9}$"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="请输入紧急联系电话"
            />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
          <textarea
            v-model="form.remark"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="请输入备注信息"
          ></textarea>
        </div>
        
        <div class="flex justify-end gap-4">
          <router-link
            to="/drivers"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            取消
          </router-link>
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { toast } from 'sonner'

const router = useRouter()
const driverStore = useDriverStore()

const loading = ref(false)

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
  remark: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await driverStore.addDriver(form.value)
    toast.success('司机信息保存成功')
    router.push('/drivers')
  } catch (error: any) {
    console.error('保存司机信息失败:', error)
    toast.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}
</script>