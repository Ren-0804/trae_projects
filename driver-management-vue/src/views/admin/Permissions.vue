<template>
  <div style="padding:16px">
    <a-card title="权限管理">
      <a-table :dataSource="users" :columns="columns" rowKey="id" :loading="loading" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getUsers, updateUser } from '@/api/users'
import { log, alert } from '@/utils/auditLogger'

const users = ref<any[]>([])
const loading = ref(false)
const roleOptions = [
  { label: 'SuperAdmin', value: 'superadmin' },
  { label: 'Admin', value: 'admin' },
  { label: 'Dispatcher', value: 'dispatcher' },
  { label: 'Manager', value: 'manager' },
  { label: 'Driver', value: 'driver' },
  { label: 'Auditor', value: 'auditor' },
]

const columns = [
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '角色', dataIndex: 'role', key: 'role',
    customRender: ({ record }: any) => {
      return (window as any).h(
        (window as any).resolveComponent('a-select'),
        {
          value: record.role,
          style: 'min-width:160px',
          onChange: async (val: string) => {
            await updateUser(record.id, { role: val as any })
            record.role = val
            await log('user.role.update', 'user', record.id, { role: val })
            await alert('user.role.update', 'user', record.id, `角色变更为 ${val}`, 'high')
          }
        },
        roleOptions.map(o => (window as any).h((window as any).resolveComponent('a-select-option'), { value: o.value }, o.label))
      )
    }
  },
]

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)
</script>