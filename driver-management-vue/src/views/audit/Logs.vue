<template>
  <div style="padding:16px">
    <a-card title="审计日志">
      <a-space style="margin-bottom:12px">
        <a-date-picker v-model:value="start" placeholder="开始日期" />
        <a-date-picker v-model:value="end" placeholder="结束日期" />
        <a-input v-model:value="user" placeholder="用户" />
        <a-button type="primary" @click="fetch">查询</a-button>
        <a-button @click="exportCsv">导出 CSV</a-button>
      </a-space>
      <a-list :data-source="logs" bordered :renderItem="renderItem" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getAuditLogs, exportAuditLogs } from '@/api/audit'

const logs = ref<any[]>([])
const start = ref<any>(null)
const end = ref<any>(null)
const user = ref('')
const router = useRouter()

const renderItem = ({ item }: any) => {
  return (window as any).h('div', { style: 'padding:8px' }, [
    (window as any).h('span', null, `${item.id} ${item.action || ''}`),
    (window as any).h((window as any).resolveComponent('a-button'), { type: 'link', onClick: () => router.push(`/audit/logs/${item.id}`) }, '详情')
  ])
}

const fetch = async () => {
  const params: any = {}
  if (start.value) params.start = start.value
  if (end.value) params.end = end.value
  if (user.value) params.user = user.value
  logs.value = await getAuditLogs(params)
}

fetch()

const exportCsv = async () => {
  const params: any = {}
  if (start.value) params.start = start.value
  if (end.value) params.end = end.value
  if (user.value) params.user = user.value
  const blob = await exportAuditLogs(params)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `audit-logs.csv`
  a.click()
  URL.revokeObjectURL(url)
}
</script>