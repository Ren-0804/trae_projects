import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Layout from '@/layouts/Layout.vue'
import DriverList from '@/views/drivers/List.vue'
import DriverDetail from '@/views/drivers/Detail.vue'
import DriverCreate from '@/views/drivers/Create.vue'
import DriverEdit from '@/views/drivers/Edit.vue'
import Statistics from '@/views/Statistics.vue'
import UserManagement from '@/views/users/Management.vue'
import Profile from '@/views/users/Profile.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/drivers'
        },
        {
          path: '/drivers',
          name: 'DriverList',
          component: DriverList,
          meta: { title: '司机列表' }
        },
        {
          path: '/drivers/new',
          name: 'DriverCreate',
          component: DriverCreate,
          meta: { title: '新增司机' }
        },
        {
          path: '/drivers/:id',
          name: 'DriverDetail',
          component: DriverDetail,
          meta: { title: '司机详情' }
        },
        {
          path: '/drivers/:id/edit',
          name: 'DriverEdit',
          component: DriverEdit,
          meta: { title: '编辑司机' }
        },
        {
          path: '/statistics',
          name: 'Statistics',
          component: Statistics,
          meta: { title: '数据统计', requiresAdmin: true }
        },
        {
          path: '/users',
          name: 'UserManagement',
          component: UserManagement,
          meta: { title: '用户管理', requiresAdmin: true }
        },
        {
          path: '/profile',
          name: 'Profile',
          component: Profile,
          meta: { title: '个人资料' }
        }
      ]
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
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
