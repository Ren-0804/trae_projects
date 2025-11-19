<template>
  <Transition name="toast" appear>
    <div v-if="visible" :class="toastClasses">
      <component :is="iconMap[type]" class="toast-icon" />
      <div class="toast-content">
        <div v-if="title" class="toast-title">{{ title }}</div>
        <div class="toast-message">{{ message }}</div>
      </div>
      <button class="toast-close" @click="close">
        <CloseOutlined />
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  CheckCircleOutlined,
  InfoCircleOutlined,
  ExclamationCircleOutlined,
  CloseCircleOutlined,
  CloseOutlined
} from '@ant-design/icons-vue'

interface Props {
  id?: string
  type?: 'success' | 'info' | 'warning' | 'error'
  title?: string
  message: string
  duration?: number
  closable?: boolean
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 4000,
  closable: true,
  position: 'top-right'
})

const emit = defineEmits<{
  close: []
}>()

const visible = ref(false)
let timer: NodeJS.Timeout | null = null

const iconMap = {
  success: CheckCircleOutlined,
  info: InfoCircleOutlined,
  warning: ExclamationCircleOutlined,
  error: CloseCircleOutlined
}

const toastClasses = computed(() => [
  'enterprise-toast',
  `enterprise-toast--${props.type}`,
  `enterprise-toast--${props.position}`
])

const close = () => {
  visible.value = false
  emit('close')
}

const startTimer = () => {
  if (props.duration > 0) {
    timer = setTimeout(() => {
      close()
    }, props.duration)
  }
}

const clearTimer = () => {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
}

onMounted(() => {
  visible.value = true
  startTimer()
})

onUnmounted(() => {
  clearTimer()
})

// 暴露方法
defineExpose({
  close,
  restartTimer: () => {
    clearTimer()
    startTimer()
  }
})
</script>

<style scoped>
.enterprise-toast {
  position: fixed;
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  background-color: var(--color-bg-container);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-3);
  padding: var(--spacing-md);
  min-width: 320px;
  max-width: 480px;
  z-index: var(--z-index-tooltip);
  backdrop-filter: blur(8px);
}

/* 位置定位 */
.enterprise-toast--top-right {
  top: var(--spacing-lg);
  right: var(--spacing-lg);
}

.enterprise-toast--top-left {
  top: var(--spacing-lg);
  left: var(--spacing-lg);
}

.enterprise-toast--bottom-right {
  bottom: var(--spacing-lg);
  right: var(--spacing-lg);
}

.enterprise-toast--bottom-left {
  bottom: var(--spacing-lg);
  left: var(--spacing-lg);
}

/* 类型样式 */
.enterprise-toast--success {
  border-left: 4px solid var(--color-success);
}

.enterprise-toast--success .toast-icon {
  color: var(--color-success);
}

.enterprise-toast--info {
  border-left: 4px solid var(--color-info);
}

.enterprise-toast--info .toast-icon {
  color: var(--color-info);
}

.enterprise-toast--warning {
  border-left: 4px solid var(--color-warning);
}

.enterprise-toast--warning .toast-icon {
  color: var(--color-warning);
}

.enterprise-toast--error {
  border-left: 4px solid var(--color-error);
}

.enterprise-toast--error .toast-icon {
  color: var(--color-error);
}

/* 内容样式 */
.toast-icon {
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 1px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 2px;
  line-height: 1.3;
}

.toast-message {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
  word-wrap: break-word;
}

.toast-close {
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  cursor: pointer;
  padding: 2px;
  border-radius: var(--radius-xs);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-out);
  flex-shrink: 0;
}

.toast-close:hover {
  color: var(--color-text-primary);
  background-color: var(--color-gray-100);
}

/* 动画效果 */
.toast-enter-active {
  transition: all var(--duration-base) var(--ease-out);
}

.toast-leave-active {
  transition: all var(--duration-fast) var(--ease-in);
}

.toast-enter-from.enterprise-toast--top-right,
.toast-leave-to.enterprise-toast--top-right {
  transform: translateX(100%);
  opacity: 0;
}

.toast-enter-from.enterprise-toast--top-left,
.toast-leave-to.enterprise-toast--top-left {
  transform: translateX(-100%);
  opacity: 0;
}

.toast-enter-from.enterprise-toast--bottom-right,
.toast-leave-to.enterprise-toast--bottom-right {
  transform: translateX(100%);
  opacity: 0;
}

.toast-enter-from.enterprise-toast--bottom-left,
.toast-leave-to.enterprise-toast--bottom-left {
  transform: translateX(-100%);
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .enterprise-toast {
    min-width: 280px;
    max-width: calc(100vw - var(--spacing-xl));
    left: var(--spacing-md) !important;
    right: var(--spacing-md) !important;
  }

  .enterprise-toast--top-right,
  .enterprise-toast--top-left {
    top: var(--spacing-md);
  }

  .enterprise-toast--bottom-right,
  .enterprise-toast--bottom-left {
    bottom: var(--spacing-md);
  }
}
</style>