import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const user = ref(null)
  // Store both tokens
  const token = ref(localStorage.getItem('token') || sessionStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken') || null)

  // Store credentials for autofill
  const savedEmail = ref(localStorage.getItem('savedEmail') || '')
  const savedPassword = ref(localStorage.getItem('savedPassword') || '')

  // Helper: Save tokens to storage
  function saveTokens(access: string, refresh: string, remember: boolean) {
    token.value = access
    refreshToken.value = refresh
    if (remember) {
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('refreshToken')
    } else {
      sessionStorage.setItem('token', access)
      sessionStorage.setItem('refreshToken', refresh)
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
    }
  }

  // Helper: Save credentials for autofill
  function saveCredentials(email: string, password: string, remember: boolean) {
    if (remember) {
      localStorage.setItem('savedEmail', email)
      localStorage.setItem('savedPassword', password)
      savedEmail.value = email
      savedPassword.value = password
    } else {
      localStorage.removeItem('savedEmail')
      localStorage.removeItem('savedPassword')
      savedEmail.value = ''
      savedPassword.value = ''
    }
  }

  // Refresh access token using refresh token
  const refreshAccessToken = async () => {
    if (!refreshToken.value) throw new Error('No refresh token')
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/auth/token/refresh/`,
        { refresh: refreshToken.value }
      )
      token.value = response.data.access
      // Update storage
      if (localStorage.getItem('refreshToken')) {
        if (token.value) localStorage.setItem('token', token.value)
      } else {
        if (token.value) sessionStorage.setItem('token', token.value)
      }
      return token.value
    } catch (error) {
      logout()
      throw error
    }
  }

  // Axios interceptor for auto-refresh
  axios.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config
      if (error.response && error.response.status === 401 && refreshToken.value && !originalRequest._retry) {
        originalRequest._retry = true
        try {
          await refreshAccessToken()
          originalRequest.headers['Authorization'] = `Bearer ${token.value}`
          return axios(originalRequest)
        } catch (e) {
          logout()
        }
      }
      return Promise.reject(error)
    }
  )

  const login = async (credentials: { email: string; password: string; remember?: boolean }) => {
    const response = await api.login(credentials)
    // Store both tokens
    saveTokens(response.data.access, response.data.refresh, !!credentials.remember)
    // Save credentials for autofill
    saveCredentials(credentials.email, credentials.password, !!credentials.remember)
    await fetchUser()
  }

  const register = async (userData: {
    first_name: string
    last_name: string
    email: string
    password: string
    role: string
    phone_number?: string
  }) => {
    await api.register(userData)
    await login({
      email: userData.email,
      password: userData.password
    })
  }

  const fetchUser = async () => {
    try {
      if (!token.value) throw new Error('No token')
      const response = await api.getProfile(token.value)
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  const updateProfile = async (profileData: any) => {
    if (!token.value) throw new Error('No token')
    const response = await axios.patch(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/auth/profile/`,
      profileData,
      { headers: { Authorization: `Bearer ${token.value}` } }
    )
    user.value = response.data
  }

  const changePassword = async (passwordData: {
    current_password: string
    new_password: string
  }) => {
    if (!token.value) throw new Error('No token')
    await axios.post(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/auth/change-password/`,
      passwordData,
      { headers: { Authorization: `Bearer ${token.value}` } }
    )
  }

  const logout = () => {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('refreshToken')
    localStorage.removeItem('savedEmail')
    localStorage.removeItem('savedPassword')
    router.push('/login')
  }

  return {
    user,
    token,
    refreshToken,
    savedEmail,
    savedPassword,
    login,
    register,
    fetchUser,
    updateProfile,
    changePassword,
    logout,
    refreshAccessToken
  }
})