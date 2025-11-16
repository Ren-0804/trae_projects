<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">个人资料</h1>
    </div>

    <div v-if="user" class="bg-white rounded-lg shadow p-6 max-w-2xl">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
          <p class="text-lg text-gray-900">{{ user.username }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
          <p class="text-lg text-gray-900">{{ user.email || '未设置' }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">角色</label>
          <p class="text-lg text-gray-900">{{ getRoleText(user.role) }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">状态</label>
          <p class="text-lg text-gray-900">{{ user.is_active ? '活跃' : '禁用' }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">最后登录时间</label>
          <p class="text-lg text-gray-900">{{ formatDate(user.last_login_at) }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">注册时间</label>
          <p class="text-lg text-gray-900">{{ formatDate(user.created_at) }}</p>
        </div>
      </div>

      <div class="mt-8 pt-6 border-t border-gray-200">
        <button
          @click="showPasswordModal = true"
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          修改密码
        </button>
      </div>
    </div>

    <!-- 修改密码模态框 -->
    <div
      v-if="showPasswordModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">修改密码</h3>
          <form @submit.prevent="handleChangePassword">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">当前密码 *</label>
                <input
                  v-model="passwordForm.old_password"
                  type="password"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请输入当前密码"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">新密码 *</label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请输入新密码"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">确认新密码 *</label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="请再次输入新密码"
                />
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button
                type="button"
                @click="showPasswordModal = false"
                class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ loading ? '修改中...' : '修改' }}
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

const user = ref<User | null>(null)
const showPasswordModal = ref(false)
const loading = ref(false)

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

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

const formatDate = (dateString: string | null) => {
  if (!dateString) return '从未登录'
  return new Date(dateString).toLocaleString('zh-CN')
}

const fetchUserInfo = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/me', {
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    })

    if (response.ok) {
      user.value = await response.json()
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const handleChangePassword = async () => {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    alert('新密码和确认密码不匹配')
    return
  }

  loading.value = true
  try {
    // TODO: 实现修改密码API
    alert('修改密码功能开发中')
    showPasswordModal.value = false
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: '',
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    alert('修改密码失败，请重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>
