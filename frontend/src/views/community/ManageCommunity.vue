<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-[80vh]">
    <!-- Header Section -->
    <div class="text-center mb-10">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Community Management</h1>
      <p class="text-black text-lg">
        Monitor your community farms.
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center h-64">
      <div class="w-12 h-12 border-4 border-emerald-100 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
      <span class="text-gray-500">Loading community data...</span>
    </div>

    <!-- No Community State -->
    <div v-else-if="!community" class="flex flex-col items-center justify-center bg-white rounded-xl shadow-sm p-8 max-w-md mx-auto">
      <div class="bg-emerald-50 p-5 rounded-full mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-800 mb-2">No Community Found</h2>
      <p class="text-gray-500 text-center mb-6">You haven't created a community yet. Get started by registering your community.</p>
      <button
        @click="goToCreateCommunity"
        class="w-full bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
      >
        Create Community
      </button>
    </div>

    <!-- Community Content -->
    <div v-else class="space-y-8">
      <!-- Community Info Card -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
        <div class="bg-gradient-to-r from-emerald-50 to-green-50 px-6 py-4 border-b border-gray-100">
          <h2 class="text-xl font-bold text-gray-800">{{ community.name }}</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-1">
              <h3 class="text-sm font-medium text-gray-500">Contact Email</h3>
              <p class="text-gray-900">{{ community.email }}</p>
            </div>
            <div class="space-y-1">
              <h3 class="text-sm font-medium text-gray-500">Location Coordinates</h3>
              <p class="text-gray-900">{{ community.latitude }}, {{ community.longitude }}</p>
            </div>
            <div class="space-y-1">
              <h3 class="text-sm font-medium text-gray-500">Date Created</h3>
              <p class="text-gray-900">{{ formatDate(community.created) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Farms Section -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Farms List -->
        <div class="lg:col-span-1 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="bg-gradient-to-r from-emerald-50 to-green-50 px-6 py-4 border-b border-gray-100">
            <h2 class="text-lg font-semibold text-gray-800">Registered Farms</h2>
          </div>
          <div class="p-4">
            <div v-if="farms.length === 0" class="text-center py-8">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="mt-2 text-gray-500">No farms registered yet</p>
            </div>
            <ul v-else class="divide-y divide-gray-100">
              <li v-for="farm in farms" :key="farm.uuid" class="py-4 hover:bg-gray-50 px-3 rounded-lg transition-colors">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="font-medium text-gray-900">{{ farm.name }}</h3>
                    <p v-if="farm.coordinates?.coordinates?.[0]?.[0]" class="text-sm text-gray-500 mt-1">
                      {{ farm.coordinates.coordinates[0][0][1]?.toFixed(4) }}, {{ farm.coordinates.coordinates[0][0][0]?.toFixed(4) }}
                    </p>
                  </div>
                  <router-link 
                    :to="{ name: 'farm', params: { id: farm.uuid } }" 
                    class="text-emerald-600 hover:text-emerald-700 text-sm font-medium flex items-center"
                  >
                    View
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </router-link>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Map Section -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full">
            <div class="bg-gradient-to-r from-emerald-50 to-green-50 px-6 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-800">Farm Locations</h2>
            </div>
            <div class="p-4 h-full">
              <div v-if="farms.length === 0" class="flex items-center justify-center h-64 text-gray-400 bg-gray-50 rounded-lg">
                <div class="text-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="mt-2">No farm locations to display</p>
                </div>
              </div>
              <div v-else id="community-map" class="w-full h-[500px] rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(true)
const community = ref<any>(null)
const farms = ref<any[]>([])
let map: any = null
let L: any = null
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

function goToCreateCommunity() {
  router.push({ name: 'create-community' })
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const options: Intl.DateTimeFormatOptions = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

async function fetchCommunityAndFarms() {
  loading.value = true
  try {
    const token = authStore.token
    if (!token) {
      loading.value = false
      return
    }
    
    // Fetch the current user's community
    const commRes = await axios.get(`${API_BASE}/users/communities/my/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    if (commRes.data) {
      community.value = commRes.data
      // Fetch farms for this community
      const farmsRes = await axios.get(`${API_BASE}/farms/?community=${community.value.uuid}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      farms.value = farmsRes.data.results || farmsRes.data || []
      
      // Initialize map after a short delay to ensure DOM is ready
      setTimeout(() => {
        initMap()
      }, 100)
    } else {
      community.value = null
      farms.value = []
    }
  } catch (error) {
    console.error('Error fetching community data:', error)
    community.value = null
    farms.value = []
  } finally {
    loading.value = false
  }
}

function initMap() {
  if (!farms.value.length) return
  if (!window.L) return
  
  // Clean up existing map if any
  if (map) {
    map.remove()
    map = null
  }

  // Use the first farm's coordinates for map center
  const firstFarm = farms.value.find(f => 
    f.coordinates?.coordinates?.[0]?.[0]
  )
  
  if (!firstFarm) return
  
  const coords = firstFarm.coordinates.coordinates[0][0]
  L = window.L
  map = L.map('community-map').setView([coords[1], coords[0]], 12)
  
  // Add tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map)

  // Add farm polygons and markers
  farms.value.forEach(farm => {
    if (farm.coordinates?.coordinates?.[0]) {
      const polyCoords = farm.coordinates.coordinates[0].map((c: any) => [c[1], c[0]])
      
      // Create polygon with nice styling
      const polygon = L.polygon(polyCoords, {
        color: '#059669',
        weight: 2,
        fillColor: '#10b981',
        fillOpacity: 0.3
      }).addTo(map)
      
      // Add marker with popup
      L.marker(polyCoords[0], {
        icon: L.divIcon({
          className: 'farm-marker',
          html: `<div class="bg-emerald-600 text-white font-semibold p-1 rounded-full border-2 border-white shadow-md">${farm.name.charAt(0)}</div>`,
          iconSize: [30, 30],
          iconAnchor: [15, 15]
        })
      })
      .addTo(map)
      .bindPopup(`<div class="font-semibold">${farm.name}</div>`)
      
      // Fit bounds to show all farms
      if (farms.value.length > 1) {
        map.fitBounds(polygon.getBounds(), { padding: [50, 50] })
      }
    }
  })
}

onMounted(async () => {
  // Load Leaflet if not already loaded
  if (!window.L) {
    await loadLeaflet()
  }
  await fetchCommunityAndFarms()
})

async function loadLeaflet() {
  if (window.L) return
  
  await Promise.all([
    loadScript('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'),
    loadStyle('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css')
  ])
}

function loadScript(src: string) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

function loadStyle(href: string) {
  return new Promise((resolve, reject) => {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = href
    link.onload = resolve
    link.onerror = reject
    document.head.appendChild(link)
  })
}

watch(farms, () => {
  if (community.value && farms.value.length) {
    setTimeout(() => {
      initMap()
    }, 100)
  }
})
</script>

<style scoped>
#community-map {
  min-height: 500px;
  width: 100%;
  border-radius: 0.5rem;
  z-index: 0;
}

/* Custom marker styling */
:deep(.farm-marker) {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loading spinner animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>