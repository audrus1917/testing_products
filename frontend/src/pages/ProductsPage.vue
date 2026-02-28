<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api, getToken, parseJwtPayload } from '../api/client'

const state = reactive({
  items: [],
  total: 0,
  loading: false,
  error: '',
})

const form = reactive({
  name: '',
  description: '',
})

const userData = parseJwtPayload(getToken())
const canManage = Boolean(userData?.is_superuser)

async function loadProducts() {
  state.loading = true
  state.error = ''
  try {
    const result = await api.getProducts()
    state.items = result.items || []
    state.total = result.total || 0
  } catch (error) {
    state.error = error.message
  } finally {
    state.loading = false
  }
}

async function createProduct() {
  try {
    await api.createProduct({
      name: form.name,
      description: form.description || null,
    })
    form.name = ''
    form.description = ''
    await loadProducts()
  } catch (error) {
    state.error = error.message
  }
}

async function removeProduct(id) {
  try {
    await api.deleteProduct(id)
    await loadProducts()
  } catch (error) {
    state.error = error.message
  }
}

onMounted(loadProducts)
</script>

<template>
  <section class="page">
    <h2>Товары ({{ state.total }})</h2>

    <form class="panel" @submit.prevent="createProduct" v-if="canManage">
      <h3>Добавить товар</h3>
      <div class="grid two">
        <label>
          Название
          <input v-model="form.name" required />
        </label>
        <label>
          Описание
          <input v-model="form.description" />
        </label>
      </div>
      <button type="submit">Создать</button>
    </form>

    <p class="muted" v-else>Создание/удаление доступно только superuser.</p>

    <div class="panel">
      <button type="button" @click="loadProducts" :disabled="state.loading">Обновить</button>
      <p class="error" v-if="state.error">{{ state.error }}</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th v-if="canManage">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in state.items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.description || '-' }}</td>
            <td v-if="canManage">
              <button type="button" class="danger" @click="removeProduct(item.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
