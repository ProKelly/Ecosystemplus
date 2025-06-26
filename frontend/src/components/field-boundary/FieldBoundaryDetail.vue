<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'
import { ArrowPathIcon, PencilSquareIcon, MapPinIcon } from '@heroicons/vue/24/outline'

// Route for field ID
const route = useRoute()
const fieldId = route.params.id

// Map and field state
const map = ref<L.Map | null>(null)
const mapContainer = ref<HTMLElement | null>(null)
const drawnItems = ref<L.FeatureGroup | null>(null)
const isLoading = ref(false)
const fieldData = ref({
  name: 'Selected Field',
  area: 0,
  geometry: [],
  soil: { type: 'Loam', pH: 6.5, texture: 'Medium', carbon: 2.3, moisture: 65 }
})
const recommendedCrops = ref(['Maize', 'Beans', 'Wheat', 'Potatoes'])

// Initialize map
onMounted(() => {
  if (mapContainer.value) {
    map.value = L.map(mapContainer.value, {
      center: [-1.2921, 36.8219], // Nairobi coordinates
      zoom: 15,
      zoomControl: false
    })

    // Add satellite layer (Mapbox)
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>',
      maxZoom: 20,
      id: 'mapbox/satellite-v9',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'your_mapbox_access_token' // Replace with actual token
    }).addTo(map.value)

    // Initialize feature group
    drawnItems.value = new L.FeatureGroup()
    map.value.addLayer(drawnItems.value)

    // Add zoom control with better styling
    L.control.zoom({
      position: 'topright',
      zoomInText: '<span class="text-lg font-bold">+</span>',
      zoomOutText: '<span class="text-lg font-bold">−</span>'
    }).addTo(map.value)

    // Fetch field data
    fetchFieldData()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
    map.value = null
  }
})

// Fetch field data (replace with API call)
async function fetchFieldData() {
  isLoading.value = true
  try {
    // Simulated API response
    const sampleField = {
      name: 'North Field',
      area: 3.7,
      geometry: [[-1.29, 36.82], [-1.29, 36.83], [-1.30, 36.83], [-1.30, 36.82]],
      soil: {
        type: 'Sandy Clay Loam',
        pH: 6.8,
        texture: 'Fine',
        carbon: 2.5,
        moisture: 70
      }
    }

    // TODO: Replace with actual API call
    // const response = await axios.get(`/api/fields/${fieldId}`)
    // const sampleField = response.data

    fieldData.value = sampleField
    updateRecommendedCrops(sampleField.soil.type)

    // Add field polygon to map with better styling
    const polygon = L.polygon(sampleField.geometry, {
      color: '#059669',
      fillColor: '#10b981',
      fillOpacity: 0.3,
      weight: 3,
      dashArray: '5, 5',
      className: 'animate-pulse'
    }).addTo(map.value!)

    // Add area measurement tooltip
    polygon.bindTooltip(`Area: ${sampleField.area} ha`, {
      permanent: true,
      direction: 'center',
      className: 'font-bold text-emerald-800 bg-white/90 px-2 py-1 rounded border border-emerald-200'
    })

    drawnItems.value?.addLayer(polygon)
    map.value?.fitBounds(polygon.getBounds(), { padding: [20, 20] })
  } catch (error) {
    console.error('Error fetching field data:', error)
    showToast('Failed to load field data', 'error')
  } finally {
    isLoading.value = false
  }
}

// Re-analyze field
async function reanalyzeField() {
  isLoading.value = true
  showToast('Re-analyzing field...', 'info')

  try {
    // Simulated API response
    const updatedSoil = {
      type: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Sandy Clay Loam'][Math.floor(Math.random() * 4)],
      pH: (5.5 + Math.random() * 2.5).toFixed(1),
      texture: ['Fine', 'Medium', 'Coarse'][Math.floor(Math.random() * 3)],
      carbon: (1 + Math.random() * 3).toFixed(1),
      moisture: Math.floor(30 + Math.random() * 60)
    }

    // TODO: Replace with actual API call
    // const response = await axios.post(`/api/analyze-field/${fieldId}`, { geometry: fieldData.value.geometry })
    // const updatedSoil = response.data.soil

    fieldData.value.soil = updatedSoil
    updateRecommendedCrops(updatedSoil.type)
    showToast('Field re-analyzed successfully!', 'success')
  } catch (error) {
    console.error('Error re-analyzing field:', error)
    showToast('Failed to re-analyze field', 'error')
  } finally {
    isLoading.value = false
  }
}

// Adjust boundary (placeholder for draw tool integration)
function adjustBoundary() {
  showToast('Boundary adjustment coming soon!', 'info')
  // TODO: Implement Leaflet Draw for boundary editing, similar to MapDashboard.vue
}

// Update recommended crops
function updateRecommendedCrops(soilType: string) {
  const cropMap: Record<string, string[]> = {
    'Sandy Loam': ['Maize', 'Beans', 'Watermelon', 'Groundnuts'],
    'Clay Loam': ['Rice', 'Wheat', 'Barley', 'Cabbage'],
    'Silty Clay': ['Potatoes', 'Carrots', 'Onions', 'Garlic'],
    'Sandy Clay Loam': ['Maize', 'Sorghum', 'Sunflower', 'Peas']
  }
  recommendedCrops.value = cropMap[soilType] || ['Maize', 'Beans', 'Wheat', 'Potatoes']
}

// Show toast notification
function showToast(message: string, type: 'success' | 'error' | 'info' = 'info') {
  const toast = document.createElement('div')
  const colors = {
    success: 'bg-emerald-600',
    error: 'bg-red-600',
    info: 'bg-blue-600'
  }
  toast.className = `fixed top-4 right-4 ${colors[type]} text-white px-4 py-2 rounded-md shadow-lg z-[1000] animate-fade-in`
  toast.textContent = message
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.classList.add('animate-fade-out')
    setTimeout(() => toast.remove(), 300)
  }, 3000)
}
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800 flex items-center">
          <MapPinIcon class="h-6 w-6 mr-2 text-emerald-600" />
          Field Details
        </h1>
        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-emerald-100 text-emerald-800">
          Field ID: {{ fieldId }}
        </span>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col md:flex-row overflow-hidden">
      <!-- Map Section -->
      <section class="md:w-2/3 w-full h-96 md:h-full relative">
        <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-gray-100/80 z-10">
          <div class="flex flex-col items-center">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 mb-2"></div>
            <p class="text-gray-600">Loading field data...</p>
          </div>
        </div>
        <div ref="mapContainer" class="h-full w-full z-0"></div>
      </section>

      <!-- Field Details Section -->
      <section class="md:w-1/3 w-full p-4 md:p-6 bg-white border-l border-gray-200 overflow-y-auto">
        <div v-if="fieldData" class="space-y-6">
          <!-- Field Header -->
          <div class="border-b border-gray-200 pb-4">
            <h2 class="text-xl font-semibold text-gray-800">{{ fieldData.name }}</h2>
            <div class="flex items-center justify-between mt-1">
              <p class="text-sm text-gray-600">
                <span class="font-medium">{{ fieldData.area }}</span> hectares
              </p>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Active Field
              </span>
            </div>
          </div>

          <!-- Soil Information -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
              <span class="w-3 h-3 bg-emerald-500 rounded-full mr-2"></span>
              Soil Information
            </h3>
            <div class="space-y-4">
              <div v-for="(item, key) in [
                { name: 'Type', value: fieldData.soil.type, levels: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Sandy Clay Loam'] },
                { name: 'pH Level', value: fieldData.soil.pH, min: 4, max: 10 },
                { name: 'Carbon %', value: fieldData.soil.carbon, min: 0, max: 4 },
                { name: 'Texture', value: fieldData.soil.texture, levels: ['Fine', 'Medium', 'Coarse'] },
                { name: 'Moisture', value: fieldData.soil.moisture, min: 0, max: 100 }
              ]" :key="item.name">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">{{ item.name }}</span>
                  <span class="font-medium text-gray-800">{{ item.value }}{{ item.name === 'Carbon %' ? '%' : '' }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full" 
                    :class="{
                      'bg-red-500': (item.name === 'pH Level' && parseFloat(item.value) < 5.5) || 
                                    (item.name === 'Carbon %' && parseFloat(item.value) < 1),
                      'bg-yellow-500': (item.name === 'pH Level' && parseFloat(item.value) >= 5.5 && parseFloat(item.value) < 6.5) || 
                                      (item.name === 'Carbon %' && parseFloat(item.value) >= 1 && parseFloat(item.value) < 2),
                      'bg-emerald-500': (item.name === 'pH Level' && parseFloat(item.value) >= 6.5) || 
                                        (item.name === 'Carbon %' && parseFloat(item.value) >= 2)
                    }"
                    :style="{
                      width: item.levels 
                        ? (((item.levels.indexOf(item.value) + 1) / item.levels.length) * 100 + '%')
                        : ((parseFloat(item.value) - item.min) / (item.max - item.min) * 100 + '%')
                    }"
                  ></div>
                </div>
                <div v-if="item.name === 'pH Level'" class="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Acidic</span>
                  <span>Neutral</span>
                  <span>Alkaline</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recommended Crops -->
          <div>
            <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
              <span class="w-3 h-3 bg-amber-500 rounded-full mr-2"></span>
              Recommended Crops
            </h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(crop, index) in recommendedCrops" 
                :key="index"
                class="px-3 py-1 bg-amber-100 text-amber-800 text-sm rounded-full flex items-center"
              >
                <span class="w-2 h-2 bg-amber-500 rounded-full mr-2"></span>
                {{ crop }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-2">
            <button 
              class="flex-1 flex items-center justify-center px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              @click="reanalyzeField"
              :disabled="isLoading"
            >
              <ArrowPathIcon class="h-5 w-5 mr-2" :class="{ 'animate-spin': isLoading }" />
              Re-analyze
            </button>
            <button 
              class="flex-1 flex items-center justify-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              @click="adjustBoundary"
              :disabled="isLoading"
            >
              <PencilSquareIcon class="h-5 w-5 mr-2" />
              Adjust Boundary
            </button>
          </div>
        </div>
        
        <!-- Loading State -->
        <div v-else class="flex flex-col items-center justify-center h-full text-gray-500">
          <div class="animate-pulse flex flex-col items-center">
            <MapPinIcon class="h-12 w-12 mb-4 text-gray-300" />
            <p class="text-gray-400">Loading field data...</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 0;
}

/* Custom animations */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-out {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(10px); }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}

.animate-fade-out {
  animation: fade-out 0.3s ease-out forwards;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .md\:w-2\/3 {
    height: 50vh;
  }
  .md\:w-1\/3 {
    height: auto;
    max-height: 50vh;
  }
}
</style>