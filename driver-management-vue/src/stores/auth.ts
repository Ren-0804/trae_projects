import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'
import { login as apiLogin, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => {
    const role = user.value?.role
    const flag = (user.value as any)?.is_admin
    return (typeof role === 'string' && role.toLowerCase() === 'admin') || flag === true
  })

  async function login(username: string, password: string) {
    try {
      const response = await apiLogin({ username, password })
      token.value = response.token
      user.value = response.user
      localStorage.setItem('token', response.token)
      return response
    } catch (error) {
      throw error
    }
  }

  async function fetchUser() {
    if (!token.value) return

    try {
      const response = await getCurrentUser() as any
      user.value = response?.user ?? response
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    fetchUser,
    logout,
  }
})
