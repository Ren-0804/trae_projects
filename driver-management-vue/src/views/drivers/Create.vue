<template>
  <div style="padding: 24px;">
    <!-- Glassmorphism Header -->
    <div style="
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <h1 style="
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            background-clip: text;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
          ">新增司机</h1>
          <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 14px;">添加新的司机信息到系统中</p>
        </div>
        <router-link to="/drivers">
          <a-button 
            type="default"
            style="
              border-radius: 12px;
              height: 44px;
              padding: 0 20px;
              background: rgba(255, 255, 255, 0.7);
              border: 1px solid rgba(0, 0, 0, 0.1);
              font-weight: 600;
              transition: all 0.3s ease;
            "
            @mouseenter="onCardHoverEnter"
            @mouseleave="onCardHoverLeave"
          >
            ← 返回列表
          </a-button>
        </router-link>
      </div>
    </div>

    <a-form layout="vertical" :model="form" :rules="rules" ref="formRef" @submit.prevent="handleSubmit">
      <div style="
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      ">
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item name="name" label="姓名" required>
              <a-input 
                v-model:value="form.name" 
                placeholder="请输入司机姓名"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="phone" label="电话" required>
              <a-input 
                v-model:value="form.phone" 
                placeholder="请输入手机号码"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="id_card" label="身份证号" required>
              <a-input 
                v-model:value="form.id_card" 
                placeholder="请输入身份证号"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="license_number" label="驾驶证号" required>
              <a-input 
                v-model:value="form.license_number" 
                placeholder="请输入驾驶证号"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="license_type" label="驾驶证类型" required>
              <a-select 
                v-model:value="form.license_type" 
                placeholder="请选择驾驶证类型"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              >
                <a-select-option value="A1">A1</a-select-option>
                <a-select-option value="A2">A2</a-select-option>
                <a-select-option value="B1">B1</a-select-option>
                <a-select-option value="B2">B2</a-select-option>
                <a-select-option value="C1">C1</a-select-option>
                <a-select-option value="C2">C2</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="main_route" label="主要线路" required>
              <template v-if="!manualRouteInput">
                <a-input v-model:value="form.main_route" type="hidden" />
                <a-form-item-rest>
                  <!-- 出发地选择 -->
                  <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 14px; color: #374151; margin-bottom: 4px;">出发地</label>
                    <a-tree-select
                      v-model:value="originRouteValue"
                      :treeData="routeTreeData"
                      :showSearch="true"
                      treeNodeFilterProp="title"
                      allowClear
                      :placeholder="'请选择出发地国家/省份'"
                      treeDefaultExpandAll
                      @search="handleRouteSearch"
                      @change="handleOriginRouteChange"
                      style="width: 100%; border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
                    />
                  </div>
                  
                  <!-- 目的地选择 -->
                  <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 14px; color: #374151; margin-bottom: 4px;">目的地</label>
                    <a-tree-select
                      v-model:value="destinationRouteValue"
                      :treeData="routeTreeData"
                      :showSearch="true"
                      treeNodeFilterProp="title"
                      allowClear
                      :placeholder="'请选择目的地国家/省份'"
                      treeDefaultExpandAll
                      @search="handleRouteSearch"
                      @change="handleDestinationRouteChange"
                      style="width: 100%; border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
                    />
                  </div>
                  
                  <!-- 添加路线按钮 -->
                  <div style="margin-bottom: 12px;">
                    <a-button 
                      type="primary" 
                      size="small" 
                      @click="addCurrentRoute"
                      :disabled="!originRouteValue || !destinationRouteValue"
                      style="border-radius: 8px;"
                    >
                      添加路线
                    </a-button>
                  </div>
                  
                  <!-- 已选择的路线显示 -->
                  <div v-if="selectedRoutes.length > 0" style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 14px; color: #374151; margin-bottom: 4px;">已选择路线</label>
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                      <div v-for="(route, index) in selectedRoutes" :key="index" 
                           style="display: flex; align-items: center; justify-content: space-between; background: rgba(59, 130, 246, 0.1); padding: 8px 12px; border-radius: 8px;">
                        <span style="font-size: 14px;">{{ route.origin }} → {{ route.destination }}</span>
                        <a-button type="link" size="small" danger @click="removeRoute(index)">删除</a-button>
                      </div>
                    </div>
                  </div>
                  
                  <div style="font-size: 12px; color: #6b7280; margin-top: 8px;">
                    <div>• 支持选择多个路线</div>
                    <div>• 若列表为空或无法选择，可
                      <a-button type="link" size="small" @click="manualRouteInput = true">手动输入路线</a-button>
                    </div>
                  </div>
                </a-form-item-rest>
              </template>
              <template v-else>
                <a-textarea 
                  v-model:value="form.main_route" 
                  placeholder="例如：&#10;中国-北京,中国-上海&#10;哈萨克斯坦-阿拉木图,乌兹别克斯坦-塔什干"
                  :rows="3"
                  style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
                />
                <div style="font-size: 12px; color: #6b7280; margin-top: 8px;">
                  <a-button type="link" size="small" @click="manualRouteInput = false">返回选择列表</a-button>
                </div>
              </template>
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="vehicle_type" label="车辆类型" required>
              <a-select 
                v-model:value="form.vehicle_type" 
                placeholder="请选择车辆类型"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              >
                <a-select-option value="厢式货车">厢式货车</a-select-option>
                <a-select-option value="平板货车">平板货车</a-select-option>
                <a-select-option value="高栏货车">高栏货车</a-select-option>
                <a-select-option value="冷藏车">冷藏车</a-select-option>
                <a-select-option value="危险品运输车">危险品运输车</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item label="车长">
              <a-select 
                v-model:value="form.vehicle_length" 
                placeholder="请选择车长"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              >
                <a-select-option value="">请选择车长</a-select-option>
                <a-select-option value="4.2米">4.2米</a-select-option>
                <a-select-option value="6.8米">6.8米</a-select-option>
                <a-select-option value="9.6米">9.6米</a-select-option>
                <a-select-option value="13米">13米</a-select-option>
                <a-select-option value="17.5米">17.5米</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="price_per_km" label="每公里价格（元)">
              <a-input-number 
                v-model:value="form.price_per_km" 
                :min="0" 
                :step="0.01" 
                style="width: 100%; border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="experience_years" label="驾龄（年）">
              <a-input-number 
                v-model:value="form.experience_years" 
                :min="0" 
                style="width: 100%; border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="emergency_contact" label="紧急联系人">
              <a-input 
                v-model:value="form.emergency_contact" 
                placeholder="请输入紧急联系人姓名"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="emergency_phone" label="紧急联系电话">
              <a-input 
                v-model:value="form.emergency_phone" 
                placeholder="请输入紧急联系电话"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item name="status" label="状态">
              <a-select 
                v-model:value="form.status" 
                placeholder="请选择状态"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              >
                <a-select-option value="active">活跃</a-select-option>
                <a-select-option value="inactive">非活跃</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="24">
            <a-form-item name="remark" label="备注">
              <a-textarea 
                v-model:value="form.remark" 
                :rows="3" 
                placeholder="请输入备注信息"
                style="border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <div style="display: flex; justify-content: flex-end; gap: 16px; margin-top: 24px;">
          <router-link to="/drivers">
            <a-button 
              size="large"
              style="
                border-radius: 12px;
                height: 44px;
                padding: 0 24px;
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 0, 0, 0.1);
                font-weight: 600;
                transition: all 0.3s ease;
              "
              @mouseenter="onCardHoverEnter"
              @mouseleave="onCardHoverLeave"
            >
              取消
            </a-button>
          </router-link>
          <a-button 
            size="large" 
            type="primary" 
            :loading="loading" 
            :disabled="loading" 
            @click="handleSubmit"
            style="
              background: linear-gradient(135deg, #667eea, #764ba2);
              border: none;
              border-radius: 12px;
              height: 44px;
              padding: 0 24px;
              font-weight: 600;
              box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
              transition: all 0.3s ease;
            "
            @mouseenter="onPrimaryEnter"
            @mouseleave="onPrimaryLeave"
          >
            保存
          </a-button>
        </div>
      </div>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import { useRouter } from 'vue-router'
import { useDriverStore } from '@/stores/drivers'
import { message } from 'ant-design-vue'
import { getCountries, getProvinces } from '@/api/regions'

const router = useRouter()
const driverStore = useDriverStore()

const loading = ref(false)
const formRef = ref<FormInstance>()
const rules: Record<string, Rule[]> = {
  name: [{ required: true, message: '请输入姓名' }],
  phone: [
    { required: true, message: '请输入手机号码' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的中国手机号' },
  ],
  id_card: [
    { required: true, message: '请输入身份证号' },
    { pattern: /^\d{17}[\dXx]$/, message: '身份证号格式不正确' },
  ],
  license_number: [{ required: true, message: '请输入驾驶证号' }],
  license_type: [{ required: true, message: '请选择驾驶证类型' }],
  main_route: [{ required: true, message: '请输入主要线路' }],
  vehicle_type: [{ required: true, message: '请选择车辆类型' }],
  status: [{ required: true, message: '请选择状态' }],
  emergency_phone: [{ pattern: /^1[3-9]\d{9}$/, message: '紧急电话格式不正确' }],
}

const form = ref({
  name: '',
  phone: '',
  id_card: '',
  license_number: '',
  license_type: '',
  main_route: '',
  vehicle_type: '',
  vehicle_length: '',
  price_per_km: 0,
  experience_years: 0,
  status: 'active' as const,
  emergency_contact: '',
  emergency_phone: '',
  remark: '',
})

const routeValue = ref<string>('')
const originRouteValue = ref<string>('')
const destinationRouteValue = ref<string>('')
const countries = ref<string[]>([])
const provinces = ref<Record<string, string[]>>({})
const routeTreeData = ref<any[]>([])
const regionsLoading = ref(false)
const manualRouteInput = ref(false)
const selectedRoutes = ref<Array<{origin: string, destination: string}>>([])

const buildTree = () => {
  routeTreeData.value = countries.value.map((c) => ({
    title: c,
    value: c,
    key: c,
    children: (provinces.value[c] || []).map((p) => ({ title: p, value: `${c}-${p}`, key: `${c}-${p}` })),
  }))
}

const initRegions = async () => {
  try {
    regionsLoading.value = true
    countries.value = await getCountries()
    for (const c of countries.value) {
      provinces.value[c] = await getProvinces(c)
    }
    buildTree()
  } catch (e) {
    message.error('主要路线数据加载失败，请稍后重试')
  } finally {
    regionsLoading.value = false
  }
}

const handleRouteSearch = async (q: string) => {
  if (!q || q.trim() === '') {
    await initRegions()
    return
  }
  for (const c of countries.value) {
    provinces.value[c] = await getProvinces(c, q)
  }
  buildTree()
}

const handleRouteChange = (val: string) => {
  routeValue.value = val
  form.value.main_route = val
}

const handleOriginRouteChange = (val: string) => {
  originRouteValue.value = val
  updateMainRoute()
}

const handleDestinationRouteChange = (val: string) => {
  destinationRouteValue.value = val
  updateMainRoute()
}

const updateMainRoute = () => {
  if (originRouteValue.value && destinationRouteValue.value) {
    const newRoute = {
      origin: originRouteValue.value,
      destination: destinationRouteValue.value
    }
    
    // 检查是否已存在相同路线
    const exists = selectedRoutes.value.some(
      route => route.origin === newRoute.origin && route.destination === newRoute.destination
    )
    
    if (!exists) {
      selectedRoutes.value.push(newRoute)
      // 清空选择框，准备下一次选择
      originRouteValue.value = ''
      destinationRouteValue.value = ''
      updateFormMainRoute()
    }
  }
}

const addCurrentRoute = () => {
  if (originRouteValue.value && destinationRouteValue.value) {
    updateMainRoute()
  }
}

const removeRoute = (index: number) => {
  selectedRoutes.value.splice(index, 1)
  updateFormMainRoute()
}

const updateFormMainRoute = () => {
  if (selectedRoutes.value.length > 0) {
    // 将多个路线格式化为字符串，用分号分隔
    form.value.main_route = selectedRoutes.value.map(route => `${route.origin}→${route.destination}`).join(';')
  } else {
    form.value.main_route = ''
  }
}

initRegions()
// 也在挂载时尝试加载，确保数据可用
onMounted(() => {
  initRegions()
  // 若初始化后没有数据，则启用手动输入作为回退
  setTimeout(() => {
    if (routeTreeData.value.length === 0) manualRouteInput.value = true
  }, 300)
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await formRef.value?.validate()
  } catch {
    loading.value = false
    return
  }
  try {
    await driverStore.addDriver(form.value)
    message.success('司机信息保存成功')
    router.push('/drivers')
  } catch (error: any) {
    message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}
const onCardHoverEnter = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(255, 255, 255, 0.9)' }
const onCardHoverLeave = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.background = 'rgba(255, 255, 255, 0.7)' }
const onPrimaryEnter = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.transform = 'translateY(-2px)' }
const onPrimaryLeave = (e: Event) => { const el = e.currentTarget as HTMLElement; if (el) el.style.transform = 'translateY(0)' }
</script>
