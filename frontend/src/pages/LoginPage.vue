<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/client'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorText = ref('')

async function submit() {
  loading.value = true
  errorText.value = ''
  try {
    await login(email.value, password.value)
    router.push('/products')
  } catch (error) {
    errorText.value = error.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="page narrow">
    <h2>Вход</h2>
    <form class="panel" @submit.prevent="submit">
      <label>
        Email
        <input v-model="email" type="email" required />
      </label>
      <label>
        Пароль
        <input v-model="password" type="password" required />
      </label>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Входим...' : 'Войти' }}
      </button>
      <p class="error" v-if="errorText">{{ errorText }}</p>
    </form>
  </section>
</template>
