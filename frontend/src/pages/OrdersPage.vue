<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '../api/client'

const state = reactive({
  items: [],
  total: 0,
  loading: false,
  error: '',
  success: '',
})

const createForm = reactive({
  order_no: '',
  client_id: '',
  delivery_method: 'DELIVERY',
})

const itemForm = reactive({
  order_id: '',
  product_id: '',
  amount: '',
  price: '',
})

async function loadOrders() {
  state.loading = true
  state.error = ''
  state.success = ''
  try {
    const result = await api.getOrders()
    state.items = result.items || []
    state.total = result.total || 0
  } catch (error) {
    state.error = error.message
  } finally {
    state.loading = false
  }
}

async function createOrder() {
  state.error = ''
  state.success = ''
  try {
    await api.createOrder({
      order_no: createForm.order_no,
      client_id: Number(createForm.client_id),
      delivery_method: createForm.delivery_method,
    })
    createForm.order_no = ''
    createForm.client_id = ''
    createForm.delivery_method = 'DELIVERY'
    state.success = 'Заказ создан'
    await loadOrders()
  } catch (error) {
    state.error = error.message
  }
}

async function addItem() {
  state.error = ''
  state.success = ''
  try {
    await api.addOrderItem(Number(itemForm.order_id), {
      order_id: Number(itemForm.order_id),
      product_id: Number(itemForm.product_id),
      amount: itemForm.amount,
      price: itemForm.price || null,
    })
    itemForm.order_id = ''
    itemForm.product_id = ''
    itemForm.amount = ''
    itemForm.price = ''
    state.success = 'Товар добавлен в заказ'
    await loadOrders()
  } catch (error) {
    state.error = error.message
  }
}

onMounted(loadOrders)
</script>

<template>
  <section class="page">
    <h2>Заказы ({{ state.total }})</h2>

    <form class="panel" @submit.prevent="createOrder">
      <h3>Создать заказ</h3>
      <div class="grid three">
        <label>
          Номер заказа
          <input v-model="createForm.order_no" required />
        </label>
        <label>
          ID клиента
          <input v-model="createForm.client_id" type="number" min="1" required />
        </label>
        <label>
          Доставка
          <select v-model="createForm.delivery_method">
            <option value="DELIVERY">DELIVERY</option>
            <option value="EXPRESS_DELIVERY">EXPRESS_DELIVERY</option>
          </select>
        </label>
      </div>
      <button type="submit">Создать</button>
    </form>

    <form class="panel" @submit.prevent="addItem">
      <h3>Добавить товар в заказ</h3>
      <div class="grid four">
        <label>
          ID заказа
          <input v-model="itemForm.order_id" type="number" min="1" required />
        </label>
        <label>
          ID товара
          <input v-model="itemForm.product_id" type="number" min="1" required />
        </label>
        <label>
          Количество
          <input v-model="itemForm.amount" type="number" min="0" step="0.01" required />
        </label>
        <label>
          Цена (опц.)
          <input v-model="itemForm.price" type="number" min="0" step="0.01" />
        </label>
      </div>
      <button type="submit">Добавить товар</button>
    </form>

    <div class="panel">
      <button type="button" @click="loadOrders" :disabled="state.loading">Обновить</button>
      <p class="error" v-if="state.error">{{ state.error }}</p>
      <p class="success" v-if="state.success">{{ state.success }}</p>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Номер</th>
            <th>ID клиента</th>
            <th>Статус</th>
            <th>Оплата</th>
            <th>Доставка</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in state.items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.order_no }}</td>
            <td>{{ item.client_id }}</td>
            <td>{{ item.status }}</td>
            <td>{{ item.payment_date || '-' }}</td>
            <td>{{ item.delivery_date || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
