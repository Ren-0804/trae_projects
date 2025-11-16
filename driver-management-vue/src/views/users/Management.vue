<template>
  <div style="padding: 16px">
    <a-page-header title="用户管理">
      <template #extra>
        <router-link to="/users/new">
          <a-button type="primary">新增用户</a-button>
        </router-link>
      </template>
    </a-page-header>

    <a-table :dataSource="users" :columns="columns" :rowKey="'id'" bordered>
        <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'role'">
          <a-tag :color="record.role === 'admin' ? 'red' : 'blue'">{{
            getRoleText(record.role)
          }}</a-tag>
        </template>
        <template v-else-if="column.key === 'status'">
          <a-tag :color="record.is_active ? 'green' : 'red'">{{
            record.is_active ? '活跃' : '禁用'
          }}</a-tag>
        </template>
        <template v-else-if="column.key === 'actions'">
          <a-space>
            <router-link :to="`/users/${record.id}`">
              <a-button type="link">查看</a-button>
            </router-link>
            <router-link :to="`/users/${record.id}/edit`">
              <a-button type="link">编辑</a-button>
            </router-link>
            <a-button type="link" @click="handleToggleStatus(record)">{{
              record.is_active ? '禁用' : '启用'
            }}</a-button>
          </a-space>
        </template>
      </template>
    </a-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/auth'

interface User {
  id: number
  username: string
  email: string | null
  role: string
  is_active: boolean
  last_login_at: string | null
  created_at: string
}

useAuthStore()

const users = ref<User[]>([])

const columns = [
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '角色', key: 'role' },
  { title: '状态', key: 'status' },
  { title: '最后登录', dataIndex: 'last_login_at', key: 'last_login_at' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '操作', key: 'actions' },
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
    const response = await api.get('/auth')
    users.value = response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 保留列表管理功能，创建跳转由路由页面完成

 

const handleToggleStatus = async (user: User) => {
  try {
    await api.put(`/auth/${user.id}`, { is_active: !user.is_active })
    fetchUsers()
  } catch (error) {
    console.error('更新用户状态失败:', error)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
