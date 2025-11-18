import { createAuditLog, createAuditAlert } from '@/api/audit'
import { useAuthStore } from '@/stores/auth'

export async function log(action: string, resource?: string, resource_id?: string | number, content?: any) {
  const auth = useAuthStore()
  await createAuditLog({ action, actor_id: auth.user?.id, actor_name: auth.user?.username, resource, resource_id, content })
}

export async function alert(action: string, resource?: string, resource_id?: string | number, description?: string, severity: 'low' | 'medium' | 'high' | 'critical' = 'high') {
  await createAuditAlert({ action, resource, resource_id, description, severity })
}