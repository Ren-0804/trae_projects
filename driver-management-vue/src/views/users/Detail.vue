<template>
  <div style="padding:16px">
    <a-page-header title="员工详情">
      <template #extra>
        <router-link to="/users">
          <a-button>返回列表</a-button>
        </router-link>
        <router-link :to="`/users/${route.params.id}/edit`">
          <a-button type="primary">编辑</a-button>
        </router-link>
      </template>
    </a-page-header>

    <a-card title="基本信息" style="margin-bottom:16px">
      <a-descriptions :column="descColumns" bordered size="middle">
        <a-descriptions-item label="用户名" :labelStyle="{width:'120px'}">{{ user?.username }}</a-descriptions-item>
        <a-descriptions-item label="邮箱">{{ user?.email || '未设置' }}</a-descriptions-item>
        <a-descriptions-item label="角色">
          <a-tag :color="user?.role === 'admin' ? 'red' : 'blue'">{{ user?.role === 'admin' ? '管理员' : '员工' }}</a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="状态">
          <a-tag :color="user?.is_active ? 'green' : 'red'">{{ user?.is_active ? '活跃' : '禁用' }}</a-tag>
        </a-descriptions-item>
      </a-descriptions>
    </a-card>

    <a-card title="工作信息" style="margin-bottom:16px">
      <a-descriptions :column="descColumns" bordered size="middle">
        <a-descriptions-item label="注册时间" :labelStyle="{width:'120px'}">{{ formatDate(user?.created_at) }}</a-descriptions-item>
        <a-descriptions-item label="最近更新时间">{{ formatDate(user?.updated_at) }}</a-descriptions-item>
        <a-descriptions-item label="最后登录">{{ formatDate(user?.last_login_at || undefined) }}</a-descriptions-item>
      </a-descriptions>
    </a-card>

    <a-card title="历史记录">
      <div style="color:#999">暂无历史记录数据</div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/auth'
import type { User } from '@/types/user'
import { useWindowSize } from '@vueuse/core'

const route = useRoute()
const data = ref<User | null>(null)
const user = computed(() => data.value)

const { width } = useWindowSize()
const descColumns = computed(() => (width.value >= 768 ? 2 : 1))

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-'
  try {
    return new Date(dateString).toLocaleString('zh-CN')
  } catch {
    return '无效日期'
  }
}

const fetchUser = async () => {
  const rawId = String(route.params.id ?? '')
  const idNum = Number(rawId)
  if (!Number.isFinite(idNum) || rawId.trim() === '') {
    return
  }
  const res = await api.get(`/auth/${idNum}`)
  data.value = res.data
}

onMounted(() => {
  fetchUser()
})
</script>