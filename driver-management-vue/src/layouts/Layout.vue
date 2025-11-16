<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider :collapsed="collapsed" collapsible breakpoint="lg" @breakpoint="onBreakpoint">
      <div style="height: 48px; margin: 16px; color: #fff; font-weight: 600">司机管理系统</div>
      <a-menu theme="dark" mode="inline" :selectedKeys="selectedKeys">
        <a-menu-item key="drivers">
          <router-link to="/drivers">司机管理</router-link>
        </a-menu-item>
        <a-menu-item v-if="authStore.isAdmin" key="statistics">
          <router-link to="/statistics">数据统计</router-link>
        </a-menu-item>
        <a-menu-item v-if="authStore.isAdmin" key="users">
          <router-link to="/users">用户管理</router-link>
        </a-menu-item>
        <a-menu-item key="profile">
          <router-link to="/profile">个人资料</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header
        style="
          background: #fff;
          display: flex;
          justify-content: flex-end;
          align-items: center;
          padding: 0 16px;
        "
      >
        <div style="display: flex; align-items: center; gap: 12px">
          <span>{{ authStore.user?.username }}</span>
          <a-tag :color="authStore.isAdmin ? 'red' : 'blue'">{{
            authStore.isAdmin ? '管理员' : '员工'
          }}</a-tag>
          <a-button type="link" @click="handleLogout">退出登录</a-button>
        </div>
      </a-layout-header>
      <a-layout-content style="margin: 16px">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const selectedKeys = ref<string[]>([])

const updateSelected = () => {
  const p = route.path
  if (p.startsWith('/drivers')) selectedKeys.value = ['drivers']
  else if (p === '/statistics') selectedKeys.value = ['statistics']
  else if (p === '/users') selectedKeys.value = ['users']
  else if (p === '/profile') selectedKeys.value = ['profile']
  else selectedKeys.value = []
}

watch(() => route.path, updateSelected, { immediate: true })

onMounted(() => {
  authStore.fetchUser()
  updateSelected()
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const onBreakpoint = (broken: boolean) => {
  collapsed.value = broken
}
</script>
