/**
 * 应用路由配置
 *
 * 路由守卫：
 * - 除登录/注册页外，其余页面都需要登录（检查 token）
 * - 管理员页面额外检查用户是否为 admin
 */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { title: '注册', requiresAuth: false },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页', requiresAuth: true },
  },
  {
    path: '/movies',
    name: 'Movies',
    component: () => import('@/views/MoviesView.vue'),
    meta: { title: '电影列表', requiresAuth: true },
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: () => import('@/views/MovieDetailView.vue'),
    meta: { title: '电影详情', requiresAuth: true },
  },
  {
    path: '/play/:id',
    name: 'Play',
    component: () => import('@/views/PlayView.vue'),
    meta: { title: '播放', requiresAuth: true },
  },
  {
    path: '/profile/:username',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: '个人主页', requiresAuth: true },
  },
  {
    path: '/profile/:username/collects',
    name: 'ProfileCollects',
    component: () => import('@/views/ProfileCollectsView.vue'),
    meta: { title: '我的收藏', requiresAuth: true },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminView.vue'),
    meta: { title: '后台管理', requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/movies/add',
    name: 'AdminAddMovie',
    component: () => import('@/views/AdminAddMovieView.vue'),
    meta: { title: '新增电影', requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/movies/:id/edit',
    name: 'AdminEditMovie',
    component: () => import('@/views/AdminEditMovieView.vue'),
    meta: { title: '编辑电影', requiresAuth: true, requiresAdmin: true },
  },
  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '页面不存在', requiresAuth: false },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // 始终滚动到顶部
    return { top: 0 }
  },
})

/**
 * 全局路由守卫
 */
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - CQUPT Movie`

  // 需要登录的页面
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }

  // 需要管理员权限的页面
  if (to.meta.requiresAdmin) {
    try {
      const userStr = localStorage.getItem('user')
      if (userStr) {
        const user = JSON.parse(userStr)
        if (user.username !== 'admin') {
          return next({ name: 'Home' })
        }
      } else {
        return next({ name: 'Home' })
      }
    } catch {
      return next({ name: 'Home' })
    }
  }

  // 已登录用户访问登录/注册页，重定向到首页
  if (!to.meta.requiresAuth && (to.name === 'Login' || to.name === 'Register')) {
    const token = localStorage.getItem('token')
    if (token) {
      return next({ name: 'Home' })
    }
  }

  next()
})

export default router
