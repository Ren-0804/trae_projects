import { createRouter, createWebHistory } from 'vue-router'
const Login = () => import('@/views/Login.vue')
const Layout = () => import('@/layouts/Layout.vue')
const DriverList = () => import('@/views/drivers/List.vue')
const DriverDetail = () => import('@/views/drivers/Detail.vue')
const DriverCreate = () => import('@/views/drivers/Create.vue')
const DriverEdit = () => import('@/views/drivers/Edit.vue')
import Statistics from '@/views/Statistics.vue'
const UserManagement = () => import('@/views/users/Management.vue')
const Profile = () => import('@/views/users/Profile.vue')
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/drivers',
        },
        {
          path: '/drivers',
          name: 'DriverList',
          component: DriverList,
          meta: { title: '司机列表' },
        },
        {
          path: '/drivers/new',
          name: 'DriverCreate',
          component: DriverCreate,
          meta: { title: '新增司机' },
        },
        {
          path: '/drivers/:id',
          name: 'DriverDetail',
          component: DriverDetail,
          meta: { title: '司机详情' },
        },
        {
          path: '/drivers/:id/edit',
          name: 'DriverEdit',
          component: DriverEdit,
          meta: { title: '编辑司机' },
        },
        {
          path: '/vehicles',
          name: 'VehicleList',
          component: () => import('@/views/vehicles/List.vue'),
          meta: { title: '车辆列表' },
        },
        {
          path: '/vehicles/new',
          name: 'VehicleCreate',
          component: () => import('@/views/vehicles/Create.vue'),
          meta: { title: '新增车辆' },
        },
        {
          path: '/vehicles/:id',
          name: 'VehicleDetail',
          component: () => import('@/views/vehicles/Detail.vue'),
          meta: { title: '车辆详情' },
        },
        {
          path: '/vehicles/:id/edit',
          name: 'VehicleEdit',
          component: () => import('@/views/vehicles/Edit.vue'),
          meta: { title: '编辑车辆' },
        },
        {
          path: '/vehicles/:id/assign-driver',
          name: 'VehicleAssignDriver',
          component: () => import('@/views/vehicles/AssignDriver.vue'),
          meta: { title: '分配司机' },
        },
        {
          path: '/vehicles/maintenance-reminders',
          name: 'VehicleMaintenanceReminders',
          component: () => import('@/views/vehicles/MaintenanceReminders.vue'),
          meta: { title: '维护提醒' },
        },
        {
          path: '/vehicles/:id/usage-history',
          name: 'VehicleUsageHistory',
          component: () => import('@/views/vehicles/DriverUsageHistory.vue'),
          meta: { title: '司机使用记录' },
        },
        {
          path: '/schedules',
          name: 'ScheduleList',
          component: () => import('@/views/schedules/List.vue'),
          meta: { title: '排班管理' },
        },
        {
          path: '/schedules/new',
          name: 'ScheduleCreate',
          component: () => import('@/views/schedules/Create.vue'),
          meta: { title: '新增排班' },
        },
        {
          path: '/schedules/calendar',
          name: 'ScheduleCalendar',
          component: () => import('@/views/schedules/Calendar.vue'),
          meta: { title: '排班日历' },
        },
        {
          path: '/certificates',
          name: 'CertificateList',
          component: () => import('@/views/certificates/List.vue'),
          meta: { title: '证书管理' },
        },
        {
          path: '/certificates/new',
          name: 'CertificateCreate',
          component: () => import('@/views/certificates/Create.vue'),
          meta: { title: '新增证书' },
        },
        {
          path: '/certificates/:id',
          name: 'CertificateDetail',
          component: () => import('@/views/certificates/Detail.vue'),
          meta: { title: '证书详情' },
        },
        {
          path: '/safety',
          name: 'SafetyDashboard',
          component: () => import('@/views/safety/Dashboard.vue'),
          meta: { title: '安全监控' },
        },
        {
          path: '/safety/alerts',
          name: 'SafetyAlerts',
          component: () => import('@/views/safety/Alerts.vue'),
          meta: { title: '安全预警' },
        },
        {
          path: '/safety/emergency',
          name: 'EmergencyAlerts',
          component: () => import('@/views/safety/Emergency.vue'),
          meta: { title: '紧急报警' },
        },
        {
          path: '/statistics',
          name: 'Statistics',
          component: Statistics,
          meta: { title: '数据统计', requiresRoles: ['admin', 'superadmin'] },
        },
        {
          path: '/security/center',
          name: 'SecurityCenter',
          component: () => import('@/views/security/Center.vue'),
          meta: { title: '安全中心', requiresAuth: true },
        },
        {
          path: '/admin/permissions',
          name: 'Permissions',
          component: () => import('@/views/admin/Permissions.vue'),
          meta: { title: '权限管理', requiresRoles: ['admin', 'superadmin'] },
        },
        {
          path: '/tasks',
          name: 'TaskBoard',
          component: () => import('@/views/tasks/Board.vue'),
          meta: { title: '任务看板', requiresRoles: ['dispatcher', 'manager', 'admin', 'superadmin'] },
        },
        {
          path: '/tasks/:id',
          name: 'TaskDetail',
          component: () => import('@/views/tasks/Detail.vue'),
          meta: { title: '任务详情', requiresAuth: true },
        },
        {
          path: '/tasks/map',
          name: 'TaskMap',
          component: () => import('@/views/tasks/Map.vue'),
          meta: { title: '任务地图', requiresAuth: true },
        },
        {
          path: '/driver/tasks',
          name: 'DriverOps',
          component: () => import('@/views/tasks/DriverOps.vue'),
          meta: { title: '司机任务', requiresRoles: ['driver'] },
        },
        {
          path: '/files',
          name: 'FileList',
          component: () => import('@/views/files/List.vue'),
          meta: { title: '文件库', requiresAuth: true, perm: { resource: 'file', action: 'view' } },
        },
        {
          path: '/files/:id',
          name: 'FileDetail',
          component: () => import('@/views/files/Detail.vue'),
          meta: { title: '文件详情', requiresAuth: true, perm: { resource: 'file', action: 'view' } },
        },
        {
          path: '/audit/logs',
          name: 'AuditLogs',
          component: () => import('@/views/audit/Logs.vue'),
          meta: { title: '审计日志', requiresRoles: ['auditor', 'admin', 'superadmin'] },
        },
        {
          path: '/audit/logs/:id',
          name: 'AuditLogDetail',
          component: () => import('@/views/audit/LogDetail.vue'),
          meta: { title: '日志详情', requiresRoles: ['auditor', 'admin', 'superadmin'] },
        },
        {
          path: '/users',
          name: 'UserManagement',
          component: UserManagement,
          meta: { title: '用户管理', requiresAdmin: true },
        },
        {
          path: '/users/:id',
          name: 'UserDetail',
          component: () => import('@/views/users/Detail.vue'),
          meta: { title: '用户详情', requiresAdmin: true },
        },
        {
          path: '/users/:id/edit',
          name: 'UserEdit',
          component: () => import('@/views/users/Edit.vue'),
          meta: { title: '编辑用户', requiresAdmin: true },
        },
        {
          path: '/users/new',
          name: 'UserCreate',
          component: () => import('@/views/users/Create.vue'),
          meta: { title: '新增用户', requiresAdmin: true },
        },
        {
          path: '/profile',
          name: 'Profile',
          component: Profile,
          meta: { title: '个人资料' },
        },
      ],
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchUser()
    } catch {
      // ignore
    }
  }

  const { usePermissionStore } = await import('@/stores/permissions')
  const p = usePermissionStore()
  p.setUser(authStore.user as any)

  // 司机ID路由参数校验
  if (to.name === 'DriverDetail' || to.name === 'DriverEdit') {
    const rawId = String(to.params.id ?? '')
    const idNum = Number(rawId)
    if (!Number.isFinite(idNum) || rawId.trim() === '') {
      next('/drivers')
      return
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  const roles = (to.meta as any).requiresRoles as Array<any> | undefined
  if (roles && !authStore.hasRole(roles as any)) {
    next('/')
    return
  }

  const permMeta = (to.meta as any).perm as { resource: string; action?: string; scope?: any } | undefined
  if (permMeta) {
    const ok = p.can(permMeta.resource, permMeta.action || 'view', permMeta.scope)
    if (!ok) {
      next('/')
      return
    }
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
    return
  }

  next()
})

router.onError((error) => {
  const msg = String((error && (error as any).message) || '')
  if (msg.includes('Failed to fetch dynamically imported module')) return
  console.error(error)
})

export default router
