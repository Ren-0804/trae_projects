<template>
  <div>
    <slot v-if="!hasError" />
    <div v-else class="error-container">
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <h2 class="error-title">出错了</h2>
        <p class="error-message">{{ errorMessage }}</p>
        <div class="error-actions">
          <a-button type="primary" @click="resetError">重试</a-button>
          <a-button @click="goHome">返回首页</a-button>
        </div>
        <details v-if="errorDetails" class="error-details">
          <summary>详细信息</summary>
          <pre>{{ errorDetails }}</pre>
        </details>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'

const router = useRouter()

const hasError = ref(false)
const errorMessage = ref('')
const errorDetails = ref('')

const resetError = () => {
  hasError.value = false
  errorMessage.value = ''
  errorDetails.value = ''
}

const goHome = () => {
  router.push('/')
  resetError()
}

onErrorCaptured((error: any, instance: any, info: string) => {
  console.error('组件错误:', error)
  console.error('错误信息:', info)
  console.error('错误实例:', instance)
  
  hasError.value = true
  errorMessage.value = error?.message || '发生了未知错误'
  errorDetails.value = error?.stack || JSON.stringify(error, null, 2) || ''
  
  // 显示错误提示
  message.error(`组件错误: ${errorMessage.value}`)
  
  // 返回 false 阻止错误继续向上传播
  return false
})
</script>

<style scoped>
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 24px;
}

.error-content {
  text-align: center;
  max-width: 500px;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.error-message {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 16px;
}

.error-details {
  margin-top: 24px;
  text-align: left;
}

.error-details summary {
  cursor: pointer;
  color: #1890ff;
  margin-bottom: 8px;
}

.error-details pre {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>