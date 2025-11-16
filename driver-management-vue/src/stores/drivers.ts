import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {
  Driver,
  DriverCreate,
  DriverUpdate,
  DriverQuery,
  DriverListResponse,
} from '@/api/drivers'
import { getDrivers, getDriver, createDriver, updateDriver, deleteDriver } from '@/api/drivers'

export const useDriverStore = defineStore('drivers', () => {
  const drivers = ref<Driver[]>([])
  const currentDriver = ref<Driver | null>(null)
  const loading = ref(false)
  const total = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(20)

  // 计算属性
  const hasDrivers = computed(() => drivers.value.length > 0)
  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

  // 获取司机列表
  async function fetchDrivers(query?: DriverQuery) {
    loading.value = true
    try {
      const response: DriverListResponse = await getDrivers({
        page: currentPage.value,
        page_size: pageSize.value,
        ...query,
      })
      drivers.value = response.data
      total.value = response.total
    } catch (error) {
      console.error('获取司机列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个司机详情
  async function fetchDriver(id: number) {
    loading.value = true
    try {
      const driver = await getDriver(id)
      currentDriver.value = driver
      return driver
    } catch (error) {
      console.error('获取司机详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建司机
  async function addDriver(data: DriverCreate) {
    loading.value = true
    try {
      const newDriver = await createDriver(data)
      drivers.value.unshift(newDriver) // 添加到列表开头
      total.value++
      return newDriver
    } catch (error) {
      console.error('创建司机失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新司机
  async function modifyDriver(id: number, data: DriverUpdate) {
    loading.value = true
    try {
      const updatedDriver = await updateDriver(id, data)
      const index = drivers.value.findIndex((d) => d.id === id)
      if (index !== -1) {
        drivers.value[index] = updatedDriver
      }
      if (currentDriver.value?.id === id) {
        currentDriver.value = updatedDriver
      }
      return updatedDriver
    } catch (error) {
      console.error('更新司机失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除司机
  async function removeDriver(id: number) {
    loading.value = true
    try {
      await deleteDriver(id)
      drivers.value = drivers.value.filter((d) => d.id !== id)
      total.value--
      if (currentDriver.value?.id === id) {
        currentDriver.value = null
      }
    } catch (error) {
      console.error('删除司机失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 设置当前页
  function setPage(page: number) {
    currentPage.value = page
  }

  // 设置每页条数
  function setPageSize(size: number) {
    pageSize.value = size
    currentPage.value = 1 // 重置到第一页
  }

  // 重置状态
  function reset() {
    drivers.value = []
    currentDriver.value = null
    total.value = 0
    currentPage.value = 1
    pageSize.value = 20
  }

  return {
    // 状态
    drivers,
    currentDriver,
    loading,
    total,
    currentPage,
    pageSize,

    // 计算属性
    hasDrivers,
    totalPages,

    // 方法
    fetchDrivers,
    fetchDriver,
    addDriver,
    modifyDriver,
    removeDriver,
    setPage,
    setPageSize,
    reset,
  }
})
