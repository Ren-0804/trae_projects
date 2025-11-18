<template>
  <div style="padding:16px">
  <a-card :title="`任务流程 #${id}`">
      <a-descriptions bordered :column="1" style="margin-bottom:12px">
        <a-descriptions-item label="编号">{{ task?.task_no }}</a-descriptions-item>
        <a-descriptions-item label="标题">{{ task?.title }}</a-descriptions-item>
        <a-descriptions-item label="负责人">{{ task?.assignee_id }}</a-descriptions-item>
        <a-descriptions-item label="起点">{{ task?.origin_address }}</a-descriptions-item>
        <a-descriptions-item label="终点">{{ task?.destination_address }}</a-descriptions-item>
        <a-descriptions-item label="预估">{{ task?.estimated_distance_km }} km / {{ task?.estimated_duration_min }} min</a-descriptions-item>
      </a-descriptions>

      <a-steps :current="currentIndex" style="margin-bottom:12px">
        <a-step title="准备出发" />
        <a-step title="到达装货地" />
        <a-step title="运输中" />
        <a-step title="到达卸货地" />
        <a-step title="任务完成" />
      </a-steps>

      <a-space>
        <a-popconfirm title="确认准备出发？" @confirm="setStatus('ready_departure')"><a-button type="primary">准备出发</a-button></a-popconfirm>
        <a-popconfirm title="确认到达装货地？" @confirm="setStatus('arrived_pickup')"><a-button>到达装货地</a-button></a-popconfirm>
        <a-popconfirm title="确认开始运输？" @confirm="setStatus('in_transit')"><a-button>运输中</a-button></a-popconfirm>
        <a-popconfirm title="确认到达卸货地？" @confirm="setStatus('arrived_dropoff')"><a-button>到达卸货地</a-button></a-popconfirm>
        <a-popconfirm title="确认完成任务？" @confirm="setStatus('completed')"><a-button type="dashed">任务完成</a-button></a-popconfirm>
      </a-space>

      <a-form layout="vertical" style="margin-top:12px">
        <a-form-item label="备注">
          <a-textarea v-model:value="remark" rows="3" />
        </a-form-item>
        <a-upload :customRequest="uploadAttachment" :multiple="true">
          <a-button>上传附件</a-button>
        </a-upload>
      </a-form>

      <a-card title="路线地图" style="margin-top:12px">
        <div style="height:300px;background:#f5f5f5;border-radius:8px;display:flex;align-items:center;justify-content:center">
          <div>
            <div>当前位置: {{ lastLocation?.lat }}, {{ lastLocation?.lng }}</div>
            <div>状态: {{ task?.status }}</div>
            <div>ETA(估算): {{ etaText }}</div>
          </div>
        </div>
      </a-card>

      <a-card title="时间线" style="margin-top:12px">
        <pre>{{ JSON.stringify(report?.timeline || [], null, 2) }}</pre>
      </a-card>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/tasks'
import { message } from 'ant-design-vue'
import api from '@/api/auth'

const route = useRoute()
const id = Number(String(route.params.id))
const store = useTaskStore()
const task = computed(()=>store.current)
const report = ref<any>(null)
const remark = ref('')
const statusOrder = ['ready_departure','arrived_pickup','in_transit','arrived_dropoff','completed']
const currentIndex = computed(()=>Math.max(0, statusOrder.indexOf(String(task.value?.status || 'ready_departure'))))
const lastLocation = ref<any>(null)
const etaText = computed(()=>{
  if (!task.value?.estimated_duration_min) return '-'
  const base = Number(task.value?.estimated_duration_min)
  return `${base} 分钟(示意)`
})

const setStatus = async (s: string) => {
  try { await api.post(`/tasks/${id}/status`, { status:s, remark: remark.value }); await refresh(); message.success('状态已更新') } catch(e:any){ message.error(e?.response?.data?.detail || '更新失败') }
}
const uploadAttachment = async (opts: any) => {
  const fd = new FormData(); fd.append('upload', opts.file); fd.append('related_type','task'); fd.append('related_id', String(id));
  try { await (await import('@/api/files')).uploadFile(fd); opts.onSuccess?.({}); } catch(e:any){ opts.onError?.(e) }
}
const refresh = async () => { await store.fetchTask(id); const r = await api.get(`/tasks/${id}/report`); report.value = r.data }

onMounted(refresh)

// SSE订阅
onMounted(async () => {
  try {
    const base = (import.meta as any).env?.VITE_API_BASE_URL || ''
    const url = `${base}/tasks/${id}/sse`
    const es = new EventSource(url)
    es.onmessage = (ev) => { try { const d = JSON.parse(ev.data); lastLocation.value = d.location } catch {} }
  } catch {}
})
</script>