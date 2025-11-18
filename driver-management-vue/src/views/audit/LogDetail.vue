<template>
  <div style="padding:16px">
    <a-card :title="title">
      <a-descriptions bordered :column="1" style="margin-bottom:12px">
        <a-descriptions-item label="操作类型">{{ log?.operation_type }}</a-descriptions-item>
        <a-descriptions-item label="表">{{ log?.table_name }}</a-descriptions-item>
        <a-descriptions-item label="记录ID">{{ log?.record_id }}</a-descriptions-item>
        <a-descriptions-item label="用户ID">{{ log?.user_id }}</a-descriptions-item>
        <a-descriptions-item label="时间">{{ log?.created_at }}</a-descriptions-item>
        <a-descriptions-item label="哈希">{{ log?.hash }}</a-descriptions-item>
        <a-descriptions-item label="前置哈希">{{ log?.prev_hash }}</a-descriptions-item>
      </a-descriptions>
      <a-row :gutter="12">
        <a-col :xs="24" :md="12">
          <a-card size="small" title="旧数据">
            <pre>{{ pretty(old) }}</pre>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12">
          <a-card size="small" title="新数据">
            <pre>{{ pretty(newd) }}</pre>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getAuditLog } from '@/api/audit'

const route = useRoute()
const id = Number(String(route.params.id))
const log = ref<any>(null)
const title = `日志详情 #${id}`
const old = ref<any>(null)
const newd = ref<any>(null)
const pretty = (obj:any) => {
  try { return JSON.stringify(obj ? JSON.parse(obj) : {}, null, 2) } catch { return obj }
}

onMounted(async () => {
  log.value = await getAuditLog(id)
  old.value = log.value?.old_data
  newd.value = log.value?.new_data
})
</script>