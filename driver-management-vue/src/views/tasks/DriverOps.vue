<template>
  <div style="padding:16px">
    <a-card title="司机任务">
      <a-list :data-source="tasks" bordered :renderItem="renderItem" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useTaskStore } from '@/stores/tasks'

const store = useTaskStore()
const tasks = computed(() => store.tasks)

const renderItem = ({ item }: any) => {
  return (window as any).h('div', { style: 'padding:8px' }, `${item.id} ${item.status}`)
}

onMounted(() => store.fetchTasks('onroad'))
</script>