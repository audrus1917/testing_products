const API_BASE = '/api/v1'
const TOKEN_KEY = 'tp_access_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function parseJwtPayload(token) {
  if (!token) {
    return null
  }
  try {
    const payload = token.split('.')[1]
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(normalized))
  } catch {
    return null
  }
}

async function request(path, options = {}) {
  const token = getToken()
  const headers = new Headers(options.headers || {})

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  const contentType = response.headers.get('content-type') || ''
  const body = contentType.includes('application/json') ? await response.json() : null

  if (!response.ok) {
    const detail = body?.detail || `HTTP ${response.status}`
    throw new Error(detail)
  }

  return body
}

export async function login(email, password) {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)

  const response = await fetch(`${API_BASE}/auth/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: form,
  })

  const body = await response.json()
  if (!response.ok) {
    throw new Error(body?.detail || 'Ошибка аутентификации')
  }

  setToken(body.access_token)
  return body
}

export const api = {
  getProducts: () => request('/products/'),
  createProduct: (payload) => request('/products/', { method: 'POST', body: JSON.stringify(payload) }),
  deleteProduct: (id) => request(`/products/${id}`, { method: 'DELETE' }),

  getClients: () => request('/clients/'),
  createClient: (payload) => request('/clients/', { method: 'POST', body: JSON.stringify(payload) }),
  deleteClient: (id) => request(`/clients/${id}`, { method: 'DELETE' }),

  getOrders: () => request('/orders/'),
  createOrder: (payload) => request('/orders/', { method: 'POST', body: JSON.stringify(payload) }),
  addOrderItem: (orderId, payload) =>
    request(`/orders/${orderId}/items/add`, { method: 'POST', body: JSON.stringify(payload) }),
}
