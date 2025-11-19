<template>
  <div style="padding:16px">
    <a-row :gutter="16">
      <a-col :xs="24" :md="8">
        <a-card title="待办">
          <div class="kanban-column" @dragover.prevent @drop="onDrop('todo')">
            <TaskCard v-for="t in tasksByStatus('todo')" :key="t.id" :task="t" :draggable="true" @dragstart="onDragStart(t)" @update="refresh" />
          </div>
          <a-button type="dashed" block @click="openCreate('todo')">新建任务</a-button>
        </a-card>
      </a-col>
      <a-col :xs="24" :md="8">
        <a-card title="进行中">
          <div class="kanban-column" @dragover.prevent @drop="onDrop('in_progress')">
            <TaskCard v-for="t in tasksByStatus('in_progress')" :key="t.id" :task="t" :draggable="true" @dragstart="onDragStart(t)" @update="refresh" />
          </div>
          <a-button type="dashed" block @click="openCreate('in_progress')">新建任务</a-button>
        </a-card>
      </a-col>
      <a-col :xs="24" :md="8">
        <a-card title="已完成">
          <div class="kanban-column" @dragover.prevent @drop="onDrop('completed')">
            <TaskCard v-for="t in tasksByStatus('completed')" :key="t.id" :task="t" :draggable="true" @dragstart="onDragStart(t)" @update="refresh" />
          </div>
          <a-button type="dashed" block @click="openCreate('completed')">新建任务</a-button>
        </a-card>
      </a-col>
    </a-row>

    <a-modal v-model:open="createOpen" title="新建任务" @ok="create">
      <a-form layout="vertical">
        <a-form-item label="标题" required>
          <a-input v-model:value="form.title" />
        </a-form-item>
        <a-form-item label="描述">
          <a-textarea v-model:value="form.description" />
        </a-form-item>
        <a-form-item label="优先级">
          <a-select v-model:value="form.priority">
            <a-select-option value="low">低</a-select-option>
            <a-select-option value="medium">中</a-select-option>
            <a-select-option value="high">高</a-select-option>
            <a-select-option value="critical">紧急</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="截止日期">
          <a-date-picker v-model:value="form.due_date" />
        </a-form-item>
        <a-form-item label="负责人">
          <a-input v-model:value="form.assignee_id" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import { message } from 'ant-design-vue'
import TaskCard from '@/components/TaskCard.vue'

const store = useTaskStore()
const dragging = ref<any | null>(null)

const tasksByStatus = (s: string) => store.tasks.filter(t => String(t.status) === s).sort((a:any,b:any)=>a.sort_index-b.sort_index)

const onDragStart = (t: any) => { dragging.value = t }
const onDrop = async (status: string) => {
  if (!dragging.value) return
  const sortIndex = (tasksByStatus(status)[tasksByStatus(status).length-1]?.sort_index || 0) + 1
  await store.move(dragging.value.id, { status, sort_index: sortIndex })
  dragging.value = null
  await store.fetchTasks()
}

const createOpen = ref(false)
const form = ref<any>({ title: '', description: '', priority: 'medium', due_date: null, assignee_id: null, status: 'todo' })
const openCreate = (status: string) => { createOpen.value = true; form.value.status = status }
const create = async () => {
  try {
    const payload = { ...form.value, due_date: form.value.due_date ? new Date(form.value.due_date).toISOString() : null }
    await store.create(payload)
    createOpen.value = false
    form.value = { title: '', description: '', priority: 'medium', due_date: null, assignee_id: null, status: 'todo' }
    await store.fetchTasks()
  } catch (e:any) {
    message.error(e?.response?.data?.detail || '创建失败')
  }
}

const refresh = async () => store.fetchTasks()

onMounted(() => store.fetchTasks())
</script>

<style scoped>
.kanban-column { min-height: 300px }
</style>
