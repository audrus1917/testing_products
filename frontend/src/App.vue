<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { clearToken, getToken, parseJwtPayload } from './api/client'

const router = useRouter()

const isAuthorized = computed(() => Boolean(getToken()))
const userData = computed(() => parseJwtPayload(getToken()))

function logout() {
  clearToken()
  router.push('/login')
}
</script>

<template>
  <div class="layout">
    <header class="header">
      <h1>Testing Products UI</h1>
      <nav class="nav" v-if="isAuthorized">
        <RouterLink to="/products">Товары</RouterLink>
        <RouterLink to="/clients">Клиенты</RouterLink>
        <RouterLink to="/orders">Заказы</RouterLink>
      </nav>
      <div class="auth-box" v-if="isAuthorized">
        <span class="user-email">{{ userData?.email || 'user' }}</span>
        <button type="button" @click="logout">Выйти</button>
      </div>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>
