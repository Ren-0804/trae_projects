<template>
  <div style="padding:16px">
    <a-card :title="title">
      <pre>{{ JSON.stringify(log, null, 2) }}</pre>
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

onMounted(async () => {
  log.value = await getAuditLog(id)
})
</script>