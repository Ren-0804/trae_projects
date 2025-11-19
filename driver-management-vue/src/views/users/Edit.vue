<template>
  <div style="padding:16px">
    <a-page-header title="编辑员工">
      <template #extra>
        <router-link :to="`/users/${route.params.id}`">
          <a-button>返回详情</a-button>
        </router-link>
      </template>
    </a-page-header>

    <a-card>
      <a-form layout="vertical" :model="form" :rules="rules" ref="formRef">
        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="username" label="用户名" required>
              <a-input v-model:value="form.username" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="email" label="邮箱">
              <a-input v-model:value="form.email" type="email" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="role" label="角色" required>
              <a-select v-model:value="form.role">
                <a-select-option value="employee">员工</a-select-option>
                <a-select-option value="admin">管理员</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="is_active" label="状态" required>
              <a-select v-model:value="form.is_active_string">
                <a-select-option value="true">活跃</a-select-option>
                <a-select-option value="false">禁用</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :xs="24" :md="12">
            <a-form-item name="position" label="职位">
              <a-input v-model:value="form.position" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="12">
            <a-form-item name="permissions" label="权限">
              <a-select v-model:value="form.permissions" mode="multiple">
                <a-select-option value="drivers:read">司机查看</a-select-option>
                <a-select-option value="drivers:write">司机编辑</a-select-option>
                <a-select-option value="users:read">用户查看</a-select-option>
                <a-select-option value="users:write">用户编辑</a-select-option>
                <a-select-option value="stats:view">统计查看</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item>
          <a-space>
            <router-link :to="`/users/${route.params.id}`">
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/auth'
import type { User } from '@/types/user'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import { message } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref<Partial<User> & { position?: string; permissions?: string[] }>({})

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, message: '请输入用户名' },
    { min: 3, message: '用户名至少3位' }
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
  role: [{ required: true, message: '请选择角色' }],
  is_active_string: [{ required: true, message: '请选择状态' }],
}

const fetchUser = async () => {
  const rawId = String(route.params.id ?? '')
  const idNum = Number(rawId)
  if (!Number.isFinite(idNum) || rawId.trim() === '') {
    router.push('/users')
    return
  }
  const res = await api.get(`/auth/${idNum}`)
  const u: User = res.data
  form.value = {
    username: u.username,
    email: u.email ?? '',
    role: u.role,
    is_active: u.is_active,
    is_active_string: String(u.is_active),
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    const rawId = String(route.params.id ?? '')
    const idNum = Number(rawId)
    if (!Number.isFinite(idNum) || rawId.trim() === '') {
      throw new Error('无效用户ID')
    }

    // 过滤掉空的邮箱字段，避免后端验证错误
    const updateData: any = {
      username: form.value.username?.trim(),
      role: form.value.role,
      is_active: form.value.is_active_string === 'true',
    }

    // 只有当邮箱不为空时才包含邮箱字段
    if (form.value.email && form.value.email.trim() !== '') {
      updateData.email = form.value.email.trim()
    }

    await api.put(`/auth/${idNum}`, updateData)
    message.success('更新成功')
    router.push(`/users/${idNum}`)
  } catch (error: any) {
    message.error(error?.response?.data?.detail || '更新失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUser()
})
</script>