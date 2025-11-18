import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTasks, getTask, createTask, assignTask, postTaskEvent } from '@/api/tasks'
import { log, alert } from '@/utils/auditLogger'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<any[]>([])
  const current = ref<any | null>(null)
  const loading = ref(false)

  async function fetchTasks(status?: string) {
    loading.value = true
    try {
      tasks.value = await getTasks(status ? { status } : undefined)
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(id: number) {
    loading.value = true
    try {
      current.value = await getTask(id)
      return current.value
    } finally {
      loading.value = false
    }
  }

  async function create(data: any) {
    loading.value = true
    try {
      const t = await createTask(data)
      tasks.value.unshift(t)
      await log('task.create', 'task', t.id, { status: t.status })
      return t
    } finally {
      loading.value = false
    }
  }

  async function assign(id: number, payload: any) {
    await assignTask(id, payload)
    await log('task.assign', 'task', id, payload)
  }

  async function addEvent(id: number, event: any) {
    await postTaskEvent(id, event)
    if (event?.type === 'abnormal') {
      await alert('task.abnormal', 'task', id, event?.description || '任务异常', 'critical')
    } else {
      await log('task.event', 'task', id, event)
    }
  }

  return { tasks, current, loading, fetchTasks, fetchTask, create, assign, addEvent }
})