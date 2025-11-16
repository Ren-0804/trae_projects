<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">司机列表</h1>
      <div class="flex justify-between items-center">
        <div class="flex gap-4">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索姓名、电话、线路"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <select
            v-model="selectedStatus"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">全部状态</option>
            <option value="active">活跃</option>
            <option value="inactive">非活跃</option>
            <option value="blocked">已封禁</option>
          </select>
          <button
            @click="handleSearch"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            搜索
          </button>
        </div>
        <router-link
          to="/drivers/new"
          class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          新增司机
        </router-link>
      </div>
    </div>

    <!-- 司机列表表格 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              姓名
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              电话
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              身份证号
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              驾驶证号
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              主要线路
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              车辆类型
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              状态
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="driver in drivers" :key="driver.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ driver.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ driver.phone }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ driver.id_card }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ driver.license_number }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ driver.main_route }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ driver.vehicle_type }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusClass(driver.status)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ getStatusText(driver.status) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex gap-2">
                <router-link
                  :to="`/drivers/${driver.id}`"
                  class="text-blue-600 hover:text-blue-900"
                >
                  查看
                </router-link>
                <button
                  @click="handleEdit(driver.id)"
                  class="text-green-600 hover:text-green-900"
                >
                  编辑
                </button>
                <button
                  @click="handleDelete(driver.id)"
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="mt-6 flex justify-between items-center">
      <div class="text-sm text-gray-700">
        共 {{ total }} 条记录，当前第 {{ currentPage }} 页
      </div>
      <div class="flex gap-2">
        <button
          @click="handlePageChange(currentPage - 1)"
          :disabled="currentPage <= 1"
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>
        <button
          @click="handlePageChange(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import type { Driver } from '@/api/drivers'
import { addToast } from '@heroui/toast'

const router = useRouter()
const driverStore = useDriverStore()

const searchKeyword = ref('')
const selectedStatus = ref('')

const drivers = computed(() => driverStore.drivers)
const total = computed(() => driverStore.total)
const currentPage = computed(() => driverStore.currentPage)
const pageSize = computed(() => driverStore.pageSize)
const loading = computed(() => driverStore.loading)

const totalPages = computed(() => driverStore.totalPages)

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

const fetchDrivers = async () => {
  try {
    await driverStore.fetchDrivers({
      keyword: searchKeyword.value || undefined,
      status: selectedStatus.value || undefined
    })
  } catch (error) {
    addToast({
      title: '获取司机列表失败',
      description: '请稍后重试'
    })
    console.error('获取司机列表失败:', error)
  }
}

const handleSearch = () => {
  driverStore.setPage(1)
  fetchDrivers()
}

const handlePageChange = (page: number) => {
  driverStore.setPage(page)
  fetchDrivers()
}

const handleEdit = (id: number) => {
  router.push(`/drivers/${id}`)
}

const handleDelete = async (id: number) => {
  if (confirm('确定要删除这个司机吗？')) {
    try {
      await driverStore.removeDriver(id)
      addToast({
        title: '司机删除成功',
        description: 'success'
      })
    } catch (error) {
      addToast({ 
        title: '删除司机失败',
        description: '请稍后重试'
      })
      console.error('删除司机失败:', error)
    }
  }
}

// 监听搜索条件变化
watch([searchKeyword, selectedStatus], () => {
  handleSearch()
})

onMounted(() => {
  fetchDrivers()
})
</script>