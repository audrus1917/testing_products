<script setup>
import { onMounted, reactive } from 'vue'
import { api, getToken, parseJwtPayload } from '../api/client'

const state = reactive({
  items: [],
  total: 0,
  loading: false,
  error: '',
})

const form = reactive({
  last_name: '',
  first_name: '',
  address: '',
  phone: '',
})

const userData = parseJwtPayload(getToken())
const canManage = Boolean(userData?.is_superuser)

async function loadClients() {
  state.loading = true
  state.error = ''
  try {
    const result = await api.getClients()
    state.items = result.items || []
    state.total = result.total || 0
  } catch (error) {
    state.error = error.message
  } finally {
    state.loading = false
  }
}

async function createClient() {
  try {
    await api.createClient({ ...form, phone: form.phone || null })
    form.last_name = ''
    form.first_name = ''
    form.address = ''
    form.phone = ''
    await loadClients()
  } catch (error) {
    state.error = error.message
  }
}

async function removeClient(id) {
  try {
    await api.deleteClient(id)
    await loadClients()
  } catch (error) {
    state.error = error.message
  }
}

onMounted(loadClients)
</script>

<template>
  <section class="page">
    <h2>Клиенты ({{ state.total }})</h2>

    <form class="panel" @submit.prevent="createClient" v-if="canManage">
      <h3>Добавить клиента</h3>
      <div class="grid two">
        <label>
          Фамилия
          <input v-model="form.last_name" required />
        </label>
        <label>
          Имя
          <input v-model="form.first_name" required />
        </label>
        <label>
          Адрес
          <input v-model="form.address" required />
        </label>
        <label>
          Телефон
          <input v-model="form.phone" />
        </label>
      </div>
      <button type="submit">Создать</button>
    </form>

    <p class="muted" v-else>Создание/удаление доступно только superuser.</p>

    <div class="panel">
      <button type="button" @click="loadClients" :disabled="state.loading">Обновить</button>
      <p class="error" v-if="state.error">{{ state.error }}</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Адрес</th>
            <th>Телефон</th>
            <th v-if="canManage">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in state.items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.last_name }} {{ item.first_name }}</td>
            <td>{{ item.address }}</td>
            <td>{{ item.phone || '-' }}</td>
            <td v-if="canManage">
              <button type="button" class="danger" @click="removeClient(item.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
