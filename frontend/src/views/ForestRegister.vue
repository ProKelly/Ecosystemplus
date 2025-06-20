<template>
  <div class="min-h-screen bg-gray-50 pt-20">
    <main class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8 py-4">
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="space-y-6 p-4 sm:p-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Forest Name</label>
            <input 
              v-model="newForest.name" 
              type="text" 
              class="w-full p-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200"
              placeholder="e.g. North Conservation Area"
            >
          </div>
          
          <div class="space-y-2">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 sm:gap-0">
              <label class="block text-sm font-medium text-gray-700">Forest Boundary</label>
              <div class="flex space-x-2 mt-2 sm:mt-0">
                <div class="relative">
                  <button
                    class="px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50 flex items-center"
                    @click="handleLayerDropdown"
                    type="button"
                  >
                    <span>{{ currentLayer.toUpperCase() }}</span>
                    <svg class="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div
                    v-if="showLayerDropdown"
                    id="layer-dropdown"
                    class="absolute z-10 mt-1 w-32 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
                    @mousedown.stop
                  >
                    <div class="py-1">
                      <button @mousedown.stop @click="changeBaseLayer('satellite')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Satellite</button>
                      <button @mousedown.stop @click="changeBaseLayer('ndvi')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">NDVI</button>
                      <button @mousedown.stop @click="changeBaseLayer('terrain')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Terrain</button>
                    </div>
                  </div>
                </div>
                <button 
                  @click="toggleFullScreen"
                  class="px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50 flex items-center"
                  :title="isFullScreen ? 'Exit fullscreen' : 'View fullscreen'"
                >
                  <svg v-if="!isFullScreen" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                  <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            <div 
              id="registration-map-container" 
              class="h-64 sm:h-96 w-full rounded-md border border-gray-300 relative"
              :class="{'fixed inset-0 z-50 h-screen w-screen m-0 border-none': isFullScreen}"
            >
              <div id="registration-map" class="w-full h-full"></div>
              <button
                v-if="isFullScreen"
                @click="toggleFullScreen"
                class="fixed top-4 right-4 z-[10000] bg-white border border-gray-300 rounded-full p-2 shadow-lg hover:bg-gray-100 focus:outline-none"
                aria-label="Exit Fullscreen"
              >
                <svg class="h-6 w-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 4v6M20 4h-6M4 20v-6M4 20h6" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3 pt-4 border-t border-gray-200">
            <router-link 
              to="/forest-monitoring"
              class="px-4 py-2.5 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors duration-200 text-center"
            >
              Cancel
            </router-link>
            <button 
              @click="registerForest"
              :disabled="!canRegister"
              :class="{'opacity-50 cursor-not-allowed': !canRegister}"
              class="px-4 py-2.5 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 transition-colors duration-200 text-center"
            >
              Register Forest
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'

const router = useRouter()
let registrationMap: L.Map | null = null
let drawnItems: L.FeatureGroup | null = null
let drawControl: L.Control.Draw | null = null
let baseLayer: L.TileLayer | null = null

const newForest = ref({
  name: '',
  coordinates: null
})

const isFullScreen = ref(false)
const showLayerDropdown = ref(false)
const currentLayer = ref<'satellite' | 'ndvi' | 'terrain'>('satellite')

const canRegister = computed(() => {
  return newForest.value.name && newForest.value.coordinates
})

const initMap = () => {
  if (registrationMap) return
  
  registrationMap = L.map('registration-map', {
    center: [3.848, 11.5021], // Yaounde, Cameroon
    zoom: 13,
    preferCanvas: true
  })

  // Add base layers
  baseLayer = L.tileLayer(getTileUrl(currentLayer.value), {
    attribution: '© OpenStreetMap contributors'
  })
  baseLayer.addTo(registrationMap)

  // Initialize feature group to store drawn items
  drawnItems = new L.FeatureGroup()
  registrationMap.addLayer(drawnItems)

  // Initialize the draw control with the specified configuration
  drawControl = new L.Control.Draw({
    edit: {
      featureGroup: drawnItems
    },
    draw: {
      polygon: {
        allowIntersection: false,
        showArea: true,
        metric: true,
        shapeOptions: {
          color: '#3B82F6',
          fillColor: '#3B82F6',
          fillOpacity: 0.4
        }
      },
      rectangle: false,
      circle: true,
      marker: false,
      circlemarker: false
    }
  })
  registrationMap.addControl(drawControl)

  // Set up event listeners
  registrationMap.on(L.Draw.Event.CREATED, handleDrawCreated)
  registrationMap.on(L.Draw.Event.EDITED, handleEdit)
  registrationMap.on(L.Draw.Event.DELETED, handleDelete)
}

function getTileUrl(layer: 'satellite' | 'ndvi' | 'terrain') {
  switch (layer) {
    case 'satellite':
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    case 'ndvi':
      return 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png'
    case 'terrain':
      return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    default:
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  }
}

const handleDrawCreated = (e: any) => {
  const layer = e.layer
  drawnItems?.addLayer(layer)
  
  // Add custom properties to the layer
  layer.feature = layer.feature || {}
  layer.feature.properties = {
    id: Date.now(),
    name: newForest.value.name || 'Unnamed Forest',
    area: L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000
  }
  
  newForest.value.coordinates = layer.getLatLngs()[0].map((ll: any) => [ll.lat, ll.lng])
  registrationMap?.fitBounds(layer.getBounds())
}

const handleEdit = (e: any) => {
  const layers = e.layers
  layers.eachLayer((layer: any) => {
    updateForestProperties(layer)
  })
}

const handleDelete = () => {
  newForest.value.coordinates = null
}

const updateForestProperties = (layer: any) => {
  const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000
  newForest.value.coordinates = layer.getLatLngs()[0].map((ll: any) => [ll.lat, ll.lng])
  layer.feature.properties.area = area.toFixed(2)
}

const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value
  const mapContainer = document.getElementById('registration-map-container')
  if (mapContainer) {
    if (isFullScreen.value) {
      mapContainer.requestFullscreen?.()
    } else {
      document.exitFullscreen?.()
    }
    setTimeout(() => { registrationMap?.invalidateSize() }, 300)
  }
}

// Listen for exiting fullscreen via ESC or browser UI
document.addEventListener('fullscreenchange', () => {
  const mapContainer = document.getElementById('registration-map-container')
  if (!document.fullscreenElement && isFullScreen.value) {
    isFullScreen.value = false
    registrationMap?.invalidateSize()
  }
})

const handleLayerDropdown = (event?: MouseEvent) => {
  if (event) event.stopPropagation()
  showLayerDropdown.value = !showLayerDropdown.value
}

const closeLayerDropdown = (e: MouseEvent) => {
  const dropdown = document.getElementById('layer-dropdown')
  if (dropdown && !dropdown.contains(e.target as Node)) {
    showLayerDropdown.value = false
    document.removeEventListener('mousedown', closeLayerDropdown)
  }
}

watch(showLayerDropdown, (val) => {
  if (val) {
    setTimeout(() => {
      document.addEventListener('mousedown', closeLayerDropdown)
    }, 0)
  } else {
    document.removeEventListener('mousedown', closeLayerDropdown)
  }
})

const changeBaseLayer = (layer: 'satellite' | 'ndvi' | 'terrain') => {
  currentLayer.value = layer
  showLayerDropdown.value = false
  if (registrationMap) {
    // Remove all tile layers (but not overlays)
    registrationMap.eachLayer(l => {
      if (l instanceof L.TileLayer && l !== drawnItems && l !== drawControl) {
        registrationMap?.removeLayer(l)
      }
    })
    baseLayer = L.tileLayer(getTileUrl(layer), {
      attribution: '© OpenStreetMap contributors'
    })
    baseLayer.addTo(registrationMap)
  }
}

const registerForest = async () => {
  if (!canRegister.value) return
  
  try {
    // Here you would call your API to register the forest
    // For now, we'll just navigate back to the monitoring view
    router.push('/forest-monitoring')
  } catch (error) {
    console.error('Error registering forest:', error)
  }
}

onMounted(() => {
  initMap()
})
</script>

<style>
#registration-map {
  z-index: 0;
}

.leaflet-draw-toolbar .leaflet-draw-draw-polygon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%233B82F6"><path d="M19 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 16H5V4h14v14z"/></svg>') !important;
}

.leaflet-draw-toolbar .leaflet-draw-edit-edit {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%2310B981"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>') !important;
}

.leaflet-draw-toolbar .leaflet-draw-edit-remove {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23EF4444"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>') !important;
}

.fullscreen-map {
  position: fixed !important;
  top: 0;
  left: 0;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 9999;
  background: #fff;
  border-radius: 0 !important;
  box-shadow: none !important;
}
.fullscreen-map #registration-map {
  width: 100vw !important;
  height: 100vh !important;
  min-height: 100vh !important;
}

@media (max-width: 640px) {
  .sm\\:h-96 {
    height: 16rem !important;
  }
  #registration-map-container {
    min-height: 12rem;
    height: 16rem !important;
  }
  .leaflet-control {
    font-size: 12px !important;
  }
  .leaflet-draw-toolbar {
    left: 0.5rem !important;
    top: 0.5rem !important;
  }
}
</style>