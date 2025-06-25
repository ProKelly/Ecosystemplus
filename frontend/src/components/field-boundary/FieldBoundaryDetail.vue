<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'
import { ArrowPathIcon, PencilSquareIcon } from '@heroicons/vue/24/outline'

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

    // Add zoom control
    L.control.zoom({ position: 'topright' }).addTo(map.value)

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

  // Add field polygon to map
  const polygon = L.polygon(sampleField.geometry, {
    color: '#2563eb',
    fillColor: '#2563eb',
    fillOpacity: 0.3,
    weight: 2
  }).addTo(map.value!)

  drawnItems.value?.addLayer(polygon)
  map.value?.fitBounds(polygon.getBounds())
  isLoading.value = false
}

// Re-analyze field
async function reanalyzeField() {
  isLoading.value = true
  const toast = document.createElement('div')
  toast.className = 'fixed top-4 right-4 bg-emerald-600 text-white px-4 py-2 rounded-md shadow-lg z-[1000]'
  toast.textContent = 'Re-analyzing field...'
  document.body.appendChild(toast)

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

  toast.textContent = 'Field re-analyzed!'
  setTimeout(() => toast.remove(), 3000)
  isLoading.value = false
}

// Adjust boundary (placeholder for draw tool integration)
function adjustBoundary() {
  // TODO: Implement Leaflet Draw for boundary editing, similar to MapDashboard.vue
  alert('Boundary adjustment feature to be implemented')
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
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <!-- Header -->
    <h1 class="text-2xl font-bold text-gray-800 p-4 md:p-6 flex items-center">
      <MapPinIcon class="h-6 w-6 mr-2 text-emerald-600" />
      Field Details
    </h1>

    <!-- Main Content -->
    <div class="flex flex-col md:flex-row flex-1 overflow-hidden">
      <!-- Map -->
      <div class="md:w-2/3 w-full h-96 md:h-full relative">
        <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75 z-10">
          <p class="text-gray-500">Loading field data...</p>
        </div>
        <div ref="mapContainer" class="h-full w-full z-0"></div>
      </div>

      <!-- Field Details -->
      <div class="md:w-1/3 w-full p-4 md:p-6 bg-white border-l border-gray-200 overflow-y-auto">
        <div v-if="fieldData" class="space-y-6">
          <div>
            <h2 class="text-xl font-semibold text-gray-800">{{ fieldData.name }}</h2>
            <p class="text-sm text-gray-600">Area: {{ fieldData.area }} hectares</p>
          </div>

          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Soil Information</h3>
            <div class="space-y-3">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>Type</span>
                  <span class="font-medium">{{ fieldData.soil.type }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    class="bg-emerald-600 h-2.5 rounded-full" 
                    :style="{ width: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Sandy Clay Loam'].indexOf(fieldData.soil.type) * 33 + 33 + '%' }"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>pH Level</span>
                  <span class="font-medium">{{ fieldData.soil.pH }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    class="bg-emerald-600 h-2.5 rounded-full" 
                    :style="{ width: ((parseFloat(fieldData.soil.pH) - 4) / 6) * 100 + '%' }"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>Carbon %</span>
                  <span class="font-medium">{{ fieldData.soil.carbon }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    class="bg-emerald-600 h-2.5 rounded-full" 
                    :style="{ width: (parseFloat(fieldData.soil.carbon) / 4 * 100) + '%' }"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>Texture</span>
                  <span class="font-medium">{{ fieldData.soil.texture }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    class="bg-emerald-600 h-2.5 rounded-full" 
                    :style="{ width: ['Fine', 'Medium', 'Coarse'].indexOf(fieldData.soil.texture) * 33 + 33 + '%' }"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span>Moisture</span>
                  <span class="font-medium">{{ fieldData.soil.moisture }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    class="bg-emerald-600 h-2.5 rounded-full" 
                    :style="{ width: fieldData.soil.moisture + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 class="font-semibold text-gray-700 mb-2">Recommended Crops</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(crop, index) in recommendedCrops" 
                :key="index"
                class="px-2 py-1 bg-emerald-100 text-emerald-800 text-xs rounded-full"
              >
                {{ crop }}
              </span>
            </div>
          </div>

          <div class="flex gap-2">
            <button 
              class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
              @click="reanalyzeField"
              :disabled="isLoading"
            >
              <ArrowPathIcon class="h-5 w-5 inline mr-2" />
              Re-analyze
            </button>
            <button 
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              @click="adjustBoundary"
              :disabled="isLoading"
            >
              <PencilSquareIcon class="h-5 w-5 inline mr-2" />
              Adjust Boundary
            </button>
          </div>
        </div>
        <div v-else class="flex flex-col items-center justify-center h-full text-gray-500">
          <MapPinIcon class="h-10 w-10 mb-2 text-gray-300" />
          <p>Loading field data...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .md\:w-2\/3 {
    height: 50vh;
  }
  .md\:w-1\/3 {
    height: auto;
  }
}
</style>