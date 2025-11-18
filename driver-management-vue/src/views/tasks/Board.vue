<template>
  <div style="padding:16px">
    <a-card title="任务看板">
      <a-segmented v-model:value="status" :options="options" style="margin-bottom:16px" />
      <a-list :data-source="tasks" :loading="loading" bordered :renderItem="renderItem" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import { useRouter } from 'vue-router'

const store = useTaskStore()
const router = useRouter()
const status = ref<string>('draft')
const options = ['draft','assigned','accepted','onroad','arrived','completed','abnormal']
const tasks = computed(() => store.tasks)
const loading = computed(() => store.loading)

const renderItem = ({ item }: any) => {
  return (window as any).h('div', { style: 'padding:8px' }, [
    (window as any).h('div', null, `${item.id} ${item.customer || ''}`),
    (window as any).h((window as any).resolveComponent('a-button'), { type: 'link', onClick: () => router.push(`/tasks/${item.id}`) }, '查看')
  ])
}

onMounted(() => store.fetchTasks(status.value))
</script>