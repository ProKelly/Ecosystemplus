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
          Create a new account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or <router-link to="/login" class="font-medium text-emerald-600 hover:text-emerald-500">
            sign in to your account
          </router-link>
        </p>
      </div>
      <div class="bg-white py-8 px-6 shadow rounded-lg">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="first_name" class="block text-sm font-medium text-gray-700">
                First name
              </label>
              <input
                id="first_name"
                v-model="form.first_name"
                name="first_name"
                type="text"
                autocomplete="given-name"
                required
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
            <div>
              <label for="last_name" class="block text-sm font-medium text-gray-700">
                Last name
              </label>
              <input
                id="last_name"
                v-model="form.last_name"
                name="last_name"
                type="text"
                autocomplete="family-name"
                required
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
          </div>
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
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
            <div>
              <label for="phone_number" class="block text-sm font-medium text-gray-700">
                Phone number
              </label>
              <input
                id="phone_number"
                v-model="form.phone_number"
                name="phone_number"
                type="tel"
                autocomplete="tel"
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
            <div>
              <label for="confirm_password" class="block text-sm font-medium text-gray-700">
                Confirm password
              </label>
              <input
                id="confirm_password"
                v-model="form.confirm_password"
                name="confirm_password"
                type="password"
                autocomplete="new-password"
                required
                class="mt-2 text-black appearance-none block w-full px-5 py-3 border border-gray-300 rounded-2xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-base"
              />
            </div>
            <div class="py-3">
              <label class="block text-sm font-medium text-gray-700">
                Account type
              </label>
              <div class="mt-1 space-y-2">
                <div class="flex items-center">
                  <input
                    id="user-role"
                    v-model="form.role"
                    name="role"
                    type="radio"
                    value="user"
                    class="focus:ring-emerald-500 h-4 w-4 text-emerald-600 border-gray-300"
                  />
                  <label for="user-role" class="ml-2 block text-sm text-gray-900">
                    Farmer
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="community-role"
                    v-model="form.role"
                    name="role"
                    type="radio"
                    value="community"
                    class="focus:ring-emerald-500 h-4 w-4 text-emerald-600 border-gray-300"
                  />
                  <label for="community-role" class="ml-2 block text-sm text-gray-900">
                    Community Admin
                  </label>
                </div>
              </div>
            </div>
            <div class="flex items-center py-2">
              <input
                id="terms"
                v-model="form.terms"
                name="terms"
                type="checkbox"
                required
                class="focus:ring-emerald-500 h-4 w-4 text-emerald-600 border-gray-300 rounded"
              />
              <label for="terms" class="ml-2 block text-sm text-gray-900">
                I agree to the <a href="#" class="text-emerald-600 hover:text-emerald-500">Terms</a> and <a href="#" class="text-emerald-600 hover:text-emerald-500">Privacy Policy</a>
              </label>
            </div>
          </div>
          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!loading">Create account</span>
              <span v-else class="flex items-center">
                <ArrowPathIcon class="animate-spin h-4 w-4 mr-2" />
                Creating account...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowPathIcon, MapPinIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  password: '',
  confirm_password: '',
  role: 'user',
  terms: false
})

const loading = ref(false)

const handleRegister = async () => {
  if (form.value.password !== form.value.confirm_password) {
    showToast('Passwords do not match', 'error')
    return
  }

  try {
    loading.value = true
    await authStore.register(form.value)
    showToast('Account created successfully!', 'success')
    router.push('/dashboard')
  } catch (error) {
    showToast(error.message, 'error')
  } finally {
    loading.value = false
  }
}
</script>