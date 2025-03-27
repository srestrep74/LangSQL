import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'
import HomeView from '../views/HomeView.vue'
import QueryChatView from '../views/QueryChatView.vue'
import CreateAlertView from '../views/CreateAlerView.vue'
import ConfigurationView from '@/views/ConfigurationView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'

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
    },
    {
      path: '/query',
      name: 'query',
      component: QueryChatView,
    },
    {
      path: '/alerts',
      name: 'alert',
      component: CreateAlertView,
    },
    {
      path: '/configuration',
      name: 'configuration',
      component: ConfigurationView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ],
})

export default router
