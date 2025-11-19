<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
  >
    <component v-if="loading" :is="LoadingOutlined" class="btn-icon--spin" />
    <component v-else-if="icon" :is="icon" class="btn-icon" />
    <span v-if="$slots.default" class="btn-text">
      <slot />
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { LoadingOutlined } from '@ant-design/icons-vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'text' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  icon?: any
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  block: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => [
  'enterprise-btn',
  `enterprise-btn--${props.variant}`,
  `enterprise-btn--${props.size}`,
  {
    'enterprise-btn--disabled': props.disabled,
    'enterprise-btn--loading': props.loading,
    'enterprise-btn--block': props.block,
    'enterprise-btn--icon-only': props.icon && !$slots.default
  }
])

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.enterprise-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  border: 1px solid transparent;
  border-radius: var(--radius-base);
  font-family: var(--font-family);
  font-weight: 500;
  line-height: 1.4;
  text-decoration: none;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  white-space: nowrap;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.enterprise-btn:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* 尺寸变体 */
.enterprise-btn--sm {
  height: var(--button-height-sm);
  padding: var(--button-padding-sm);
  font-size: var(--font-size-xs);
}

.enterprise-btn--md {
  height: var(--button-height-md);
  padding: var(--button-padding-md);
  font-size: var(--font-size-sm);
}

.enterprise-btn--lg {
  height: var(--button-height-lg);
  padding: var(--button-padding-lg);
  font-size: var(--font-size-base);
}

/* 主要按钮 */
.enterprise-btn--primary {
  background-color: var(--color-primary-500);
  color: white;
  border-color: var(--color-primary-500);
}

.enterprise-btn--primary:hover:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-primary-600);
  border-color: var(--color-primary-600);
}

.enterprise-btn--primary:active:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-primary-700);
  border-color: var(--color-primary-700);
}

/* 次要按钮 */
.enterprise-btn--secondary {
  background-color: var(--color-bg-container);
  color: var(--color-text-primary);
  border-color: var(--color-border);
}

.enterprise-btn--secondary:hover:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-gray-50);
  border-color: var(--color-gray-300);
}

.enterprise-btn--secondary:active:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-400);
}

/* 文字按钮 */
.enterprise-btn--text {
  background-color: transparent;
  color: var(--color-primary-600);
  border-color: transparent;
  padding-left: 0;
  padding-right: 0;
}

.enterprise-btn--text:hover:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-primary-50);
  color: var(--color-primary-700);
}

.enterprise-btn--text:active:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: var(--color-primary-100);
}

/* 危险按钮 */
.enterprise-btn--danger {
  background-color: var(--color-error);
  color: white;
  border-color: var(--color-error);
}

.enterprise-btn--danger:hover:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: #ff7875;
  border-color: #ff7875;
}

.enterprise-btn--danger:active:not(.enterprise-btn--disabled):not(.enterprise-btn--loading) {
  background-color: #d9363e;
  border-color: #d9363e;
}

/* 禁用状态 */
.enterprise-btn--disabled {
  background-color: var(--disabled-bg);
  color: var(--disabled-color);
  border-color: var(--disabled-border);
  cursor: not-allowed;
}

/* 加载状态 */
.enterprise-btn--loading {
  cursor: wait;
}

/* 块级按钮 */
.enterprise-btn--block {
  width: 100%;
}

/* 仅图标按钮 */
.enterprise-btn--icon-only {
  padding: 0;
  width: var(--button-height-md);
}

.enterprise-btn--icon-only.enterprise-btn--sm {
  width: var(--button-height-sm);
}

.enterprise-btn--icon-only.enterprise-btn--lg {
  width: var(--button-height-lg);
}

.btn-icon {
  font-size: 1em;
}

.btn-icon--spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.btn-text {
  display: inline-block;
}
</style>