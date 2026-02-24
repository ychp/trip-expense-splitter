import api from './index'

export const getSummary = (params) => api.get('/statistics/summary', { params })
export const getByCategory = (params) => api.get('/statistics/by-category', { params })
export const getTrend = (params) => api.get('/statistics/trend', { params })
export const getAccountsSummary = () => api.get('/statistics/accounts')
