import { createApp, App, ref, Component, h } from 'vue'
import EnterpriseToast from '@/components/common/EnterpriseToast.vue'

interface ToastOptions {
  type?: 'success' | 'info' | 'warning' | 'error'
  title?: string
  message: string
  duration?: number
  closable?: boolean
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
}

interface ToastInstance {
  id: string
  close: () => void
  restartTimer: () => void
}

class ToastManager {
  private toasts = ref<Map<string, ToastInstance>>(new Map())
  private container: HTMLElement | null = null

  private ensureContainer() {
    if (!this.container) {
      this.container = document.createElement('div')
      this.container.id = 'toast-container'
      this.container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 9999;
      `
      document.body.appendChild(this.container)
    }
  }

  private createToastId(): string {
    return `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  private createToastComponent(options: ToastOptions & { id: string }): Component {
    return {
      name: 'DynamicToast',
      setup() {
        const handleClose = () => {
          toastManager.removeToast(options.id)
        }

        return () => h(EnterpriseToast, {
          ...options,
          onClose: handleClose,
          key: options.id
        })
      }
    }
  }

  show(options: ToastOptions): ToastInstance {
    this.ensureContainer()

    const id = this.createToastId()
    const toastOptions = { ...options, id }

    // 创建Vue应用实例
    const toastApp = createApp(this.createToastComponent(toastOptions))

    // 创建容器元素
    const toastElement = document.createElement('div')
    this.container.appendChild(toastElement)

    // 挂载组件
    toastApp.mount(toastElement)

    // 创建Toast实例
    const toastInstance: ToastInstance = {
      id,
      close: () => {
        this.removeToast(id)
      },
      restartTimer: () => {
        // 重启计时器逻辑由组件内部处理
      }
    }

    // 保存实例
    this.toasts.value.set(id, {
      ...toastInstance,
      close: () => {
        // 延迟移除DOM，等待动画完成
        setTimeout(() => {
          toastApp.unmount()
          toastElement.remove()
          this.toasts.value.delete(id)

          // 如果没有更多Toast，移除容器
          if (this.toasts.value.size === 0 && this.container) {
            this.container.remove()
            this.container = null
          }
        }, 200) // 等待离开动画完成
      }
    })

    return toastInstance
  }

  success(message: string, options?: Omit<ToastOptions, 'message' | 'type'>): ToastInstance {
    return this.show({ ...options, message, type: 'success' })
  }

  info(message: string, options?: Omit<ToastOptions, 'message' | 'type'>): ToastInstance {
    return this.show({ ...options, message, type: 'info' })
  }

  warning(message: string, options?: Omit<ToastOptions, 'message' | 'type'>): ToastInstance {
    return this.show({ ...options, message, type: 'warning' })
  }

  error(message: string, options?: Omit<ToastOptions, 'message' | 'type'>): ToastInstance {
    return this.show({ ...options, message, type: 'error', duration: 0 }) // 错误消息默认不自动关闭
  }

  removeToast(id: string) {
    const toast = this.toasts.value.get(id)
    if (toast) {
      toast.close()
    }
  }

  clear() {
    this.toasts.value.forEach(toast => {
      toast.close()
    })
  }

  // 批量显示多个消息
  showMultiple(messages: (ToastOptions & { key?: string })[]) {
    const instances: ToastInstance[] = []

    messages.forEach(msg => {
      const instance = this.show(msg)
      instances.push(instance)
    })

    return instances
  }

  // 显示带Promise的消息
  async showPromise<T>(
    promise: Promise<T>,
    options: {
      loading?: string
      success?: string
      error?: string
    }
  ): Promise<T> {
    const loadingInstance = this.info(options.loading || '处理中...', {
      duration: 0,
      closable: false
    })

    try {
      const result = await promise
      loadingInstance.close()

      if (options.success) {
        this.success(options.success)
      }

      return result
    } catch (error) {
      loadingInstance.close()

      if (options.error) {
        this.error(options.error)
      } else if (error instanceof Error) {
        this.error(error.message)
      }

      throw error
    }
  }
}

// 创建全局Toast管理器实例
export const toastManager = new ToastManager()

// 导出便捷方法
export const toast = {
  success: (message: string, options?: Omit<ToastOptions, 'message' | 'type'>) =>
    toastManager.success(message, options),
  info: (message: string, options?: Omit<ToastOptions, 'message' | 'type'>) =>
    toastManager.info(message, options),
  warning: (message: string, options?: Omit<ToastOptions, 'message' | 'type'>) =>
    toastManager.warning(message, options),
  error: (message: string, options?: Omit<ToastOptions, 'message' | 'type'>) =>
    toastManager.error(message, options),
  show: (options: ToastOptions) => toastManager.show(options),
  clear: () => toastManager.clear(),
  showPromise: <T>(promise: Promise<T>, options?: Parameters<typeof toastManager.showPromise>[1]) =>
    toastManager.showPromise(promise, options || {})
}

// Vue插件
export const ToastPlugin = {
  install(app: App) {
    app.config.globalProperties.$toast = toast
    app.provide('toast', toast)
  }
}

// Composable
export function useToast() {
  return toast
}