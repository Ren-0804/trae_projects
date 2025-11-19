<template>
  <div style="padding:16px">
    <a-card :title="title" :extra="extra">
      <div v-if="isImage(file?.mime_type)" style="text-align:center">
        <a-image :src="fileUrl" :alt="file?.name" style="max-height:380px" />
      </div>
      <div v-else-if="isPdf(file?.mime_type)" style="height:380px">
        <iframe :src="fileUrl" style="width:100%;height:100%;border:none"></iframe>
      </div>
      <a-descriptions bordered :column="1" style="margin-top:12px">
        <a-descriptions-item label="名称">{{ file?.name }}</a-descriptions-item>
        <a-descriptions-item label="类型">{{ file?.mime_type }}</a-descriptions-item>
        <a-descriptions-item label="大小">{{ formatSize(file?.size) }}</a-descriptions-item>
        <a-descriptions-item label="版本">{{ file?.version }}</a-descriptions-item>
        <a-descriptions-item label="关联">{{ file?.related_type }}#{{ file?.related_id }}</a-descriptions-item>
        <a-descriptions-item label="上传者">{{ file?.uploader_id }}</a-descriptions-item>
        <a-descriptions-item label="路径">{{ file?.path }}</a-descriptions-item>
      </a-descriptions>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h, resolveComponent } from 'vue'
import { useRoute } from 'vue-router'
import { getFile } from '@/api/files'

const route = useRoute()
const id = Number(String(route.params.id))
const file = ref<any>(null)
const title = `文件详情 #${id}`
const base = (import.meta as any).env?.VITE_API_BASE_URL?.replace('/api/v1','') || ''
const isImage = (mime?: string) => !!mime && mime.startsWith('image/')
const isPdf = (mime?: string) => mime === 'application/pdf'
const formatSize = (s?: number) => s ? `${(s/1024).toFixed(1)} KB` : ''
const fileUrl = ref('')

const extra = h('div', null, [
  h(resolveComponent('a-button'), { type:'link', href:fileUrl.value, target:'_blank' }, '打开'),
  h(resolveComponent('a-button'), { type:'link', danger:true, onClick: async ()=>{ const { deleteFile } = await import('@/api/files'); await deleteFile(id); history.back() } }, '删除')
])

onMounted(async () => {
  file.value = await getFile(id)
  fileUrl.value = `${base}${file.value?.path || ''}`
})
</script>
