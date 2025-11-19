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
              <a-select v-model:value="form.is_active">
                <a-select-option :value="true">活跃</a-select-option>
                <a-select-option :value="false">禁用</a-select-option>
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
  username: [{ required: true, message: '请输入用户名' }],
  email: [{ type: 'email', message: '邮箱格式不正确' }],
  role: [{ required: true, message: '请选择角色' }],
  is_active: [{ required: true, message: '请选择状态' }],
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
    await api.put(`/auth/${idNum}`, form.value)
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