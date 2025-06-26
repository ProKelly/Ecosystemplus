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
const activePolygon = ref<L.Polygon | null>(null)

// Farm and field data
const farms = ref([
  { 
    id: 1, 
    name: 'Main Field', 
    location: 'Nairobi', 
    size: 4.2, 
    date: '2023-10-15',
    geometry: [[-1.29, 36.82], [-1.29, 36.83], [-1.30, 36.83], [-1.30, 36.82]]
  },
  { 
    id: 2, 
    name: 'North Plot', 
    location: 'Kiambu', 
    size: 2.8, 
    date: '2023-09-22',
    geometry: [[-1.28, 36.82], [-1.28, 36.825], [-1.285, 36.825], [-1.285, 36.82]]
  },
  { 
    id: 3, 
    name: 'River Side', 
    location: 'Machakos', 
    size: 3.5, 
    date: '2023-11-05',
    geometry: [[-1.31, 36.81], [-1.31, 36.815], [-1.315, 36.815], [-1.315, 36.81]]
  }
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

    // Add base layers
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    })

    const satelliteLayer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>',
      maxZoom: 20,
      id: 'mapbox/satellite-v9',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'your_mapbox_access_token'
    })

    // Add default layer
    satelliteLayer.addTo(map.value)

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

    // Add layer control
    const baseLayers = {
      'Satellite': satelliteLayer,
      'Street Map': osmLayer
    }
    L.control.layers(baseLayers, null, { position: 'topright' }).addTo(map.value)

    // Add zoom control with better styling
    L.control.zoom({
      position: 'topright',
      zoomInText: '<span class="text-lg font-bold">+</span>',
      zoomOutText: '<span class="text-lg font-bold">−</span>'
    }).addTo(map.value)

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
    loadFieldsOnMap()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
    map.value = null
  }
})

// Load fields onto the map
function loadFieldsOnMap() {
  // Clear existing fields
  drawnItems.value?.clearLayers()
  
  farms.value.forEach(farm => {
    const polygon = L.polygon(farm.geometry, {
      color: '#10b981',
      fillColor: '#10b981',
      fillOpacity: 0.3,
      weight: 2
    }).addTo(map.value!)

    polygon.bindPopup(`
      <div class="space-y-1">
        <h4 class="font-bold text-base">${farm.name}</h4>
        <p class="text-sm">${farm.location}</p>
        <p class="text-sm">${farm.size} ha</p>
        <button 
          onclick="this.dispatchEvent(new CustomEvent('view-farm', { bubbles: true }))" 
          class="mt-1 w-full px-2 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
        >
          View Details
        </button>
      </div>
    `)

    // Add click handler directly to the DOM element
    polygon.on('popupopen', () => {
      const btn = document.querySelector('.leaflet-popup-content button')
      if (btn) {
        btn.addEventListener('view-farm', () => {
          selectFarm(farm)
        })
      }
    })

    polygon.on('click', () => {
      selectFarm(farm)
    })

    drawnItems.value?.addLayer(polygon)
  })
}

// Select a farm and display it prominently
function selectFarm(farm: any) {
  // Remove previous active polygon if exists
  if (activePolygon.value) {
    drawnItems.value?.removeLayer(activePolygon.value)
  }

  // Create highlighted polygon
  activePolygon.value = L.polygon(farm.geometry, {
    color: '#2563eb',
    fillColor: '#2563eb',
    fillOpacity: 0.3,
    weight: 3
  }).addTo(map.value!)

  // Zoom to the selected farm
  map.value?.fitBounds(activePolygon.value.getBounds(), { padding: [50, 50] })

  // Update selected field data
  selectedField.value = {
    id: farm.id,
    name: farm.name,
    area: farm.size,
    geometry: farm.geometry
  }

  // Analyze the field (simulated)
  analyzeField(activePolygon.value)
  
  // Open right panel if closed
  rightPanelOpen.value = true
}

// Analyze field (replace with API call)
async function analyzeField(layer: any) {
  isLoading.value = true
  
  // Calculate area
  const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000

  // Simulated API response
  const fieldData = {
    id: selectedField.value?.id || Math.floor(Math.random() * 100000),
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

  // Update state
  selectedField.value = fieldData
  soilData.value = fieldData.soil
  updateRecommendedCrops(fieldData.soil.type)

  // Update popup
  layer.bindPopup(`
    <div class='space-y-2 p-2'>
      <h4 class='font-bold text-base'>${selectedField.value?.name || 'Field Analysis'}</h4>
      <p class='text-sm'>Area: ${area.toFixed(2)} ha</p>
      <p class='text-sm'>Soil: ${fieldData.soil.type}</p>
      <p class='text-sm'>pH: ${fieldData.soil.pH}</p>
      <button 
        onclick="this.dispatchEvent(new CustomEvent('view-details', { bubbles: true }))" 
        class='mt-2 w-full px-3 py-1 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600'
      >
        View Details
      </button>
    </div>
  `).openPopup()

  // Add event listener for the View Details button in the popup
  setTimeout(() => {
    const btn = document.querySelector('.leaflet-popup-content button')
    if (btn) {
      btn.addEventListener('view-details', () => {
        router.push(`/fields/${fieldData.id}`)
      })
    }
  }, 100)

  isLoading.value = false
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
  showToast('Detecting field boundaries...', 'info')

  try {
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

    const newField = L.polygon(newFieldCoords, {
      color: '#10b981',
      fillColor: '#10b981',
      fillOpacity: 0.3,
      weight: 2
    }).addTo(map.value!)

    newField.bindPopup('Detected Field<br>Click to analyze')
    newField.on('click', () => analyzeField(newField))
    drawnItems.value?.addLayer(newField)

    // Add to farms list
    const newFarm = {
      id: Math.max(...farms.value.map(f => f.id)) + 1,
      name: `New Field ${new Date().getFullYear()}`,
      location: 'Nairobi',
      size: (L.GeometryUtil.geodesicArea(newFieldCoords) / 10000).toFixed(2),
      date: new Date().toISOString().split('T')[0],
      geometry: newFieldCoords
    }
    farms.value.push(newFarm)

    // Select the new field
    selectFarm(newFarm)
    showToast('Field boundaries detected!', 'success')
  } catch (error) {
    console.error('Error detecting boundaries:', error)
    showToast('Failed to detect boundaries', 'error')
  } finally {
    isLoading.value = false
  }
}

// Toggle full-screen map
function toggleFullScreenMap() {
  isFullScreenMap.value = !isFullScreenMap.value
  if (isFullScreenMap.value) {
    leftPanelOpen.value = false
    rightPanelOpen.value = false
  }
  setTimeout(() => map.value?.invalidateSize(), 300)
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
  <div class="flex flex-col h-screen overflow-hidden bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <h1 class="text-2xl font-bold text-gray-800">Farm Management Dashboard</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col md:flex-row overflow-hidden">
      <!-- Left Sidebar (Your Farms) -->
      <aside 
        class="md:w-80 w-full bg-white border-r border-gray-200 shadow-sm transition-all duration-300 z-20 flex flex-col"
        :class="{
          'translate-x-0': leftPanelOpen && !isFullScreenMap,
          '-translate-x-full absolute md:relative': !leftPanelOpen || isFullScreenMap,
          'hidden md:flex': isFullScreenMap
        }"
      >
        <div class="p-4 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-800 flex items-center">
            <MapPinIcon class="h-5 w-5 mr-2 text-emerald-600" />
            Your Farms
          </h2>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div 
            v-for="farm in farms" 
            :key="farm.id"
            class="p-3 border border-gray-200 rounded-lg hover:border-emerald-300 hover:bg-emerald-50 cursor-pointer transition-colors"
            :class="{ 'border-emerald-400 bg-emerald-50': selectedField?.id === farm.id }"
            @click="selectFarm(farm)"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-semibold text-gray-800">{{ farm.name }}</h3>
                <p class="text-sm text-gray-600">{{ farm.location }}</p>
              </div>
              <span class="text-xs font-medium px-2 py-1 bg-gray-100 text-gray-800 rounded-full">
                {{ farm.size }} ha
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-1">Added: {{ farm.date }}</p>
          </div>
        </div>

        <div class="p-4 border-t border-gray-200">
          <button 
            class="w-full flex items-center justify-center px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            :disabled="isLoading"
            @click="triggerBoundaryDetection"
          >
            <ArrowPathIcon class="h-5 w-5 mr-2" :class="{ 'animate-spin': isLoading }" />
            Delimit New Field
          </button>
        </div>
      </aside>

      <!-- Map Area -->
      <section class="flex-1 relative">
        <div 
          ref="mapContainer" 
          class="h-full w-full z-0"
        ></div>

        <!-- Map Controls -->
        <div class="absolute top-4 left-4 space-y-2 z-30">
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
      </section>

      <!-- Right Sidebar (Field Analysis) -->
      <aside 
        class="md:w-80 w-full bg-white border-l border-gray-200 shadow-sm transition-all duration-300 z-20 flex flex-col"
        :class="{
          'translate-x-0': rightPanelOpen && !isFullScreenMap,
          'translate-x-full absolute right-0 md:relative': !rightPanelOpen || isFullScreenMap,
          'hidden md:flex': isFullScreenMap
        }"
      >
        <div class="p-4 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-800 flex items-center">
            <ScaleIcon class="h-5 w-5 mr-2 text-emerald-600" />
            Field Analysis
          </h2>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4">
          <div v-if="selectedField" class="space-y-6">
            <!-- Field Summary -->
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <h3 class="font-semibold text-gray-800">{{ selectedField.name || 'Selected Field' }}</h3>
              <div class="flex justify-between items-center mt-2">
                <span class="text-sm text-gray-600">{{ selectedField.area }} hectares</span>
                <button 
                  class="text-sm text-blue-600 hover:text-blue-800 font-medium"
                  @click="map?.fitBounds(activePolygon?.getBounds())"
                >
                  Zoom to Field
                </button>
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

            <!-- Soil Information -->
            <div>
              <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                <span class="w-3 h-3 bg-emerald-500 rounded-full mr-2"></span>
                Soil Information
              </h3>
              <div class="space-y-4">
                <div v-for="(item, key) in [
                  { name: 'Type', value: soilData.type, levels: ['Sandy Loam', 'Clay Loam', 'Silty Clay', 'Loam'] },
                  { name: 'pH Level', value: soilData.pH, min: 4, max: 10 },
                  { name: 'Carbon %', value: soilData.carbon, min: 0, max: 4 },
                  { name: 'Texture', value: soilData.texture, levels: ['Fine', 'Medium', 'Coarse'] },
                  { name: 'Moisture', value: soilData.moisture, min: 0, max: 100 }
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

            <!-- View Details Button -->
            <button
              v-if="selectedField.id"
              class="w-full mt-4 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
              @click="router.push(`/fields/${selectedField.id}`)"
            >
              View Full Details
            </button>
          </div>
          
          <!-- Empty State -->
          <div v-else class="flex flex-col items-center justify-center h-full text-gray-500">
            <MapPinIcon class="h-10 w-10 mb-4 text-gray-300" />
            <p class="text-center">Select a field from the map or farms list to view analysis</p>
          </div>
        </div>
      </aside>
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

/* Leaflet Draw customization */
.leaflet-draw-toolbar a {
  background-image: none !important;
  background-color: #10b981 !important;
  color: white !important;
  border-radius: 4px !important;
  margin: 2px !important;
}

.leaflet-draw-toolbar a:hover {
  background-color: #059669 !important;
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
  .md\:w-80 {
    width: 100%;
    max-height: 50vh;
  }
}
</style>