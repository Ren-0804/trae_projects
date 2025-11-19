<template>
  <div :class="cardClasses">
    <div v-if="showHeader" class="enterprise-card-header">
      <div class="enterprise-card-title">
        <component v-if="headerIcon" :is="headerIcon" class="header-icon" />
        <h3 v-if="title" class="title-text">{{ title }}</h3>
        <slot name="title" />
      </div>

      <div v-if="$slots.extra" class="enterprise-card-extra">
        <slot name="extra" />
      </div>
    </div>

    <div v-if="$slots.default" class="enterprise-card-body">
      <slot />
    </div>

    <div v-if="$slots.actions" class="enterprise-card-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  headerIcon?: any
  variant?: 'default' | 'bordered' | 'shadow'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  padding: 'lg',
  hoverable: false,
  loading: false
})

const showHeader = computed(() => props.title || props.headerIcon || !!props.$slots?.title || !!props.$slots?.extra)

const cardClasses = computed(() => [
  'enterprise-card',
  `enterprise-card--${props.variant}`,
  `enterprise-card--padding-${props.padding}`,
  {
    'enterprise-card--hoverable': props.hoverable,
    'enterprise-card--loading': props.loading
  }
])
</script>

<style scoped>
.enterprise-card {
  background-color: var(--card-bg);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden;
  transition: all var(--duration-fast) var(--ease-out);
  border: 1px solid var(--color-border-light);
}

.enterprise-card--bordered {
  border: 1px solid var(--color-border);
  box-shadow: none;
}

.enterprise-card--shadow {
  box-shadow: var(--shadow-2);
}

.enterprise-card--hoverable:hover {
  box-shadow: var(--shadow-3);
  transform: translateY(-2px);
}

.enterprise-card--loading {
  opacity: 0.7;
  pointer-events: none;
}

/* 内边距变体 */
.enterprise-card--padding-none .enterprise-card-body {
  padding: 0;
}

.enterprise-card--padding-sm .enterprise-card-body {
  padding: var(--spacing-sm);
}

.enterprise-card--padding-md .enterprise-card-body {
  padding: var(--spacing-md);
}

.enterprise-card--padding-lg .enterprise-card-body {
  padding: var(--card-padding);
}

/* 头部样式 */
.enterprise-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) var(--card-padding) 0;
  margin-bottom: var(--spacing-md);
}

.enterprise-card-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
  min-width: 0;
}

.header-icon {
  color: var(--color-primary-500);
  font-size: 18px;
  flex-shrink: 0;
}

.title-text {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.enterprise-card-extra {
  flex-shrink: 0;
  margin-left: var(--spacing-md);
}

/* 主体内容 */
.enterprise-card-body {
  color: var(--color-text-primary);
  line-height: 1.6;
}

/* 操作区域 */
.enterprise-card-actions {
  padding: 0 var(--card-padding) var(--spacing-lg);
  margin-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

.enterprise-card--padding-sm .enterprise-card-header,
.enterprise-card--padding-sm .enterprise-card-actions {
  padding-left: var(--spacing-sm);
  padding-right: var(--spacing-sm);
}

.enterprise-card--padding-md .enterprise-card-header,
.enterprise-card--padding-md .enterprise-card-actions {
  padding-left: var(--spacing-md);
  padding-right: var(--spacing-md);
}

.enterprise-card--padding-none .enterprise-card-header,
.enterprise-card--padding-none .enterprise-card-actions {
  padding-left: 0;
  padding-right: 0;
}
</style>