<template>
  <div style="padding:16px">
    <a-card title="权限管理">
      <a-table :dataSource="users" :columns="columns" rowKey="id" :loading="loading">
        <template #bodyCell="{ column, record }">
          <template v-if="column.dataIndex==='role'">
            <a-select :value="record.role" style="min-width:160px" @change="(val:string)=>onRoleChange(record, val)">
              <a-select-option v-for="o in roleOptions" :key="o.value" :value="o.value">{{ o.label }}</a-select-option>
            </a-select>
          </template>
        </template>
      </a-table>
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
  { title: '角色', dataIndex: 'role', key: 'role' },
]

const onRoleChange = async (record: any, val: string) => {
  await updateUser(record.id, { role: val as any })
  record.role = val
  await log('user.role.update', 'user', record.id, { role: val })
  await alert('user.role.update', 'user', record.id, `角色变更为 ${val}`, 'high')
}

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