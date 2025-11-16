<template>
  <div style="padding: 16px">
    <a-page-header title="司机详情">
      <template #extra>
        <router-link to="/drivers">
          <a-button>返回列表</a-button>
        </router-link>
        <a-button type="primary" @click="handleEdit">编辑</a-button>
        <a-button danger @click="handleDelete">删除</a-button>
      </template>
    </a-page-header>

    <div v-if="driver" class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <a-card title="基本信息">
            <a-descriptions :column="descColumns" bordered size="middle">
              <a-descriptions-item label="姓名" :labelStyle="{width:'120px'}">{{ driver.name }}</a-descriptions-item>
              <a-descriptions-item label="电话">{{ driver.phone }}</a-descriptions-item>
              <a-descriptions-item label="紧急联系人">{{ driver.emergency_contact || '-' }}</a-descriptions-item>
              <a-descriptions-item label="紧急联系电话">{{ driver.emergency_phone || '-' }}</a-descriptions-item>
              <a-descriptions-item label="状态">
                <a-tag :color="statusColor(driver.status)">{{ getStatusText(driver.status) }}</a-tag>
              </a-descriptions-item>
            </a-descriptions>
            <div style="height:8px"></div>
            <a-descriptions :column="descColumns" bordered size="middle" title="证件信息">
              <a-descriptions-item label="身份证号" :labelStyle="{width:'120px'}">{{ driver.id_card }}</a-descriptions-item>
              <a-descriptions-item label="驾驶证号">{{ driver.license_number }}</a-descriptions-item>
              <a-descriptions-item label="驾驶证类型">{{ driver.license_type }}</a-descriptions-item>
            </a-descriptions>
          </a-card>
        </div>

        <div>
          <a-card title="车辆信息">
            <a-descriptions :column="descColumns" bordered size="middle">
              <a-descriptions-item label="主要线路" :labelStyle="{width:'120px'}">{{ driver.main_route }}</a-descriptions-item>
              <a-descriptions-item label="车辆类型">{{ driver.vehicle_type }}</a-descriptions-item>
              <a-descriptions-item label="车长">{{ driver.vehicle_length || '-' }}</a-descriptions-item>
              <a-descriptions-item label="每公里价格">¥{{ driver.price_per_km }}/公里</a-descriptions-item>
              <a-descriptions-item label="驾龄">{{ driver.experience_years }} 年</a-descriptions-item>
              <a-descriptions-item label="备注">{{ driver.remark || '-' }}</a-descriptions-item>
            </a-descriptions>
            <div style="height:8px"></div>
            <a-descriptions :column="descColumns" bordered size="middle" title="保险信息">
              <a-descriptions-item label="保险公司" :labelStyle="{width:'120px'}">-</a-descriptions-item>
              <a-descriptions-item label="保单号">-</a-descriptions-item>
              <a-descriptions-item label="到期时间">-</a-descriptions-item>
            </a-descriptions>
            <div style="height:12px"></div>
            <a-card size="small" title="车辆图片">
              <img v-if="getPhotoByType('vehicle')" :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('vehicle')?.id}`" style="width:100%;max-width:360px;height:200px;object-fit:cover;border-radius:4px" />
              <div v-else style="height:200px;border:1px dashed #d9d9d9;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#999">暂无车辆图片</div>
            </a-card>
          </a-card>
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
              <a-tag :color="statusColor(driver.status)">{{ getStatusText(driver.status) }}</a-tag>
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
                <img
                  :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('id_card_front')?.id}`"
                  alt="身份证正面"
                  class="w-full h-32 object-cover rounded"
                />
              </div>
              <div v-else>
                <svg
                  class="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">身份证正面</p>
            <a-upload
              :showUploadList="false"
              accept="image/*"
              :beforeUpload="(file: File) => handleUpload('id_card_front', file)"
            >
              <a-button type="primary">{{
                getPhotoByType('id_card_front') ? '重新上传' : '上传'
              }}</a-button>
            </a-upload>
          </div>

          <!-- 身份证背面 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('id_card_back')" class="mb-2">
                <a-image
                  :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('id_card_back')?.id}`"
                  :width="160"
                  :height="128"
                  :preview="true"
                />
              </div>
              <div v-else>
                <svg
                  class="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">身份证背面</p>
            <a-upload
              :showUploadList="false"
              accept="image/*"
              :beforeUpload="(file: File) => handleUpload('id_card_back', file)"
            >
              <a-button type="primary">{{
                getPhotoByType('id_card_back') ? '重新上传' : '上传'
              }}</a-button>
            </a-upload>
          </div>

          <!-- 驾驶证 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('license')" class="mb-2">
                <a-image
                  :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('license')?.id}`"
                  :width="160"
                  :height="128"
                  :preview="true"
                />
              </div>
              <div v-else>
                <svg
                  class="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">驾驶证</p>
            <a-upload
              :showUploadList="false"
              accept="image/*"
              :beforeUpload="(file: File) => handleUpload('license', file)"
            >
              <a-button type="primary">{{
                getPhotoByType('license') ? '重新上传' : '上传'
              }}</a-button>
            </a-upload>
          </div>

          <!-- 车辆照片 -->
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <div class="mb-2">
              <div v-if="getPhotoByType('vehicle')" class="mb-2">
                <a-image
                  :src="`http://localhost:8000/api/v1/drivers/photos/${getPhotoByType('vehicle')?.id}`"
                  :width="160"
                  :height="128"
                  :preview="true"
                />
              </div>
              <div v-else>
                <svg
                  class="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-2">车辆照片</p>
            <a-upload
              :showUploadList="false"
              accept="image/*"
              :beforeUpload="(file: File) => handleUpload('vehicle', file)"
            >
              <a-button type="primary">{{
                getPhotoByType('vehicle') ? '重新上传' : '上传'
              }}</a-button>
            </a-upload>
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { toast } from 'sonner'
import { Modal, message } from 'ant-design-vue'
import type { Driver } from '@/api/drivers'
import { uploadDriverPhoto, getDriverPhotos } from '@/api/drivers'
import { useWindowSize } from '@vueuse/core'

const route = useRoute()
const router = useRouter()
const driverStore = useDriverStore()

const driver = ref<Driver | null>(null)
// descriptions responsive columns
const { width } = useWindowSize()
const descColumns = computed(() => (width.value >= 768 ? 2 : 1))

// 照片数据
const photos = ref<any[]>([])

// 文件上传引用

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

const handleUpload = async (photoType: string, file: File) => {
  if (!driver.value) return false
  try {
    await uploadDriverPhoto(driver.value.id, photoType, file)
    toast.success('照片上传成功')
    photos.value = await getDriverPhotos(driver.value.id)
  } catch {
    toast.error('照片上传失败')
  }
  return false
}

const getPhotoByType = (photoType: string) => {
  return photos.value.find((photo) => photo.photo_type === photoType)
}

const handleDelete = async () => {
  Modal.confirm({
    title: '确认删除',
    content: '删除后不可恢复，是否继续？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    async onOk() {
      try {
        await driverStore.removeDriver(Number(route.params.id))
        message.success('司机删除成功')
        router.push('/drivers')
      } catch {
        message.error('删除失败')
      }
    },
  })
}

onMounted(() => {
  fetchDriver()
})
</script>
