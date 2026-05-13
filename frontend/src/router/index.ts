import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import PositionsView from '@/views/positions/PositionsView.vue'
import PositionsForm from '@/views/positions/Form.vue'
import EmployeesView from '@/views/employees/EmployeesView.vue'
import ServiceTypesView from '@/views/service-types/ServiceTypesView.vue'
import ServiceOrdersView from '@/views/service-orders/ServiceOrdersView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/positions',
      name: 'positions',
      component: PositionsView,
    },
    {
      path: '/positions/new',
      name: 'positions-new',
      component: PositionsForm,
    },
    {
      path: '/positions/:id',
      name: 'positions-visualize',
      component: PositionsForm,
      props: true,
    },
    {
      path: '/employees',
      name: 'employees',
      component: EmployeesView,
    },
    {
      path: '/service-types',
      name: 'service-types',
      component: ServiceTypesView,
    },
    {
      path: '/service-orders',
      name: 'service-orders',
      component: ServiceOrdersView,
    },
  ],
})

export default router
