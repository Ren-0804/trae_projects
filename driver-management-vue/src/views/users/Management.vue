<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">用户管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
      >
        新增用户
      </button>
    </div>

    <!-- 用户列表表格 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              用户名
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              邮箱
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              角色
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              状态
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              最后登录
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              创建时间
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ user.username }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ user.email || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span :class="getRoleClass(user.role)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ getRoleText(user.role) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span :class="getStatusClass(user.is_active)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ user.is_active ? '活跃' : '禁用' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(user.last_login_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(user.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex gap-2">
                <button
                  @click="handleEdit(user)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  编辑
                </button>
                <button
                  @click="handleToggleStatus(user)"
                  class="text-orange-600 hover:text-orange-900"
                >
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 创建用户模态框 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">新增用户</h3>
          <form @submit.prevent="handleCreateUser">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">用户名 *</label>
                <input
                  v-model="createForm.username"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请输入用户名"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                <input
                  v-model="createForm.email"
                  type="email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请输入邮箱地址"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">密码 *</label>
                <input
                  v-model="createForm.password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请输入密码"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">角色 *</label>
                <select
                  v-model="createForm.role"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="employee">员工</option>
                  <option value="admin">管理员</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ loading ? '创建中...' : '创建' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

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
const showCreateModal = ref(false)
const loading = ref(false)

const createForm = ref({
  username: '',
  email: '',
  password: '',
  role: 'employee'
})

const getRoleClass = (role: string) => {
  switch (role) {
    case 'admin':
      return 'bg-red-100 text-red-800'
    case 'employee':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

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

const getStatusClass = (isActive: boolean) => {
  return isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
}

const formatDate = (dateString: string | null) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

const fetchUsers = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      users.value = await response.json()
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

const handleCreateUser = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(createForm.value)
    })
    
    if (response.ok) {
      showCreateModal.value = false
      createForm.value = {
        username: '',
        email: '',
        password: '',
        role: 'employee'
      }
      fetchUsers()
    } else {
      const error = await response.json()
      alert('创建失败: ' + (error.detail || '未知错误'))
    }
  } catch (error) {
    console.error('创建用户失败:', error)
    alert('创建失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleEdit = (user: User) => {
  // TODO: 实现编辑功能
  alert('编辑功能开发中')
}

const handleToggleStatus = async (user: User) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/auth/${user.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({ is_active: !user.is_active })
    })
    
    if (response.ok) {
      fetchUsers()
    }
  } catch (error) {
    console.error('更新用户状态失败:', error)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>