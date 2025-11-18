<template>
  <a-layout style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
    <a-layout-sider 
      :collapsed="collapsed" 
      collapsible 
      breakpoint="lg" 
      @breakpoint="onBreakpoint"
      style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.2)"
    >
      <div style="height: 80px; display: flex; align-items: center; justify-content: center; padding: 0 24px; border-bottom: 1px solid rgba(0, 0, 0, 0.05)">
        <div style="font-size: 24px; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          🚗 司机管理系统
        </div>
      </div>
      <a-menu 
        theme="light" 
        mode="inline" 
        :selectedKeys="selectedKeys"
        style="background: transparent; border: none; padding: 8px"
      >
        <a-menu-item key="drivers" style="border-radius: 12px; margin: 4px 0;">
          <UserOutlined />
          <router-link to="/drivers">司机管理</router-link>
        </a-menu-item>
        <a-menu-item key="vehicles" style="border-radius: 12px; margin: 4px 0;">
          <CarOutlined />
          <router-link to="/vehicles">车辆管理</router-link>
        </a-menu-item>
        <a-menu-item key="schedules" style="border-radius: 12px; margin: 4px 0;">
          <CalendarOutlined />
          <router-link to="/schedules">排班调度</router-link>
        </a-menu-item>
        <a-menu-item key="certificates" style="border-radius: 12px; margin: 4px 0;">
          <SafetyOutlined />
          <router-link to="/certificates">证书管理</router-link>
        </a-menu-item>
        <a-menu-item key="safety" style="border-radius: 12px; margin: 4px 0;">
          <WarningOutlined />
          <router-link to="/safety">安全管理</router-link>
        </a-menu-item>
        <a-menu-item v-if="authStore.isAdmin" key="statistics" style="border-radius: 12px; margin: 4px 0;">
          <BarChartOutlined />
          <router-link to="/statistics">数据统计</router-link>
        </a-menu-item>
        <a-menu-item v-if="authStore.isAdmin" key="users" style="border-radius: 12px; margin: 4px 0;">
          <TeamOutlined />
          <router-link to="/users">用户管理</router-link>
        </a-menu-item>
        <a-divider style="margin: 16px 0; border-color: rgba(0, 0, 0, 0.05)" />
        <a-menu-item key="profile" style="border-radius: 12px; margin: 4px 0;">
          <UserOutlined />
          <router-link to="/profile">个人资料</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout style="background: transparent">
      <a-layout-header
        style="
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(10px);
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 28px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
          height: 68px;
        "
      >
        <div style="font-size: 20px; font-weight: 600; color: #2c3e50; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">
          {{ $route.meta.title || '仪表板' }}
        </div>
        <div style="display: flex; align-items: center; gap: 12px">
          <div style="display: flex; align-items: center; gap: 10px; padding: 6px 12px; background: rgba(255, 255, 255, 0.85); border-radius: 18px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 12px; box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);">
              {{ authStore.user?.username?.charAt(0).toUpperCase() }}
            </div>
            <div style="display: flex; flex-direction: column; gap: 1px;">
              <div style="font-weight: 500; color: #2c3e50; font-size: 12px; line-height: 1.2;">{{ authStore.user?.username }}</div>
              <a-tag :color="authStore.isAdmin ? '#ff4d4f' : '#1890ff'" style="border-radius: 8px; font-size: 9px; padding: 0 5px; height: 16px; line-height: 16px; margin: 0; border: none; font-weight: 500;">
                {{ authStore.isAdmin ? '管理员' : '员工' }}
              </a-tag>
            </div>
          </div>
          <a-button 
            type="text" 
            @click="handleLogout"
            style="border-radius: 18px; padding: 6px 12px; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); display: flex; align-items: center; gap: 5px; font-weight: 500; transition: all 0.3s ease; font-size: 12px;"
            @mouseenter="(e: any) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.95)'"
            @mouseleave="(e: any) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.85)'"
          >
            <LogoutOutlined style="font-size: 12px;" />
            退出
          </a-button>
        </div>
      </a-layout-header>
      <a-layout-content class="glass-card" style="margin: 24px; padding: 24px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'
import {
  UserOutlined,
  CarOutlined,
  CalendarOutlined,
  SafetyOutlined,
  WarningOutlined,
  BarChartOutlined,
  TeamOutlined,
  LogoutOutlined
} from '@ant-design/icons-vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const selectedKeys = ref<string[]>([])

const updateSelected = () => {
  const p = route.path
  if (p.startsWith('/drivers')) selectedKeys.value = ['drivers']
  else if (p.startsWith('/vehicles')) selectedKeys.value = ['vehicles']
  else if (p.startsWith('/schedules')) selectedKeys.value = ['schedules']
  else if (p.startsWith('/certificates')) selectedKeys.value = ['certificates']
  else if (p.startsWith('/safety')) selectedKeys.value = ['safety']
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
