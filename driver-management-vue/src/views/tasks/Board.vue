<template>
  <div style="padding:16px">
    <a-card title="任务看板">
      <a-segmented v-model:value="status" :options="options" style="margin-bottom:16px" />
      <a-list :data-source="tasks" :loading="loading" bordered>
        <template #renderItem="{ item }">
          <a-list-item>
            <div>{{ item.id }} {{ item.customer || '' }}</div>
            <a-button type="link" @click="router.push(`/tasks/${item.id}`)">查看</a-button>
          </a-list-item>
        </template>
      </a-list>
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

onMounted(() => store.fetchTasks(status.value))
</script>