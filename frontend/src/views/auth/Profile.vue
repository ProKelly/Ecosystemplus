<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Change Password Modal -->
    <TransitionRoot appear :show="isPasswordModalOpen" as="template">
      <Dialog as="div" class="relative z-50" @close="closePasswordModal">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25 backdrop-blur-sm" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900"
                >
                  Change Password
                </DialogTitle>
                
                <form @submit.prevent="changePassword" class="mt-4 space-y-4">
                  <div>
                    <label for="current_password" class="block text-sm font-medium text-gray-700">
                      Current password
                    </label>
                    <input
                      id="current_password"
                      v-model="password.current"
                      type="password"
                      required
                      class="text-black mt-1 p-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="new_password" class="block text-sm font-medium text-gray-700">
                      New password
                    </label>
                    <input
                      id="new_password"
                      v-model="password.new"
                      type="password"
                      required
                      class="text-black mt-1 p-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="confirm_password" class="block text-sm font-medium text-gray-700">
                      Confirm new password
                    </label>
                    <input
                      id="confirm_password"
                      v-model="password.confirm"
                      type="password"
                      required
                      class="my-2 p-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                    />
                  </div>

                  <div class="mt-6 flex justify-end space-x-3">
                    <button
                      type="button"
                      @click="closePasswordModal"
                      class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      :disabled="changingPassword"
                      class="inline-flex justify-center rounded-md border border-transparent bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <span v-if="!changingPassword">Update Password</span>
                      <span v-else class="flex items-center">
                        <ArrowPathIcon class="h-4 w-4 mr-2 animate-spin" />
                        Updating...
                      </span>
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Profile Photo Upload Modal -->
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden" 
      accept="image/*" 
      @change="handleFileUpload"
    />

    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Profile Settings</h1>
        <p class="mt-1 text-sm text-gray-600">Manage your personal information and account security</p>
      </div>
      <button
        @click="handleLogout"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Logout
      </button>
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <!-- Profile Details -->
      <div class="lg:col-span-2">
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Personal Information</h3>
          </div>
          <div class="px-6 py-5">
            <form @submit.prevent="updateProfile">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="first_name" class="block text-sm font-medium text-gray-700">First name</label>
                  <input
                    id="first_name"
                    v-model="profile.first_name"
                    type="text"
                    required
                    class="text-black mt-1 p-3 block w-full rounded-lg border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label for="last_name" class="block text-sm font-medium text-gray-700">Last name</label>
                  <input
                    id="last_name"
                    v-model="profile.last_name"
                    type="text"
                    required
                    class="text-black mt-1 p-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                  <input
                    id="email"
                    v-model="profile.email"
                    type="email"
                    disabled
                    class="text-black mt-1 p-3 block w-full rounded-md border-gray-300 bg-gray-100 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label for="phone_number" class="block text-sm font-medium text-gray-700">Phone number</label>
                  <input
                    id="phone_number"
                    v-model="profile.phone_number"
                    type="tel"
                    class="text-black mt-1 p-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm"
                  />
                </div>
              </div>

              <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700">Profile photo</label>
                <div class="mt-2 flex items-center">
                  <div class="relative">
                    <div class="h-16 w-16 rounded-full overflow-hidden bg-gray-100 border-2 border-emerald-100">
                      <img
                        v-if="profile.profile_image"
                        :src="profile.profile_image"
                        alt="Profile"
                        class="h-full w-full object-cover"
                      />
                      <UserCircleIcon v-else class="h-full w-full text-gray-300" />
                    </div>
                    <button
                      type="button"
                      @click="$refs.fileInput.click()"
                      class="absolute -bottom-1 -right-1 bg-white p-1.5 rounded-full shadow-md border border-gray-200 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    >
                      <PencilIcon class="h-4 w-4 text-emerald-600" />
                    </button>
                  </div>
                  <button
                    type="button"
                    @click="$refs.fileInput.click()"
                    class="ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
                  >
                    Change
                  </button>
                </div>
              </div>

              <div class="mt-8 border-t border-gray-200 pt-5">
                <div class="flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="resetForm"
                    class="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="updating"
                    class="inline-flex justify-center rounded-md border border-transparent bg-emerald-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span v-if="!updating">Save Changes</span>
                    <span v-else class="flex items-center">
                      <ArrowPathIcon class="h-4 w-4 mr-2 animate-spin" />
                      Saving...
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Account Type & Security -->
      <div class="space-y-6">
        <!-- Account Type -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Account Type</h3>
          </div>
          <div class="px-6 py-5">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-gradient-to-r from-emerald-500 to-green-500 rounded-lg p-3 shadow-sm">
                <UserGroupIcon v-if="isCommunity" class="h-6 w-6 text-white" />
                <UserIcon v-else class="h-6 w-6 text-white" />
              </div>
              <div class="ml-4">
                <h4 class="text-sm font-medium text-gray-900">
                  {{ isCommunity ? 'Community Admin' : 'Farmer' }}
                </h4>
                <p class="text-sm text-gray-500">
                  {{ isCommunity ? 'Manage your community settings' : 'Access farming tools and resources' }}
                </p>
              </div>
            </div>
             <div v-if="isCommunity" class="mt-8 flex justify-end">
              <router-link
                to="/community/manage"
                class="inline-flex items-center rounded-md border border-emerald-600 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700 hover:bg-emerald-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
              >
                Manage Community
              </router-link>
            </div>
          </div>
        </div>

        <!-- Security Card -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Security</h3>
          </div>
          <div class="px-6 py-5">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Password</h4>
                  <p class="text-sm text-gray-500">Last changed 3 months ago</p>
                </div>
                <button
                  @click="openPasswordModal"
                  class="inline-flex items-center rounded-md border border-transparent bg-emerald-100 px-3 py-1.5 text-sm font-medium text-emerald-700 hover:bg-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                >
                  Change
                </button>
              </div>
              
              <!-- <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Two-factor authentication</h4>
                  <p class="text-sm text-gray-500">Not enabled</p>
                </div>
                <button
                  class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
                >
                  Enable
                </button>
              </div> -->
            </div>
            <!-- Community Management Button for Admins -->
           
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'
import {
  UserCircleIcon,
  UserGroupIcon,
  UserIcon,
  ArrowPathIcon,
  PencilIcon
} from '@heroicons/vue/24/outline'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from '@headlessui/vue'

const authStore = useAuthStore()

// Profile data
const profile = ref({
  first_name: authStore.user?.first_name || '',
  last_name: authStore.user?.last_name || '',
  email: authStore.user?.email || '',
  phone_number: authStore.user?.phone_number || '',
  profile_image: authStore.user?.profile_image || null
})

// Password modal state
const isPasswordModalOpen = ref(false)
const password = ref({
  current: '',
  new: '',
  confirm: ''
})

// Loading states
const updating = ref(false)
const changingPassword = ref(false)
const fileInput = ref(null)

// Computed properties
const isCommunity = computed(() => authStore.user?.role === 'community')

// Methods
const openPasswordModal = () => {
  isPasswordModalOpen.value = true
}

const closePasswordModal = () => {
  isPasswordModal.value = false
  password.value = { current: '', new: '', confirm: '' }
}

const resetForm = () => {
  profile.value = {
    first_name: authStore.user?.first_name || '',
    last_name: authStore.user?.last_name || '',
    email: authStore.user?.email || '',
    phone_number: authStore.user?.phone_number || '',
    profile_image: authStore.user?.profile_image || null
  }
}

const updateProfile = async () => {
  try {
    updating.value = true
    await authStore.updateProfile(profile.value)
    showToast('Profile updated successfully!', 'success')
  } catch (error) {
    showToast(error.message, 'error')
  } finally {
    updating.value = false
  }
}

const changePassword = async () => {
  if (password.value.new !== password.value.confirm) {
    showToast('New passwords do not match', 'error')
    return
  }

  try {
    changingPassword.value = true
    await authStore.changePassword({
      current_password: password.value.current,
      new_password: password.value.new
    })
    showToast('Password changed successfully!', 'success')
    closePasswordModal()
  } catch (error) {
    showToast(error.message, 'error')
  } finally {
    changingPassword.value = false
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.match('image.*')) {
    showToast('Please select an image file', 'error')
    return
  }

  // Validate file size (max 2MB)
  if (file.size > 2 * 1024 * 1024) {
    showToast('Image size should be less than 2MB', 'error')
    return
  }

  // Create preview and update profile image
  const reader = new FileReader()
  reader.onload = (e) => {
    profile.value.profile_image = e.target.result
    // In a real app, you would upload the file to your server here
    showToast('Profile photo updated! Don\'t forget to save your changes.', 'info')
  }
  reader.readAsDataURL(file)
}

const handleLogout = async () => {
  await authStore.logout()
  showToast('Logged out successfully', 'success')
}
</script>

<style scoped>
/* Custom styling for the file input button */
input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>