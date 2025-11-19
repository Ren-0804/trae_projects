<template>
  <div style="padding: 16px">
    <a-page-header title="新增员工">
      <template #extra>
        <router-link to="/users">
          <a-button>返回用户管理</a-button>
        </router-link>
      </template>
    </a-page-header>

    <a-card>
      <a-form layout="vertical" :model="form" :rules="rules" ref="formRef">
        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="username" label="用户名" required>
              <a-input v-model:value="form.username" placeholder="请输入用户名" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="email" label="邮箱">
              <a-input v-model:value="form.email" type="email" placeholder="请输入邮箱" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="password" label="密码" required>
              <a-input-password v-model:value="form.password" placeholder="请输入密码" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="role" label="角色" required>
              <a-select v-model:value="form.role" placeholder="请选择角色">
                <a-select-option value="employee">员工</a-select-option>
                <a-select-option value="admin">管理员</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <!-- 这些字段后端暂时不需要，注释掉以备后续使用 -->
        <!--
        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="position" label="职位">
              <a-input v-model:value="form.position" placeholder="请输入职位" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="permissions" label="权限">
              <a-select v-model:value="form.permissions" mode="multiple" placeholder="请选择权限">
                <a-select-option value="drivers:read">司机查看</a-select-option>
                <a-select-option value="drivers:write">司机编辑</a-select-option>
                <a-select-option value="users:read">用户查看</a-select-option>
                <a-select-option value="users:write">用户编辑</a-select-option>
                <a-select-option value="stats:view">统计查看</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        -->

        <a-form-item>
          <a-space>
            <router-link to="/users">
              <a-button>取消</a-button>
            </router-link>
            <a-button type="primary" :loading="loading" @click="handleSubmit">保存</a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/api/auth'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'employee',
  position: '',
  permissions: [] as string[],
})

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, message: '请输入用户名' },
    { min: 2, message: '用户名至少2位' }
  ],
  email: [
    {
      validator: async (_, value) => {
        if (!value || value.trim() === '') {
          return Promise.resolve() // 允许空值
        }
        // 简单的邮箱格式验证
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value.trim())) {
          return Promise.reject(new Error('邮箱格式不正确'))
        }
        return Promise.resolve()
      }
    }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { min: 6, message: '密码至少6位' },
  ],
  role: [{ required: true, message: '请选择角色' }],
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    // 只发送后端需要的字段
    const payload = {
      username: form.value.username?.trim(),
      email: form.value.email?.trim() || undefined, // 如果邮箱为空则不发送
      password: form.value.password,
      role: form.value.role,
    }
    console.log('创建用户请求数据:', payload)
    const res = await api.post('/auth/register', payload)
    if (res.status >= 200 && res.status < 300) {
      message.success('用户创建成功')
      window.location.href = '/users'
    } else {
      message.error('创建失败')
    }
  } catch (error: any) {
    console.error('创建用户失败:', error)
    const errorMessage = error?.response?.data?.detail || 
                        error?.response?.data?.message || 
                        '创建失败'
    message.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>
