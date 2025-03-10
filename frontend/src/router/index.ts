import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/synthetic_data',
      component: SyntheticDataView,
    },
  ],
})

export default router
