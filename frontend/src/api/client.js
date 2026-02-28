import api from './index'

export const apiClient = {
  trips: {
    list: () => api.get('/trips/'),
    get: (id) => api.get(`/trips/${id}`),
    create: (data) => api.post('/trips/', data),
    update: (id, data) => api.put(`/trips/${id}`, data),
    delete: (id) => api.delete(`/trips/${id}`)
  },
  members: {
    listByTrip: (tripId) => api.get(`/members/trip/${tripId}`),
    create: (data) => api.post('/members/', data),
    delete: (id) => api.delete(`/members/${id}`)
  },
  wallets: {
    list: (params) => api.get('/wallets/', { params }),
    get: (id) => api.get(`/wallets/${id}`),
    create: (data) => api.post('/wallets/', data),
    update: (id, data) => api.put(`/wallets/${id}`, data),
    delete: (id) => api.delete(`/wallets/${id}`),
    updateMembers: (id, members) => api.put(`/wallets/${id}/members`, members)
  },
  transactions: {
    list: (params) => api.get('/transactions/', { params }),
    get: (id) => api.get(`/transactions/${id}`),
    create: (data) => api.post('/transactions/', data),
    update: (id, data) => api.put(`/transactions/${id}`, data),
    delete: (id) => api.delete(`/transactions/${id}`)
  },
  categories: {
    list: () => api.get('/categories/'),
    create: (data) => api.post('/categories/', data),
    delete: (id) => api.delete(`/categories/${id}`)
  },
  stats: {
    perPerson: (tripId) => api.get(`/stats/per-person/${tripId}`),
    walletSummary: (tripId) => api.get(`/stats/wallet-summary/${tripId}`)
  }
}
