<template>
  <a-row justify="center" align="middle" style="min-height: 100vh; background: #f5f5f5">
    <a-col :xs="22" :sm="16" :md="12" :lg="8" :xl="6">
      <a-card title="司机管理系统" bordered>
        <a-form layout="vertical" @submit.prevent="handleLogin">
          <a-form-item label="用户名" required>
            <a-input v-model:value="form.username" placeholder="请输入用户名" />
          </a-form-item>
          <a-form-item label="密码" required>
            <a-input-password v-model:value="form.password" placeholder="请输入密码" />
          </a-form-item>
          <a-form-item>
            <a-button type="primary" block :loading="loading" html-type="submit">登录</a-button>
          </a-form-item>
          <a-alert v-if="error" type="error" :message="error" show-icon />
        </a-form>
      </a-card>
    </a-col>
  </a-row>
</template>

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

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(form.username, form.password)
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
</script>
