<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Bars3Icon, XMarkIcon, MapPinIcon, ScaleIcon, ChartBarIcon, ArrowsPointingOutIcon, ArrowsPointingInIcon, ArrowPathIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'
import router from '@/router'

// Map and UI state
const map = ref<L.Map | null>(null)
const mapContainer = ref<HTMLElement | null>(null)
const drawnItems = ref<L.FeatureGroup | null>(null)
const drawControl = ref<L.Control.Draw | null>(null)
const leftPanelOpen = ref(true)
const rightPanelOpen = ref(true)
const isFullScreenMap = ref(false)
const selectedField = ref<any>(null)
const isLoading = ref(false)

// Dummy data (replace with API calls)
const farms = ref([
  { id: 1, name: 'Main Field', location: 'Nairobi', size: 4.2, date: '2023-10-15' },
  { id: 2, name: 'North Plot', location: 'Kiambu', size: 2.8, date: '2023-09-22' },
  { id: 3, name: 'River Side', location: 'Machakos', size: 3.5, date: '2023-11-05' }
])
const soilData = ref({
  type: 'Loam',
  pH: 6.5,
  texture: 'Medium',
  carbon: 2.3,
  moisture: 65
})
const recommendedCrops = ref(['Maize', 'Beans', 'Wheat', 'Potatoes'])

// Initialize map
onMounted(() => {
  if (mapContainer.value) {
    map.value = L.map(mapContainer.value, {
      center: [-1.2921, 36.8219], // Nairobi coordinates
      zoom: 13,
      zoomControl: false
    })

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map.value)

    // Add satellite layer (Mapbox)
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>',
      maxZoom: 20,
      id: 'mapbox/satellite-v9',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'your_mapbox_access_token' // Replace with actual token
    }).addTo(map.value)

    // Initialize feature group for drawn items
    drawnItems.value = new L.FeatureGroup()
    map.value.addLayer(drawnItems.value)

    // Initialize draw control
    drawControl.value = new L.Control.Draw({
      position: 'topright',
      draw: {
        polygon: {
          allowIntersection: false,
          showArea: true,
          metric: true,
          shapeOptions: {
            color: '#10b981',
            fillColor: '#10b981',
            fillOpacity: 0.3
          }
        },
        rectangle: false,
        circle: false,
        circlemarker: false,
        marker: false,
        polyline: false
      },
      edit: {
        featureGroup: drawnItems.value
      }
    })
    map.value.addControl(drawControl.value)

    // Add zoom control
    L.control.zoom({ position: 'topright' }).addTo(map.value)

    // Handle draw events
    map.value.on(L.Draw.Event.CREATED, (e: any) => {
      const layer = e.layer
      drawnItems.value?.addLayer(layer)
      const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000
      layer.bindPopup(`Field Area: ${area.toFixed(2)} ha`)
      analyzeField(layer)
    })

    // Handle edit events
    map.value.on(L.Draw.Event.EDITED, (e: any) => {
      e.layers.eachLayer((layer: any) => analyzeField(layer))
    })

    // Load sample fields
    fetchSampleFields()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
    map.value = null
  }
})

// Fetch sample fields (replace with API call)
async function fetchSampleFields() {
  // Simulated API call
  const sampleFields = [
    {
      name: 'North Field',
      coords: [[-1.29, 36.82], [-1.29, 36.83], [-1.30, 36.83], [-1.30, 36.82]]
    },
    {
      name: 'East Plot',
      coords: [[-1.28, 36.82], [-1.28, 36.825], [-1.285, 36.825], [-1.285, 36.82]]
    }
  ]

  // TODO: Replace with actual API call
  // const response = await axios.get('/api/fields')
  // const sampleFields = response.data

  sampleFields.forEach(field => {
    const polygon = L.polygon(field.coords, {
      color: '#10b981',
      fillColor: '#10b981',
      fillOpacity: 0.3,
      weight: 2
    }).addTo(map.value!)

    polygon.bindPopup(`<b>${field.name}</b><br>Click to analyze`)
    polygon.on('click', () => analyzeField(polygon))
  })
}

// Analyze field (replace with API call)
async function analyzeField(layer: any) {
  isLoading.value = true
  const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000

  // Simulated API response
  const fieldData = {
    geometry: layer.getLatLngs()[0],
    area: area.toFixed(2),
    soil: {
      type: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Loam'][Math.floor(Math.random() * 4)],
      pH: (5.5 + Math.random() * 2.5).toFixed(1),
      carbon: (1 + Math.random() * 3).toFixed(1),
      texture: ['Fine', 'Medium', 'Coarse'][Math.floor(Math.random() * 3)],
      moisture: Math.floor(30 + Math.random() * 60)
    }
  }

  // TODO: Replace with actual API call
  // const response = await axios.post('/api/analyze-field', { geometry: layer.getLatLngs()[0] })
  // const fieldData = response.data

  selectedField.value = fieldData
  soilData.value = fieldData.soil
  updateRecommendedCrops(fieldData.soil.type)

  layer.setStyle({
    color: '#2563eb',
    fillColor: '#2563eb',
    fillOpacity: 0.3
  })

  layer.bindPopup(`
    <div class="space-y-2 p-2">
      <h4 class="font-bold text-base">Field Analysis</h4>
      <p class="text-sm">Area: ${area.toFixed(2)} ha</p>
      <p class="text-sm">Soil: ${fieldData.soil.type}</p>
      <p class="text-sm">pH: ${fieldData.soil.pH}</p>
      <button onclick="this.dispatchEvent(new CustomEvent('view-details', { bubbles: true }))" 
        class="mt-2 px-3 py-1 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600"
        @click="viewField(selectedField.value.geometry)">
        View Details
      </button>
    </div>
  `).openPopup()

  isLoading.value = false
}

function viewField(geometry: any) {
  // Navigate to farm details page (replace with actual navigation logic)
  console.log('Viewing farm with geometry:', geometry)
  router.push(`/fields/${geometry.id}`)
}

// Update recommended crops based on soil type
function updateRecommendedCrops(soilType: string) {
  const cropMap: Record<string, string[]> = {
    'Sandy Loam': ['Maize', 'Beans', 'Watermelon', 'Groundnuts'],
    'Clay Loam': ['Rice', 'Wheat', 'Barley', 'Cabbage'],
    'Silty Clay': ['Potatoes', 'Carrots', 'Onions', 'Garlic'],
    'Loam': ['Maize', 'Beans', 'Tomatoes', 'Kale']
  }
  recommendedCrops.value = cropMap[soilType] || ['Maize', 'Beans', 'Wheat', 'Potatoes']
}

// Trigger boundary detection (replace with API call)
async function triggerBoundaryDetection() {
  isLoading.value = true
  const toast = document.createElement('div')
  toast.className = 'fixed top-4 right-4 bg-emerald-600 text-white px-4 py-2 rounded-md shadow-lg z-[1000]'
  toast.textContent = 'Detecting field boundaries...'
  document.body.appendChild(toast)

  // Simulated API response
  const newFieldCoords = [
    [-1.291, 36.818],
    [-1.291, 36.821],
    [-1.293, 36.821],
    [-1.293, 36.818]
  ]

  // TODO: Replace with actual API call
  // const response = await axios.post('/api/detect-boundaries', { center: map.value?.getCenter() })
  // const newFieldCoords = response.data.coords

  setTimeout(() => {
    const newField = L.polygon(newFieldCoords, {
      color: '#10b981',
      fillColor: '#10b981',
      fillOpacity: 0.3,
      weight: 2
    }).addTo(map.value!)

    newField.bindPopup('Detected Field<br>Click to analyze')
    newField.on('click', () => analyzeField(newField))

    toast.textContent = 'Field boundaries detected!'
    setTimeout(() => toast.remove(), 3000)
    isLoading.value = false
  }, 2000)
}

// Toggle full-screen map
function toggleFullScreenMap() {
  isFullScreenMap.value = !isFullScreenMap.value
  if (isFullScreenMap.value) {
    leftPanelOpen.value = false
    rightPanelOpen.value = false
  }
  // Trigger map resize
  setTimeout(() => map.value?.invalidateSize(), 300)
}
</script>

<template>
  <div class="flex flex-col h-screen overflow-hidden">
    <div class="block p-8">

    </div>
    <!-- Main Content -->
    <div class="flex flex-col flex-1 overflow-hidden">
      <!-- Map and Sidebars -->
      <div class="relative flex flex-col md:flex-row flex-1 overflow-hidden">
        <!-- Left Sidebar (Your Farms) -->
        <div 
          class="md:w-80 w-full bg-white border-r border-gray-200 shadow-sm transition-all duration-300 z-20"
          :class="{
            'translate-x-0': leftPanelOpen && !isFullScreenMap,
            '-translate-x-full absolute md:relative': !leftPanelOpen || isFullScreenMap,
            'hidden md:block': isFullScreenMap
          }"
        >
          <div class="p-4 h-full flex flex-col overflow-y-auto">
            <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <MapPinIcon class="h-5 w-5 mr-2 text-emerald-600" />
              Your Farms
            </h2>
            <div class="space-y-3 mb-4">
              <div 
                v-for="farm in farms" 
                :key="farm.id"
                class="p-3 border border-gray-200 rounded-lg hover:border-emerald-300 hover:bg-emerald-50 cursor-pointer transition-colors"
                @click="selectedField = { name: farm.name, area: farm.size }"
              >
                <h3 class="font-semibold text-gray-800">{{ farm.name }}</h3>
                <p class="text-sm text-gray-600">{{ farm.location }} • {{ farm.size }} ha</p>
                <p class="text-xs text-gray-500 mt-1">Added: {{ farm.date }}</p>
              </div>
            </div>
            <button 
              class="mt-auto w-full flex items-center justify-center px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
              :disabled="isLoading"
              @click="triggerBoundaryDetection"
            >
              <ArrowPathIcon class="h-5 w-5 mr-2" />
              Delimit Boundaries
            </button>
          </div>
        </div>

        <!-- Map Area -->
        <div class="flex-1 relative">
          <div 
            ref="mapContainer" 
            class="h-full w-full z-0"
          ></div>

          <!-- Map Controls -->
          <div class="absolute top-4 left-4 space-y-2 z-30 md:top-4 md:left-4 left-2 top-2">
            <button 
              class="p-2 bg-white rounded-md shadow-md hover:bg-gray-50 transition-colors"
              @click="leftPanelOpen = !leftPanelOpen"
              :title="leftPanelOpen ? 'Hide Farms panel' : 'Show Farms panel'"
              :disabled="isFullScreenMap"
            >
              <Bars3Icon v-if="!leftPanelOpen" class="h-5 w-5 text-gray-700" />
              <XMarkIcon v-else class="h-5 w-5 text-gray-700" />
            </button>
            <button 
              class="p-2 bg-white rounded-md shadow-md hover:bg-gray-50 transition-colors"
              @click="rightPanelOpen = !rightPanelOpen"
              :title="rightPanelOpen ? 'Hide Analysis panel' : 'Show Analysis panel'"
              :disabled="isFullScreenMap"
            >
              <ChartBarIcon class="h-5 w-5 text-gray-700" />
            </button>
            <button 
              class="p-2 bg-white rounded-md shadow-md hover:bg-gray-50 transition-colors"
              @click="toggleFullScreenMap"
              :title="isFullScreenMap ? 'Exit full screen' : 'Full screen map'"
            >
              <ArrowsPointingOutIcon v-if="!isFullScreenMap" class="h-5 w-5 text-gray-700" />
              <ArrowsPointingInIcon v-else class="h-5 w-5 text-gray-700" />
            </button>
          </div>
        </div>

        <!-- Right Sidebar (Field Analysis) -->
        <div 
          class="md:w-80 w-full bg-white border-l border-gray-200 shadow-sm transition-all duration-300 z-20"
          :class="{
            'translate-x-0': rightPanelOpen && !isFullScreenMap,
            'translate-x-full absolute right-0 md:relative': !rightPanelOpen || isFullScreenMap,
            'hidden md:block': isFullScreenMap
          }"
        >
          <div class="p-4 h-full flex flex-col overflow-y-auto">
            <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <ScaleIcon class="h-5 w-5 mr-2 text-emerald-600" />
              Field Analysis
            </h2>
            <div v-if="selectedField" class="space-y-4">
              <div class="bg-gray-50 p-3 rounded-lg">
                <h3 class="font-semibold text-gray-800">{{ selectedField.name || 'Selected Field' }}</h3>
                <p class="text-sm text-gray-600">{{ selectedField.area }} hectares</p>
              </div>
              <div>
                <h3 class="font-semibold text-gray-700 mb-2 flex items-center">
                  <MapPinIcon class="h-4 w-4 mr-1 text-emerald-600" />
                  Recommended Crops
                </h3>
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
              <div>
                <h3 class="font-semibold text-gray-700 mb-2">Soil Information</h3>
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span>Type</span>
                      <span class="font-medium">{{ soilData.type }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        class="bg-emerald-600 h-2.5 rounded-full" 
                        :style="{ width: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Loam'].indexOf(soilData.type) * 33 + 33 + '%' }"
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span>pH Level</span>
                      <span class="font-medium">{{ soilData.pH }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        class="bg-emerald-600 h-2.5 rounded-full" 
                        :style="{ width: ((parseFloat(soilData.pH) - 4) / 6) * 100 + '%' }"
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span>Carbon %</span>
                      <span class="font-medium">{{ soilData.carbon }}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        class="bg-emerald-600 h-2.5 rounded-full" 
                        :style="{ width: (parseFloat(soilData.carbon) / 4 * 100) + '%' }"
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span>Moisture</span>
                      <span class="font-medium">{{ soilData.moisture }}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        class="bg-emerald-600 h-2.5 rounded-full" 
                        :style="{ width: soilData.moisture + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="flex flex-col items-center justify-center h-full text-gray-500">
              <MapPinIcon class="h-10 w-10 mb-2 text-gray-300" />
              <p>Select a field on the map to view analysis</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 0;
}

.leaflet-container.fullscreen {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 50 !important;
  border-radius: 0 !important;
}

.fullscreen-map {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 50 !important;
  background: #fff;
}

body.fullscreen-active {
  overflow: hidden;
}

.leaflet-draw-toolbar a {
  background-image: none !important;
  background-color: #10b981 !important;
  color: white !important;
  border-radius: 4px !important;
  margin: 2px !important;
}

.leaflet-popup-content {
  margin: 12px !important;
}

.leaflet-popup-content-wrapper {
  border-radius: 8px !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .md\\:w-80 {
    width: 100%;
    max-height: 50vh;
  }
}
</style>