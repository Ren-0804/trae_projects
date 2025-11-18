<template>
  <a-card :title="task.title" size="small" style="margin-bottom:8px" :draggable="draggable" @dragstart="$emit('dragstart')">
    <div>{{ task.description }}</div>
    <a-space style="margin-top:8px">
      <a-tag>{{ task.priority }}</a-tag>
      <a-tag v-if="task.assignee_id">负责人: {{ task.assignee_id }}</a-tag>
    </a-space>
    <a-space style="margin-top:8px">
      <a-button size="small" @click="openEdit">编辑</a-button>
      <a-button size="small" danger @click="remove">删除</a-button>
    </a-space>
    <a-modal v-model:open="editOpen" title="编辑任务" @ok="save">
      <a-form layout="vertical">
        <a-form-item label="标题">
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
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import { message } from 'ant-design-vue'

const props = defineProps<{ task: any; draggable?: boolean }>()
const emit = defineEmits(['dragstart','update'])
const store = useTaskStore()
const editOpen = ref(false)
const form = ref<any>({ title: '', description: '', priority: 'medium' })

const openEdit = () => {
  editOpen.value = true
  form.value = { title: props.task.title, description: props.task.description, priority: props.task.priority }
}
const save = async () => {
  try { await store.update(props.task.id, form.value); editOpen.value = false; message.success('已保存'); emit('update') } catch(e:any){ message.error(e?.response?.data?.detail || '保存失败') }
}
const remove = async () => {
  try { await store.remove(props.task.id); message.success('已删除'); emit('update') } catch(e:any){ message.error(e?.response?.data?.detail || '删除失败') }
}
</script>