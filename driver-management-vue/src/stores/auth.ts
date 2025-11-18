import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'
import { login as apiLogin, getCurrentUser, refreshToken, logout as apiLogout } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => {
    const role = user.value?.role
    const r = typeof role === 'string' ? role.toLowerCase() : ''
    return r === 'admin' || r === 'superadmin'
  })

  function hasRole(required: Array<User['role']>) {
    const role = user.value?.role
    return required.includes(role as any)
  }

  async function login(username: string, password: string) {
    try {
      const response = await apiLogin({ username, password })
      token.value = response.token
      user.value = response.user
      localStorage.setItem('token', response.token)
      scheduleRefresh(response.expires_in)
      return response
    } catch (error) {
      throw error
    }
  }

  async function refresh() {
    if (!token.value) return
    const r = await refreshToken()
    token.value = r.token
    localStorage.setItem('token', r.token)
    scheduleRefresh(r.expires_in)
  }

  function scheduleRefresh(expiresIn?: number) {
    const ttl = typeof expiresIn === 'number' ? Math.max(30, Math.floor(expiresIn * 0.8)) : 900
    window.clearTimeout((scheduleRefresh as any)._t)
    ;(scheduleRefresh as any)._t = window.setTimeout(() => {
      refresh().catch(() => {})
    }, ttl * 1000)
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
    window.clearTimeout((scheduleRefresh as any)._t)
  }

  async function forceLogout() {
    await apiLogout().catch(() => {})
    logout()
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    hasRole,
    login,
    fetchUser,
    logout,
    forceLogout,
  }
})
