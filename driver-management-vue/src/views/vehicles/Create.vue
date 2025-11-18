<template>
  <div class="vehicle-create">
    <a-card title="新增车辆">
      <a-form
        :model="form"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 12 }"
        @finish="handleSubmit"
      >
        <a-form-item label="车牌号" name="plate_number">
          <a-input v-model:value="form.plate_number" placeholder="请输入车牌号" />
        </a-form-item>
        
        <a-form-item label="车辆类型" name="vehicle_type">
          <a-select v-model:value="form.vehicle_type" placeholder="请选择车辆类型">
            <a-select-option value="truck">货车</a-select-option>
            <a-select-option value="bus">客车</a-select-option>
            <a-select-option value="van">面包车</a-select-option>
            <a-select-option value="car">小轿车</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="品牌" name="brand">
          <a-input v-model:value="form.brand" placeholder="请输入品牌" />
        </a-form-item>
        
        <a-form-item label="型号" name="model">
          <a-input v-model:value="form.model" placeholder="请输入型号" />
        </a-form-item>
        
        <a-form-item label="购买日期" name="purchase_date">
          <a-date-picker v-model:value="form.purchase_date" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="当前里程" name="mileage">
          <a-input-number v-model:value="form.mileage" :min="0" style="width: 100%" />
        </a-form-item>
        
        <a-form-item label="备注" name="notes">
          <a-textarea v-model:value="form.notes" placeholder="请输入备注信息" :rows="4" />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 6, span: 12 }">
          <a-space>
            <a-button type="primary" html-type="submit">提交</a-button>
            <router-link to="/vehicles">
              <a-button>取消</a-button>
            </router-link>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { createVehicle } from '@/api/vehicles'
import type { VehicleCreateRequest } from '@/types/vehicle'
import dayjs from 'dayjs'

const router = useRouter()

const form = ref<Partial<VehicleCreateRequest>>({
  plate_number: '',
  vehicle_type: '',
  brand: '',
  model: '',
  purchase_date: undefined,
  mileage: 0,
  notes: ''
})

const rules = {
  plate_number: [{ required: true, message: '请输入车牌号' }],
  vehicle_type: [{ required: true, message: '请选择车辆类型' }],
  brand: [{ required: true, message: '请输入品牌' }],
  model: [{ required: true, message: '请输入型号' }],
  mileage: [{ required: true, message: '请输入当前里程' }]
}

const handleSubmit = async () => {
  try {
    const submitData = {
      ...form.value,
      purchase_date: form.value.purchase_date ? dayjs(form.value.purchase_date).toDate() : undefined
    }
    
    await createVehicle(submitData as VehicleCreateRequest)
    message.success('车辆创建成功')
    router.push('/vehicles')
  } catch (error) {
    message.error('创建失败，请重试')
  }
}
</script>

<style scoped>
.vehicle-create {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}
</style>