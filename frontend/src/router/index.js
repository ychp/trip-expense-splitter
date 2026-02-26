import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/trips',
    name: 'Trips',
    component: () => import('../views/Trips.vue')
  },
  {
    path: '/trips/:id',
    name: 'TripDetail',
    component: () => import('../views/TripDetail.vue')
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: () => import('../views/Transactions.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue')
  },
  {
    path: '/wallets',
    name: 'Wallets',
    component: () => import('../views/Wallets.vue')
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('../views/Categories.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
