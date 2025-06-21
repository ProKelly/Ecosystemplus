<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet-draw'

// State management
const mapLoaded = ref(false)
const isProcessing = ref(false)
const showTutorial = ref(false)
const activeTab = ref<'detect' | 'edit' | 'analyze'>('detect')
const detectionHistory = ref<Array<any>>([])
const collaborationMode = ref(false)
const mapMode = ref<'2d' | '3d'>('2d') // '2d' or '3d'
const currentLayer = ref<'satellite' | 'ndvi' | 'terrain'>('satellite')
const sensitivity = ref<number>(70)
const accuracyScore = ref<number>(0)
const processingProgress = ref<number>(0)
const estimatedTime = ref<string>('2 minutes')
const activeUsers = ref<Array<{ id: number; name: string; color: string }>>([])
const showLayerDropdown = ref(false)
const isFullScreen = ref(false)

// Mock data
const detectedFields = ref<Array<{
  id: number;
  name: string;
  area: string;
  coordinates: any[];
  date: string;
  accuracy: string;
  problems: { type: string; location: number[] }[];
}>>([
  {
    id: 1,
    name: 'North Field',
    area: '12.5 ha',
    coordinates: [],
    date: '2023-11-15',
    accuracy: '98%',
    problems: [{ type: 'overlap', location: [35.12, -89.99] }]
  },
  {
    id: 2,
    name: 'South Field',
    area: '8.2 ha',
    coordinates: [],
    date: '2023-11-10',
    accuracy: '95%',
    problems: []
  }
])

// Map references
let map: L.Map | null = null
let drawnItems: L.FeatureGroup | null = null
let drawControl: L.Control.Draw | null = null
let baseLayer: L.TileLayer | null = null

onMounted(() => {
  initMap()
  loadUserHistory()
})

const initMap = () => {
  // Initialize Leaflet map with Yaounde, Cameroon as default
  if (map) return; // Prevent double initialization
  map = L.map('boundary-map', {
    center: [3.848, 11.5021], // Yaounde, Cameroon
    zoom: 13,
    preferCanvas: true
  })

  // Add base layers
  baseLayer = L.tileLayer(getTileUrl(currentLayer.value), {
    attribution: '&copy; OpenStreetMap contributors'
  })
  baseLayer.addTo(map)

  // Initialize feature group to store drawn items
  drawnItems = new L.FeatureGroup()
  map.addLayer(drawnItems)

  // Initialize the draw control
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
  map.addControl(drawControl)

  // Add event listeners
  map.on(L.Draw.Event.CREATED, handleDrawCreated)
  map.on(L.Draw.Event.EDITED, handleEdit)
  map.on(L.Draw.Event.DELETED, handleDelete)

  mapLoaded.value = true
}

function getTileUrl(layer: 'satellite' | 'ndvi' | 'terrain') {
  switch (layer) {
    case 'satellite':
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    case 'ndvi':
      // Placeholder NDVI layer (replace with real NDVI tiles if available)
      return 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png';
    case 'terrain':
      // Placeholder terrain layer (replace with real terrain tiles if available)
      return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
    default:
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  }
}

const handleDrawCreated = (e: any) => {
  const layer = e.layer
  drawnItems?.addLayer(layer)
  // Add custom properties to the layer
  layer.feature = layer.feature || {}
  layer.feature.properties = {
    id: Date.now(),
    name: `Field ${detectedFields.value.length + 1}`,
    accuracy: 0,
    area: L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000
  }
  detectedFields.value.push(layer.feature.properties)
}

const handleEdit = (e: any) => {
  const layers = e.layers
  layers.eachLayer((layer: any) => {
    updateFieldProperties(layer)
  })
}

const handleDelete = (e: any) => {
  const layers = e.layers
  layers.eachLayer((layer: any) => {
    // Remove from detectedFields if needed
  })
}

const updateFieldProperties = (layer: any) => {
  // Recalculate area and update accuracy
  const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 10000
  const accuracy = calculateAccuracy(layer)
  
  layer.feature.properties.area = area.toFixed(2)
  layer.feature.properties.accuracy = accuracy
  
  // Update our state
  const index = detectedFields.value.findIndex(
    field => field.id === layer.feature.properties.id
  )
  if (index !== -1) {
    detectedFields.value[index] = { ...layer.feature.properties }
  }
}

const calculateAccuracy = (layer: any) => {
  // Mock accuracy calculation based on polygon complexity
  const latLngs = layer.getLatLngs()[0]
  const complexityScore = Math.min(100, latLngs.length * 5)
  return Math.floor(complexityScore * 0.8 + Math.random() * 20)
}

const autoDetectBoundaries = () => {
  isProcessing.value = true
  processingProgress.value = 0
  
  // Simulate processing with progress updates
  const interval = setInterval(() => {
    processingProgress.value += Math.floor(Math.random() * 10)
    estimatedTime.value = `${Math.max(0, 120 - processingProgress.value * 1.2)} seconds`
    
    if (processingProgress.value >= 100) {
      clearInterval(interval)
      isProcessing.value = false
      completeDetection()
    }
  }, 800)
}

const completeDetection = () => {
  // Mock detection results
  const mockField = {
    id: Date.now(),
    name: 'Mock Field',
    area: '10.0 ha',
    date: new Date().toISOString().slice(0, 10),
    accuracy: '90%',
    coordinates: [],
    problems: []
  }
  
  detectionHistory.value.unshift(mockField)
  accuracyScore.value = parseInt(mockField.accuracy)
  
  // Add to map
  const polygon = L.polygon(mockField.coordinates, {
    color: '#10B981',
    fillColor: '#10B981',
    fillOpacity: 0.4
  })
  polygon.feature = {
    properties: mockField
  }
  drawnItems.addLayer(polygon)
  detectedFields.value.push(mockField)
}

const generateMockPolygon = () => {
  // Generate a simple mock polygon around the center
  const center = map.getCenter()
  const lat = center.lat
  const lng = center.lng
  const variation = 0.02
  
  return [
    [lat + variation * Math.random(), lng + variation * Math.random()],
    [lat + variation * Math.random(), lng - variation * Math.random()],
    [lat - variation * Math.random(), lng - variation * Math.random()],
    [lat - variation * Math.random(), lng + variation * Math.random()]
  ]
}

const exportData = (format: string) => {
  // Export functionality would go here
  alert(`Exporting data in ${format} format`)
}

const toggle3DView = () => {
  mapMode.value = mapMode.value === '2d' ? '3d' : '2d'
  // Placeholder: Show alert for now
  alert('3D view is not implemented. Please integrate a 3D map library for full support.')
}

const handleLayerDropdown = (event?: MouseEvent) => {
  if (event) event.stopPropagation();
  showLayerDropdown.value = !showLayerDropdown.value;
}

const closeLayerDropdown = (e: MouseEvent) => {
  const dropdown = document.getElementById('layer-dropdown');
  if (dropdown && !dropdown.contains(e.target as Node)) {
    showLayerDropdown.value = false;
    document.removeEventListener('mousedown', closeLayerDropdown);
  }
}

watch(showLayerDropdown, (val) => {
  if (val) {
    setTimeout(() => {
      document.addEventListener('mousedown', closeLayerDropdown);
    }, 0);
  } else {
    document.removeEventListener('mousedown', closeLayerDropdown);
  }
})

const changeBaseLayer = (layer: 'satellite' | 'ndvi' | 'terrain') => {
  currentLayer.value = layer
  showLayerDropdown.value = false
  if (map) {
    // Remove all tile layers (but not overlays)
    map.eachLayer(l => {
      if (l instanceof L.TileLayer && l !== drawnItems && l !== drawControl) {
        map.removeLayer(l)
      }
    })
    baseLayer = L.tileLayer(getTileUrl(layer), {
      attribution: '&copy; OpenStreetMap contributors'
    })
    baseLayer.addTo(map)
  }
}

const loadUserHistory = () => {
  // Simulate loading user's detection history
  setTimeout(() => {
    detectionHistory.value = [
      {
        id: 3,
        name: 'East Field',
        area: '15.2 ha',
        date: '2023-10-28',
        accuracy: '92%',
        coordinates: [],
        problems: []
      },
      {
        id: 4,
        name: 'West Field',
        area: '9.7 ha',
        date: '2023-10-15',
        accuracy: '89%',
        coordinates: [],
        problems: []
      }
    ]
  }, 500)
}

const startTutorial = () => {
  showTutorial.value = true
}

const inviteCollaborator = () => {
  collaborationMode.value = true
  activeUsers.value = [
    { id: 1, name: 'You', color: '#3B82F6' },
    { id: 2, name: 'Collaborator 1', color: '#10B981' }
  ]
}

const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value
  const mapContainer = document.getElementById('boundary-map-container')
  if (mapContainer) {
    if (isFullScreen.value) {
      mapContainer.requestFullscreen?.()
    } else {
      document.exitFullscreen?.()
    }
    setTimeout(() => { map?.invalidateSize() }, 300)
  }
}

// Listen for exiting fullscreen via ESC or browser UI
if (typeof window !== 'undefined') {
  document.addEventListener('fullscreenchange', () => {
    const mapContainer = document.getElementById('boundary-map-container')
    if (!document.fullscreenElement && isFullScreen.value) {
      isFullScreen.value = false
      map?.invalidateSize()
    }
  })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="block p-8">

    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Left Sidebar - Controls -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Detection Mode Tabs -->
          <div class="bg-white rounded-lg shadow p-4">
            <div class="border-b border-gray-200">
              <nav class="-mb-px flex space-x-4">
                <button
                  v-for="tab in ['detect', 'edit', 'analyze']"
                  :key="tab"
                  @click="activeTab = tab as 'detect' | 'edit' | 'analyze'"
                  :class="[
                    activeTab === tab
                      ? 'border-emerald-500 text-emerald-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                  ]"
                >
                  {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
                </button>
              </nav>
            </div>

            <!-- Detection Controls -->
            <div v-show="activeTab === 'detect'" class="mt-4 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Detection Sensitivity</label>
                <input 
                  type="range" 
                  v-model="sensitivity"
                  min="0" 
                  max="100" 
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                >
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Low</span>
                  <span>Medium</span>
                  <span>High</span>
                </div>
              </div>

              <div class="grid grid-cols-2 md:flex gap-2">
                <button
                  @click="autoDetectBoundaries"
                  class="flex items-center justify-center px-2 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none"
                >
                  <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Auto-Detect
                </button>
                <button
                  class="flex items-center justify-center px-2 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                >
                  <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Manual
                </button>
              </div>
            </div>

            <!-- Edit Controls -->
            <div v-show="activeTab === 'edit'" class="mt-4 space-y-4">
              <div class="space-y-2">
                <button
                  class="w-full flex items-center justify-between px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <span>Split Field</span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
                <button
                  class="w-full flex items-center justify-between px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <span>Merge Fields</span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
                <button
                  class="w-full flex items-center justify-between px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <span>Adjust Vertices</span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
                <button
                  class="w-full flex items-center justify-between px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <span>Highlight Problem Areas</span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
                <button
                  class="w-full flex items-center justify-between px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <span>Compare with History</span>
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Data Import/Export -->
          <div class="bg-white rounded-lg shadow p-4">
            <h3 class="text-sm font-medium text-gray-900 mb-3">Data Management</h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                class="flex items-center justify-center px-3 py-2 border border-gray-300 text-xs font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
              >
                <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Import
              </button>
              <div class="relative">
                <button
                  @click="exportData('geojson')"
                  class="w-full flex items-center justify-center px-3 py-2 border border-gray-300 text-xs font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
                >
                  <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Export
                </button>
                <div class="absolute right-0 mt-1 w-40 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-10 hidden">
                  <div class="py-1">
                    <button @click="exportData('geojson')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">GeoJSON</button>
                    <button @click="exportData('shapefile')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Shapefile</button>
                    <button @click="exportData('kml')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">KML</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Detected Fields List -->
          <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="px-4 py-3 border-b border-gray-200 bg-gray-50">
              <h3 class="text-sm font-medium text-gray-900">Detected Fields</h3>
            </div>
            <ul class="divide-y divide-gray-200">
              <li v-for="field in detectedFields" :key="field.id" class="px-4 py-3 hover:bg-gray-50 cursor-pointer">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ field.name }}</p>
                    <p class="text-xs text-gray-500">{{ field.area }} • {{ field.accuracy }} accuracy</p>
                  </div>
                  <button class="text-gray-400 hover:text-gray-500">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Main Map Area -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow overflow-hidden">
            <!-- Map Toolbar -->
            <div class="px-4 py-2 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
              <div class="flex space-x-2">
                <button
                  @click="toggle3DView"
                  class="px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  {{ mapMode === '2d' ? '3D View' : '2D View' }}
                </button>
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
                <!-- Fullscreen Button -->
                <button
                  @click="toggleFullScreen"
                  class="px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50 flex items-center"
                  :aria-pressed="isFullScreen.toString()"
                  title="Toggle Fullscreen"
                >
                  <svg v-if="!isFullScreen" class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h6M4 4v6M20 20h-6M20 20v-6" />
                  </svg>
                  <svg v-else class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 4v6M20 4h-6M4 20v-6M4 20h6" />
                  </svg>
                  <span>{{ isFullScreen ? 'Exit Fullscreen' : 'Fullscreen' }}</span>
                </button>
              </div>
              <div v-if="collaborationMode" class="flex items-center space-x-2">
                <span class="text-xs text-gray-500">Active collaborators:</span>
                <div v-for="user in activeUsers" :key="user.id" class="flex items-center">
                  <span class="h-3 w-3 rounded-full mr-1" :style="{ backgroundColor: user.color }"></span>
                  <span class="text-xs font-medium">{{ user.name }}</span>
                </div>
              </div>
            </div>

            <!-- Map Container -->
            <div :id="'boundary-map-container'" :class="{ 'fullscreen-map': isFullScreen }">
              <div id="boundary-map" class="w-full h-[600px]"></div>
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

            <!-- Processing Status -->
            <ProcessingStatus 
              v-if="isProcessing"
              :progress="processingProgress"
              :estimatedTime="estimatedTime"
            />
          </div>

          <!-- Detection History -->
          <div class="mt-6 bg-white rounded-lg shadow overflow-hidden">
            <div class="px-4 py-3 border-b border-gray-200 bg-gray-50">
              <h3 class="text-sm font-medium text-gray-900">Detection History</h3>
            </div>
            <BoundaryHistory :history="detectionHistory" />
          </div>
        </div>
      </div>
    </main>

    <!-- Tutorial Overlay -->
    <TutorialOverlay 
      v-if="showTutorial"
      @close="showTutorial = false"
    />
  </div>
</template>

<style>
#boundary-map {
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
.fullscreen-map #boundary-map {
  width: 100vw !important;
  height: 100vh !important;
  min-height: 100vh !important;
}
</style>