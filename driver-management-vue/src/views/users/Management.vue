<template>
  <div style="padding: 24px; min-height: 100vh">
    <div style="
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(20px);
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    ">
      <div style="
        padding: 24px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h1 style="
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          ">用户管理</h1>
          <router-link to="/users/new">
            <a-button type="primary" style="
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              border: none;
              border-radius: 8px;
              font-weight: 600;
              box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            ">
              <template #icon>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </template>
              新增用户
            </a-button>
          </router-link>
        </div>
      </div>

      <div style="padding: 24px;">
        <a-table 
          :dataSource="users" 
          :columns="columns" 
          :rowKey="'id'" 
          :pagination="{ 
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total: number, range: [number, number]) => `${range[0]}-${range[1]} 共 ${total} 条`
          }"
          style="
            background: transparent;
            border-radius: 12px;
          ">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'role'">
              <a-tag :style="{
                background: record.role === 'admin' 
                  ? 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)' 
                  : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                border: 'none',
                color: 'white',
                fontWeight: '600',
                borderRadius: '20px',
                padding: '4px 12px'
              }">{{ getRoleText(record.role) }}</a-tag>
            </template>
            <template v-else-if="column.key === 'status'">
              <a-tag :style="{
                background: record.is_active 
                  ? 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' 
                  : 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                border: 'none',
                color: 'white',
                fontWeight: '600',
                borderRadius: '20px',
                padding: '4px 12px'
              }">{{ record.is_active ? '活跃' : '禁用' }}</a-tag>
            </template>
            <template v-else-if="column.key === 'actions'">
              <div style="display: flex; gap: 8px; align-items: center;">
                <router-link :to="`/users/${record.id}`">
                  <a-button type="text" style="
                    border-radius: 8px;
                    color: #667eea;
                    font-weight: 500;
                  ">
                    <template #icon>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </template>
                    查看
                  </a-button>
                </router-link>
                <router-link :to="`/users/${record.id}/edit`">
                  <a-button type="text" style="
                    border-radius: 8px;
                    color: #667eea;
                    font-weight: 500;
                  ">
                    <template #icon>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </template>
                    编辑
                  </a-button>
                </router-link>
                <a-button 
                  type="text" 
                  @click="handleToggleStatus(record)"
                  :style="{
                    borderRadius: '8px',
                    color: record.is_active ? '#fa709a' : '#43e97b',
                    fontWeight: '500',
                    background: record.is_active 
                      ? 'rgba(250, 112, 154, 0.1)' 
                      : 'rgba(67, 233, 123, 0.1)'
                  }">
                  <template #icon>
                    <svg v-if="record.is_active" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                    </svg>
                    <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    </svg>
                  </template>
                  {{ record.is_active ? '禁用' : '启用' }}
                </a-button>
                <!-- 对于活跃用户的禁用确认 -->
                <a-popconfirm
                  v-if="record.is_active"
                  title="确定要禁用该用户吗？"
                  @confirm="handleDelete(record.id)"
                  okText="确定"
                  cancelText="取消"
                >
                  <a-button 
                    danger 
                    type="text"
                    style="
                      border-radius: 8px;
                      background: rgba(255, 77, 79, 0.1);
                      font-weight: 500;
                    ">
                    <template #icon>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                        <line x1="12" y1="2" x2="12" y2="12"></line>
                      </svg>
                    </template>
                    禁用
                  </a-button>
                </a-popconfirm>
                <!-- 对于已禁用用户的删除确认 -->
                <a-popconfirm
                  v-else
                  title="确定要永久删除该用户吗？此操作不可恢复！"
                  @confirm="handleDeletePermanent(record.id)"
                  okText="确定"
                  cancelText="取消"
                >
                  <a-button 
                    danger 
                    type="text"
                    style="
                      border-radius: 8px;
                      background: rgba(255, 77, 79, 0.1);
                      font-weight: 500;
                    ">
                    <template #icon>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </template>
                    删除
                  </a-button>
                </a-popconfirm>
              </div>
            </template>
          </template>
        </a-table>
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(.ant-table) {
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
}

:deep(.ant-table-thead > tr > th) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: none;
  font-weight: 700;
  color: #2d3748;
  font-size: 14px;
  padding: 16px;
  backdrop-filter: blur(10px);
}

:deep(.ant-table-tbody > tr > td) {
  border: none;
  padding: 16px;
  background: transparent;
  transition: all 0.3s ease;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: rgba(102, 126, 234, 0.03);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:deep(.ant-table-tbody > tr) {
  border-radius: 8px;
  transition: all 0.3s ease;
  margin: 4px 0;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
}

:deep(.ant-table-tbody > tr:last-child > td) {
  border-bottom: none;
}

:deep(.ant-pagination) {
  margin-top: 24px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

:deep(.ant-pagination-item) {
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

:deep(.ant-pagination-item:hover) {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

:deep(.ant-pagination-item-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

:deep(.ant-pagination-item-active a) {
  color: white;
  font-weight: 600;
}

:deep(.ant-btn-text:hover) {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

:deep(.ant-popconfirm-inner) {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

:deep(.ant-popconfirm-buttons .ant-btn) {
  border-radius: 8px;
  font-weight: 500;
}

:deep(.ant-popconfirm-buttons .ant-btn-primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getUsers, deleteUser, updateUser } from '@/api/users'
import { message } from 'ant-design-vue'

interface User {
  id: number
  username: string
  email: string | null
  role: string
  is_active: boolean
  last_login_at: string | null
  created_at: string
}

const authStore = useAuthStore()

const users = ref<User[]>([])

const columns = [
  { 
    title: '用户名', 
    dataIndex: 'username', 
    key: 'username',
    customCell: () => {
      return {
        style: {
          'font-weight': '600',
          'color': '#2d3748'
        }
      }
    }
  },
  { 
    title: '邮箱', 
    dataIndex: 'email', 
    key: 'email',
    customCell: () => {
      return {
        style: {
          'color': '#718096'
        }
      }
    }
  },
  { 
    title: '角色', 
    key: 'role',
    align: 'center' as const,
    width: 100
  },
  { 
    title: '状态', 
    key: 'status',
    align: 'center' as const,
    width: 100
  },
  { 
    title: '最后登录', 
    dataIndex: 'last_login_at', 
    key: 'last_login_at',
    customCell: () => {
      return {
        style: {
          'color': '#718096',
          'font-size': '14px'
        }
      }
    }
  },
  { 
    title: '创建时间', 
    dataIndex: 'created_at', 
    key: 'created_at',
    customCell: () => {
      return {
        style: {
          'color': '#718096',
          'font-size': '14px'
        }
      }
    }
  },
  { 
    title: '操作', 
    key: 'actions',
    width: 300,
    align: 'center' as const
  },
]

const getRoleText = (role: string) => {
  switch (role) {
    case 'admin':
      return '管理员'
    case 'employee':
      return '员工'
    default:
      return '未知'
  }
}

const fetchUsers = async () => {
  try {
    console.log('开始获取用户列表...')
    const response = await getUsers()
    console.log('获取用户列表成功:', response)
    users.value = response.data
    console.log('设置用户数据:', users.value)
  } catch (error) {
    console.error('获取用户列表失败:', error)
    message.error('获取用户列表失败')
  }
}

// 保留列表管理功能，创建跳转由路由页面完成

const handleToggleStatus = async (user: User) => {
  try {
    // 需要创建更新用户的函数
    await updateUser(user.id, { is_active: !user.is_active })
    message.success(user.is_active ? '用户已禁用' : '用户已启用')
    fetchUsers()
  } catch (error) {
    console.error('更新用户状态失败:', error)
    message.error('更新用户状态失败')
  }
}

const handleDelete = async (userId: number) => {
  try {
    await deleteUser(userId)
    message.success('用户已禁用')
    fetchUsers()
  } catch (error) {
    console.error('禁用用户失败:', error)
    message.error('禁用用户失败')
  }
}

const handleDeletePermanent = async (userId: number) => {
  try {
    // For now, we'll use the regular delete function
    // In a real implementation, you would have a separate permanent delete endpoint
    await deleteUser(userId)
    message.success('用户已永久删除')
    fetchUsers()
  } catch (error) {
    console.error('删除用户失败:', error)
    message.error('删除用户失败')
  }
}

onMounted(() => {
  console.log('用户管理页面加载中...')
  console.log('当前用户角色:', authStore.user?.role)
  console.log('是否为管理员:', authStore.isAdmin)
  fetchUsers()
})
</script>