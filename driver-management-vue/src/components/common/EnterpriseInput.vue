<template>
  <div class="enterprise-input-wrapper">
    <label v-if="label" :for="inputId" class="enterprise-input-label">
      {{ label }}
      <span v-if="required" class="required-indicator">*</span>
    </label>

    <div class="enterprise-input-container">
      <component
        v-if="prefixIcon"
        :is="prefixIcon"
        class="input-prefix-icon"
      />

      <input
        :id="inputId"
        ref="inputRef"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :maxlength="maxlength"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        @keydown="handleKeydown"
      />

      <component
        v-if="suffixIcon"
        :is="suffixIcon"
        class="input-suffix-icon"
      />

      <button
        v-if="clearable && modelValue"
        type="button"
        class="input-clear-btn"
        @click="handleClear"
      >
        <CloseCircleOutlined />
      </button>
    </div>

    <div v-if="error" class="enterprise-input-error">
      {{ error }}
    </div>

    <div v-else-if="helperText" class="enterprise-input-helper">
      {{ helperText }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, nextTick } from 'vue'
import { CloseCircleOutlined } from '@ant-design/icons-vue'

interface Props {
  modelValue?: string | number
  label?: string
  placeholder?: string
  type?: 'text' | 'password' | 'email' | 'number' | 'tel'
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  clearable?: boolean
  error?: string
  helperText?: string
  maxlength?: number
  prefixIcon?: any
  suffixIcon?: any
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  readonly: false,
  required: false,
  clearable: false,
  size: 'md'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  input: [event: Event]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
  clear: []
  keydown: [event: KeyboardEvent]
}>()

const inputRef = ref<HTMLInputElement>()
const isFocused = ref(false)

const inputId = computed(() => `enterprise-input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => [
  'enterprise-input',
  `enterprise-input--${props.size}`,
  {
    'enterprise-input--disabled': props.disabled,
    'enterprise-input--readonly': props.readonly,
    'enterprise-input--error': props.error,
    'enterprise-input--focused': isFocused.value,
    'enterprise-input--with-prefix': props.prefixIcon,
    'enterprise-input--with-suffix': props.suffixIcon || props.clearable
  }
])

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
  emit('input', event)
}

const handleBlur = (event: FocusEvent) => {
  isFocused.value = false
  emit('blur', event)
}

const handleFocus = (event: FocusEvent) => {
  isFocused.value = true
  emit('focus', event)
}

const handleClear = () => {
  emit('update:modelValue', '')
  emit('clear')
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleKeydown = (event: KeyboardEvent) => {
  emit('keydown', event)
}

// 暴露方法给父组件
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  select: () => inputRef.value?.select()
})
</script>

<style scoped>
.enterprise-input-wrapper {
  width: 100%;
}

.enterprise-input-label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
  line-height: 1.4;
}

.required-indicator {
  color: var(--color-error);
  margin-left: 2px;
}

.enterprise-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.enterprise-input {
  width: 100%;
  border: var(--input-border-width) solid var(--input-border-color);
  border-radius: var(--input-border-radius);
  background-color: var(--color-bg-container);
  color: var(--color-text-primary);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  line-height: 1.4;
  transition: all var(--duration-fast) var(--ease-out);
  outline: none;
  box-sizing: border-box;
}

.enterprise-input::placeholder {
  color: var(--color-text-tertiary);
}

/* 尺寸变体 */
.enterprise-input--sm {
  height: var(--input-height-sm);
  padding: 4px 8px;
  font-size: var(--font-size-xs);
}

.enterprise-input--md {
  height: var(--input-height-md);
  padding: var(--input-padding);
  font-size: var(--font-size-sm);
}

.enterprise-input--lg {
  height: var(--input-height-lg);
  padding: 12px 16px;
  font-size: var(--font-size-base);
}

/* 状态样式 */
.enterprise-input:hover:not(.enterprise-input--disabled):not(.enterprise-input--readonly) {
  border-color: var(--color-primary-300);
}

.enterprise-input:focus {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.enterprise-input--error {
  border-color: var(--color-error);
}

.enterprise-input--error:focus {
  border-color: var(--color-error);
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.1);
}

.enterprise-input--disabled {
  background-color: var(--disabled-bg);
  color: var(--disabled-color);
  cursor: not-allowed;
}

.enterprise-input--readonly {
  background-color: var(--color-gray-50);
  cursor: default;
}

/* 前缀和后缀图标 */
.enterprise-input--with-prefix {
  padding-left: 36px;
}

.enterprise-input--with-suffix {
  padding-right: 36px;
}

.enterprise-input--with-prefix.enterprise-input--sm {
  padding-left: 28px;
}

.enterprise-input--with-suffix.enterprise-input--sm {
  padding-right: 28px;
}

.enterprise-input--with-prefix.enterprise-input--lg {
  padding-left: 44px;
}

.enterprise-input--with-suffix.enterprise-input--lg {
  padding-right: 44px;
}

.input-prefix-icon,
.input-suffix-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  font-size: 14px;
  pointer-events: none;
}

.input-prefix-icon {
  left: 12px;
}

.input-suffix-icon {
  right: 12px;
}

.input-clear-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  cursor: pointer;
  padding: 2px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-out);
}

.input-clear-btn:hover {
  color: var(--color-text-secondary);
  background-color: var(--color-gray-100);
}

/* 错误和帮助文本 */
.enterprise-input-error {
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-error);
  line-height: 1.3;
}

.enterprise-input-helper {
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  line-height: 1.3;
}
</style>