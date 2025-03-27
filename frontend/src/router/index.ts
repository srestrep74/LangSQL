import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'
import HomeView from '../views/HomeView.vue'
import QueryChatView from '../views/QueryChatView.vue'
import CreateAlertView from '../views/CreateAlerView.vue'
import ConfigurationView from '@/views/ConfigurationView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import { userStore } from '@/store/userStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/synthetic_data',
      name: 'synthetic_data',
      component: SyntheticDataView,
      meta: { requiresAuth: true }
    },
    {
      path: '/query',
      name: 'query',
      component: QueryChatView,
      meta: { requiresAuth: true }
    },
    {
      path: '/alerts',
      name: 'alert',
      component: CreateAlertView,
      meta: { requiresAuth: true }
    },
    {
      path: '/configuration',
      name: 'configuration',
      component: ConfigurationView,
      meta: { requiresAuth: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = userStore.isAuthenticated;

  if(to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  }else if((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    next('/');
  }else {
    next();
  }
})

export default router
