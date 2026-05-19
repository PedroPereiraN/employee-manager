import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import PositionsView from '@/views/positions/PositionsView.vue'
import PositionsForm from '@/views/positions/Form.vue'
import EmployeesView from '@/views/employees/EmployeesView.vue'
import EmployeesForm from '@/views/employees/Form.vue'
import ServiceTypesView from '@/views/service-types/ServiceTypesView.vue'
import ServiceTypesForm from '@/views/service-types/Form.vue'
import ServiceOrdersView from '@/views/service-orders/ServiceOrdersView.vue'
import ServiceOrdersForm from '@/views/service-orders/Form.vue'
import ServiceOrdersReportProgress from '@/views/service-orders/ReportProgress.vue'
import ServiceOrdersTimeline from '@/views/service-orders/Timeline.vue'
import UsersView from '@/views/users/UsersView.vue'
import UsersForm from '@/views/users/Form.vue'

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
      path: '/employees/new',
      name: 'employees-new',
      component: EmployeesForm,
    },
    {
      path: '/employees/:id',
      name: 'employees-visualize',
      component: EmployeesForm,
      props: true,
    },
    {
      path: '/service-types',
      name: 'service-types',
      component: ServiceTypesView,
    },
    {
      path: '/service-types/new',
      name: 'service-types-new',
      component: ServiceTypesForm,
    },
    {
      path: '/service-types/:id',
      name: 'service-types-visualize',
      component: ServiceTypesForm,
      props: true,
    },
    {
      path: '/service-orders',
      name: 'service-orders',
      component: ServiceOrdersView,
    },
    {
      path: '/service-orders/new',
      name: 'service-orders-new',
      component: ServiceOrdersForm,
    },
    {
      path: '/service-orders/:id',
      name: 'service-orders-visualize',
      component: ServiceOrdersForm,
      props: true,
    },
    {
      path: '/service-orders/:id/report-progress',
      name: 'service-orders-report-progress',
      component: ServiceOrdersReportProgress,
      props: true,
    },
    {
      path: '/service-orders/:id/timeline',
      name: 'service-orders-timeline',
      component: ServiceOrdersTimeline,
      props: true,
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView,
    },
    {
      path: '/users/new',
      name: 'users-new',
      component: UsersForm,
    },
    {
      path: '/users/:id',
      name: 'users-visualize',
      component: UsersForm,
      props: true,
    },
  ],
})

export default router
