import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')

window.addEventListener('error', (e: any) => {
  const msg = String(e?.message || '')
  if (msg.includes('net::ERR_ABORTED')) {
    e.preventDefault?.()
  }
})

window.addEventListener('unhandledrejection', (e: any) => {
  const msg = String((e?.reason && e.reason.message) || '')
  if (msg.includes('Failed to fetch dynamically imported module')) {
    e.preventDefault?.()
  }
})

const _origConsoleError = console.error.bind(console)
console.error = (...args: any[]) => {
  const first = args?.[0]
  const text = typeof first === 'string' ? first : String(first || '')
  if (text.includes('net::ERR_ABORTED') || text.includes('Failed to fetch dynamically imported module')) return
  _origConsoleError(...args)
}
