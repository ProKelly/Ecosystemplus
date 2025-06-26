<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Create New Community</h1>
      <p class="mt-2 text-sm text-gray-600">
        Set up your farming community to connect with local farmers and manage shared resources.
      </p>
    </div>

    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-5 border-b border-gray-200">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Community Information</h3>
      </div>
      <div class="px-6 py-5">
        <form @submit.prevent="createCommunity">
          <div class="grid grid-cols-1 gap-6">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Community name</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                required
              />
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Contact email</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Location</label>
              <div class="mt-1 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label for="latitude" class="sr-only">Latitude</label>
                  <input
                    id="latitude"
                    v-model="form.latitude"
                    type="number"
                    step="any"
                    placeholder="Latitude"
                    class="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                    required
                  />
                </div>
                <div>
                  <label for="longitude" class="sr-only">Longitude</label>
                  <input
                    id="longitude"
                    v-model="form.longitude"
                    type="number"
                    step="any"
                    placeholder="Longitude"
                    class="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                    required
                  />
                </div>
              </div>
              <p class="mt-2 text-sm text-gray-500">
                Enter the approximate coordinates of your community center
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Location on map</label>
              <!-- Search bar above the map -->
              <div class="flex items-center mb-2 gap-2">
                <input v-model="searchQuery" type="text" placeholder="Search location by name..." class="text-black flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-emerald-300" />
                <button @click="searchLocation" type="button" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded shadow">Search</button>
              </div>
              <div class="mt-1 h-64 bg-gray-100 rounded-md overflow-hidden">
                <div ref="mapContainer" class="h-full w-full"></div>
              </div>
              <p class="mt-2 text-sm text-gray-500">
                Click on the map to set your community location
              </p>
            </div>
          </div>

          <div class="mt-8 border-t border-gray-200 pt-5">
            <div class="flex justify-end">
              <router-link
                to="/dashboard"
                class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
              >
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="submitting"
                class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="!submitting">Create Community</span>
                <span v-else class="flex items-center">
                  <ArrowPathIcon class="animate-spin h-4 w-4 mr-2" />
                  Creating...
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { ArrowPathIcon } from '@heroicons/vue/24/outline'
import { useCommunityStore } from '@/stores/community'
import { showToast } from '@/utils/toast'

const router = useRouter()
const communityStore = useCommunityStore()

const form = ref({
  name: '',
  email: '',
  latitude: -1.2921,
  longitude: 36.8219
})

const map = ref<L.Map | null>(null)
const mapContainer = ref<HTMLElement | null>(null)
const marker = ref<L.Marker | null>(null)
const submitting = ref(false)
const searchQuery = ref('')

// Initialize map
onMounted(() => {
  if (mapContainer.value) {
    map.value = L.map(mapContainer.value, {
      center: [form.value.latitude, form.value.longitude],
      zoom: 13,
      zoomControl: false
    })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map.value)

    // Add marker
    marker.value = L.marker([form.value.latitude, form.value.longitude], {
      draggable: true
    }).addTo(map.value)

    // Update form when marker is dragged
    marker.value.on('dragend', (e) => {
      const { lat, lng } = e.target.getLatLng()
      form.value.latitude = lat
      form.value.longitude = lng
    })

    // Update marker when form changes
    watch(
      () => [form.value.latitude, form.value.longitude],
      ([lat, lng]) => {
        if (marker.value && lat && lng) {
          marker.value.setLatLng([lat, lng])
          map.value?.panTo([lat, lng])
        }
      }
    )

    // Click handler to move marker
    map.value.on('click', (e) => {
      form.value.latitude = e.latlng.lat
      form.value.longitude = e.latlng.lng
    })
  }
})

const createCommunity = async () => {
  try {
    submitting.value = true
    await communityStore.createCommunity(form.value)
    showToast('Community created successfully!', 'success')
    router.push('/dashboard')
  } catch (error) {
    showToast(error.message, 'error')
  } finally {
    submitting.value = false
  }
}

// Search location by name
const searchLocation = async () => {
  if (!searchQuery.value) return
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}`
  try {
    const res = await fetch(url)
    const data = await res.json()
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat)
      const lon = parseFloat(data[0].lon)
      form.value.latitude = lat
      form.value.longitude = lon
      if (map.value) {
        map.value.setView([lat, lon], 15)
        if (marker.value) {
          marker.value.setLatLng([lat, lon])
        }
      }
    } else {
      showToast('Location not found!', 'error')
    }
  } catch (e) {
    showToast('Error searching location!', 'error')
  }
}
</script>