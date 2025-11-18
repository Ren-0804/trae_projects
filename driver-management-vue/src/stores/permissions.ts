import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types/user'

type Scope = 'own' | 'department' | 'all'

export const usePermissionStore = defineStore('permissions', () => {
  const user = ref<User | null>(null)
  const perms = ref<Record<string, Record<string, Scope | boolean>>>({})

  function setUser(u: User | null) {
    user.value = u
    const role = u?.role || 'driver'
    perms.value = mapRoleToPerms(role)
  }

  function can(resource: string, action: string, scope?: Scope) {
    const r = perms.value[resource]
    if (!r) return false
    const v = r[action]
    if (typeof v === 'boolean') return v
    if (!scope) return v === 'all'
    const order = { own: 1, department: 2, all: 3 } as const
    return order[(v as Scope)] >= order[scope]
  }

  return { user, perms, setUser, can }
})

function mapRoleToPerms(role: User['role']): Record<string, Record<string, Scope | boolean>> {
  const base: Record<string, Record<string, Scope | boolean>> = {
    menu: {
      drivers: true,
      vehicles: true,
      schedules: true,
      certificates: true,
      safety: true,
      statistics: role === 'admin' || role === 'superadmin',
      users: role === 'admin' || role === 'superadmin',
      security: role !== 'driver',
      permissions: role === 'admin' || role === 'superadmin',
      tasks: role !== 'auditor',
      files: true,
      audit: role === 'auditor' || role === 'admin' || role === 'superadmin',
    },
    user: { view: true, create: role !== 'driver', update: role !== 'driver', delete: role === 'superadmin' },
    driver: { view: true, create: role !== 'auditor', update: role !== 'auditor', delete: role === 'admin' || role === 'superadmin' },
    task: { view: true, create: role !== 'driver', update: true, delete: role === 'admin' || role === 'superadmin', data: role === 'manager' ? 'department' : role === 'superadmin' ? 'all' : 'own' },
    file: { view: true, upload: role !== 'auditor', delete: role === 'admin' || role === 'superadmin', data: role === 'admin' || role === 'superadmin' ? 'all' : 'own' },
    audit: { view: role === 'auditor' || role === 'admin' || role === 'superadmin', export: role !== 'driver', alert: role !== 'driver' },
  }
  return base
}