import { createRouter, createWebHistory } from 'vue-router'
import SyntheticDataView from '../views/SyntheticDataView.vue'
import HomeView from '../views/HomeView.vue'
import QueryChatView from '../views/QueryChatView.vue'
import CreateAlertView from '../views/CreateAlerView.vue'
import ConfigurationView from '@/views/ConfigurationView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import { userStore } from '@/store/userStore'
import ShowAlertsView from '@/views/ShowAlertsView.vue'
import ShowAlertView from '@/views/ShowAlertView.vue'
import EditAlertView from '@/views/EditAlertView.vue'
import ConfigurationDatabaseView from '@/views/ConfigurationDatabaseView.vue'
import ReportView from '@/views/ReportView.vue'



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
      name: 'alerts',
      component: ShowAlertsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/alerts/create',
      name: 'create_alert',
      component: CreateAlertView,
      meta: { requiresAuth: true }
    },
    {
      path: '/alerts/:id',
      name: 'alert_details',
      component: ShowAlertView,
      meta: { requiresAuth: true },
    },
    {
      path: '/alerts/:id/edit',
      name: 'alert_edit',
      component: EditAlertView,
      meta: { requiresAuth: true },
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
    },
    {
      path: '/databases',
      name: 'databases',
      component: ConfigurationDatabaseView,
      meta: { requiresAuth: true }
    },
    {
      path: '/reports',
      name: 'report',
      component: ReportView,
      meta: { requiresAuth: true }
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
