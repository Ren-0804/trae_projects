<template>
  <div style="padding: 16px">
    <a-page-header title="个人资料">
      <template #extra>
        <a-button type="primary" @click="openEditModal">编辑资料</a-button>
      </template>
    </a-page-header>

    <a-row :gutter="16">
      <a-col :xs="24" :md="12">
        <a-card title="基本信息" style="margin-bottom: 16px">
          <a-descriptions bordered :column="1">
            <a-descriptions-item label="用户名">{{ user?.username || '-' }}</a-descriptions-item>
            <a-descriptions-item label="邮箱">{{ user?.email || '未设置' }}</a-descriptions-item>
            <a-descriptions-item label="角色">
              <a-tag :color="user?.role === 'admin' ? 'red' : 'blue'">{{
                user?.role === 'admin' ? '管理员' : '员工'
              }}</a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-tag :color="user?.is_active ? 'green' : 'red'">{{
                user?.is_active ? '活跃' : '禁用'
              }}</a-tag>
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
      <a-col :xs="24" :md="12">
        <a-card title="工作信息" style="margin-bottom: 16px">
          <a-descriptions bordered :column="1">
            <a-descriptions-item label="最后登录">{{
              user?.last_login_at ? formatDate(user?.last_login_at) : '-'
            }}</a-descriptions-item>
            <a-descriptions-item label="注册时间">{{
              user?.created_at ? formatDate(user?.created_at) : '-'
            }}</a-descriptions-item>
            <a-descriptions-item label="最近更新时间">{{
              user?.updated_at ? formatDate(user?.updated_at) : '-'
            }}</a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>

    <a-card title="历史记录">
      <div style="color: #999">暂无历史记录数据</div>
    </a-card>

    <a-modal v-model:open="openEdit" title="编辑个人资料" :confirmLoading="saving" @ok="handleSave">
      <a-form layout="vertical" :model="editForm" :rules="rules" ref="formRef">
        <a-form-item name="email" label="邮箱">
          <a-input v-model:value="editForm.email" type="email" />
        </a-form-item>
        <a-form-item name="username" label="用户名">
          <a-input v-model:value="editForm.username" disabled />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/auth'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import { message } from 'ant-design-vue'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '从未登录'
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN')
  } catch {
    return '无效日期'
  }
}

const openEdit = ref(false)
const saving = ref(false)
const editForm = ref({
  email: '',
  username: '',
})

// 打开编辑对话框时初始化表单数据
const openEditModal = () => {
  editForm.value = {
    email: user.value?.email || '',
    username: user.value?.username || '',
  }
  openEdit.value = true
}
const formRef = ref<FormInstance>()
const rules: Record<string, Rule[]> = {
  email: [{ type: 'email', message: '邮箱格式不正确' }],
}

const handleSave = async () => {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  saving.value = true
  try {
    // 只提交邮箱字段，因为用户名不能修改
    const updateData = {
      email: editForm.value.email
    }
    const res = await api.put('/auth/me', updateData)
    if (res.status >= 200 && res.status < 300) {
      message.success('个人资料更新成功')
      openEdit.value = false
      await authStore.fetchUser()
    } else {
      message.error('更新失败')
    }
  } catch (error: any) {
    console.error('更新个人资料失败:', error)
    message.error(error?.response?.data?.detail || '更新失败')
  } finally {
    saving.value = false
  }
}
</script>
