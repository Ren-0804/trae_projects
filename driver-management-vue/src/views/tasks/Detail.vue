<template>
  <div style="padding:16px">
    <a-card :title="`任务详情 #${id}`">
      <pre>{{ JSON.stringify(task, null, 2) }}</pre>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/tasks'

const route = useRoute()
const store = useTaskStore()
const id = Number(String(route.params.id))
const task = computed(() => store.current)

onMounted(() => store.fetchTask(id))
</script>