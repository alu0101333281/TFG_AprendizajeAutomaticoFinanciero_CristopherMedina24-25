import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import BacktestingView from '../views/BacktestingView.vue'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  {
    path: '/app',
    component: BacktestingView,
    meta: { requiresAuth: true }
  },
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🚧 Protege rutas que necesitan autenticación
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login') // Redirige a login si no hay token
  } else {
    next() // Permite la navegación
  }
})

export default router
