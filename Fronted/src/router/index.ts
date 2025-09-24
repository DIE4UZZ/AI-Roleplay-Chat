import { createRouter, createWebHistory } from 'vue-router';
import authService from '../services/auth.service';

// 定义路由
const routes = [
  {
    path: '/',
    redirect: '/login', // 默认重定向到登录页面
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: {
      guestOnly: true, // 仅游客可访问
    },
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: {
      requiresAuth: true, // 需要登录才能访问
    },
  },
  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 导航守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = authService.isLoggedIn();

  // 需要登录才能访问的页面
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next('/login');
    } else {
      next();
    }
  }
  // 仅游客可访问的页面
  else if (to.matched.some((record) => record.meta.guestOnly)) {
    if (isLoggedIn) {
      next('/home');
    } else {
      next();
    }
  }
  // 其他页面直接放行
  else {
    next();
  }
});

export default router;