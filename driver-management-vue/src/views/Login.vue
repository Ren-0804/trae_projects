<template>
  <div class="login-container">
    <!-- Background Elements -->
    <div class="bg-shape shape-1"></div>
    <div class="bg-shape shape-2"></div>
    <div class="bg-grid"></div>

    <div class="login-content">
      <div class="brand-section">
        <div class="brand-logo">
          <div class="logo-circle">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4"></path>
              <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"></path>
              <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"></path>
              <path d="M12 3c0 1-1 3-3 3s-3-2-3-3 1-3 3-3 3 2 3 3"></path>
              <path d="M12 21c0-1 1-3 3-3s3 2 3 3-1 3-3 3-3-2-3-3"></path>
            </svg>
          </div>
          <span class="brand-name">Driver Management</span>
        </div>
        <h1 class="welcome-text">Welcome Back</h1>
        <p class="welcome-subtext">Enterprise Fleet Management Solution</p>
      </div>

      <div class="login-card glass-panel">
        <div class="card-header">
          <h2 class="card-title">Sign In</h2>
          <div class="login-mode-switch">
            <button 
              :class="['mode-btn', { active: mode === 'password' }]"
              @click="mode = 'password'"
            >
              Password
            </button>
            <button 
              :class="['mode-btn', { active: mode === 'sms' }]"
              @click="mode = 'sms'"
            >
              SMS Code
            </button>
          </div>
        </div>

        <a-form layout="vertical" @submit.prevent="handleSubmit" class="login-form">
          <template v-if="mode === 'password'">
            <a-form-item label="Username" required>
              <a-input 
                v-model:value="form.username" 
                placeholder="Enter your username"
                size="large"
                class="custom-input"
              >
                <template #prefix>
                  <UserOutlined class="input-icon" />
                </template>
              </a-input>
            </a-form-item>
            <a-form-item label="Password" required>
              <a-input-password 
                v-model:value="form.password" 
                placeholder="Enter your password"
                size="large"
                class="custom-input"
              >
                <template #prefix>
                  <LockOutlined class="input-icon" />
                </template>
              </a-input-password>
            </a-form-item>
          </template>

          <template v-if="mode === 'sms'">
            <a-form-item label="Phone Number" required>
              <a-input 
                v-model:value="sms.phone" 
                placeholder="Enter phone number"
                size="large"
                class="custom-input"
              >
                <template #prefix>
                  <MobileOutlined class="input-icon" />
                </template>
              </a-input>
            </a-form-item>
            <a-form-item label="Verification Code" required>
              <div class="sms-group">
                <a-input 
                  v-model:value="sms.code" 
                  placeholder="6-digit code"
                  size="large"
                  class="custom-input"
                />
                <a-button 
                  size="large" 
                  @click="sendSmsCode" 
                  :disabled="sms.sending"
                  class="sms-btn"
                >
                  {{ sms.sending ? 'Sending...' : 'Send Code' }}
                </a-button>
              </div>
            </a-form-item>
          </template>

          <a-form-item v-if="mfaRequired" label="MFA Code" required>
            <div class="sms-group">
              <a-input 
                v-model:value="mfa.code" 
                placeholder="Authenticator code"
                size="large"
                class="custom-input"
              />
              <a-button size="large" type="primary" @click="submitMfa" :loading="loading" class="verify-btn">Verify</a-button>
            </div>
          </a-form-item>

          <a-button 
            type="primary" 
            block 
            :loading="loading" 
            html-type="submit"
            size="large"
            class="submit-btn"
          >
            Sign In
          </a-button>

          <a-alert v-if="error" type="error" :message="error" show-icon class="error-alert" />
        </a-form>
      </div>
      
      <div class="footer-text">
        &copy; 2024 Driver Management System. All rights reserved.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined, MobileOutlined } from '@ant-design/icons-vue'

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

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    if (mode.value === 'password') {
      const r: any = await authStore.login(form.username, form.password)
      if (r?.mfa_required) {
        mfaRequired.value = true
        message.info('Please enter MFA code')
        return
      }
    } else {
      const { loginWithSms } = await import('@/api/auth')
      const r = await loginWithSms(sms.phone, sms.code)
      authStore.setSession(r)
    }
    message.success('Login successful')
    router.push('/')
  } catch (err: any) {
    const msg = err.response?.data?.message || 'Login failed. Please check your credentials.'
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
    message.success('Login successful')
    router.push('/')
  } catch (err: any) {
    const msg = err.response?.data?.message || 'Invalid code'
    error.value = msg
    message.error(msg)
  } finally {
    loading.value = false
  }
}

const sendSmsCode = async () => {
  sms.sending = true
  try {
    message.info('SMS functionality requires backend support')
  } finally {
    sms.sending = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background-color: var(--color-bg-body);
  background-image: 
    radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(15, 23, 42, 0.15) 0px, transparent 50%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  font-family: var(--font-family);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  z-index: 0;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.6;
}

.shape-1 {
  top: -10%;
  left: -10%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, var(--color-accent-200), var(--color-primary-200));
  animation: float 20s ease-in-out infinite;
}

.shape-2 {
  bottom: -10%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--color-primary-300), var(--color-accent-300));
  animation: float 25s ease-in-out infinite reverse;
}

.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.brand-section {
  text-align: center;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.logo-circle {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-accent-500), var(--color-primary-600));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

.brand-name {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.025em;
}

.welcome-text {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs);
}

.welcome-subtext {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
}

.login-card {
  padding: var(--spacing-xl);
  border-radius: var(--radius-xl);
  background: rgba(255, 255, 255, 0.8);
}

.card-header {
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.login-mode-switch {
  display: inline-flex;
  background: var(--color-gray-100);
  padding: 4px;
  border-radius: var(--radius-lg);
}

.mode-btn {
  border: none;
  background: none;
  padding: 6px 16px;
  border-radius: var(--radius-base);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.mode-btn.active {
  background: white;
  color: var(--color-primary-700);
  box-shadow: var(--shadow-sm);
}

.custom-input {
  border-radius: var(--radius-base);
  border-color: var(--color-border);
  padding-left: 12px;
}

.custom-input:hover, .custom-input:focus {
  border-color: var(--color-accent-500);
}

.input-icon {
  color: var(--color-text-tertiary);
}

.sms-group {
  display: flex;
  gap: var(--spacing-sm);
}

.sms-btn, .verify-btn {
  border-radius: var(--radius-base);
}

.submit-btn {
  height: 44px;
  border-radius: var(--radius-base);
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-800) 100%);
  border: none;
  font-weight: 600;
  font-size: var(--font-size-base);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
  transition: all var(--transition-base);
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35);
}

.error-alert {
  margin-top: var(--spacing-md);
  border-radius: var(--radius-base);
}

.footer-text {
  text-align: center;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}
</style>
