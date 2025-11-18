<template>
  <div style="padding:16px">
    <a-card title="文件库">
      <a-input-search v-model:value="keyword" placeholder="搜索" @search="fetch" style="margin-bottom:12px" />
      <a-list :data-source="files" bordered :renderItem="renderItem" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { getFiles } from '@/api/files'
import { useRouter } from 'vue-router'

const files = ref<any[]>([])
const keyword = ref('')
const router = useRouter()

const renderItem = ({ item }: any) => {
  return (window as any).h('div', { style: 'padding:8px' }, [
    (window as any).h('span', null, `${item.id} ${item.name || ''}`),
    (window as any).h((window as any).resolveComponent('a-button'), { type: 'link', onClick: () => router.push(`/files/${item.id}`) }, '查看')
  ])
}

const fetch = async () => {
  files.value = await getFiles(keyword.value ? { q: keyword.value } : undefined)
}

fetch()
</script>