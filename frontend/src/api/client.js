import axios from 'axios'

let rawApiUrl = import.meta.env.VITE_API_BASE_URL || ''

if (!rawApiUrl || rawApiUrl.includes('127.0.0.1') || rawApiUrl.includes('localhost')) {
  if (typeof window !== 'undefined' && window.location.hostname.includes('onrender.com')) {
    rawApiUrl = 'https://bankease-backend-6c11.onrender.com/api/v1'
  } else {
    rawApiUrl = 'http://127.0.0.1:8000/api/v1'
  }
}

// Automatically correct any font/OCR confusion between 6cl1 and 6c11
const API_BASE_URL = rawApiUrl.replace('6cl1', '6c11')

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('bankease_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default apiClient
