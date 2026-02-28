import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './pages/LoginPage.vue'
import ProductsPage from './pages/ProductsPage.vue'
import ClientsPage from './pages/ClientsPage.vue'
import OrdersPage from './pages/OrdersPage.vue'
import { getToken } from './api/client'

const routes = [
  { path: '/', redirect: '/products' },
  { path: '/login', component: LoginPage, meta: { public: true } },
  { path: '/products', component: ProductsPage },
  { path: '/clients', component: ClientsPage },
  { path: '/orders', component: OrdersPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.public) {
    return true
  }
  if (!getToken()) {
    return '/login'
  }
  return true
})
