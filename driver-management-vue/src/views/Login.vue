<template>
  <div style="
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  ">
    <!-- 背景装饰 -->
    <div style="
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
      background-size: 50px 50px;
      animation: float 20s ease-in-out infinite;
    "></div>
    
    <div style="
      position: absolute;
      top: 20%;
      right: 10%;
      width: 300px;
      height: 300px;
      background: rgba(255,255,255,0.1);
      border-radius: 50%;
      filter: blur(40px);
      animation: pulse 4s ease-in-out infinite;
    "></div>
    
    <div style="
      position: absolute;
      bottom: 20%;
      left: 10%;
      width: 200px;
      height: 200px;
      background: rgba(255,255,255,0.08);
      border-radius: 50%;
      filter: blur(30px);
      animation: pulse 6s ease-in-out infinite reverse;
    "></div>

    <a-col :xs="22" :sm="16" :md="12" :lg="8" :xl="6" style="z-index: 10;">
      <div style="
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        overflow: hidden;
        animation: slideIn 0.8s ease-out;
      ">
        <!-- 头部装饰 -->
        <div style="
          padding: 40px 32px 24px;
          background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
          text-align: center;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        ">
          <div style="
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            animation: bounce 2s infinite;
          ">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <path d="M9 12l2 2 4-4"></path>
              <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"></path>
              <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"></path>
              <path d="M12 3c0 1-1 3-3 3s-3-2-3-3 1-3 3-3 3 2 3 3"></path>
              <path d="M12 21c0-1 1-3 3-3s3 2 3 3-1 3-3 3-3-2-3-3"></path>
            </svg>
          </div>
          <h1 style="
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          ">司机管理系统</h1>
          <p style="
            margin: 8px 0 0;
            color: #718096;
            font-size: 14px;
            font-weight: 500;
          ">现代化车队管理解决方案</p>
        </div>
        
        <div style="padding: 32px;">
          <a-radio-group v-model:value="mode" style="margin-bottom: 16px;">
            <a-radio-button value="password">密码登录</a-radio-button>
            <a-radio-button value="sms">短信验证码登录</a-radio-button>
          </a-radio-group>
          <a-form layout="vertical" @submit.prevent="handleSubmit">
            <a-form-item v-if="mode==='password'" label="用户名" required>
              <a-input 
                v-model:value="form.username" 
                placeholder="请输入用户名"
                size="large"
                style="
                  border-radius: 12px;
                  border: 1px solid rgba(102, 126, 234, 0.2);
                  background: rgba(255, 255, 255, 0.8);
                  transition: all 0.3s ease;
                "
                @focus="onFocus"
                @blur="onBlur"
              >
                <template #prefix>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </template>
              </a-input>
            </a-form-item>
            <a-form-item v-if="mode==='password'" label="密码" required>
              <a-input-password 
                v-model:value="form.password" 
                placeholder="请输入密码"
                size="large"
                style="
                  border-radius: 12px;
                  border: 1px solid rgba(102, 126, 234, 0.2);
                  background: rgba(255, 255, 255, 0.8);
                  transition: all 0.3s ease;
                "
                @focus="onFocus"
                @blur="onBlur"
              >
                <template #prefix>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <circle cx="12" cy="16" r="1"></circle>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </template>
              </a-input-password>
            </a-form-item>
            <a-form-item v-if="mode==='sms'" label="手机号" required>
              <a-input 
                v-model:value="sms.phone" 
                placeholder="请输入手机号"
                size="large"
                style="border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2); background: rgba(255, 255, 255, 0.8);"
              />
            </a-form-item>
            <a-form-item v-if="mode==='sms'" label="验证码" required>
              <div style="display:flex; gap:8px;">
                <a-input 
                  v-model:value="sms.code" 
                  placeholder="请输入验证码"
                  size="large"
                  style="border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2); background: rgba(255, 255, 255, 0.8);"
                />
                <a-button size="large" @click="sendSmsCode" :disabled="sms.sending" style="border-radius:12px;">
                  {{ sms.sending ? '发送中...' : '发送验证码' }}
                </a-button>
              </div>
            </a-form-item>
            <a-form-item v-if="mfaRequired" label="二次验证码" required>
              <div style="display:flex; gap:8px;">
                <a-input 
                  v-model:value="mfa.code" 
                  placeholder="请输入6位验证码"
                  size="large"
                  style="border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2); background: rgba(255, 255, 255, 0.8);"
                />
                <a-button size="large" type="primary" @click="submitMfa" :disabled="loading" style="border-radius:12px;">验证</a-button>
              </div>
            </a-form-item>
            <a-form-item style="margin-bottom: 16px;">
              <a-button 
                type="primary" 
                block 
                :loading="loading" 
                html-type="submit"
                size="large"
                style="
                  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  border: none;
                  border-radius: 12px;
                  font-weight: 600;
                  font-size: 16px;
                  height: 48px;
                  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
                  transition: all 0.3s ease;
                "
                @mouseenter="onEnter"
                @mouseleave="onLeave"
              >
                <template #icon>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                    <polyline points="10 17 15 12 10 7"></polyline>
                    <line x1="15" y1="12" x2="3" y2="12"></line>
                  </svg>
                </template>
                登录
              </a-button>
            </a-form-item>
            <a-alert v-if="error" type="error" :message="error" show-icon style="
              border-radius: 12px;
              border: none;
              background: rgba(255, 77, 79, 0.1);
              backdrop-filter: blur(10px);
            " />
          </a-form>
        </div>
      </div>
    </a-col>
  </div>
</template>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
})
const sms = reactive({
  phone: '',
  code: '',
  sending: false,
})
const mode = ref<'password' | 'sms'>('password')

const loading = ref(false)
const error = ref('')
const mfaRequired = ref(false)
const mfa = reactive({ code: '' })

const onFocus = (e: Event) => { const el = e.target as HTMLInputElement; if (el && el.style) el.style.borderColor = '#667eea' }
const onBlur = (e: Event) => { const el = e.target as HTMLInputElement; if (el && el.style) el.style.borderColor = 'rgba(102, 126, 234, 0.2)' }
const onEnter = (e: Event) => { const el = e.target as HTMLElement; if (el && el.style) el.style.transform = 'translateY(-2px)' }
const onLeave = (e: Event) => { const el = e.target as HTMLElement; if (el && el.style) el.style.transform = 'translateY(0)' }

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    if (mode.value === 'password') {
      const r: any = await authStore.login(form.username, form.password)
      if (r?.mfa_required) {
        mfaRequired.value = true
        message.info('请输入二次验证码')
        return
      }
    } else {
      const { loginWithSms } = await import('@/api/auth')
      const r = await loginWithSms(sms.phone, sms.code)
      authStore.setSession(r)
    }
    message.success('登录成功')
    router.push('/')
  } catch (err: any) {
    const msg = err.response?.data?.message || '登录失败，请检查用户名和密码'
    error.value = msg
    message.error(msg)
  } finally {
    loading.value = false
  }
}

const submitMfa = async () => {
  loading.value = true
  try {
    const { verifyMfa } = await import('@/api/auth')
    const r = await verifyMfa(form.username, mfa.code)
    authStore.setSession(r)
    message.success('登录成功')
    router.push('/')
  } catch (err: any) {
    const msg = err.response?.data?.message || '验证码错误'
    error.value = msg
    message.error(msg)
  } finally {
    loading.value = false
  }
}

const sendSmsCode = async () => {
  sms.sending = true
  try {
    message.info('验证码发送逻辑需后端支持')
  } finally {
    sms.sending = false
  }
}
</script>
