<template>
  <div style="padding:16px">
    <a-card title="文件库">
      <a-space style="margin-bottom:12px" wrap>
        <a-input-search v-model:value="keyword" placeholder="搜索名称或类型" @search="fetch" style="min-width:220px" />
        <a-select v-model:value="type" placeholder="类型" style="min-width:140px" @change="fetch">
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="image">图片</a-select-option>
          <a-select-option value="pdf">PDF</a-select-option>
          <a-select-option value="other">其他</a-select-option>
        </a-select>
        <a-input v-model:value="relatedType" placeholder="关联类型" style="min-width:160px" />
        <a-input v-model:value="relatedId" placeholder="关联ID" style="min-width:120px" />
        <a-button type="primary" @click="fetch">筛选</a-button>
      </a-space>

      <a-upload-dragger :multiple="true" :customRequest="handleUpload" style="margin-bottom:12px">
        <p class="ant-upload-drag-icon"></p>
        <p class="ant-upload-text">点击或拖拽文件到此区域上传</p>
        <p class="ant-upload-hint">支持批量上传，图片/PDF/其他类型</p>
      </a-upload-dragger>

      <a-row :gutter="12">
        <a-col v-for="item in files" :key="item.id" :xs="24" :md="8" :lg="6">
          <a-card :title="item.name" size="small" :extra="extraActions(item)">
            <div v-if="isImage(item.mime_type)" style="text-align:center">
              <a-image :src="fileUrl(item)" :alt="item.name" style="max-height:180px" />
            </div>
            <div v-else-if="isPdf(item.mime_type)" style="height:180px">
              <iframe :src="fileUrl(item)" style="width:100%;height:100%;border:none"></iframe>
            </div>
            <div v-else>
              <a-typography-text type="secondary">{{ item.mime_type || '未知类型' }} · {{ formatSize(item.size) }}</a-typography-text>
            </div>
            <div style="margin-top:8px">
              <a-tag v-if="item.version">v{{ item.version }}</a-tag>
              <a-tag v-if="item.related_type">{{ item.related_type }}#{{ item.related_id }}</a-tag>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, h, resolveComponent } from 'vue'
import { getFiles, uploadFile, getFile, deleteFile } from '@/api/files'
import { useRouter } from 'vue-router'

const files = ref<any[]>([])
const keyword = ref('')
const type = ref('all')
const relatedType = ref('')
const relatedId = ref('')
const router = useRouter()

const fetch = async () => {
  const params: any = {}
  if (keyword.value) params.q = keyword.value
  if (relatedType.value) params.related_type = relatedType.value
  if (relatedId.value) params.related_id = relatedId.value
  const list = await getFiles(params)
  files.value = list.filter((f:any) => {
    if (type.value === 'all') return true
    if (type.value === 'image') return isImage(f.mime_type)
    if (type.value === 'pdf') return isPdf(f.mime_type)
    return !isImage(f.mime_type) && !isPdf(f.mime_type)
  })
}

const isImage = (mime?: string) => !!mime && mime.startsWith('image/')
const isPdf = (mime?: string) => mime === 'application/pdf'
const formatSize = (s?: number) => s ? `${(s/1024).toFixed(1)} KB` : ''
const base = (import.meta as any).env?.VITE_API_BASE_URL?.replace('/api/v1','') || ''
const fileUrl = (item:any) => `${base}${item.path}`

const handleUpload = async (opts: any) => {
  const file: File = opts.file
  const fd = new FormData()
  fd.append('upload', file)
  if (relatedType.value) fd.append('related_type', relatedType.value)
  if (relatedId.value) fd.append('related_id', relatedId.value)
  try {
    await uploadFile(fd)
    opts.onSuccess?.({}, file)
    await fetch()
  } catch (e:any) {
    opts.onError?.(e)
  }
}

const extraActions = (item:any) => h('div', null, [
  h(resolveComponent('a-button'), { type:'link', onClick: ()=>router.push(`/files/${item.id}`) }, '详情'),
  h(resolveComponent('a-button'), { type:'link', danger:true, onClick: ()=>remove(item.id) }, '删除')
])

const remove = async (id:number) => {
  await deleteFile(id)
  await fetch()
}

fetch()
</script>