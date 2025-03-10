import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'
import HomeView from '../views/HomeView.vue'
import QueryChatView from '../views/QueryChatView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/synthetic_data',
      component: SyntheticDataView,
    },
    {
      path: '/query',
      name: 'query',
      component: QueryChatView,
    },
  ],
})

export default router
