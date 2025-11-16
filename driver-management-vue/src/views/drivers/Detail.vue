<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">司机详情</h1>
      <router-link
        to="/drivers"
        class="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
      >
        ← 返回列表
      </router-link>
    </div>

    <div v-if="driver" class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">基本信息</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-500">姓名</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.name }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">电话</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.phone }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">身份证号</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.id_card }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">驾驶证号</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.license_number }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">驾驶证类型</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.license_type }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">紧急联系人</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.emergency_contact || '-' }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">紧急联系电话</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.emergency_phone || '-' }}</p>
            </div>
          </div>
        </div>
        
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">车辆信息</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-500">主要线路</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.main_route }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">车辆类型</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.vehicle_type }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">车长</label>
              <p class="mt-1 text-sm text-gray-900">{{ driver.vehicle_length || '-' }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500">每公里价格</label>
              <p class="mt-1 text-sm text-gray-900">¥{{ driver.price_per_km }}/公里</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6 pt-6 border-t border-gray-200">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-500">驾龄</label>
            <p class="mt-1 text-sm text-gray-900">{{ driver.experience_years }} 年</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">状态</label>
            <p class="mt-1">
              <span :class="getStatusClass(driver.status)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ getStatusText(driver.status) }}
              </span>
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">备注</label>
            <p class="mt-1 text-sm text-gray-900">{{ driver.remark || '-' }}</p>
          </div>
        </div>
      </div>
      
      <!-- 照片管理 -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <h3 class="text-lg font-medium text-gray-900 mb-4">照片管理</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- 身份证正面 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('id_card_front')" class="mb-2">
                <img :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('id_card_front')?.id}`" alt="身份证正面" class="w-full h-32 object-cover rounded" />
              </div>
              <div v-else>
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">身份证正面</p>
            <button
              @click="triggerFileUpload('id_card_front')"
              class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
            >
              {{ getPhotoByType('id_card_front') ? '重新上传' : '上传' }}
            </button>
            <input
              ref="id_card_front_input"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('id_card_front', $event)"
            />
          </div>
          
          <!-- 身份证背面 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('id_card_back')" class="mb-2">
                <img :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('id_card_back')?.id}`" alt="身份证背面" class="w-full h-32 object-cover rounded" />
              </div>
              <div v-else>
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">身份证背面</p>
            <button
              @click="triggerFileUpload('id_card_back')"
              class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
            >
              {{ getPhotoByType('id_card_back') ? '重新上传' : '上传' }}
            </button>
            <input
              ref="id_card_back_input"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('id_card_back', $event)"
            />
          </div>
          
          <!-- 驾驶证 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('license')" class="mb-2">
                <img :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('license')?.id}`" alt="驾驶证" class="w-full h-32 object-cover rounded" />
              </div>
              <div v-else>
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">驾驶证</p>
            <button
              @click="triggerFileUpload('license')"
              class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
            >
              {{ getPhotoByType('license') ? '重新上传' : '上传' }}
            </button>
            <input
              ref="license_input"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('license', $event)"
            />
          </div>
          
          <!-- 车辆照片 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('vehicle')" class="mb-2">
                <img :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('vehicle')?.id}`" alt="车辆照片" class="w-full h-32 object-cover rounded" />
              </div>
              <div v-else>
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">车辆照片</p>
            <button
              @click="triggerFileUpload('vehicle')"
              class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
            >
              {{ getPhotoByType('vehicle') ? '重新上传' : '上传' }}
            </button>
            <input
              ref="vehicle_input"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('vehicle', $event)"
            />
          </div>
        </div>
      </div>
      
      <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end gap-4">
        <button
          @click="handleEdit"
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          编辑
        </button>
        <button
          @click="handleDelete"
          class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          删除
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { toast } from 'sonner'
import type { Driver } from '@/api/drivers'
import { uploadDriverPhoto, getDriverPhotos } from '@/api/drivers'

const route = useRoute()
const router = useRouter()
const driverStore = useDriverStore()

const driver = ref<Driver | null>(null)

// 照片数据
const photos = ref<any[]>([])

// 文件上传引用
const id_card_front_input = ref<HTMLInputElement>()
const id_card_back_input = ref<HTMLInputElement>()
const license_input = ref<HTMLInputElement>()
const vehicle_input = ref<HTMLInputElement>()

const getStatusClass = (status: string) => {
  switch (status) {
    case 'active':
      return 'bg-green-100 text-green-800'
    case 'inactive':
      return 'bg-gray-100 text-gray-800'
    case 'blocked':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

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

const fetchDriver = async () => {
  try {
    driver.value = await driverStore.fetchDriver(Number(route.params.id))
    if (driver.value) {
      photos.value = await getDriverPhotos(driver.value.id)
    }
  } catch (error) {
    console.error('获取司机信息失败:', error)
    toast.error('获取司机信息失败')
  }
}

const handleEdit = () => {
  router.push(`/drivers/${route.params.id}/edit`)
}

const triggerFileUpload = (photoType: string) => {
  const inputRef = photoType === 'id_card_front' ? id_card_front_input.value :
                   photoType === 'id_card_back' ? id_card_back_input.value :
                   photoType === 'license' ? license_input.value :
                   vehicle_input.value
  
  if (inputRef) {
    inputRef.click()
  }
}

const handleFileUpload = async (photoType: string, event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file || !driver.value) return
  
  try {
    await uploadDriverPhoto(driver.value.id, photoType, file)
    toast.success('照片上传成功')
    // 刷新照片列表
    photos.value = await getDriverPhotos(driver.value.id)
  } catch (error: any) {
    console.error('照片上传失败:', error)
    toast.error('照片上传失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
  }
}

const getPhotoByType = (photoType: string) => {
  return photos.value.find(photo => photo.photo_type === photoType)
}

const handleDelete = async () => {
  if (confirm('确定要删除这个司机吗？')) {
    try {
      await driverStore.removeDriver(Number(route.params.id))
      toast.success('司机删除成功')
      router.push('/drivers')
    } catch (error) {
      console.error('删除司机失败:', error)
      toast.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchDriver()
})
</script>