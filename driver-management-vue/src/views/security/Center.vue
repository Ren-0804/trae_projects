<template>
  <div style="padding:16px">
    <a-card title="安全中心">
      <a-descriptions bordered :column="1" size="middle" style="margin-bottom:16px">
        <a-descriptions-item label="当前用户">{{ user?.username || '-' }}</a-descriptions-item>
        <a-descriptions-item label="角色">{{ user?.role || '-' }}</a-descriptions-item>
      </a-descriptions>
      <div style="margin-bottom:16px">
        <a-button type="primary" @click="logoutAll" :loading="loading">退出当前设备</a-button>
      </div>
      <a-table :dataSource="sessions" :columns="columns" :loading="loading" rowKey="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key==='action'">
            <a-button type="link" danger @click="revoke(record.id)">强制下线</a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getSessions, revokeSession } from '@/api/auth'

const auth = useAuthStore()
const user = computed(() => auth.user)
const sessions = ref<any[]>([])
const loading = ref(false)

const columns = [
  { title: '设备', dataIndex: 'device', key: 'device' },
  { title: 'IP', dataIndex: 'ip', key: 'ip' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '最近活跃', dataIndex: 'last_active_at', key: 'last_active_at' },
  { title: '操作', key: 'action' },
]

const fetchSessions = async () => {
  loading.value = true
  try {
    sessions.value = await getSessions()
  } catch (err: any) {
    const msg = err?.response?.data?.detail || err?.message || '会话加载失败'
    ;(await import('ant-design-vue')).message.error(msg)
  } finally {
    loading.value = false
  }
}

const revoke = async (id: string) => {
  loading.value = true
  try {
    await revokeSession(id)
    await fetchSessions()
  } catch (err: any) {
    const msg = err?.response?.data?.detail || err?.message || '强制下线失败'
    ;(await import('ant-design-vue')).message.error(msg)
  } finally {
    loading.value = false
  }
}

const logoutAll = async () => {
  loading.value = true
  try {
    await auth.forceLogout()
  } finally {
    loading.value = false
  }
}

onMounted(fetchSessions)
</script>