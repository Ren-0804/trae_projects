import { createRouter, createWebHistory } from 'vue-router'
const Login = () => import('@/views/Login.vue')
const Layout = () => import('@/layouts/Layout.vue')
const DriverList = () => import('@/views/drivers/List.vue')
const DriverDetail = () => import('@/views/drivers/Detail.vue')
const DriverCreate = () => import('@/views/drivers/Create.vue')
const DriverEdit = () => import('@/views/drivers/Edit.vue')
const Statistics = () => import('@/views/Statistics.vue')
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
          path: '/statistics',
          name: 'Statistics',
          component: Statistics,
          meta: { title: '数据统计', requiresAdmin: true },
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

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/')
    return
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
