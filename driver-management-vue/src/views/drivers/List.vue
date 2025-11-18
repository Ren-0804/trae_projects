<template>
  <div style="padding: 24px">
    <!-- Glassmorphism Header -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <div>
          <h1 style="
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
          ">司机管理</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">管理所有司机信息和状态</p>
        </div>
        <router-link to="/drivers/new">
          <a-button 
            type="primary" 
            size="large"
            style="
              background: linear-gradient(135deg, #667eea, #764ba2);
              border: none;
              border-radius: 12px;
              height: 44px;
              padding: 0 24px;
              font-weight: 600;
              box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            "
          >
            <template #icon><PlusOutlined /></template>
            新增司机
          </a-button>
        </router-link>
      </div>
    </div>

    <!-- Glassmorphism Search Card -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
      <a-space style="width: 100%" wrap>
        <a-input
          v-model:value="searchKeyword"
          placeholder="搜索姓名、电话、线路"
          style="
            width: 280px;
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.7);
          "
        >
          <template #prefix><SearchOutlined style="color: #9ca3af" /></template>
        </a-input>
        <a-select 
          v-model:value="selectedStatus" 
          style="
            width: 160px;
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.7);
          " 
          allowClear 
          placeholder="状态筛选"
        >
          <a-select-option value="active">活跃</a-select-option>
          <a-select-option value="inactive">非活跃</a-select-option>
          <a-select-option value="blocked">已封禁</a-select-option>
        </a-select>
        <a-button 
          type="primary" 
          @click="handleSearch"
          style="
            border-radius: 12px;
            height: 40px;
            padding: 0 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            font-weight: 600;
          "
        >
          <template #icon><SearchOutlined /></template>
          搜索
        </a-button>
      </a-space>
    </div>

    <!-- Glassmorphism Table Card -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    ">
      <a-table 
        :dataSource="drivers" 
        :columns="columns" 
        :rowKey="'id'" 
        :pagination="false"
        style="background: transparent;"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag 
              :color="statusColor(record.status)"
              style="border-radius: 20px; padding: 4px 12px; font-weight: 500;"
            >
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'actions'">
            <a-space>
              <router-link :to="`/drivers/${record.id}`">
                <a-button 
                  type="text" 
                  style="
                    color: #667eea;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 500;
                  "
                >
                  <template #icon><EyeOutlined /></template>
                  查看
                </a-button>
              </router-link>
              <a-button 
                type="text" 
                @click="handleEdit(record.id)"
                style="
                  color: #10b981;
                  border-radius: 8px;
                  padding: 4px 12px;
                  font-weight: 500;
                "
              >
                <template #icon><EditOutlined /></template>
                编辑
              </a-button>
              <a-popconfirm
                title="确认删除此司机？"
                @confirm="handleDelete(record.id)"
                okText="确认"
                cancelText="取消"
                okButtonProps="{ style: { backgroundColor: '#ef4444', borderColor: '#ef4444' } }"
              >
                <a-button 
                  danger 
                  type="text"
                  style="
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 500;
                  "
                >
                  <template #icon><DeleteOutlined /></template>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>

      <div style="
        padding: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.5);
        border-top: 1px solid rgba(0, 0, 0, 0.05);
      ">
        <div style="color: #6b7280; font-size: 14px;">
          共 <span style="font-weight: 600; color: #374151;">{{ total }}</span> 条记录，当前第 <span style="font-weight: 600; color: #374151;">{{ currentPage }}</span> 页
        </div>
        <a-pagination
          :current="currentPage"
          :total="total"
          :pageSize="pageSize"
          @change="handlePageChange"
          style="margin: 0;"
          :showSizeChanger="false"
          :showQuickJumper="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { message, Modal } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const driverStore = useDriverStore()

const searchKeyword = ref('')
const selectedStatus = ref('')

const drivers = computed(() => driverStore.drivers)
const total = computed(() => driverStore.total)
const currentPage = computed(() => driverStore.currentPage)

const pageSize = computed(() => driverStore.pageSize)

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
      status: selectedStatus.value || undefined,
    })
  } catch (error) {
    message.error('获取司机列表失败')
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
  Modal.confirm({
    title: '确认删除',
    content: '删除后不可恢复，是否继续？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    async onOk() {
      try {
        await driverStore.removeDriver(id)
        message.success('司机删除成功')
      } catch (error) {
        message.error('删除司机失败')
        console.error('删除司机失败:', error)
      }
    },
  })
}

// 监听搜索条件变化
watch([searchKeyword, selectedStatus], () => {
  handleSearch()
})

onMounted(() => {
  fetchDrivers()
})

const columns = [
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '电话', dataIndex: 'phone', key: 'phone' },
  { title: '身份证号', dataIndex: 'id_card', key: 'id_card' },
  { title: '驾驶证号', dataIndex: 'license_number', key: 'license_number' },
  { title: '主要线路', dataIndex: 'main_route', key: 'main_route' },
  { title: '车辆类型', dataIndex: 'vehicle_type', key: 'vehicle_type' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'actions' },
]

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
</script>
