<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">司机管理系统</h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-700">{{ authStore.user?.username }}</span>
              <span class="px-2 py-1 text-xs rounded-full" :class="authStore.isAdmin ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'">
                {{ authStore.isAdmin ? '管理员' : '员工' }}
              </span>
            </div>
            
            <button
              @click="handleLogout"
              class="text-sm text-gray-500 hover:text-gray-700"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>
    
    <div class="flex">
      <aside class="w-64 bg-white shadow-sm min-h-screen">
        <nav class="mt-5 px-2">
          <router-link
            to="/drivers"
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            :class="$route.path.startsWith('/drivers') ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50'"
          >
            <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            司机管理
          </router-link>
          
          <router-link
            v-if="authStore.isAdmin"
            to="/statistics"
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            :class="$route.path === '/statistics' ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50'"
          >
            <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            数据统计
          </router-link>
          
          <router-link
            v-if="authStore.isAdmin"
            to="/users"
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            :class="$route.path === '/users' ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50'"
          >
            <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            用户管理
          </router-link>
          
          <router-link
            to="/profile"
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            :class="$route.path === '/profile' ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50'"
          >
            <svg class="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            个人资料
          </router-link>
        </nav>
      </aside>
      
      <main class="flex-1 p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>