import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'
import HomeView from '../views/HomeView.vue'
import QueryChatView from '../views/QueryChatView.vue'
import CreateAlertView from '../views/CreateAlerView.vue'

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
  ],
})

export default router
