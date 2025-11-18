<template>
  <div style="padding:16px">
    <a-card title="审计日志">
      <a-space style="margin-bottom:12px" wrap>
        <a-date-picker v-model:value="start" placeholder="开始日期" />
        <a-date-picker v-model:value="end" placeholder="结束日期" />
        <a-input v-model:value="user" placeholder="用户ID" style="min-width:160px" />
        <a-input v-model:value="operation" placeholder="操作类型" style="min-width:160px" />
        <a-button type="primary" @click="fetch">查询</a-button>
        <a-button @click="exportCsv">导出 CSV</a-button>
      </a-space>

      <a-row :gutter="12" style="margin-bottom:12px">
        <a-col :xs="24" :md="8">
          <a-card size="small" title="按操作类型">
            <div v-for="(v,i) in stats.by_operation" :key="i">{{ v[0] }}: {{ v[1] }}</div>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="8">
          <a-card size="小" title="按表">
            <div v-for="(v,i) in stats.by_table" :key="i">{{ v[0] }}: {{ v[1] }}</div>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="8">
          <a-card size="small" title="按用户">
            <div v-for="(v,i) in stats.by_user" :key="i">{{ v[0] }}: {{ v[1] }}</div>
          </a-card>
        </a-col>
      </a-row>

      <a-table :dataSource="logs" :columns="columns" rowKey="id" :pagination="pagination">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key==='action'">
            <a-space>
              <a-button type="link" @click="router.push(`/audit/logs/${record.id}`)">详情</a-button>
            </a-space>
          </template>
          <template v-else-if="column.dataIndex==='new_data'">
            <a-tag v-if="extractSeverity(record.new_data)" :color="severityColor(extractSeverity(record.new_data))">{{ extractSeverity(record.new_data) }}</a-tag>
          </template>
        </template>
      </a-table>
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
const operation = ref('')
const router = useRouter()
const stats = ref<any>({ by_operation: [], by_table: [], by_user: [] })
const pagination = { pageSize: 10 }
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id' },
  { title: '操作类型', dataIndex: 'operation_type', key: 'operation_type' },
  { title: '表', dataIndex: 'table_name', key: 'table_name' },
  { title: '记录ID', dataIndex: 'record_id', key: 'record_id' },
  { title: '用户ID', dataIndex: 'user_id', key: 'user_id' },
  { title: '时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '新数据', dataIndex: 'new_data', key: 'new_data' },
  { title: '操作', key: 'action' },
]

const fetch = async () => {
  const params: any = {}
  if (start.value) params.start = start.value
  if (end.value) params.end = end.value
  if (user.value) params.user_id = user.value
  if (operation.value) params.operation_type = operation.value
  logs.value = await getAuditLogs(params)
  try {
    const res = await (await import('@/api/audit')).default.get('/audit/stats')
    stats.value = res.data
  } catch {}
}

fetch()

const exportCsv = async () => {
  const params: any = {}
  if (start.value) params.start = start.value
  if (end.value) params.end = end.value
  if (user.value) params.user_id = user.value
  if (operation.value) params.operation_type = operation.value
  const blob = await exportAuditLogs(params)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `audit-logs.csv`
  a.click()
  URL.revokeObjectURL(url)
}

function extractSeverity(newData?: string) {
  try { const obj = JSON.parse(newData || '{}'); return obj.severity } catch { return null }
}
function severityColor(s?: string) {
  switch (s) {
    case 'critical': return 'red'
    case 'high': return 'volcano'
    case 'medium': return 'orange'
    case 'low': return 'green'
    default: return 'blue'
  }
}
</script>