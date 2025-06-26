<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8">
      <div>
        <div class="flex justify-center">
          <div class="w-16 h-16 rounded-full bg-emerald-600 flex items-center justify-center">
            <MapPinIcon class="h-8 w-8 text-white" />
          </div>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or <router-link to="/register" class="font-medium text-emerald-600 hover:text-emerald-500">
            create a new account
          </router-link>
        </p>
      </div>
      <div class="bg-white py-8 px-6 shadow rounded-lg">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="mt-2 appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base text-black"
              />
            </div>
            <div class="py-3">
              <label for="password" class="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="mt-2 appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base text-black"
              />
            </div>
          </div>
          <div class="flex items-center justify-between py-4">
            <div class="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                v-model="form.remember"
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>
            <div class="text-sm">
              <router-link to="/forgot-password" class="font-medium text-emerald-600 hover:text-emerald-500">
                Forgot your password?
              </router-link>
            </div>
          </div>
          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full my-2 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!loading">Sign in</span>
              <span v-else class="flex items-center">
                <ArrowPathIcon class="animate-spin h-4 w-4 mr-2" />
                Signing in...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowPathIcon, MapPinIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
  remember: false
})

const loading = ref(false)

onMounted(() => {
  // Autofill credentials if saved
  if (authStore.savedEmail && authStore.savedPassword) {
    form.value.email = authStore.savedEmail
    form.value.password = authStore.savedPassword
    form.value.remember = true
  } else {
    form.value.remember = false
  }
})

// Also update form if savedEmail/savedPassword change (after login)
watchEffect(() => {
  if (authStore.savedEmail && authStore.savedPassword) {
    form.value.email = authStore.savedEmail
    form.value.password = authStore.savedPassword
    form.value.remember = true
  }
})

const handleLogin = async () => {
  try {
    loading.value = true
    await authStore.login({
      email: form.value.email,
      password: form.value.password,
      remember: form.value.remember
    })
    showToast('Login successful!', 'success')
    router.push('/')
  } catch (error) {
    showToast(error.message, 'error')
  } finally {
    loading.value = false
  }
}
</script>