<template>
  <div class="enterprise-layout">
    <!-- 左侧菜单 -->
    <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
      <div class="sidebar__logo">
        <div class="logo-icon">🚗</div>
        <div v-if="!collapsed" class="logo-text">司机管理系统</div>
      </div>

      <nav class="sidebar__nav">
        <a-menu
          mode="inline"
          :selectedKeys="selectedKeys"
          class="sidebar-menu"
        >
          <template v-if="permStore.can('menu', 'drivers')">
            <a-menu-item key="drivers" class="sidebar-menu__item">
              <UserOutlined />
              <router-link to="/drivers">司机管理</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'vehicles')">
            <a-menu-item key="vehicles" class="sidebar-menu__item">
              <CarOutlined />
              <router-link to="/vehicles">车辆管理</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'schedules')">
            <a-menu-item key="schedules" class="sidebar-menu__item">
              <CalendarOutlined />
              <router-link to="/schedules">排班调度</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'certificates')">
            <a-menu-item key="certificates" class="sidebar-menu__item">
              <SafetyOutlined />
              <router-link to="/certificates">证书管理</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'safety')">
            <a-menu-item key="safety" class="sidebar-menu__item">
              <WarningOutlined />
              <router-link to="/safety">安全管理</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'statistics')">
            <a-menu-item key="statistics" class="sidebar-menu__item">
              <BarChartOutlined />
              <router-link to="/statistics">数据统计</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'users')">
            <a-menu-item key="users" class="sidebar-menu__item">
              <TeamOutlined />
              <router-link to="/users">用户管理</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'tasks')">
            <a-menu-item key="tasks" class="sidebar-menu__item">
              <CalendarOutlined />
              <router-link to="/tasks">任务看板</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'files')">
            <a-menu-item key="files" class="sidebar-menu__item">
              <SafetyOutlined />
              <router-link to="/files">文件库</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'audit')">
            <a-menu-item key="audit" class="sidebar-menu__item">
              <WarningOutlined />
              <router-link to="/audit/logs">审计日志</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'security')">
            <a-menu-item key="security" class="sidebar-menu__item">
              <SafetyOutlined />
              <router-link to="/security/center">安全中心</router-link>
            </a-menu-item>
          </template>
          <template v-if="permStore.can('menu', 'permissions')">
            <a-menu-item key="permissions" class="sidebar-menu__item">
              <TeamOutlined />
              <router-link to="/admin/permissions">权限管理</router-link>
            </a-menu-item>
          </template>

          <div class="sidebar__divider"></div>

          <a-menu-item key="profile" class="sidebar-menu__item">
            <UserOutlined />
            <router-link to="/profile">个人资料</router-link>
          </a-menu-item>
        </a-menu>
      </nav>
    </aside>

    <!-- 主要内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <header class="header">
        <div class="header__left">
          <button
            class="header__trigger"
            @click="collapsed = !collapsed"
          >
            <MenuUnfoldOutlined v-if="collapsed" />
            <MenuFoldOutlined v-else />
          </button>
          <h1 class="header__title">
            {{ $route.meta.title || '仪表板' }}
          </h1>
        </div>

        <div class="header__right">
          <div class="user-info">
            <div class="user-avatar">
              {{ authStore.user?.username?.charAt(0).toUpperCase() }}
            </div>
            <div class="user-details">
              <div class="user-name">{{ authStore.user?.username }}</div>
              <div class="user-role">
                <span class="role-tag" :class="authStore.isAdmin ? 'role-tag--admin' : 'role-tag--staff'">
                  {{ authStore.isAdmin ? '管理员' : '员工' }}
                </span>
              </div>
            </div>
          </div>

          <button class="logout-btn" @click="handleLogout">
            <LogoutOutlined />
            退出
          </button>
        </div>
      </header>

      <!-- 内容区域 -->
      <main class="content">
        <div class="content-wrapper">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { usePermissionStore } from '@/stores/permissions'
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
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons-vue'

const authStore = useAuthStore()
const permStore = usePermissionStore()
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
  permStore.setUser(authStore.user as any)
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

<style scoped>
.enterprise-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg-body);
  font-family: var(--font-family);
  background-image: 
    radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.1) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(15, 23, 42, 0.1) 0px, transparent 50%);
}

/* 侧边栏样式 */
.sidebar {
  width: var(--layout-sidebar-width);
  background-color: var(--color-bg-sidebar);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-base);
  position: fixed;
  height: 100vh;
  z-index: var(--z-index-fixed);
  box-shadow: var(--shadow-xl);
}

.sidebar--collapsed {
  width: var(--layout-sidebar-collapsed-width);
}

.sidebar__logo {
  height: var(--layout-header-height);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 var(--spacing-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  gap: var(--spacing-sm);
  background: transparent; /* Removed darker background */
}

.logo-icon {
  font-size: var(--font-size-xl);
  flex-shrink: 0;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.5));
}

.logo-text {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-inverse);
  white-space: nowrap;
  letter-spacing: -0.025em;
}

.sidebar__nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md) var(--spacing-sm);
}

.sidebar-menu {
  background: transparent;
  border: none;
}

.sidebar-menu__item {
  margin: var(--spacing-xs) 0;
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
  color: var(--color-text-disabled);
  font-weight: 500; /* Added weight */
}

.sidebar-menu__item:hover {
  background-color: rgba(255, 255, 255, 0.1); /* Increased opacity */
  color: var(--color-text-inverse);
}

.sidebar-menu__item.ant-menu-item-selected {
  background: var(--color-accent-600); /* Solid accent color */
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4); /* Matching shadow */
}

.sidebar-menu__item.ant-menu-item-selected::after {
  display: none;
}

.sidebar__divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: var(--spacing-lg) var(--spacing-md);
}

/* 主容器样式 */
.main-container {
  flex: 1;
  margin-left: var(--layout-sidebar-width);
  transition: margin-left var(--transition-base);
  display: flex;
  flex-direction: column;
}

.sidebar--collapsed + .main-container {
  margin-left: var(--layout-sidebar-collapsed-width);
}

/* 头部样式 */
.header {
  height: var(--layout-header-height);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-bottom: var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  position: sticky;
  top: 0;
  z-index: var(--z-index-sticky);
  transition: all var(--transition-base);
}

.header__left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.header__trigger {
  background: none;
  border: none;
  padding: var(--spacing-sm);
  border-radius: var(--radius-base);
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.header__trigger:hover {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.header__title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: -0.01em;
}

.header__right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
  background-color: rgba(255, 255, 255, 0.5);
  border: 1px solid var(--color-border-light);
  transition: all var(--transition-fast);
  cursor: pointer;
}

.user-info:hover {
  background-color: white;
  box-shadow: var(--shadow-sm);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-800) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--font-size-sm);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding-right: var(--spacing-xs);
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.user-role {
  display: flex;
  align-items: center;
}

.role-tag {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: var(--radius-full);
  font-weight: 600;
  line-height: 1.2;
  display: inline-block;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.role-tag--admin {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--color-error);
}

.role-tag--staff {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--color-info);
}

.logout-btn {
  background: none;
  border: 1px solid transparent;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-base);
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.logout-btn:hover {
  background-color: rgba(239, 68, 68, 0.05);
  color: var(--color-error);
  border-color: rgba(239, 68, 68, 0.2);
}

/* 内容区域样式 */
.content {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
}

.content-wrapper {
  max-width: var(--layout-content-max-width);
  margin: 0 auto;
  animation: fadeIn var(--transition-base);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar--collapsed {
    transform: translateX(0);
    width: var(--layout-sidebar-width);
  }

  .main-container {
    margin-left: 0;
  }

  .sidebar--collapsed + .main-container {
    margin-left: 0;
  }

  .header__title {
    font-size: var(--font-size-md);
  }

  .user-details {
    display: none;
  }
}
</style>
